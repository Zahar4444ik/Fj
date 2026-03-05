import random
from typing import List

from core.regex.automata.dka.dka_builder import build_DKA
from core.regex.automata.utils.automata_operations import get_regex_alphabet
from core.regex.frontend.helper import get_ast_from_regex, regex_from_tree


# ---------------------------------------------------------------------------
# Accepted word generation
# ---------------------------------------------------------------------------
# Strategy: walk the AST and at every Star node try a range of iteration
# counts (0..max_iterations). We enumerate combinations systematically by
# assigning each Star a different count per attempt, then fall back to random
# variation. Because every regex is guaranteed to contain at least one Star
# the word space is infinite, so filling any medium-sized count is always
# possible without duplicates.
# ---------------------------------------------------------------------------

def _collect_stars(node: dict) -> List[dict]:
    """Return every Star node in the tree in traversal order."""
    result = []

    def _walk(n: dict):
        children = n.get("children", [])
        if n.get("type") == "element" and children and children[0].get("value") == "<LBRACE>":
            result.append(n)
        for child in children:
            if isinstance(child, dict):
                _walk(child)

    _walk(node)
    return result


def _generate_word(node: dict, star_counts: dict, max_iterations: int) -> str:
    """
    Walk the AST and produce one word.

    star_counts maps id(star_node) -> exact iteration count to use.
    Any star not in the map falls back to a random count in [0, max_iterations].
    """
    node_type = node.get("type")

    if node_type == "symbol":
        value = node.get("value", "")
        return "" if value.startswith("<") else value

    if node_type in ("regular", "sequence"):
        return "".join(
            _generate_word(child, star_counts, max_iterations)
            for child in node.get("children", [])
        )

    if node_type == "alternative":
        sequences = [
            c for c in node.get("children", [])
            if c.get("type") != "symbol"
        ]
        if not sequences:
            return ""
        return _generate_word(random.choice(sequences), star_counts, max_iterations)

    if node_type == "element":
        children = node.get("children", [])
        if len(children) >= 3:
            first = children[0].get("value", "")

            if first == "<LBRACE>":
                count = star_counts.get(id(node), random.randint(0, max_iterations))
                return "".join(
                    _generate_word(children[1], star_counts, max_iterations)
                    for _ in range(count)
                )

            if first == "<LBRACKET>":
                if random.choice([True, False]):
                    return _generate_word(children[1], star_counts, max_iterations)
                return ""

            if first == "<LPAREN>":
                return _generate_word(children[1], star_counts, max_iterations)

        return "".join(
            _generate_word(child, star_counts, max_iterations)
            for child in children
        )

    return ""


def _iter_star_assignments(stars: List[dict], max_iterations: int):
    """
    Yield star_count dicts that systematically cover the iteration space.

    Phase 1 — systematic: for N stars and M+1 possible counts we cycle through
    all combinations in a round-robin fashion. This guarantees that for a single
    star we see every count from 0 to max_iterations before repeating.

    Phase 2 — random: once systematic combinations are exhausted, yield random
    assignments indefinitely so the caller can always fill its quota.
    """
    if not stars:
        while True:
            yield {}
        return

    # Phase 1: systematic round-robin
    total_counts = max_iterations + 1
    # Number of systematic combos before we start repeating
    # (cap at a reasonable ceiling to avoid huge loops for many stars)
    n_systematic = total_counts ** min(len(stars), 3)

    for i in range(n_systematic):
        assignment = {}
        remainder = i
        for star in stars:
            assignment[id(star)] = remainder % total_counts
            remainder //= total_counts
        yield assignment

    # Phase 2: random forever
    while True:
        yield {id(star): random.randint(0, max_iterations) for star in stars}


def generate_accepted_words(
    tree: dict,
    count: int = 10,
    max_iterations: int = 10,
) -> List[str]:
    """
    Generate exactly `count` unique words accepted by the regex.

    Automatically increases max_iterations if the word space is exhausted
    before `count` unique words are found.
    """
    stars = _collect_stars(tree)
    seen: set[str] = set()
    words: List[str] = []

    while len(words) < count:
        max_attempts = count * 200
        stars = _collect_stars(tree)

        for star_counts in _iter_star_assignments(stars, max_iterations):
            if len(words) == count:
                break
            if max_attempts <= 0:
                break  # retry with higher max_iterations
            max_attempts -= 1

            word = _generate_word(tree, star_counts, max_iterations)
            if word not in seen:
                seen.add(word)
                words.append(word)

        if len(words) < count:
            max_iterations += 1  # expand search space and retry

    return words


# ---------------------------------------------------------------------------
# Rejected word generation
# ---------------------------------------------------------------------------
# Strategy: generate candidate strings from the alphabet (with varying lengths
# and compositions) and verify each one against the DFA. Only confirmed-wrong
# words are kept. Because we verify via DFA these are guaranteed rejections.
# ---------------------------------------------------------------------------

def _check_word_rejected(word: str, automaton) -> bool:
    """Return True if the DFA rejects `word`."""
    state = automaton.start
    for char in word:
        transitions = state.transitions.get(char, set())
        if not transitions:
            return True  # dead — rejected
        state = next(iter(transitions))
    return state not in automaton.accepts


def _candidate_rejected_words(alphabet: List[str], max_len: int = 8):
    """
    Yield an infinite stream of candidate strings to test for rejection.

    Mix of strategies to cover diverse failure modes:
      - Pure random strings of varying length (most common)
      - Length-0 empty string
      - Single characters
      - Repeated single characters
    """
    # Always try empty string first
    yield ""

    # Single characters
    for ch in alphabet:
        yield ch

    # Then random mix
    while True:
        strategy = random.random()

        if strategy < 0.6:
            # Random string, biased toward short-to-medium lengths
            length = random.randint(1, max_len)
            yield "".join(random.choice(alphabet) for _ in range(length))

        elif strategy < 0.8:
            # Repeated single character (catches many simple length violations)
            ch = random.choice(alphabet)
            length = random.randint(2, max_len)
            yield ch * length

        else:
            # Two random words concatenated (longer, tests suffix mismatches)
            a = "".join(random.choice(alphabet) for _ in range(random.randint(1, 4)))
            b = "".join(random.choice(alphabet) for _ in range(random.randint(1, 4)))
            yield a + b


def generate_rejected_words(
    tree: dict,
    count: int = 10,
    max_attempts: int = 10_000,
) -> List[str]:
    """
    Generate exactly `count` unique words guaranteed to be rejected by the DFA.

    Args:
        tree:          Parse tree (unused here, reserved for future heuristics)
        count:         Number of rejected words to produce
        max_attempts:  Hard ceiling on DFA checks before giving up

    Raises:
        RuntimeError if `count` confirmed-rejected words cannot be found within
        max_attempts checks (very unlikely for any non-trivial regex).
    """

    alphabet = get_regex_alphabet(tree)

    regex = regex_from_tree(tree)
    automaton = build_DKA(tree, regex)

    seen: set[str] = set()
    words: List[str] = []
    attempts = 0

    for candidate in _candidate_rejected_words(alphabet):
        if len(words) == count:
            break
        if attempts >= max_attempts:
            raise RuntimeError(
                f"Could not find {count} rejected words within {max_attempts} attempts. "
                "The regex may accept almost all strings over this alphabet."
            )
        attempts += 1

        if candidate in seen:
            continue
        seen.add(candidate)

        if _check_word_rejected(candidate, automaton):
            words.append(candidate)

    return words


if __name__ == "__main__":
    # Example usage (requires a parsed tree and DFA instance):
    regex = "j{t∗}[E|s]"
    tree = get_ast_from_regex(regex)
    alphabet = get_regex_alphabet(tree)
    dka = build_DKA(tree, regex)

    accepted = generate_accepted_words(tree, count=10, max_iterations=5)
    print(accepted)
    rejected = generate_rejected_words(tree, count=10, max_attempts=1000)
    print(rejected)