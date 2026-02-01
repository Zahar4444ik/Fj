def validate_evaluation_profile(profile: dict):
    # ----------------------------
    # Global validation
    # ----------------------------
    assert "global" in profile, "Missing 'global' section"

    global_cfg = profile["global"]
    total_score = global_cfg.get("total_score")

    assert isinstance(total_score, int) and total_score > 0, \
        "global.total_score must be a positive integer"

    # ----------------------------
    # Automaton types
    # ----------------------------
    for automaton_type in ("DKA", "NKA"):
        assert automaton_type in profile, \
            f"Missing '{automaton_type}' section"

        auto_cfg = profile[automaton_type]

        # ============================
        # FSA section
        # ============================
        fsa_cfg = auto_cfg.get("fsa")
        assert isinstance(fsa_cfg, dict), \
            f"{automaton_type}.fsa missing"

        fsa_total = fsa_cfg.get("total")
        assert isinstance(fsa_total, int) and fsa_total > 0, \
            f"{automaton_type}.fsa.total must be positive int"

        if automaton_type == "DKA":
            required = {"total", "isomorphism", "annotations"}
            missing = required - fsa_cfg.keys()
            assert not missing, \
                f"{automaton_type}.fsa missing keys: {missing}"

            iso = fsa_cfg["isomorphism"]
            ann = fsa_cfg["annotations"]

            assert iso + ann == fsa_total, (
                f"{automaton_type}.fsa mismatch: "
                f"isomorphism({iso}) + annotations({ann}) != total({fsa_total})"
            )

            extra = set(fsa_cfg) - required
            assert not extra, \
                f"{automaton_type}.fsa unknown keys: {extra}"

        else:  # NKA
            required = {"total", "isomorphism"}
            missing = required - fsa_cfg.keys()
            assert not missing, \
                f"{automaton_type}.fsa missing keys: {missing}"

            iso = fsa_cfg["isomorphism"]
            assert iso == fsa_total, (
                f"{automaton_type}.fsa mismatch: "
                f"isomorphism({iso}) != total({fsa_total})"
            )

            extra = set(fsa_cfg) - required
            assert not extra, \
                f"{automaton_type}.fsa unknown keys: {extra}"

        # ============================
        # Implementation section
        # ============================
        impl_cfg = auto_cfg.get("implementation")
        assert isinstance(impl_cfg, dict), \
            f"{automaton_type}.implementation missing"

        impl_total = impl_cfg.get("total")
        assert isinstance(impl_total, int) and impl_total > 0, \
            f"{automaton_type}.implementation.total must be positive int"

        extra = set(impl_cfg) - {"total"}
        assert not extra, \
            f"{automaton_type}.implementation unknown keys: {extra}"

        # ============================
        # Final automaton total
        # ============================
        assert fsa_total + impl_total == total_score, (
            f"{automaton_type} total score mismatch: "
            f"fsa({fsa_total}) + implementation({impl_total}) "
            f"!= global.total_score({total_score})"
        )

    return True
