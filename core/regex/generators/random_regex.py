import random

from core.config.settings_parse import REGEX_MIN_DEPTH, REGEX_MAX_DEPTH
from core.regex.frontend.syntax import ALPHABET

MIN_DEPTH = REGEX_MIN_DEPTH
MAX_DEPTH = REGEX_MAX_DEPTH
MAX_UNION_RETRIES = 8


def random_symbol():
    return random.choice(ALPHABET)


def generate_regex(depth=0, last_op=None, needs_star=False):
    """
    Generate a regex expression.

    :param depth: Current recursion depth
    :param last_op: Last operator used (for compatibility rules)
    :param needs_star: If True, guarantees at least one star in this subtree
    """
    # Base case - if we need a star but we're at max depth, force star on a symbol
    if depth >= MAX_DEPTH:
        if needs_star:
            return f"{{{random_symbol()}}}"
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

    choices = allowed_next.get(last_op, ["union", "concat"])

    # Add depth-based rules
    if depth >= MIN_DEPTH and "group" not in choices:
        choices.append("group")

    # If we need a star, force it into the choices if allowed
    if needs_star and depth < MAX_DEPTH - 1:
        if "star" not in choices:
            # Can we add star based on context?
            if last_op in {None, "union", "concat", "group"}:
                choices = ["star"]  # Force star
            else:
                # Try to route through concat/group to reach star
                if "concat" in choices or "group" in choices:
                    choices = [c for c in choices if c in {"concat", "group"}]

    choice = random.choice(choices)

    # Build expression
    if choice == "union":
        # Pass needs_star to one of the branches randomly
        left_needs = needs_star and random.choice([True, False])
        right_needs = needs_star and not left_needs

        left = generate_regex(depth + 1, last_op="union", needs_star=left_needs)
        right = generate_regex(depth + 1, last_op="union", needs_star=right_needs)

        attempts = 0
        while left == right and attempts < MAX_UNION_RETRIES:
            right = generate_regex(depth + 1, last_op="union", needs_star=right_needs)
            attempts += 1

        return f"{left}|{right}"

    elif choice == "concat":
        # Pass needs_star to one of the branches randomly
        left_needs = needs_star and random.choice([True, False])
        right_needs = needs_star and not left_needs

        left = generate_regex(depth + 1, last_op="concat", needs_star=left_needs)
        right = generate_regex(depth + 1, last_op="concat", needs_star=right_needs)
        return f"{left}{right}"

    elif choice == "star":
        # Star found - need is satisfied
        inner = generate_regex(depth + 1, last_op="star", needs_star=False)
        return f"{{{inner}}}"

    elif choice == "optional":
        # Optional doesn't satisfy star need, pass it through
        inner = generate_regex(depth + 1, last_op="optional", needs_star=needs_star)
        return f"[{inner}]"

    elif choice == "group":
        inner = generate_regex(depth + 1, last_op="group", needs_star=needs_star)
        if needs_group(inner, parent_op=last_op):
            return f"({inner})"
        return inner

    return random_symbol()


def strip_outer_parens_once(s: str) -> str:
    """Remove one layer of outer parentheses if they wrap the entire expression."""
    s = s.strip()
    if len(s) >= 2 and s[0] == "(" and s[-1] == ")":
        depth = 0
        for i, ch in enumerate(s):
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            if depth == 0:
                if i == len(s) - 1:
                    return s[1:-1]
                break
    return s


def strip_outer_parens(s: str) -> str:
    """Strip all outer parentheses layers recursively."""
    prev = None
    cur = s
    while cur != prev:
        prev = cur
        cur = strip_outer_parens_once(cur)
    return cur


def is_pure_concat_of_symbols(s: str) -> bool:
    """Check if string is pure concatenation of alphabet symbols."""
    return all(ch in ALPHABET for ch in s) and len(s) >= 1


def needs_group(inner: str, parent_op: str) -> bool:
    """Decide if parentheses are needed around inner expression."""
    stripped = strip_outer_parens(inner)

    if is_pure_concat_of_symbols(stripped):
        return False

    if stripped.startswith("{") or stripped.startswith("["):
        return False

    if "|" in stripped:
        if parent_op in {"concat", "star", "optional"}:
            return True
        return False

    return False


def has_star(regex: str) -> bool:
    """Check if regex contains at least one star operator."""
    return "{" in regex and "}" in regex


def generate_valid_regex():
    """
    Generate regex that:
    - has at least 2 symbols
    - contains at least one star operator {}
    """
    while True:
        expr = generate_regex(needs_star=True)
        symbols_in_regex = [c for c in expr if c in ALPHABET]
        symbols_in_regex = set(symbols_in_regex)

        # Verify constraints
        if len(symbols_in_regex) >= 3 and has_star(expr):
            return expr