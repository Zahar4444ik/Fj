"""
Tests for core/regex/automata/nka/thompson_nka_builder.py

Verifies three properties:
  1. Structural invariant  — Thompson NFAs always have exactly one accept state
  2. Language equivalence  — Thompson and custom builder accept the same words
  3. Non-isomorphism       — the two constructions produce structurally different NFAs,
                             confirming the fallback check is genuinely needed
"""

import pytest

from core.regex.automata.nka.nka_builder import (
    build_NKA,
    symbol_NKA as custom_symbol,
    concat_NKA as custom_concat,
    union_NKA as custom_union,
    kleene_star_NKA as custom_star,
    optional_NKA as custom_optional,
)
from core.regex.automata.nka.thompson_nka_builder import (
    build_thompson_NKA,
    symbol_NKA as thompson_symbol,
    concat_NKA as thompson_concat,
    union_NKA as thompson_union,
    kleene_star_NKA as thompson_star,
    optional_NKA as thompson_optional,
)
from core.regex.frontend.helper import get_ast_from_regex
from graders.isomorphism.checker.compare import check_isomorphism
from core.regex.generators.fsa.fsa_generator import fsa_from_nka
import tempfile, os


# ---------------------------------------------------------------------------
# NFA simulator (ε-closure BFS)
# ---------------------------------------------------------------------------

def _epsilon_closure(states):
    closure = set(states)
    stack = list(states)
    while stack:
        s = stack.pop()
        for ns in s.transitions.get('', set()):
            if ns not in closure:
                closure.add(ns)
                stack.append(ns)
    return closure


def nfa_accepts(nka, word):
    current = _epsilon_closure({nka.start})
    for ch in word:
        nxt = set()
        for s in current:
            for ns in s.transitions.get(ch, set()):
                nxt.add(ns)
        current = _epsilon_closure(nxt)
    return bool(current & nka.accepts)


# ---------------------------------------------------------------------------
# Helper: write NFA to a tmp .fsa file, return path
# ---------------------------------------------------------------------------

def _to_fsa_file(nka, alphabet):
    fd, path = tempfile.mkstemp(suffix=".fsa")
    os.close(fd)
    fsa_from_nka(nka, filename=path, alphabet=alphabet)
    return path


# ---------------------------------------------------------------------------
# 1. Structural invariant: Thompson NFAs must have exactly one accept state
# ---------------------------------------------------------------------------

class TestThompsonInvariant:
    def test_symbol_has_one_accept(self):
        nka = thompson_symbol("a")
        assert len(nka.accepts) == 1

    def test_concat_has_one_accept(self):
        nka = thompson_concat(thompson_symbol("a"), thompson_symbol("b"))
        assert len(nka.accepts) == 1

    def test_union_has_one_accept(self):
        nka = thompson_union(thompson_symbol("a"), thompson_symbol("b"))
        assert len(nka.accepts) == 1

    def test_star_has_one_accept(self):
        nka = thompson_star(thompson_symbol("a"))
        assert len(nka.accepts) == 1

    def test_optional_has_one_accept(self):
        nka = thompson_optional(thompson_symbol("a"))
        assert len(nka.accepts) == 1

    def test_complex_expression_has_one_accept(self):
        # {ab}|[c]  →  star(concat(a,b)) union optional(c)
        inner = thompson_star(thompson_concat(thompson_symbol("a"), thompson_symbol("b")))
        opt = thompson_optional(thompson_symbol("c"))
        nka = thompson_union(inner, opt)
        assert len(nka.accepts) == 1

    def test_custom_union_has_multiple_accepts(self):
        """Confirm the custom builder does NOT keep one-accept — so the invariant test is meaningful."""
        nka = custom_union(custom_symbol("a"), custom_symbol("b"))
        assert len(nka.accepts) > 1

    def test_custom_star_has_multiple_accepts(self):
        nka = custom_star(custom_symbol("a"))
        assert len(nka.accepts) > 1


# ---------------------------------------------------------------------------
# 2. Language equivalence: same words accepted by both builders
# ---------------------------------------------------------------------------

REGEX_CASES = [
    ("{ab}",        {"", "ab", "abab", "ababab"}, {"a", "b", "aba", "ba"}),
    ("a|b",         {"a", "b"},                   {"", "ab", "c"}),
    ("[a]b",        {"b", "ab"},                  {"", "a", "ba"}),
    ("{a|b}c",      {"c", "ac", "bc", "abc"},     {"", "a", "b", "ab"}),
    ("a{b}",        {"a", "ab", "abb", "abbb"},   {"", "b", "ba"}),
]


class TestLanguageEquivalence:
    @pytest.mark.parametrize("regex,accept_words,reject_words", REGEX_CASES)
    def test_thompson_accepts_same_words(self, regex, accept_words, reject_words):
        ast = get_ast_from_regex(regex)
        custom = build_NKA(ast)
        thompson = build_thompson_NKA(ast)
        for word in accept_words:
            assert nfa_accepts(custom, word) == nfa_accepts(thompson, word), (
                f"Disagreement on accepted word '{word}' for regex '{regex}'"
            )
        for word in reject_words:
            assert nfa_accepts(custom, word) == nfa_accepts(thompson, word), (
                f"Disagreement on rejected word '{word}' for regex '{regex}'"
            )

    @pytest.mark.parametrize("regex,accept_words,_", REGEX_CASES)
    def test_thompson_accepts_all_expected_words(self, regex, accept_words, _):
        ast = get_ast_from_regex(regex)
        thompson = build_thompson_NKA(ast)
        for word in accept_words:
            assert nfa_accepts(thompson, word), (
                f"Thompson NFA for '{regex}' should accept '{word}'"
            )

    @pytest.mark.parametrize("regex,_,reject_words", REGEX_CASES)
    def test_thompson_rejects_all_expected_words(self, regex, _, reject_words):
        ast = get_ast_from_regex(regex)
        thompson = build_thompson_NKA(ast)
        for word in reject_words:
            assert not nfa_accepts(thompson, word), (
                f"Thompson NFA for '{regex}' should reject '{word}'"
            )


# ---------------------------------------------------------------------------
# 3. Non-isomorphism: Thompson and custom produce different structures
#    (confirms the fallback check is actually needed in evaluation)
# ---------------------------------------------------------------------------

class TestNonIsomorphism:
    def _compare_via_fsa(self, regex, alphabet):
        ast = get_ast_from_regex(regex)
        custom = build_NKA(ast)
        thompson = build_thompson_NKA(ast)

        p1 = _to_fsa_file(custom, alphabet)
        p2 = _to_fsa_file(thompson, alphabet)
        try:
            from graders.isomorphism.checker.compare import prepare_automaton_for_fsa_test
            a1, _ = prepare_automaton_for_fsa_test(p1)
            a2, _ = prepare_automaton_for_fsa_test(p2)
            return check_isomorphism(a1, a2)
        finally:
            os.unlink(p1)
            os.unlink(p2)

    def test_union_constructions_are_not_isomorphic(self):
        assert self._compare_via_fsa("a|b", {"a", "b"}) is False

    def test_star_constructions_are_not_isomorphic(self):
        assert self._compare_via_fsa("{a}", {"a"}) is False

    def test_optional_constructions_are_not_isomorphic(self):
        assert self._compare_via_fsa("[a]", {"a"}) is False

    def test_concat_only_constructions_are_isomorphic(self):
        """Concat is identical in both builders — should be isomorphic."""
        assert self._compare_via_fsa("ab", {"a", "b"}) is True
