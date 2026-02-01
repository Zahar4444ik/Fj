from tasks.task1_isomorphism.generator.automata.canonical import canonical_signature


def format_annotation_diff(reference, student) -> str:
    _, ref_ann, ref_id_to_state = canonical_signature(reference)
    _, stu_ann, stu_id_to_state = canonical_signature(student)

    lines = [
        "State          Expected                    Received",
        "-" * 65
    ]

    has_diff = False
    for cid in sorted(ref_ann):
        exp = ref_ann.get(cid, "")
        got = stu_ann.get(cid, "")
        if exp != got:
            ref_name = ref_id_to_state.get(cid, "?")
            stu_name = stu_id_to_state.get(cid, "?")
            lines.append(f"{ref_name}/{stu_name:<7} {exp:<27} {got}")
            has_diff = True

    if not has_diff:
        lines.append("No mismatches found.")

    return "\n".join(lines)
