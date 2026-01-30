BAD_WORD_RATIO_LEVELS = {0, 1, 2, 3}
MIN_REGEX_DEPTH = 1
MAX_REGEX_DEPTH = 4


def validate_evaluation_profile(profile: dict):
    """
    Validates the structure and values of the evaluation profile.
    Raises AssertionError if the profile is invalid.
    """

    # ============================
    # GLOBAL VALIDATION
    # ============================

    global_cfg = profile.get("global")
    assert global_cfg is not None, "Missing 'global' section"

    total_score = global_cfg.get("total_score")
    assert total_score == 100, "global.total_score must be exactly 100"

    # ----------------------------
    # Test words validation
    # ----------------------------
    test_words = global_cfg.get("test_words")
    assert test_words is not None, "Missing global.test_words"

    count = test_words.get("count")
    assert isinstance(count, int) and count > 0, \
        "test_words.count must be a positive integer"

    bad_ratio_level = test_words.get("bad_word_ratio_level")
    assert bad_ratio_level in BAD_WORD_RATIO_LEVELS, \
        "bad_word_ratio_level must be in range 0–3"

    # ----------------------------
    # Regex complexity validation
    # ----------------------------
    regex_cfg = global_cfg.get("regex_complexity")
    assert regex_cfg is not None, "Missing global.regex_complexity"

    min_depth = regex_cfg.get("min_depth")
    max_depth = regex_cfg.get("max_depth")

    assert isinstance(min_depth, int) and isinstance(max_depth, int), \
        "regex depth values must be integers"

    assert MIN_REGEX_DEPTH <= min_depth <= MAX_REGEX_DEPTH, \
        f"min_depth must be between {MIN_REGEX_DEPTH} and {MAX_REGEX_DEPTH}"

    assert MIN_REGEX_DEPTH <= max_depth <= MAX_REGEX_DEPTH, \
        f"max_depth must be between {MIN_REGEX_DEPTH} and {MAX_REGEX_DEPTH}"

    assert min_depth <= max_depth, \
        "min_depth cannot be greater than max_depth"

    # ============================
    # AUTOMATON-SPECIFIC VALIDATION
    # ============================

    for automaton_type in ("DKA", "NKA"):
        assert automaton_type in profile, \
            f"Missing profile section for {automaton_type}"

        auto_cfg = profile[automaton_type]

        # ----------------------------
        # FSA section
        # ----------------------------
        fsa_cfg = auto_cfg.get("fsa")
        assert fsa_cfg is not None, f"Missing {automaton_type}.fsa section"

        fsa_total = fsa_cfg.get("total")
        assert isinstance(fsa_total, int) and fsa_total > 0, \
            f"{automaton_type}.fsa.total must be a positive integer"

        fsa_sum = sum(
            v for k, v in fsa_cfg.items() if k != "total"
        )
        assert fsa_sum == fsa_total, \
            f"{automaton_type}.fsa subtotals ({fsa_sum}) != total ({fsa_total})"

        # ----------------------------
        # Implementation section
        # ----------------------------
        impl_cfg = auto_cfg.get("implementation")
        assert impl_cfg is not None, f"Missing {automaton_type}.implementation"

        impl_total = impl_cfg.get("total")
        assert isinstance(impl_total, int) and impl_total > 0, \
            f"{automaton_type}.implementation.total must be positive"

        impl_sum = sum(
            v for k, v in impl_cfg.items() if k != "total"
        )
        assert impl_sum >= impl_total, \
            f"{automaton_type}.implementation subtotals < total"

        # ----------------------------
        # Automaton total validation
        # ----------------------------
        auto_total = fsa_total + impl_total
        assert auto_total == total_score, \
            (
                f"{automaton_type} total score mismatch: "
                f"{auto_total} != {total_score}"
            )

    return True
