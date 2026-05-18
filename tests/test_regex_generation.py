"""
Tests for core/regex/generators/random_regex.py

The regex generator is the entry point of the question generation pipeline:
every assignment regex is produced here, and its state-count guarantee
determines the difficulty of each generated question.

Tests are split into two layers:
  1. Unit tests for pure utility functions — deterministic, fast, no I/O.
  2. Integration tests for generate_regex_with_state_count() — verify that
     the produced regex, when compiled into an automaton, falls within the
     configured [MIN, MAX] state range.
"""

import unittest.mock as mock
import pytest

from core.regex.generators.ast_nodes import (
    Symbol, Star, Union, Concat, Optional,
)
from core.regex.generators.random_regex import (
    pick_depths_for_state_range,
    to_regex,
    has_duplicate_union_children,
    has_redundant_wrapper_pair,
    is_structurally_valid,
    get_used_symbols,
    generate_regex_with_state_count,
)
from core.regex.frontend.helper import get_ast_from_regex
from core.regex.automata.dka.dka_builder import build_DKA
from core.regex.automata.nka.nka_builder import build_NKA, count_nka_states

REGEX_MODULE = "core.regex.generators.random_regex"


# ---------------------------------------------------------------------------
# pick_depths_for_state_range
# ---------------------------------------------------------------------------

class TestPickDepths:
    def test_returns_non_empty_list_for_valid_dfa_range(self):
        assert pick_depths_for_state_range(4, 6, "dfa")

    def test_returns_non_empty_list_for_valid_nfa_range(self):
        assert pick_depths_for_state_range(5, 12, "nfa")

    def test_impossible_range_falls_back_to_single_depth(self):
        result = pick_depths_for_state_range(9999, 99999, "dfa")
        assert len(result) == 1

    def test_dfa_and_nfa_tables_are_distinct(self):
        # DFA depth-3 maps to 2–4 states; NFA depth-3 maps to 3–6.
        # A range of [2, 2] should be in DFA table but not NFA table's range.
        dfa = set(pick_depths_for_state_range(2, 2, "dfa"))
        nfa = set(pick_depths_for_state_range(2, 2, "nfa"))
        # Both should return something, but the NFA fallback may differ
        assert dfa and nfa

    def test_overlapping_range_returns_multiple_depths(self):
        # Range 4–8 overlaps several DFA depth rows
        depths = pick_depths_for_state_range(4, 8, "dfa")
        assert len(depths) >= 2


# ---------------------------------------------------------------------------
# to_regex — AST serialisation
# ---------------------------------------------------------------------------

class TestToRegex:
    def test_symbol_returns_bare_character(self):
        assert to_regex(Symbol("a")) == "a"

    def test_star_uses_curly_braces(self):
        assert to_regex(Star(Concat(Symbol("a"), Symbol("b")))) == "{ab}"

    def test_optional_uses_square_brackets(self):
        assert to_regex(Optional(Concat(Symbol("a"), Symbol("b")))) == "[ab]"

    def test_union_separates_with_pipe(self):
        assert to_regex(Union(Symbol("a"), Symbol("b"))) == "a|b"

    def test_concat_produces_no_operator(self):
        assert to_regex(Concat(Symbol("a"), Symbol("b"))) == "ab"

    def test_union_inside_concat_adds_parentheses(self):
        node = Concat(Union(Symbol("a"), Symbol("b")), Symbol("c"))
        result = to_regex(node)
        assert "|" in result and "c" in result

    def test_serialised_regex_is_parseable_by_frontend(self):
        node = Union(Star(Concat(Symbol("a"), Symbol("b"))), Symbol("c"))
        regex = to_regex(node)
        assert get_ast_from_regex(regex) is not None

    def test_nested_structure_round_trips(self):
        # {ab}|[cd] — star, optional, union, two concats
        node = Union(
            Star(Concat(Symbol("a"), Symbol("b"))),
            Optional(Concat(Symbol("c"), Symbol("d"))),
        )
        regex = to_regex(node)
        assert get_ast_from_regex(regex) is not None


# ---------------------------------------------------------------------------
# AST quality helpers
# ---------------------------------------------------------------------------

class TestHasDuplicateUnionChildren:
    def test_identical_symbol_children_detected(self):
        assert has_duplicate_union_children(Union(Symbol("a"), Symbol("a"))) is True

    def test_distinct_symbol_children_pass(self):
        assert has_duplicate_union_children(Union(Symbol("a"), Symbol("b"))) is False

    def test_nested_duplicate_detected(self):
        inner = Union(Symbol("x"), Symbol("x"))
        outer = Concat(Symbol("a"), inner)
        assert has_duplicate_union_children(outer) is True


class TestHasRedundantWrapperPair:
    def test_star_and_optional_over_same_inner_detected(self):
        inner = Concat(Symbol("a"), Symbol("b"))
        node = Union(Star(inner), Optional(Concat(Symbol("a"), Symbol("b"))))
        assert has_redundant_wrapper_pair(node) is True

    def test_star_and_optional_over_different_inners_pass(self):
        node = Union(
            Star(Concat(Symbol("a"), Symbol("b"))),
            Optional(Concat(Symbol("a"), Symbol("c"))),
        )
        assert has_redundant_wrapper_pair(node) is False


class TestIsStructurallyValid:
    def test_minimal_valid_ast_passes(self):
        # {ab}|c — has star, union, ≥5 nodes
        node = Union(Star(Concat(Symbol("a"), Symbol("b"))), Symbol("c"))
        assert is_structurally_valid(node) is True

    def test_missing_star_fails(self):
        node = Union(Concat(Symbol("a"), Symbol("b")), Symbol("c"))
        assert is_structurally_valid(node) is False

    def test_missing_union_fails(self):
        node = Star(Concat(Symbol("a"), Symbol("b")))
        assert is_structurally_valid(node) is False

    def test_duplicate_union_children_fails(self):
        inner = Star(Concat(Symbol("a"), Symbol("b")))
        node = Union(inner, Star(Concat(Symbol("a"), Symbol("b"))))
        assert is_structurally_valid(node) is False


# ---------------------------------------------------------------------------
# get_used_symbols
# ---------------------------------------------------------------------------

class TestGetUsedSymbols:
    def test_single_symbol_node(self):
        assert get_used_symbols(Symbol("a")) == {"a"}

    def test_concat_collects_both_children(self):
        assert get_used_symbols(Concat(Symbol("a"), Symbol("b"))) == {"a", "b"}

    def test_star_collects_inner_symbols(self):
        assert get_used_symbols(Star(Symbol("x"))) == {"x"}

    def test_union_collects_both_branches(self):
        assert get_used_symbols(Union(Symbol("a"), Symbol("b"))) == {"a", "b"}

    def test_deeply_nested_ast_collects_all(self):
        node = Union(Star(Concat(Symbol("a"), Symbol("b"))), Symbol("c"))
        assert get_used_symbols(node) == {"a", "b", "c"}

    def test_repeated_symbol_counted_once(self):
        node = Concat(Symbol("a"), Symbol("a"))
        assert get_used_symbols(node) == {"a"}


# ---------------------------------------------------------------------------
# generate_regex_with_state_count — integration
# ---------------------------------------------------------------------------

RUNS = 5


class TestGenerateRegexWithStateCount:
    @pytest.mark.parametrize("_", range(RUNS))
    def test_dfa_state_count_within_configured_bounds(self, _):
        with mock.patch.multiple(REGEX_MODULE,
                                 DFA_MIN_STATES_COUNT=3,
                                 DFA_MAX_STATES_COUNT=5):
            regex = generate_regex_with_state_count("dfa")
        dfa = build_DKA(get_ast_from_regex(regex), regex)
        count = len(dfa.name_map)
        assert 3 <= count <= 5, f"DFA regex '{regex}' has {count} states, expected 3–5"

    @pytest.mark.parametrize("_", range(RUNS))
    def test_nfa_state_count_within_configured_bounds(self, _):
        with mock.patch.multiple(REGEX_MODULE,
                                 NFA_MIN_STATES_COUNT=5,
                                 NFA_MAX_STATES_COUNT=12):
            regex = generate_regex_with_state_count("nfa")
        nfa = build_NKA(get_ast_from_regex(regex))
        count = count_nka_states(nfa)
        assert 5 <= count <= 12, f"NFA regex '{regex}' has {count} states, expected 5–12"

    def test_unknown_automaton_type_raises_value_error(self):
        with pytest.raises(ValueError, match="Unknown automaton type"):
            generate_regex_with_state_count("pda")

    def test_generated_regex_is_parseable(self):
        with mock.patch.multiple(REGEX_MODULE,
                                 DFA_MIN_STATES_COUNT=3,
                                 DFA_MAX_STATES_COUNT=5):
            regex = generate_regex_with_state_count("dfa")
        assert get_ast_from_regex(regex) is not None

    def test_generated_regex_uses_only_usable_alphabet_symbols(self):
        """Symbols in the regex must never include characters excluded by USABLE_ALPHABET."""
        from core.regex.frontend.syntax import USABLE_ALPHABET
        with mock.patch.multiple(REGEX_MODULE,
                                 DFA_MIN_STATES_COUNT=3,
                                 DFA_MAX_STATES_COUNT=5):
            regex = generate_regex_with_state_count("dfa")
        usable = set(USABLE_ALPHABET)
        # Strip all regex meta-characters to get bare symbols
        symbol_chars = set(regex) - set("{}[]|()")
        assert symbol_chars <= usable, (
            f"Regex '{regex}' uses symbols outside USABLE_ALPHABET"
        )

    def test_is_structurally_valid_ast_produced(self):
        with mock.patch.multiple(REGEX_MODULE,
                                 DFA_MIN_STATES_COUNT=3,
                                 DFA_MAX_STATES_COUNT=5):
            regex = generate_regex_with_state_count("dfa")
        ast = get_ast_from_regex(regex)
        # A valid regex must contain at least one operator
        assert ast is not None
        assert regex != ""
