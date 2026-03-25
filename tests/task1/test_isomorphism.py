from pathlib import Path

from testing.task1_isomorphism.checker.compare import check_isomorphism, prepare_automaton_for_fsa_test

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"


def fsa(path):
    return str(DATA_DIR / path)


def check(f1, f2, expected):
    a1, error = prepare_automaton_for_fsa_test(fsa(f1))
    a2, error = prepare_automaton_for_fsa_test(fsa(f2))
    assert check_isomorphism(a1, a2) is expected


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
