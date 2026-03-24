"""
Configuration validation for FSA assignments lifecycle.

This module validates all environment variables loaded from settings_parse.py
to ensure they meet requirements for each stage of the assignment workflow.
"""

from .settings_parse import *


def validate_all_settings():
    errors = []

    # Question Generation
    errors.extend(_validate_generation_settings())

    # Question Properties & Evaluation
    errors.extend(_validate_evaluation_settings())

    # Moodle & File Operations
    errors.extend(_validate_moodle_settings())

    # Final decision
    if errors:
        raise ValueError(
            "Invalid configuration:\n" +
            "\n".join(f"- {e}" for e in errors)
        )


def _validate_generation_settings():
    """Validate Question Generation settings."""
    errors = []

    if not CATEGORY or not isinstance(CATEGORY, str):
        errors.append("CATEGORY must be a non-empty string")

    if NUMBER_OF_QUESTIONS <= 0:
        errors.append("NUMBER_OF_QUESTIONS must be > 0")

    # Regex difficulty validation
    if DFA_MIN_STATES_COUNT < 1:
        errors.append("DFA_MIN_STATES_COUNT must be >= 1")

    if DFA_MAX_STATES_COUNT < 1:
        errors.append("DFA_MAX_STATES_COUNT must be >= 1")

    if not isinstance(DFA_MIN_STATES_COUNT, int):
        errors.append("DFA_MIN_STATES_COUNT must be an integer")

    if not isinstance(DFA_MAX_STATES_COUNT, int):
        errors.append("DFA_MAX_STATES_COUNT must be an integer")

    if DFA_MIN_STATES_COUNT > DFA_MAX_STATES_COUNT:
        errors.append(
            f"DFA_MIN_STATES_COUNT ({DFA_MIN_STATES_COUNT}) must be <= "
            f"DFA_MAX_STATES_COUNT ({DFA_MAX_STATES_COUNT})"
        )

    if NFA_MIN_STATES_COUNT < 1:
        errors.append("NFA_MIN_STATES_COUNT must be >= 1")

    if NFA_MAX_STATES_COUNT < 1:
        errors.append("NFA_MAX_STATES_COUNT must be >= 1")

    if not isinstance(NFA_MIN_STATES_COUNT, int):
        errors.append("NFA_MIN_STATES_COUNT must be an integer")

    if not isinstance(NFA_MAX_STATES_COUNT, int):
        errors.append("NFA_MAX_STATES_COUNT must be an integer")

    if NFA_MIN_STATES_COUNT > NFA_MAX_STATES_COUNT:
        errors.append(
            f"NFA_MIN_STATES_COUNT ({NFA_MIN_STATES_COUNT}) must be <= "
            f"NFA_MAX_STATES_COUNT ({NFA_MAX_STATES_COUNT})"
        )

    if not AUTOMATON_TYPE or not isinstance(AUTOMATON_TYPE, str):
        errors.append("CATEGORY must be a non-empty string")

    if AUTOMATON_TYPE not in ["dfa", "nfa", "any"]:
        errors.append('AUTOMATON_TYPE can only be "dfa", "nfa", "any"')

    if not IMPLEMENTATION_TYPE or not isinstance(IMPLEMENTATION_TYPE, str):
        errors.append("IMPLEMENTATION_TYPE must be a non-empty string")

    if IMPLEMENTATION_TYPE not in ["iterative", "recursive", "any"]:
        errors.append('IMPLEMENTATION_TYPE can only be "iterative", "recursive", "any"')

    if not isinstance(MAX_ALPHABET_SIZE, int) or MAX_ALPHABET_SIZE < 1:
        errors.append("MAX_ALPHABET_SIZE must be a positive integer")

    if not isinstance(MIN_ALPHABET_SIZE, int) or MIN_ALPHABET_SIZE < 1:
        errors.append("MIN_ALPHABET_SIZE must be a positive integer")

    if MIN_ALPHABET_SIZE > MAX_ALPHABET_SIZE:
        errors.append(
            f"MIN_ALPHABET_SIZE ({MIN_ALPHABET_SIZE}) must be <= "
            f"MAX_ALPHABET_SIZE ({MAX_ALPHABET_SIZE})"
        )

    return errors


def _validate_evaluation_settings():
    """Validate Question Properties & Evaluation settings."""
    errors = []

    # Basic string validation
    if not TITLE or not isinstance(TITLE, str):
        errors.append("TITLE must be a non-empty string")

    # Test configuration validation
    if ASSIGNMENT_MAX_POINTS <= 0:
        errors.append("ASSIGNMENT_MAX_POINTS must be > 0")

    if TEST_WORDS_COUNT <= 0:
        errors.append("TEST_WORDS_COUNT must be > 0")

    if not isinstance(TEST_WORDS_COUNT, int):
        errors.append("TEST_WORDS_COUNT must be an integer")

    if not (0.0 <= BAD_WORD_RATIO_LEVEL <= 1.0):
        errors.append("BAD_WORD_RATIO_LEVEL must be between 0.0 and 1.0")

    if not isinstance(BAD_WORD_RATIO_LEVEL, (int, float)):
        errors.append("BAD_WORD_RATIO_LEVEL must be a number")

    if GROUP_SIZE <= 0:
        errors.append("GROUP_SIZE must be > 0")

    if not isinstance(GROUP_SIZE, int):
        errors.append("GROUP_SIZE must be an integer")

    # DKA scoring validation
    errors.extend(_validate_dka_scoring())

    # NKA scoring validation
    errors.extend(_validate_nka_scoring())

    return errors


def _validate_dka_scoring():
    """Validate DKA scoring configuration."""
    errors = []

    # Type validation
    if not isinstance(DKA_FSA_ISOMORPHISM, int) or DKA_FSA_ISOMORPHISM < 0:
        errors.append("DKA_FSA_ISOMORPHISM must be a non-negative integer")

    if not isinstance(DKA_FSA_ANNOTATIONS, int) or DKA_FSA_ANNOTATIONS < 0:
        errors.append("DKA_FSA_ANNOTATIONS must be a non-negative integer")

    if not isinstance(DKA_IMPLEMENTATION, int) or DKA_IMPLEMENTATION < 0:
        errors.append("DKA_IMPLEMENTATION must be a non-negative integer")

    # Total score validation
    dka_total = DKA_FSA_ISOMORPHISM + DKA_FSA_ANNOTATIONS + DKA_IMPLEMENTATION

    if dka_total != TOTAL_SCORE:
        errors.append(
            f"DKA total score mismatch: {dka_total} != {TOTAL_SCORE} "
            f"(ISomorphism: {DKA_FSA_ISOMORPHISM} + "
            f"Annotations: {DKA_FSA_ANNOTATIONS} + "
            f"Implementation: {DKA_IMPLEMENTATION})"
        )

    # Individual score bounds
    if DKA_FSA_ISOMORPHISM > TOTAL_SCORE:
        errors.append(
            f"DKA_FSA_ISOMORPHISM ({DKA_FSA_ISOMORPHISM}) "
            f"cannot exceed TOTAL_SCORE ({TOTAL_SCORE})"
        )

    if DKA_FSA_ANNOTATIONS > TOTAL_SCORE:
        errors.append(
            f"DKA_FSA_ANNOTATIONS ({DKA_FSA_ANNOTATIONS}) "
            f"cannot exceed TOTAL_SCORE ({TOTAL_SCORE})"
        )

    if DKA_IMPLEMENTATION > TOTAL_SCORE:
        errors.append(
            f"DKA_IMPLEMENTATION ({DKA_IMPLEMENTATION}) "
            f"cannot exceed TOTAL_SCORE ({TOTAL_SCORE})"
        )

    return errors


def _validate_nka_scoring():
    """Validate NKA scoring configuration."""
    errors = []

    # Type validation
    if not isinstance(NKA_FSA_ISOMORPHISM, int) or NKA_FSA_ISOMORPHISM < 0:
        errors.append("NKA_FSA_ISOMORPHISM must be a non-negative integer")

    if not isinstance(NKA_IMPLEMENTATION, int) or NKA_IMPLEMENTATION < 0:
        errors.append("NKA_IMPLEMENTATION must be a non-negative integer")

    # Total score validation
    nka_total = NKA_FSA_ISOMORPHISM + NKA_IMPLEMENTATION

    if nka_total != TOTAL_SCORE:
        errors.append(
            f"NKA total score mismatch: {nka_total} != {TOTAL_SCORE} "
            f"(Isomorphism: {NKA_FSA_ISOMORPHISM} + "
            f"Implementation: {NKA_IMPLEMENTATION})"
        )

    # Individual score bounds
    if NKA_FSA_ISOMORPHISM > TOTAL_SCORE:
        errors.append(
            f"NKA_FSA_ISOMORPHISM ({NKA_FSA_ISOMORPHISM}) "
            f"cannot exceed TOTAL_SCORE ({TOTAL_SCORE})"
        )

    if NKA_IMPLEMENTATION > TOTAL_SCORE:
        errors.append(
            f"NKA_IMPLEMENTATION ({NKA_IMPLEMENTATION}) "
            f"cannot exceed TOTAL_SCORE ({TOTAL_SCORE})"
        )

    return errors


def _validate_moodle_settings():
    """Validate Moodle authentication and file operations."""
    errors = []

    # Credentials validation
    if not USERNAME or not isinstance(USERNAME, str):
        errors.append("USERNAME must be a non-empty string (required for automated testing)")

    if not PASSWORD or not isinstance(PASSWORD, str):
        errors.append("PASSWORD must be a non-empty string (required for automated testing)")

    if not ASSIGNMENT_LINK or not isinstance(ASSIGNMENT_LINK, str):
        errors.append("ASSIGNMENT_LINK must be a non-empty string (required for automated testing)")

    if QUESTION_NUMBER <= 0:
        errors.append("QUESTION_NUMBER must be > 0")

    if not isinstance(HEADLESS, bool):
        errors.append("HEADLESS must be a boolean value")

    return errors
