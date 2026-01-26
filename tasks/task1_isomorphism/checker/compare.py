from tasks.task1_isomorphism.generator.automata.canonical import canonical_signature
from tasks.task1_isomorphism.generator.automata.normalize import normalize_automaton
from tasks.task1_isomorphism.generator.automata.parser import parse_fsa


def structurally_equivalent(a1, a2):
    if a1.is_dfa != a2.is_dfa:
        return False
    return canonical_signature(a1) == canonical_signature(a2)


def check_isomorphism(reference, student):
    return structurally_equivalent(reference, student)


def check_annotations(reference, student):
    return reference.annotations == student.annotations


def prepare_automaton_for_fsa_test(file):
    a = parse_fsa(file)
    normalize_automaton(a)
    return a
