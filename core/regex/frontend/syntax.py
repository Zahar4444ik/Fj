import string

ALPHABET = (
    list(string.ascii_lowercase) +
    list(string.ascii_uppercase) +
    list(string.digits) +
    list("!@$%^&*-+=<>?~")
)


OPERATORS = {
    "union": "|",
    "concat": "",
    "star": "{}",
    "optional": "[]",
    "group": "()",
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
