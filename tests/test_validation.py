"""
Tests for core/config/validation.py

Validates that the configuration system correctly accepts valid settings
and rejects all categories of invalid input before any pipeline step runs.
Each test isolates one settings group using unittest.mock.patch so the
live .env values do not affect the outcome.
"""

import unittest.mock as mock
import pytest

from core.config.validation import (
    _validate_generation_settings,
    _validate_dka_scoring,
    _validate_nka_scoring,
    _validate_moodle_settings,
)

MODULE = "core.config.validation"

# ---------------------------------------------------------------------------
# Baseline valid configurations — override per test as needed
# ---------------------------------------------------------------------------

VALID_GENERATION = dict(
    CATEGORY="FSA Test",
    NUMBER_OF_QUESTIONS=10,
    DFA_MIN_STATES_COUNT=3,
    DFA_MAX_STATES_COUNT=5,
    NFA_MIN_STATES_COUNT=5,
    NFA_MAX_STATES_COUNT=10,
    AUTOMATON_TYPE="dfa",
    IMPLEMENTATION_TYPE="iterative",
    MAX_ALPHABET_SIZE=3,
    MIN_ALPHABET_SIZE=2,
    REGEX_LATEX_FORMAT=True,
    RESTRICTED_SYMBOLS=set(),
)

VALID_DKA_SCORING = dict(
    DKA_FSA_ISOMORPHISM=30,
    DKA_FSA_ANNOTATIONS=20,
    DKA_IMPLEMENTATION=50,
    TOTAL_SCORE=100,
)

VALID_NKA_SCORING = dict(
    NKA_FSA_ISOMORPHISM=40,
    NKA_IMPLEMENTATION=60,
    TOTAL_SCORE=100,
)

VALID_MOODLE = dict(
    USERNAME="admin",
    PASSWORD="secret",
    ASSIGNMENT_LINK="https://moodle.example.com/quiz",
    QUESTION_NUMBER=1,
    HEADLESS=True,
)


# ---------------------------------------------------------------------------
# Generation settings
# ---------------------------------------------------------------------------

class TestGenerationSettings:
    def test_valid_config_produces_no_errors(self):
        with mock.patch.multiple(MODULE, **VALID_GENERATION):
            assert _validate_generation_settings() == []

    def test_empty_category_is_rejected(self):
        with mock.patch.multiple(MODULE, **{**VALID_GENERATION, "CATEGORY": ""}):
            errors = _validate_generation_settings()
            assert any("CATEGORY" in e for e in errors)

    def test_zero_question_count_is_rejected(self):
        with mock.patch.multiple(MODULE, **{**VALID_GENERATION, "NUMBER_OF_QUESTIONS": 0}):
            errors = _validate_generation_settings()
            assert any("NUMBER_OF_QUESTIONS" in e for e in errors)

    def test_dfa_min_exceeds_max_is_rejected(self):
        with mock.patch.multiple(MODULE, **{
            **VALID_GENERATION,
            "DFA_MIN_STATES_COUNT": 8,
            "DFA_MAX_STATES_COUNT": 5,
        }):
            errors = _validate_generation_settings()
            assert any("DFA_MIN_STATES_COUNT" in e for e in errors)

    def test_nfa_min_exceeds_max_is_rejected(self):
        with mock.patch.multiple(MODULE, **{
            **VALID_GENERATION,
            "NFA_MIN_STATES_COUNT": 15,
            "NFA_MAX_STATES_COUNT": 10,
        }):
            errors = _validate_generation_settings()
            assert any("NFA_MIN_STATES_COUNT" in e for e in errors)

    def test_invalid_automaton_type_is_rejected(self):
        with mock.patch.multiple(MODULE, **{**VALID_GENERATION, "AUTOMATON_TYPE": "pda"}):
            errors = _validate_generation_settings()
            assert any("AUTOMATON_TYPE" in e for e in errors)

    def test_invalid_implementation_type_is_rejected(self):
        with mock.patch.multiple(MODULE, **{**VALID_GENERATION, "IMPLEMENTATION_TYPE": "functional"}):
            errors = _validate_generation_settings()
            assert any("IMPLEMENTATION_TYPE" in e for e in errors)

    def test_min_alphabet_exceeds_max_is_rejected(self):
        with mock.patch.multiple(MODULE, **{
            **VALID_GENERATION,
            "MIN_ALPHABET_SIZE": 5,
            "MAX_ALPHABET_SIZE": 2,
        }):
            errors = _validate_generation_settings()
            assert any("MIN_ALPHABET_SIZE" in e for e in errors)

    def test_restricted_symbols_invalid_character_is_rejected(self):
        with mock.patch.multiple(MODULE, **{**VALID_GENERATION, "RESTRICTED_SYMBOLS": {"!"}}):
            errors = _validate_generation_settings()
            assert any("RESTRICTED_SYMBOLS" in e for e in errors)

    def test_restricted_symbols_leaving_too_few_usable_is_rejected(self):
        from core.regex.frontend.syntax import ALPHABET
        # Keep only 2 usable symbols but MAX_ALPHABET_SIZE=3
        big_restriction = set(ALPHABET[:-2])
        with mock.patch.multiple(MODULE, **{
            **VALID_GENERATION,
            "RESTRICTED_SYMBOLS": big_restriction,
            "MAX_ALPHABET_SIZE": 3,
        }):
            errors = _validate_generation_settings()
            assert any("RESTRICTED_SYMBOLS" in e or "usable" in e.lower() for e in errors)

    def test_empty_restricted_symbols_always_passes(self):
        with mock.patch.multiple(MODULE, **{**VALID_GENERATION, "RESTRICTED_SYMBOLS": set()}):
            errors = _validate_generation_settings()
            assert not any("RESTRICTED_SYMBOLS" in e for e in errors)

    @pytest.mark.parametrize("automaton_type", ["dfa", "nfa", "any"])
    def test_all_valid_automaton_types_are_accepted(self, automaton_type):
        with mock.patch.multiple(MODULE, **{**VALID_GENERATION, "AUTOMATON_TYPE": automaton_type}):
            errors = _validate_generation_settings()
            assert not any("AUTOMATON_TYPE" in e for e in errors)

    @pytest.mark.parametrize("impl_type", ["iterative", "recursive", "any"])
    def test_all_valid_implementation_types_are_accepted(self, impl_type):
        with mock.patch.multiple(MODULE, **{**VALID_GENERATION, "IMPLEMENTATION_TYPE": impl_type}):
            errors = _validate_generation_settings()
            assert not any("IMPLEMENTATION_TYPE" in e for e in errors)


# ---------------------------------------------------------------------------
# DKA scoring
# ---------------------------------------------------------------------------

class TestDkaScoringValidation:
    def test_valid_scores_produce_no_errors(self):
        with mock.patch.multiple(MODULE, **VALID_DKA_SCORING):
            assert _validate_dka_scoring() == []

    def test_scores_not_summing_to_100_is_rejected(self):
        # 30 + 20 + 40 = 90 ≠ 100
        with mock.patch.multiple(MODULE, **{**VALID_DKA_SCORING, "DKA_IMPLEMENTATION": 40}):
            errors = _validate_dka_scoring()
            assert any("mismatch" in e.lower() or "DKA" in e for e in errors)

    def test_negative_isomorphism_score_is_rejected(self):
        with mock.patch.multiple(MODULE, **{**VALID_DKA_SCORING, "DKA_FSA_ISOMORPHISM": -1}):
            errors = _validate_dka_scoring()
            assert any("DKA_FSA_ISOMORPHISM" in e for e in errors)

    def test_negative_annotation_score_is_rejected(self):
        with mock.patch.multiple(MODULE, **{**VALID_DKA_SCORING, "DKA_FSA_ANNOTATIONS": -5}):
            errors = _validate_dka_scoring()
            assert any("DKA_FSA_ANNOTATIONS" in e for e in errors)

    def test_negative_implementation_score_is_rejected(self):
        with mock.patch.multiple(MODULE, **{**VALID_DKA_SCORING, "DKA_IMPLEMENTATION": -10}):
            errors = _validate_dka_scoring()
            assert any("DKA_IMPLEMENTATION" in e for e in errors)


# ---------------------------------------------------------------------------
# NKA scoring
# ---------------------------------------------------------------------------

class TestNkaScoringValidation:
    def test_valid_scores_produce_no_errors(self):
        with mock.patch.multiple(MODULE, **VALID_NKA_SCORING):
            assert _validate_nka_scoring() == []

    def test_scores_not_summing_to_100_is_rejected(self):
        # 40 + 50 = 90 ≠ 100
        with mock.patch.multiple(MODULE, **{**VALID_NKA_SCORING, "NKA_IMPLEMENTATION": 50}):
            errors = _validate_nka_scoring()
            assert any("mismatch" in e.lower() or "NKA" in e for e in errors)

    def test_negative_isomorphism_score_is_rejected(self):
        with mock.patch.multiple(MODULE, **{**VALID_NKA_SCORING, "NKA_FSA_ISOMORPHISM": -1}):
            errors = _validate_nka_scoring()
            assert any("NKA_FSA_ISOMORPHISM" in e for e in errors)

    def test_negative_implementation_score_is_rejected(self):
        with mock.patch.multiple(MODULE, **{**VALID_NKA_SCORING, "NKA_IMPLEMENTATION": -1}):
            errors = _validate_nka_scoring()
            assert any("NKA_IMPLEMENTATION" in e for e in errors)


# ---------------------------------------------------------------------------
# Moodle settings
# ---------------------------------------------------------------------------

class TestMoodleSettings:
    def test_valid_config_produces_no_errors(self):
        with mock.patch.multiple(MODULE, **VALID_MOODLE):
            assert _validate_moodle_settings() == []

    def test_empty_username_is_rejected(self):
        with mock.patch.multiple(MODULE, **{**VALID_MOODLE, "USERNAME": ""}):
            errors = _validate_moodle_settings()
            assert any("USERNAME" in e for e in errors)

    def test_empty_password_is_rejected(self):
        with mock.patch.multiple(MODULE, **{**VALID_MOODLE, "PASSWORD": ""}):
            errors = _validate_moodle_settings()
            assert any("PASSWORD" in e for e in errors)

    def test_empty_assignment_link_is_rejected(self):
        with mock.patch.multiple(MODULE, **{**VALID_MOODLE, "ASSIGNMENT_LINK": ""}):
            errors = _validate_moodle_settings()
            assert any("ASSIGNMENT_LINK" in e for e in errors)

    def test_zero_question_number_is_rejected(self):
        with mock.patch.multiple(MODULE, **{**VALID_MOODLE, "QUESTION_NUMBER": 0}):
            errors = _validate_moodle_settings()
            assert any("QUESTION_NUMBER" in e for e in errors)
