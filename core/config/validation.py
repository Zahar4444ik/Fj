import os
from .settings_parse import *


def validate_all_settings():
    """Validate all environment variables from settings_parse.py"""
    errors = []

    # -----------------------------
    # String variables validation
    # -----------------------------
    if not CATEGORY or not isinstance(CATEGORY, str):
        errors.append("CATEGORY must be a non-empty string")

    if not TITLE or not isinstance(TITLE, str):
        errors.append("TITLE must be a non-empty string")

    validate_scoring_profile()

    if not ASSIGNMENT_LINK or not isinstance(ASSIGNMENT_LINK, str):
        errors.append("ASSIGNMENT_LINK must be a non-empty string (required for automated testing)")

    if not USERNAME or not isinstance(USERNAME, str):
        errors.append("USERNAME must be a non-empty string (required for automated testing)")

    if not PASSWORD or not isinstance(PASSWORD, str):
        errors.append("PASSWORD must be a non-empty string (required for automated testing)")

    if not DOWNLOAD_PATH or not isinstance(DOWNLOAD_PATH, str):
        errors.append("DOWNLOAD_PATH must be a non-empty string (required for automated testing)")

    if not RESULTS_PATH or not isinstance(RESULTS_PATH, str):
        errors.append("RESULTS_PATH must be a non-empty string (required for automated testing)")

    # Validate paths exist
    if DOWNLOAD_PATH and not os.path.exists(DOWNLOAD_PATH):
        errors.append(f"DOWNLOAD_PATH does not exist: {DOWNLOAD_PATH}")

    if RESULTS_PATH and not os.path.exists(RESULTS_PATH):
        errors.append(f"RESULTS_PATH does not exist: {RESULTS_PATH}")

    if errors:
        raise ValueError(
            "Invalid environment settings:\n" +
            "\n".join(f"- {e}" for e in errors)
        )


def validate_scoring_profile():
    errors = []

    # -----------------------------
    # Global sanity checks
    # -----------------------------
    if TEST_WORDS_COUNT <= 0:
        errors.append("TEST_WORDS_COUNT must be > 0")

    if not (0.0 <= BAD_WORD_RATIO_LEVEL <= 1.0):
        errors.append("BAD_WORD_RATIO_LEVEL must be between 0.0 and 1.0")

    if GROUP_SIZE <= 0:
        errors.append("GROUP_SIZE must be > 0")

    if REGEX_MIN_STATES_COUNT < 1:
        errors.append("REGEX_MIN_STATES_COUNT must be >= 1")

    if REGEX_MAX_STATES_COUNT < 1:
        errors.append("REGEX_MAX_STATES_COUNT must be >= 1")

    if REGEX_MIN_STATES_COUNT > REGEX_MAX_STATES_COUNT:
        errors.append("REGEX_MIN_STATES_COUNT must be <= REGEX_MAX_STATES_COUNT")

    # Numeric type validation
    if not isinstance(TEST_WORDS_COUNT, int):
        errors.append("TEST_WORDS_COUNT must be an integer")

    if not isinstance(BAD_WORD_RATIO_LEVEL, (int, float)):
        errors.append("BAD_WORD_RATIO_LEVEL must be a number")

    if not isinstance(GROUP_SIZE, int):
        errors.append("GROUP_SIZE must be an integer")

    if not isinstance(REGEX_MIN_STATES_COUNT, int):
        errors.append("REGEX_MIN_STATES_COUNT must be an integer")

    if not isinstance(REGEX_MAX_STATES_COUNT, int):
        errors.append("REGEX_MAX_STATES_COUNT must be an integer")

    # -----------------------------
    # DKA scoring validation
    # -----------------------------
    if not isinstance(DKA_FSA_ISOMORPHISM, int) or DKA_FSA_ISOMORPHISM < 0:
        errors.append("DKA_FSA_ISOMORPHISM must be a non-negative integer")

    if not isinstance(DKA_FSA_ANNOTATIONS, int) or DKA_FSA_ANNOTATIONS < 0:
        errors.append("DKA_FSA_ANNOTATIONS must be a non-negative integer")

    if not isinstance(DKA_IMPLEMENTATION, int) or DKA_IMPLEMENTATION < 0:
        errors.append("DKA_IMPLEMENTATION must be a non-negative integer")

    dka_total = (
        DKA_FSA_ISOMORPHISM +
        DKA_FSA_ANNOTATIONS +
        DKA_IMPLEMENTATION
    )

    if dka_total != TOTAL_SCORE:
        errors.append(
            f"DKA scoring mismatch: "
            f"{dka_total} != {TOTAL_SCORE}"
        )

    # Individual DKA scores must not exceed total
    if DKA_FSA_ISOMORPHISM > TOTAL_SCORE:
        errors.append(f"DKA_FSA_ISOMORPHISM ({DKA_FSA_ISOMORPHISM}) cannot exceed TOTAL_SCORE ({TOTAL_SCORE})")

    if DKA_FSA_ANNOTATIONS > TOTAL_SCORE:
        errors.append(f"DKA_FSA_ANNOTATIONS ({DKA_FSA_ANNOTATIONS}) cannot exceed TOTAL_SCORE ({TOTAL_SCORE})")

    if DKA_IMPLEMENTATION > TOTAL_SCORE:
        errors.append(f"DKA_IMPLEMENTATION ({DKA_IMPLEMENTATION}) cannot exceed TOTAL_SCORE ({TOTAL_SCORE})")

    # -----------------------------
    # NKA scoring validation
    # -----------------------------
    if not isinstance(NKA_FSA_ISOMORPHISM, int) or NKA_FSA_ISOMORPHISM < 0:
        errors.append("NKA_FSA_ISOMORPHISM must be a non-negative integer")

    if not isinstance(NKA_IMPLEMENTATION, int) or NKA_IMPLEMENTATION < 0:
        errors.append("NKA_IMPLEMENTATION must be a non-negative integer")

    nka_total = (
        NKA_FSA_ISOMORPHISM +
        NKA_IMPLEMENTATION
    )

    if nka_total != TOTAL_SCORE:
        errors.append(
            f"NKA scoring mismatch: "
            f"{nka_total} != {TOTAL_SCORE}"
        )

    # Individual NKA scores must not exceed total
    if NKA_FSA_ISOMORPHISM > TOTAL_SCORE:
        errors.append(f"NKA_FSA_ISOMORPHISM ({NKA_FSA_ISOMORPHISM}) cannot exceed TOTAL_SCORE ({TOTAL_SCORE})")

    if NKA_IMPLEMENTATION > TOTAL_SCORE:
        errors.append(f"NKA_IMPLEMENTATION ({NKA_IMPLEMENTATION}) cannot exceed TOTAL_SCORE ({TOTAL_SCORE})")

    # ...existing code...
    # Final decision
    # -----------------------------
    if errors:
        raise ValueError(
            "Invalid evaluation configuration:\n" +
            "\n".join(f"- {e}" for e in errors)
        )
