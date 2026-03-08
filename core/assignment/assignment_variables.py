import random

from core.regex.generators.regex.random_regex import generate_regex_with_state_count


def generate_assignment_variables(seed=None):
    random.seed(seed)

    automaton_type = random.choice(["nfa", "dfa"])
    implementation = random.choice(["iterative", "recursive"])

    regex = generate_regex_with_state_count()

    assignment = {
        "regex": regex,
        "automaton_type": automaton_type,
        "implementation": implementation,
    }

    return assignment
