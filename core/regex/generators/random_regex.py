import random

from core.config.scoring import REGEX_MIN_DEPTH, REGEX_MAX_DEPTH
from core.regex.frontend.syntax import ALPHABET

MIN_DEPTH = REGEX_MIN_DEPTH
MAX_DEPTH = REGEX_MAX_DEPTH

MAX_UNION_RETRIES = 8


def random_symbol():
    return random.choice(ALPHABET)


def generate_regex(depth=0, last_op=None):

    # Base case
    if depth >= MAX_DEPTH:
        return random_symbol()

    # Operator compatibility rules
    allowed_next = {
        None: ["union", "concat"],
        "union": ["concat", "group"],
        "concat": ["star", "optional", "group"],
        "star": ["union", "concat"],
        "optional": ["union", "concat"],
        "group": ["union", "concat"],

    }

    # Get choices for this depth
    choices = allowed_next.get(last_op, ["union", "concat"])

    # Add depth-based rules. Group cant be at top level
    if depth == MIN_DEPTH:
        if "group" not in choices:
            choices.append("group")

    choice = random.choice(choices)

    # Build expression parts
    # if choice == "symbol":
    #     return random_symbol()

    if choice == "union":
        left = generate_regex(depth + 1, last_op="union")
        right = generate_regex(depth + 1, last_op="union")

        attempts = 0
        while (left == right) and attempts < MAX_UNION_RETRIES:
            # regenerate the right side to try to get a different expression
            right = generate_regex(depth + 1, last_op="union")
            attempts += 1

        return f"{left}|{right}"

    elif choice == "concat":
        left = generate_regex(depth + 1, last_op="concat")
        right = generate_regex(depth + 1, last_op="concat")
        return f"{left}{right}"

    elif choice == "star":
        inner = generate_regex(depth + 1, last_op="star")
        return f"{{{inner}}}"

    elif choice == "optional":
        inner = generate_regex(depth + 1, last_op="optional")
        return f"[{inner}]"

    elif choice == "group":

        inner = generate_regex(depth + 1, last_op="group")
        if needs_group(inner, parent_op=last_op):
            return f"({inner})"
        else:
            return inner
    return None


def strip_outer_parens_once(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and s[0] == "(" and s[-1] == ")":
        # ensure the first '(' matches the very last ')'
        depth = 0
        for i, ch in enumerate(s):
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            if depth == 0:
                # if the matching ')' for the first '(' is last char, it's a full-wrap
                return s[1:-1]
    return s


def strip_outer_parens(s: str) -> str:
    # strip repeatedly like ((a|b)) -> a|b
    prev = None
    cur = s
    while cur != prev:
        prev = cur
        cur = strip_outer_parens_once(cur)
    return cur


def is_pure_concat_of_symbols(s: str) -> bool:
    # Returns True if s is concat of alphabet symbols only (no operators, no braces/brackets)
    # e.g. "ab" -> True, "a(b)" -> False, "a|b" -> False
    return all(ch in ALPHABET for ch in s) and len(s) >= 1


def needs_group(inner: str, parent_op: str) -> bool:
    """
    Decide whether parentheses are needed around `inner` when placed under `parent_op`.
    parent_op is one of: None, 'union', 'concat', 'star', 'optional', 'group', 'symbol'
    """
    # normalize by stripping outer parentheses fully
    stripped = strip_outer_parens(inner)

    # if the stripped content is a single symbol or a pure concatenation of symbols,
    # parentheses are useless in almost all contexts
    if is_pure_concat_of_symbols(stripped):
        return False

    # if inner starts with unary operator { or [ ] then parentheses around it are useless
    if stripped.startswith("{") or stripped.startswith("["):
        return False

    # If the inner expression contains '|' (an alternation)
    if "|" in stripped:
        # grouping is required if the parent is concat or unary operators
        if parent_op in {"concat", "star", "optional"}:
            return True
        # if parent is union or top-level, grouping is usually unnecessary
        return False

    # otherwise, no '|' inside and not a pure symbol concat -> grouping rarely needed
    return False


def generate_valid_regex():
    """
    Generate regex that:
    - has at least 2 symbols
    """
    while True:
        expr = generate_regex()
        symbol_count = sum(1 for c in expr if c in ALPHABET)
        if symbol_count >= 2:
            return expr