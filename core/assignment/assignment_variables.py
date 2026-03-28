import random

from core.config.settings_parse import AUTOMATON_TYPE, IMPLEMENTATION_TYPE
from core.regex.generators.random_regex import generate_regex_with_state_count


def generate_assignment_variables(seed=None):
    random.seed(seed)

    if AUTOMATON_TYPE == "any":
        automaton_type = random.choice(["nfa", "dfa"])
    else:
        automaton_type = AUTOMATON_TYPE

    if IMPLEMENTATION_TYPE == "any":
        implementation_type = random.choice(["iterative", "recursive"])
    else:
        implementation_type = IMPLEMENTATION_TYPE

    regex = generate_regex_with_state_count(automaton_type)

    assignment = {
        "regex": regex,
        "automaton_type": automaton_type,
        "implementation": implementation_type,
    }

    return assignment
