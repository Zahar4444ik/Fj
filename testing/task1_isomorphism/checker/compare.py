from testing.task1_isomorphism.generator.automata.canonical import canonical_signature
from testing.task1_isomorphism.generator.automata.normalize import normalize_automaton
from testing.task1_isomorphism.generator.automata.parser import parse_fsa


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

    total = len(ref_ann)
    correct = sum(1 for cid, ann in ref_ann.items() if stu_ann.get(cid) == ann)
    return correct, total


def prepare_automaton_for_fsa_test(file):
    a, syntax_errors = parse_fsa(file)
    if not syntax_errors:
        normalize_automaton(a)
    return a, syntax_errors