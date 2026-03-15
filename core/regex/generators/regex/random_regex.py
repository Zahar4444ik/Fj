import random

from core.config.settings_parse import REGEX_MIN_STATES_COUNT, REGEX_MAX_STATES_COUNT, MAX_ALPHABET_SIZE, \
    MIN_ALPHABET_SIZE
from core.regex.frontend.syntax import ALPHABET
from core.regex.frontend.helper import get_ast_from_regex
from core.regex.automata.dka.dka_builder import build_DKA
from core.regex.generators.regex.ast_nodes import (
    Symbol, Star, Union, Concat, Optional,
    is_atomic, count_stars, count_unions, count_nodes,
)

# ---------------------------------------------------------------------------
# Empirical depth → DFA state count mapping (p25, p75 from profiling).
#
#   depth=3  →  2–4  states
#   depth=4  →  4–6  states
#   depth=5  →  5–8  states
#   depth=6  →  6–11 states
#
# Used to pre-select a sensible generation depth before the rejection sampler
# does fine-grained filtering. Re-run profile_depth_states.py after any major
# change to generation logic and update this table accordingly.
# ---------------------------------------------------------------------------
_DEPTH_STATE_TABLE: list[tuple[int, int, int]] = [
    (2,  4,  3),
    (4,  6,  4),
    (5,  8,  5),
    (6, 11,  6),
]


# ---------------------------------------------------------------------------
# Depth selection
# ---------------------------------------------------------------------------

def pick_depths_for_state_range(min_states: int, max_states: int) -> list[int]:
    """
    Return every depth whose empirical p25-p75 state range overlaps
    [min_states, max_states]. Using multiple candidate depths keeps structural
    variety high and reduces rejection-sampler retries.

    Falls back to the shallowest depth if the target is below the profiled
    range, or the deepest if it is above.
    """
    candidates = [
        depth
        for lo, hi, depth in _DEPTH_STATE_TABLE
        if lo <= max_states and hi >= min_states
    ]
    if not candidates:
        candidates = [
            _DEPTH_STATE_TABLE[0][2] if max_states < _DEPTH_STATE_TABLE[0][0]
            else _DEPTH_STATE_TABLE[-1][2]
        ]
    return candidates


# ---------------------------------------------------------------------------
# AST generation
# ---------------------------------------------------------------------------

def contains_wrapper(node) -> bool:
    """Return True if a Star or Optional exists anywhere in the subtree."""
    if isinstance(node, (Star, Optional)):
        return True
    if isinstance(node, (Union, Concat)):
        return contains_wrapper(node.left) or contains_wrapper(node.right)
    return False


def generate_ast(depth: int = 0, max_depth: int = 3, alphabet: list[str] = None):
    """
    Recursively build a random regex AST up to max_depth.

    Structural constraints enforced during generation:
      - Star / Optional inner must be non-atomic and wrapper-free
        (prevents trivial {a} and nested wrappers like {[...]})
      - Union children must not themselves be Unions (caps branches at 2)
      - Union must have at least one non-atomic child (prevents a|b at depth limit)
      - Concat must not have two Union children (prevents ambiguous rendering)
    """
    if alphabet is None:
        alphabet = ALPHABET

    if depth >= max_depth:
        return Symbol(random.choice(alphabet))

    can_nest = depth + 1 < max_depth
    choices = ["concat", "symbol"]
    if can_nest:
        choices += ["star", "optional", "union"]
    else:
        choices += ["union_unconstrained"]

    choice = random.choice(choices)

    # helper to recurse with the same alphabet
    def recurse(d=None):
        return generate_ast(depth + 1, max_depth, alphabet)

    if choice == "symbol":
        return Symbol(random.choice(alphabet))

    if choice == "star":
        inner = recurse()
        while is_atomic(inner) or contains_wrapper(inner):
            inner = recurse()
        return Star(inner)

    if choice == "optional":
        inner = recurse()
        while is_atomic(inner) or contains_wrapper(inner):
            inner = recurse()
        return Optional(inner)

    if choice == "union":
        left, right = recurse(), recurse()
        while (is_atomic(left) and is_atomic(right)) \
                or isinstance(left, Union) or isinstance(right, Union):
            left, right = recurse(), recurse()
        return Union(left, right)

    if choice == "union_unconstrained":
        return Union(recurse(), recurse())

    if choice == "concat":
        left, right = recurse(), recurse()
        while isinstance(left, Union) and isinstance(right, Union):
            left, right = recurse(), recurse()
        return Concat(left, right)

    raise ValueError(f"Unexpected choice: {choice!r}")


def has_duplicate_union_children(node) -> bool:
    """Return True if any Union has two identical children."""
    if isinstance(node, Union):
        if to_regex(node.left) == to_regex(node.right):
            return True
        return has_duplicate_union_children(node.left) or has_duplicate_union_children(node.right)
    if isinstance(node, (Star, Optional)):
        return has_duplicate_union_children(node.inner)
    if isinstance(node, Concat):
        return has_duplicate_union_children(node.left) or has_duplicate_union_children(node.right)
    return False


def has_redundant_wrapper_pair(node) -> bool:
    """Return True if a Union has one Star and one Optional over the same inner expression."""
    if isinstance(node, Union):
        l, r = node.left, node.right
        if isinstance(l, (Star, Optional)) and isinstance(r, (Star, Optional)):
            if to_regex(l.inner) == to_regex(r.inner):
                return True
        return has_redundant_wrapper_pair(l) or has_redundant_wrapper_pair(r)
    if isinstance(node, (Star, Optional)):
        return has_redundant_wrapper_pair(node.inner)
    if isinstance(node, Concat):
        return has_redundant_wrapper_pair(node.left) or has_redundant_wrapper_pair(node.right)
    return False


def is_structurally_valid(node) -> bool:
    return (
        count_stars(node) >= 1
        and count_unions(node) >= 1
        and count_nodes(node) >= 5
        and not has_duplicate_union_children(node)
        and not has_redundant_wrapper_pair(node)
    )


def get_used_symbols(node) -> set[str]:
    if isinstance(node, Symbol):
        return {node.value}
    if isinstance(node, (Star, Optional)):
        return get_used_symbols(node.inner)
    if isinstance(node, (Union, Concat)):
        return get_used_symbols(node.left) | get_used_symbols(node.right)
    return set()


def generate_valid_ast(max_depth: int = 3):
    """ Pick a small random subset of the alphabet for this regex """
    subset_size = random.randint(MIN_ALPHABET_SIZE, MAX_ALPHABET_SIZE)
    local_alphabet = random.sample(ALPHABET, subset_size)

    while True:
        ast = generate_ast(max_depth=max_depth, alphabet=local_alphabet)
        if (
                is_structurally_valid(ast)
                and get_used_symbols(ast) == set(local_alphabet)  # ← all symbols must appear
        ):
            return ast


# ---------------------------------------------------------------------------
# AST -> regex string
# ---------------------------------------------------------------------------

def to_regex(node, parent_prec: int = 0) -> str:
    """
    Serialise an AST to a regex string.

    Precedence levels:
      1 - Union   (lowest)
      2 - Concat
      3 - Star / Optional  (highest; but {} and [] act as grouping so inner
                            is always rendered at precedence 0)

    Parentheses are added only when a lower-precedence operator appears
    inside a higher-precedence context, e.g. (a|b)c.
    Because {} and [] are implicit groups, their contents never need extra
    parentheses — so Star and Optional always pass parent_prec=0 inward.
    """
    if isinstance(node, Symbol):
        return node.value

    if isinstance(node, Star):
        return f"{{{to_regex(node.inner, 0)}}}"

    if isinstance(node, Optional):
        return f"[{to_regex(node.inner, 0)}]"

    if isinstance(node, Concat):
        left = to_regex(node.left, 2)
        right = to_regex(node.right, 2)
        expr = left + right
        return f"({expr})" if parent_prec > 2 else expr

    if isinstance(node, Union):
        left = to_regex(node.left, 1)
        right = to_regex(node.right, 1)
        expr = f"{left}|{right}"
        return f"({expr})" if parent_prec > 1 else expr

    raise TypeError(f"Unknown node type: {type(node)}")


def generate_valid_regex(max_depth: int = 3) -> str:
    good_length = False
    while not good_length:
        generated_regex = to_regex(generate_valid_ast(max_depth=max_depth))
        if REGEX_MIN_STATES_COUNT*2 <= len(generated_regex) <= REGEX_MAX_STATES_COUNT*3:
            good_length = True
    return generated_regex


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_regex_with_state_count(
    min_states: int = REGEX_MIN_STATES_COUNT,
    max_states: int = REGEX_MAX_STATES_COUNT,
) -> str:
    """
    Generate a regex whose minimal DFA has a state count in [min_states, max_states].

    Strategy:
      1. Pre-select candidate depths from the empirical table so most generated
         regexes are already close to the target state count.
      2. Build the DFA and accept only if the state count is in range;
         otherwise retry (rejection sampling).
    """
    candidate_depths = pick_depths_for_state_range(min_states, max_states)

    while True:
        max_depth = random.choice(candidate_depths)
        regex = generate_valid_regex(max_depth=max_depth)
        try:
            automaton = build_DKA(get_ast_from_regex(regex), regex)
            if min_states <= len(automaton.name_map) <= max_states:
                return regex
        except Exception:
            continue


def generate_assignment_regexes(
    count: int,
    min_states: int = REGEX_MIN_STATES_COUNT,
    max_states: int = REGEX_MAX_STATES_COUNT,
) -> list[str]:
    """Generate `count` regexes each satisfying the given state count range."""
    return [generate_regex_with_state_count(min_states, max_states) for _ in range(count)]


# ---------------------------------------------------------------------------
# Manual testing
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    for regex in generate_assignment_regexes(count=20, min_states=4, max_states=4):
        automaton = build_DKA(get_ast_from_regex(regex), regex)
        print(f"{regex:<30} ->  {len(automaton.name_map)} states")