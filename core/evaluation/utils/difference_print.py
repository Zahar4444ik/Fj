from testing.task1_isomorphism.generator.automata.canonical import canonical_signature


def format_annotation_diff(reference, student) -> str:
    _, ref_ann, ref_id_to_state = canonical_signature(reference)
    _, stu_ann, stu_id_to_state = canonical_signature(student)

    lines = [
        "State          Expected                    Received",
        "-" * 60
    ]

    has_diff = False
    for cid in sorted(ref_ann):
        exp = ref_ann.get(cid, "")
        got = stu_ann.get(cid, "")
        if exp != got:
            stu_name = stu_id_to_state.get(cid, "?")
            lines.append(f"{stu_name:<11} {exp:<27} {got}")
            has_diff = True

    if not has_diff:
        lines.append("No mismatches found.")

    return "\n".join(lines)


def format_acceptance_diff(mismatches: list[dict]) -> str:
    """
    mismatches: list of dicts with keys:
        - word
        - expected (bool)
        - got (bool)
    """

    def fmt(val: bool) -> str:
        return "ACCEPTED" if val else "REJECTED"

    lines = [
        "Acceptance mismatches detected:",
        "",
        f"{'Input string':<15} {'Expected':<15} {'Received'}",
        "-" * 60,
    ]

    if not mismatches:
        lines.append("No mismatches found.")
        return "\n".join(lines)

    for m in mismatches:
        lines.append(
            f"{m['word'] if m['word'] != '' else f'"{m['word']}"':<15} "
            f"{fmt(m['expected']):<15} "
            f"{fmt(m['got'])}"
        )

    return "\n".join(lines) + '\n'

