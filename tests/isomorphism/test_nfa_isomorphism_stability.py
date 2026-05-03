"""
Tests for NFA isomorphism stability across multiple build_NKA() calls.

The root cause of instability: build_NKA() assigns q-names via list(set_of_State_objects),
whose iteration order depends on hash(memory_address) — different per call.
The fix in canonical.py sorts NFA branch targets by structural properties instead
of arbitrary string names, so structurally equivalent NFAs produce the same signature.
"""

import tempfile
import os
import pytest

from core.regex.frontend.helper import get_ast_from_regex
from core.regex.automata.nka.nka_builder import build_NKA
from core.regex.automata.dka.dka_builder import build_DKA
from core.regex.generators.fsa.fsa_generator import fsa_from_nka
from graders.isomorphism.checker.compare import (
    prepare_automaton_for_fsa_test,
    check_isomorphism,
    check_annotations,
)
from graders.isomorphism.fsa_parser.automata.canonical import canonical_signature


RUNS = 10


def _build_nka_automata(regex: str, runs: int):
    """Build `runs` NFA automata for the given regex and return loaded automaton objects."""
    automata = []
    with tempfile.TemporaryDirectory() as tmpdir:
        paths = []
        for i in range(runs):
            ast = get_ast_from_regex(regex)
            nka = build_NKA(ast)
            path = os.path.join(tmpdir, f"nka_{i}.fsa")
            fsa_from_nka(nka, filename=path)
            paths.append(path)

        for path in paths:
            a, errors = prepare_automaton_for_fsa_test(path)
            assert not errors, f"Syntax errors in generated FSA: {errors}"
            automata.append(a)
    return automata


def _build_dka_automata(regex: str, runs: int):
    """Build `runs` DFA automata for the given regex and return loaded automaton objects."""
    automata = []
    with tempfile.TemporaryDirectory() as tmpdir:
        paths = []
        for i in range(runs):
            ast = get_ast_from_regex(regex)
            dka = build_DKA(ast, regex)
            path = os.path.join(tmpdir, f"dka_{i}.fsa")
            fsa_from_nka(dka, filename=path)
            paths.append(path)

        for path in paths:
            a, errors = prepare_automaton_for_fsa_test(path)
            assert not errors, f"Syntax errors in generated FSA: {errors}"
            automata.append(a)
    return automata


# ---------------------------------------------------------------------------
# NFA stability tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("regex", [
    "Z(i5|{55})",       # original regression case
    "a|b",              # simple alternation with epsilon branches
    "{a|b}c",           # kleene + alternation
    "(a|b)(c|d)",       # two alternations
    "a{b|c}d",          # nested kleene
    "4t|ti",            # symmetric branches: one direct-accept vs one intermediate
    "(ac|b)|(a|bc)",    # depth-3 asymmetry: 2-level lookahead is insufficient
])
def test_nfa_isomorphism_stable_across_runs(regex):
    """All NFA builds from the same regex must be mutually isomorphic."""
    automata = _build_nka_automata(regex, RUNS)
    ref = automata[0]
    for i, a in enumerate(automata[1:], start=1):
        assert check_isomorphism(ref, a), (
            f"NFA run {i} is NOT isomorphic to run 0 for regex '{regex}'"
        )


@pytest.mark.parametrize("regex", [
    "Z(i5|{55})",
    "a|b",
    "{a|b}c",
    "(a|b)(c|d)",
    "a{b|c}d",
    "4t|ti",
    "(ac|b)|(a|bc)",
])
def test_nfa_annotations_stable_across_runs(regex):
    """All NFA builds from the same regex must produce identical state annotations."""
    automata = _build_nka_automata(regex, RUNS)
    ref = automata[0]
    for i, a in enumerate(automata[1:], start=1):
        correct, total = check_annotations(ref, a)
        assert correct == total, (
            f"NFA run {i} has {correct}/{total} matching annotations for regex '{regex}'"
        )


def test_nfa_canonical_signature_stable():
    """canonical_signature() must return the same result on repeated calls (cache test)."""
    regex = "Z(i5|{55})"
    with tempfile.TemporaryDirectory() as tmpdir:
        ast = get_ast_from_regex(regex)
        nka = build_NKA(ast)
        path = os.path.join(tmpdir, "nka.fsa")
        fsa_from_nka(nka, filename=path)
        a, errors = prepare_automaton_for_fsa_test(path)
        assert not errors

        sig1, ann1, _ = canonical_signature(a)
        # Clear cache to force recomputation
        if hasattr(a, "_canonical_cache"):
            del a._canonical_cache
        sig2, ann2, _ = canonical_signature(a)

        assert sig1 == sig2, "canonical_signature() is not deterministic for the same automaton"
        assert ann1 == ann2


# ---------------------------------------------------------------------------
# DFA stability tests (regression guard — DFA was always stable)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("regex", [
    "{(h|F)h(h|Fh)}k",   # original student report regression
    "a|b",
    "{a|b}c",
])
def test_dfa_isomorphism_stable_across_runs(regex):
    """DFA builds must remain isomorphic across runs (guard against regressions)."""
    automata = _build_dka_automata(regex, RUNS)
    ref = automata[0]
    for i, a in enumerate(automata[1:], start=1):
        assert check_isomorphism(ref, a), (
            f"DFA run {i} is NOT isomorphic to run 0 for regex '{regex}'"
        )


# ---------------------------------------------------------------------------
# Cross-type sanity test
# ---------------------------------------------------------------------------


def test_nfa_and_dfa_are_not_isomorphic_by_type():
    """An NFA and a DFA loaded from FSA files must not be reported as isomorphic
    (is_dfa flag differs, so check_isomorphism returns False)."""
    regex = "ab"
    with tempfile.TemporaryDirectory() as tmpdir:
        ast = get_ast_from_regex(regex)

        nka = build_NKA(ast)
        nka_path = os.path.join(tmpdir, "nka.fsa")
        fsa_from_nka(nka, filename=nka_path)

        dka = build_DKA(ast, regex)
        dka_path = os.path.join(tmpdir, "dka.fsa")
        fsa_from_nka(dka, filename=dka_path)

        a_nka, _ = prepare_automaton_for_fsa_test(nka_path)
        a_dka, _ = prepare_automaton_for_fsa_test(dka_path)

        assert not check_isomorphism(a_nka, a_dka), (
            "NFA and DFA should not be considered isomorphic by check_isomorphism"
        )
