from tasks.task1_isomorphism.generator.automata.canonical import canonical_signature
from tasks.task1_isomorphism.generator.automata.normalize import normalize_automaton
from tasks.task1_isomorphism.generator.automata.parser import parse_fsa


def check_alphabet(reference, student):
    return reference.alphabet == student.alphabet


def check_isomorphism(reference, student):
    if reference.is_dfa != student.is_dfa:
        return False
    ref_sig, _, _ = canonical_signature(reference)
    stu_sig, _, _ = canonical_signature(student)
    return ref_sig == stu_sig


def check_annotations(reference, student):
    _, ref_ann, _ = canonical_signature(reference)
    _, stu_ann, _ = canonical_signature(student)
    return ref_ann == stu_ann


def prepare_automaton_for_fsa_test(file):
    a = parse_fsa(file)
    normalize_automaton(a)
    return a