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

    return errors


def _validate_evaluation_settings():
    """Validate Question Properties & Evaluation settings."""
    errors = []

    # Basic string validation
    if not TITLE or not isinstance(TITLE, str):
        errors.append("TITLE must be a non-empty string")

    # Test configuration validation
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

    # Regex difficulty validation
    if REGEX_MIN_STATES_COUNT < 1:
        errors.append("REGEX_MIN_STATES_COUNT must be >= 1")

    if REGEX_MAX_STATES_COUNT < 1:
        errors.append("REGEX_MAX_STATES_COUNT must be >= 1")

    if not isinstance(REGEX_MIN_STATES_COUNT, int):
        errors.append("REGEX_MIN_STATES_COUNT must be an integer")

    if not isinstance(REGEX_MAX_STATES_COUNT, int):
        errors.append("REGEX_MAX_STATES_COUNT must be an integer")

    if REGEX_MIN_STATES_COUNT > REGEX_MAX_STATES_COUNT:
        errors.append(
            f"REGEX_MIN_STATES_COUNT ({REGEX_MIN_STATES_COUNT}) must be <= "
            f"REGEX_MAX_STATES_COUNT ({REGEX_MAX_STATES_COUNT})"
        )

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

    # Path validation
    if not DOWNLOAD_PATH or not isinstance(DOWNLOAD_PATH, str):
        errors.append("DOWNLOAD_PATH must be a non-empty string (required for automated testing)")

    if DOWNLOAD_PATH and not os.path.exists(DOWNLOAD_PATH):
        errors.append(f"DOWNLOAD_PATH does not exist: {DOWNLOAD_PATH}")

    if not RESULTS_PATH or not isinstance(RESULTS_PATH, str):
        errors.append("RESULTS_PATH must be a non-empty string (required for automated testing)")

    if RESULTS_PATH and not os.path.exists(RESULTS_PATH):
        errors.append(f"RESULTS_PATH does not exist: {RESULTS_PATH}")

    return errors
