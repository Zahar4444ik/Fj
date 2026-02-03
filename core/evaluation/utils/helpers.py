def bad_word_ratio(level: int) -> float:
    """
    Maps difficulty level to ratio of rejected words.
    0 → 0%
    1 → 10%
    2 → 20%
    3 → 30%
    """
    return {
        0: 0.0,
        1: 0.1,
        2: 0.2,
        3: 0.3,
    }[level]


def split_into_groups(words, group_size):
    return [
        words[i:i + group_size]
        for i in range(0, len(words), group_size)
    ]