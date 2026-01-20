from tasks.task1_isomorphism.generator.automata.canonical import canonical_signature
from tasks.task1_isomorphism.generator.automata.normalize import normalize_automaton
from tasks.task1_isomorphism.generator.automata.parser import parse_fsa


def structurally_equivalent(a1, a2):
    if a1.is_dfa != a2.is_dfa:
        return False
    return canonical_signature(a1) == canonical_signature(a2)


def compare(file1, file2):
    a1 = parse_fsa(file1)
    a2 = parse_fsa(file2)

    normalize_automaton(a1)
    normalize_automaton(a2)

    return structurally_equivalent(a1, a2)