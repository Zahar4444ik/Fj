import random

from core.config.settings_parse import REGEX_MIN_DEPTH, REGEX_MAX_DEPTH
from core.regex.frontend.syntax import ALPHABET
from core.regex.generators.regex.ast_nodes import (
    Symbol, Star, Union, Concat, Optional,
    is_atomic, count_stars, count_unions, count_nodes,
)
from core.regex.frontend.helper import get_ast_from_regex
from core.regex.automata.dka.dka_builder import build_DKA

MIN_DEPTH = REGEX_MIN_DEPTH
MAX_DEPTH = REGEX_MAX_DEPTH


def contains_wrapper(node) -> bool:
    """Return True if any node in the subtree is a Star or Optional."""
    if isinstance(node, (Star, Optional)):
        return True
    if isinstance(node, (Union, Concat)):
        return contains_wrapper(node.left) or contains_wrapper(node.right)
    return False


def generate_ast(depth=0):
    if depth >= MAX_DEPTH:
        return Symbol(random.choice(ALPHABET))

    # star and optional require a non-atomic child, so they need at least one
    # more level of depth available to guarantee that's possible.
    # union's non-atomic constraint has the same requirement.
    can_nest = depth + 1 < MAX_DEPTH
    choices = ["concat", "symbol"]
    if can_nest:
        choices += ["star", "optional", "union"]
    else:
        choices += ["union_unconstrained"]
    choice = random.choice(choices)

    if choice == "symbol":
        return Symbol(random.choice(ALPHABET))

    if choice == "star":
        inner = generate_ast(depth + 1)
        # Reject: atomic, direct wrapper child, or any wrapper anywhere in subtree
        while is_atomic(inner) or contains_wrapper(inner):
            inner = generate_ast(depth + 1)
        return Star(inner)

    if choice == "optional":
        inner = generate_ast(depth + 1)
        while is_atomic(inner) or contains_wrapper(inner):
            inner = generate_ast(depth + 1)
        return Optional(inner)

    if choice == "union":
        left = generate_ast(depth + 1)
        right = generate_ast(depth + 1)
        # At least one side must be non-atomic — safe because can_nest is True
        # Also forbid Union as child of Union to cap branches at 2
        while (is_atomic(left) and is_atomic(right)) \
                or isinstance(left, Union) or isinstance(right, Union) \
                or left == right:
            left = generate_ast(depth + 1)
            right = generate_ast(depth + 1)
        return Union(left, right)

    if choice == "union_unconstrained":
        # At max depth children are always symbols — just forbid Union children for consistency
        left = generate_ast(depth + 1)
        right = generate_ast(depth + 1)
        return Union(left, right)

    if choice == "concat":
        left = generate_ast(depth + 1)
        right = generate_ast(depth + 1)
        # Concat of two Unions requires parens to be unambiguous — forbid it
        # to keep output clean (no parens ever needed inside {} or [])
        while isinstance(left, Union) and isinstance(right, Union):
            left = generate_ast(depth + 1)
            right = generate_ast(depth + 1)
        return Concat(left, right)

    raise ValueError(f"Unexpected choice: {choice!r}")


def is_structurally_valid(ast) -> bool:
    return (
        count_stars(ast) >= 1
        and count_unions(ast) >= 1
        and count_nodes(ast) >= 5
    )


def generate_valid_ast():
    while True:
        ast = generate_ast()
        if is_structurally_valid(ast):
            return ast


def to_regex(node, parent_prec=0) -> str:
    if isinstance(node, Symbol):
        return node.value

    if isinstance(node, Star):
        # {} acts as implicit grouping — render inner at precedence 0, no extra parens needed
        inner = to_regex(node.inner, 0)
        return f"{{{inner}}}"

    if isinstance(node, Optional):
        # [] acts as implicit grouping — render inner at precedence 0, no extra parens needed
        inner = to_regex(node.inner, 0)
        return f"[{inner}]"

    if isinstance(node, Concat):
        left = to_regex(node.left, 2)
        right = to_regex(node.right, 2)
        expr = left + right
        if parent_prec > 2:
            return f"({expr})"
        return expr

    if isinstance(node, Union):
        left = to_regex(node.left, 1)
        right = to_regex(node.right, 1)
        expr = f"{left}|{right}"
        if parent_prec > 1:
            return f"({expr})"
        return expr

    raise TypeError(f"Unknown node type: {type(node)}")


def generate_valid_regex() -> str:
    ast = generate_valid_ast()
    return to_regex(ast)


def generate_regex_with_state_count(min_states: int, max_states: int) -> str:
    """
    Generate a valid regex whose DFA has a state count in [min_states, max_states].
    """
    while True:
        regex = generate_valid_regex()
        try:
            ast = get_ast_from_regex(regex)
            automaton = build_DKA(ast, regex)
            state_count = len(automaton.name_map)
            if min_states <= state_count <= max_states:
                return regex
        except Exception:
            # Malformed regex or DFA build failure — just retry
            continue


def generate_assignment_regexes(
    count: int,
    min_states: int,
    max_states: int,
) -> list[str]:
    """
    Generate `count` valid regexes each with DFA state count in [min_states, max_states].
    """
    return [generate_regex_with_state_count(min_states, max_states) for _ in range(count)]


if __name__ == "__main__":
    # Basic generation
    for _ in range(5):
        print(generate_valid_regex())

    print("---")

    # DFA state count controlled generation (e.g. medium difficulty: 4–7 states)
    for regex in generate_assignment_regexes(count=15, min_states=4, max_states=4):
        ast = get_ast_from_regex(regex)
        automaton = build_DKA(ast, regex)
        print(f"{regex}  →  {len(automaton.name_map)} states")