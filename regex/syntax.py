ALPHABET = ['1', '2', 'c', 'd']


OPERATORS = {
    "union": "|",
    "concat": "",
    "star": "{}",
    "optional": "[]",
    "plus": "{a}",
}

# Define precedence levels (lower number = higher precedence)
PRECEDENCE = {
    "group": 4,
    "star": 3,
    "optional": 3,
    "plus": 3,
    "concat": 2,
    "union": 1
}
