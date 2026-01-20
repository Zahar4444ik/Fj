import random
from typing import List


def generate_from_tree(node: dict, alphabet: List[str], max_iterations: int = 3) -> str:
    """
    Recursively generate a word from parse tree.

    Args:
        node: Parse tree node
        alphabet: List of valid symbols
        max_iterations: Maximum repetitions for {}

    Returns:
        Generated word as string
    """
    node_type = node.get("type")

    if node_type == "symbol":
        value = node.get("value", "")
        # Skip structural symbols like <PIPE>, <LPAREN>, etc.
        if value.startswith("<"):
            return ""
        return value

    elif node_type == "regular":
        children = node.get("children", [])
        return "".join(generate_from_tree(child, alphabet, max_iterations) for child in children)

    elif node_type == "alternative":
        # Choose one of the alternatives (skip PIPE symbols)
        children = node.get("children", [])
        sequences = [c for c in children if c.get("type") != "symbol"]
        if sequences:
            chosen = random.choice(sequences)
            return generate_from_tree(chosen, alphabet, max_iterations)
        return ""

    elif node_type == "sequence":
        children = node.get("children", [])
        return "".join(generate_from_tree(child, alphabet, max_iterations) for child in children)

    elif node_type == "element":
        children = node.get("children", [])

        # Check for special constructs
        if len(children) >= 3:
            first_symbol = children[0].get("value", "")

            # {} - zero or more (star)
            if first_symbol == "<LBRACE>":
                iterations = random.randint(0, max_iterations)
                inner = children[1]
                return "".join(generate_from_tree(inner, alphabet, max_iterations) for _ in range(iterations))

            # [] - optional
            elif first_symbol == "<LBRACKET>":
                if random.choice([True, False]):
                    return generate_from_tree(children[1], alphabet, max_iterations)
                return ""

            # () - grouping
            elif first_symbol == "<LPAREN>":
                return generate_from_tree(children[1], alphabet, max_iterations)

        # Single symbol
        return "".join(generate_from_tree(child, alphabet, max_iterations) for child in children)

    return ""


def generate_accepted_words(tree: dict, alphabet: List[str], count: int = 10,
                            max_iterations: int = 3) -> List[str]:
    """
    Generate words that should be ACCEPTED by the regex.

    Args:
        tree: Parse tree from Parser
        alphabet: List of valid symbols
        count: Number of words to generate
        max_iterations: Maximum repetitions for {}

    Returns:
        List of accepted words
    """
    words = set()
    attempts = 0
    max_attempts = count * 10

    while len(words) < count and attempts < max_attempts:
        try:
            word = generate_from_tree(tree, alphabet, max_iterations)
            words.add(word)
        except Exception:
            pass
        attempts += 1

    return list(words)


def mutate_word(word: str, alphabet: List[str]) -> str:
    """
    Mutate a word by adding, removing, or changing characters.

    Args:
        word: Original word
        alphabet: List of valid symbols

    Returns:
        Mutated word
    """
    if not word:
        # If empty, return a random word
        length = random.randint(1, 3)
        return ''.join(random.choice(alphabet) for _ in range(length))

    mutation_type = random.choice(['add', 'remove', 'change'])

    if mutation_type == 'add':
        # Add random character at random position
        pos = random.randint(0, len(word))
        return word[:pos] + random.choice(alphabet) + word[pos:]

    elif mutation_type == 'remove' and len(word) > 1:
        # Remove random character
        pos = random.randint(0, len(word) - 1)
        return word[:pos] + word[pos + 1:]

    elif mutation_type == 'change':
        # Change random character
        pos = random.randint(0, len(word) - 1)
        new_char = random.choice([c for c in alphabet if c != word[pos]])
        if new_char:
            return word[:pos] + new_char + word[pos + 1:]

    return word


def violate_structure(word: str, alphabet: List[str]) -> str:
    """
    Violate word structure by duplication, truncation, swapping, or insertion.

    Args:
        word: Original word
        alphabet: List of valid symbols

    Returns:
        Word with violated structure
    """
    if not word:
        # If empty, return a random word
        length = random.randint(1, 5)
        return ''.join(random.choice(alphabet) for _ in range(length))

    violation_type = random.choice(['duplicate', 'truncate', 'swap', 'insert'])

    if violation_type == 'duplicate' and len(word) > 0:
        # Duplicate a part
        pos = random.randint(0, len(word))
        return word[:pos] + word[:pos]

    elif violation_type == 'truncate' and len(word) > 1:
        # Remove a portion
        length = random.randint(1, len(word) - 1)
        return word[:length]

    elif violation_type == 'swap' and len(word) > 1:
        # Swap two characters
        i = random.randint(0, len(word) - 2)
        chars = list(word)
        chars[i], chars[i + 1] = chars[i + 1], chars[i]
        return ''.join(chars)

    elif violation_type == 'insert':
        # Insert random characters
        pos = random.randint(0, len(word))
        insert_len = random.randint(1, 3)
        insertion = ''.join(random.choice(alphabet) for _ in range(insert_len))
        return word[:pos] + insertion + word[pos:]

    return word


def generate_rejected_words(tree: dict, alphabet: List[str], count: int = 10,
                            max_iterations: int = 3) -> List[str]:
    """
    Generate words that are likely REJECTED by the regex.
    Note: Some generated words might still be accepted - your reference automaton
    will filter these during testing.

    Args:
        tree: Parse tree from Parser
        alphabet: List of valid symbols
        count: Number of words to generate
        max_iterations: Maximum repetitions for {}

    Returns:
        List of potentially rejected words
    """
    rejected = set()

    # Strategy 1: Random words from alphabet (count // 3)
    for _ in range(count // 3):
        length = random.randint(1, 10)
        word = ''.join(random.choice(alphabet) for _ in range(length))
        rejected.add(word)

    # Strategy 2: Mutate accepted words (count // 3)
    accepted = generate_accepted_words(tree, alphabet, count // 3, max_iterations)
    for word in accepted:
        mutated = mutate_word(word, alphabet)
        rejected.add(mutated)

    # Strategy 3: Violate structure (count // 3)
    for _ in range(count // 3):
        base_word = generate_from_tree(tree, alphabet, max_iterations)
        violated = violate_structure(base_word, alphabet)
        rejected.add(violated)

    # Convert to list and trim to requested count
    result = list(rejected)[:count]

    # Fill with random words if needed
    while len(result) < count:
        length = random.randint(1, 8)
        word = ''.join(random.choice(alphabet) for _ in range(length))
        if word not in result:
            result.append(word)

    return result


# Example usage and testing
if __name__ == "__main__":
    from core.regex.frontend.lexer import Lexer
    from core.regex.frontend.parser import Parser

    ALPHABET = ['a', 'b', 'c', 'd']

    # Example regex patterns
    test_patterns = [
        "a|b",  # Simple union
        "ab",  # Concatenation
        "{a}b",  # Star then symbol
        "[a]b",  # Optional then symbol
        "(a|b)c",  # Grouped union then symbol
        "a{bc}d",  # Symbol, star group, symbol
    ]

    for pattern in test_patterns:
        print(f"\n{'=' * 50}")
        print(f"Pattern: {pattern}")
        print('=' * 50)

        # Parse the regex
        lexer = Lexer(pattern)
        parser = Parser(lexer)
        tree = parser.parse()

        # Generate words
        accepted = generate_accepted_words(tree, ALPHABET, count=5, max_iterations=3)
        rejected = generate_rejected_words(tree, ALPHABET, count=5, max_iterations=3)

        print(f"\nAccepted words: {accepted}")
        print(f"Rejected words: {rejected}")
        print(f"\nNote: Some 'rejected' words might actually be accepted.")
        print(f"Your reference automaton will verify during testing.")