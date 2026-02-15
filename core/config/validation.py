from .settings_parse import *


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

    if REGEX_MIN_DEPTH < 1:
        errors.append("REGEX_MIN_DEPTH must be >= 1")

    if REGEX_MIN_DEPTH > REGEX_MAX_DEPTH:
        errors.append("REGEX_MIN_DEPTH must be <= REGEX_MAX_DEPTH")

    # -----------------------------
    # DKA scoring validation
    # -----------------------------
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

    # -----------------------------
    # NKA scoring validation
    # -----------------------------
    nka_total = (
        NKA_FSA_ISOMORPHISM +
        NKA_IMPLEMENTATION
    )

    if nka_total != TOTAL_SCORE:
        errors.append(
            f"NKA scoring mismatch: "
            f"{nka_total} != {TOTAL_SCORE}"
        )

    # -----------------------------
    # Final decision
    # -----------------------------
    if errors:
        raise ValueError(
            "Invalid evaluation configuration:\n" +
            "\n".join(f"- {e}" for e in errors)
        )
