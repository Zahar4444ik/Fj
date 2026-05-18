from pathlib import Path

from graders.isomorphism.checker.compare import (
    check_isomorphism,
    check_annotations,
    prepare_automaton_for_fsa_test,
)

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"


def fsa(path):
    return str(DATA_DIR / path)


def load(path):
    a, errors = prepare_automaton_for_fsa_test(fsa(path))
    assert not errors, f"Syntax errors in {path}: {errors}"
    return a


def check(f1, f2, expected):
    a1, error = prepare_automaton_for_fsa_test(fsa(f1))
    a2, error = prepare_automaton_for_fsa_test(fsa(f2))
    assert check_isomorphism(a1, a2) is expected


# ---------------------------------------------------------------------------
# Isomorphism — structural equivalence
# ---------------------------------------------------------------------------

def test_dka_simple_equivalent():
    check("dka/dka1.fsa", "dka/dka2.fsa", True)


def test_dka_reordered_transitions():
    check("dka/dka_reordered1.fsa", "dka/dka_reordered2.fsa", True)


def test_dka_different_transitions():
    check("dka/dka_bad1.fsa", "dka/dka_bad2.fsa", False)


def test_nka_simple_equivalent():
    check("nka/nka1.fsa", "nka/nka2.fsa", True)


def test_nka_reordered_transitions():
    check("nka/nka_reordered1.fsa", "nka/nka_reordered2.fsa", True)


def test_nka_different_transitions():
    check("nka/nka_bad1.fsa", "nka/nka_bad2.fsa", False)


# ---------------------------------------------------------------------------
# Annotation checking — DFA state labels
# ---------------------------------------------------------------------------

def test_dka_matching_annotations_score_full():
    """Two isomorphic DFAs with identical annotations must score 3/3."""
    a1 = load("dka/dka_annotated1.fsa")
    a2 = load("dka/dka_annotated2.fsa")
    correct, total = check_annotations(a1, a2)
    assert correct == total


def test_dka_wrong_annotation_reduces_score():
    """A DFA with one wrong annotation must score less than full marks."""
    ref = load("dka/dka_annotated1.fsa")
    wrong = load("dka/dka_annotated_wrong.fsa")
    correct, total = check_annotations(ref, wrong)
    assert correct < total


def test_dka_annotation_check_is_symmetric():
    """check_annotations(a, b) and check_annotations(b, a) must agree."""
    a1 = load("dka/dka_annotated1.fsa")
    a2 = load("dka/dka_annotated2.fsa")
    c1, t1 = check_annotations(a1, a2)
    c2, t2 = check_annotations(a2, a1)
    assert c1 == c2 and t1 == t2


def test_dka_annotation_total_equals_state_count():
    """Total annotation slots must equal the number of states in the reference."""
    a = load("dka/dka_annotated1.fsa")
    _, total = check_annotations(a, a)
    assert total == len(a.states)
