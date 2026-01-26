import random

from core.regex.generators.random_regex import generate_regex


def generate_assignment_variables(seed=None):
    random.seed(seed)

    automaton_type = random.choice(["NKA", "DKA"])
    implementation = random.choice(["iterative", "recursive"])

    regex = generate_regex()

    assignment = {
        "regex": regex,
        "automaton_type": automaton_type,
        "implementation": implementation,
    }

    return assignment
