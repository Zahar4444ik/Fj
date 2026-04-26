import random
import time

from core.config.settings_parse import MAX_ALPHABET_SIZE, \
    MIN_ALPHABET_SIZE, DFA_MIN_STATES_COUNT, DFA_MAX_STATES_COUNT, NFA_MIN_STATES_COUNT, NFA_MAX_STATES_COUNT
from core.regex.automata.nka.nka_builder import build_NKA, count_nka_states
from core.regex.frontend.syntax import USABLE_ALPHABET
from core.regex.frontend.helper import get_ast_from_regex
from core.regex.automata.dka.dka_builder import build_DKA
from core.regex.generators.ast_nodes import (
    Symbol, Star, Union, Concat, Optional,
    is_atomic, count_stars, count_unions, count_nodes,
)

# ---------------------------------------------------------------------------
# Empirical depth → state count mapping (p25, p75 from profiling).
# Separate tables for DFA and NFA because they grow differently.
#
# DFA:
#   depth=3  →  2–4  states
#   depth=4  →  4–6  states
#   depth=5  →  5–8  states
#   depth=6  →  6–11 states
#
# NFA (grows faster):
#   depth=3  →  3–6  states
#   depth=4  →  5–12 states
#   depth=5  →  8–20 states
#   depth=6  →  12–30 states
#
# Format: (min_states, max_states, depth)
# ---------------------------------------------------------------------------
_DFA_DEPTH_TABLE: list[tuple[int, int, int]] = [
    (2,  4,  3),
    (4,  6,  4),
    (5,  8,  5),
    (6, 11,  6),
]

_NFA_DEPTH_TABLE: list[tuple[int, int, int]] = [
    (3,  6,  3),
    (5, 12,  4),
    (8, 20,  5),
    (12, 30, 6),
]

# Maximum time to spend trying to generate a single regex (seconds)
_GENERATION_TIMEOUT = 10.0


# ---------------------------------------------------------------------------
# Depth selection
# ---------------------------------------------------------------------------

def pick_depths_for_state_range(min_states: int, max_states: int, automaton_type: str = "dfa") -> list[int]:
    """
    Return every depth whose empirical state range overlaps [min_states, max_states].
    Uses separate tables for DFA and NFA since they grow differently.

    Falls back to the deepest available depth if no overlap is found.
    """
    table = _DFA_DEPTH_TABLE if automaton_type == "dfa" else _NFA_DEPTH_TABLE

    candidates = [
        depth
        for lo, hi, depth in table
        if lo <= max_states and hi >= min_states
    ]

    if not candidates:
        # Fallback: use deepest depth
        candidates = [table[-1][2]]

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
        alphabet = USABLE_ALPHABET

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
    local_alphabet = random.sample(USABLE_ALPHABET, subset_size)

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


def generate_valid_regex(max_depth: int = 3, automaton_type: str = "nfa") -> str:
    good_length = True if automaton_type == "nfa" else False
    generated_regex = to_regex(generate_valid_ast(max_depth=max_depth))
    while not good_length:
        generated_regex = to_regex(generate_valid_ast(max_depth=max_depth))
        if DFA_MIN_STATES_COUNT*2 <= len(generated_regex) <= DFA_MAX_STATES_COUNT*3:
            good_length = True

    return generated_regex


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_regex_with_state_count(automaton_type: str) -> str:
    """
    Generate a regex whose state count matches the target range for the automaton type.

    Strategy:
      1. Pre-select candidate depths from the appropriate empirical table (DFA or NFA)
      2. Build the automaton and accept only if the state count is in range
      3. Timeout after _GENERATION_TIMEOUT seconds to prevent infinite loops

    Args:
        automaton_type: Either "dfa" or "nfa"

    Returns:
        A regex string matching the state count requirements

    Raises:
        TimeoutError: If generation takes longer than _GENERATION_TIMEOUT seconds
    """

    if automaton_type == "dfa":
        min_states = DFA_MIN_STATES_COUNT
        max_states = DFA_MAX_STATES_COUNT
    elif automaton_type == "nfa":
        min_states = NFA_MIN_STATES_COUNT
        max_states = NFA_MAX_STATES_COUNT
    else:
        raise ValueError(f"Unknown automaton type: {automaton_type}")

    candidate_depths = pick_depths_for_state_range(min_states, max_states, automaton_type)
    start_time = time.time()

    while time.time() - start_time < _GENERATION_TIMEOUT:
        max_depth = random.choice(candidate_depths)
        regex = generate_valid_regex(max_depth=max_depth, automaton_type=automaton_type)

        try:
            ast = get_ast_from_regex(regex)

            if automaton_type == "dfa":
                automaton = build_DKA(ast, regex)
                if min_states <= len(automaton.name_map) <= max_states:
                    return regex

            elif automaton_type == "nfa":
                automaton = build_NKA(ast)
                if min_states <= count_nka_states(automaton) <= max_states:
                    return regex
        except Exception:
            continue

    # Timeout reached
    raise TimeoutError(
        f"Failed to generate {automaton_type.upper()} regex with {min_states}-{max_states} states "
        f"within {_GENERATION_TIMEOUT} seconds. "
        f"Check env vars DFA/NFA_MIN/MAX_STATES_COUNT are reasonable."
    )


# ---------------------------------------------------------------------------
# Manual testing
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    automaton_type = "dfa"
    for regex in [generate_regex_with_state_count(automaton_type) for _ in range(20)]:
        if automaton_type == "dfa":
            automaton = build_DKA(get_ast_from_regex(regex), regex)
            count = len(automaton.name_map)
        else:
            automaton = build_NKA(get_ast_from_regex(regex))
            count = count_nka_states(automaton)
        print(f"{regex:<30} ->  {count} states")
