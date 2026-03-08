from core.config.settings_parse import DKA_FSA_ISOMORPHISM, DKA_FSA_ANNOTATIONS, NKA_FSA_ISOMORPHISM
from core.evaluation.utils.difference_print import format_annotation_diff
from core.regex.automata.dka.dka_builder import DKA
from core.regex.automata.nka.nka_builder import NKA
from core.regex.generators.fsa.fsa_generator import fsa_from_dka, fsa_from_nka
from core.evaluation.report import AssignmentReport
from tasks.task1_isomorphism.checker.compare import (
    prepare_automaton_for_fsa_test,
    check_isomorphism,
    check_annotations,
    check_alphabet,
)
import os

FSA_CONFIG = {
    "dfa": {
        "generate": fsa_from_dka,
        "reference_path": r"C:\Users\Захар\Desktop\tuke\bakalarska\fj_assignments\output\fsa\dka.fsa",
        "student_fsa_filename": "specification.fsa",
        "check_annotations": True,
    },
    "nfa": {
        "generate": fsa_from_nka,
        "reference_path": r"C:\Users\Захар\Desktop\tuke\bakalarska\fj_assignments\output\fsa\nka.fsa",
        "student_fsa_filename": "specification.fsa",
        "check_annotations": False,
    },
}


def evaluate_fsa(automaton: NKA | DKA, automaton_type: str, report: AssignmentReport, work_dir: str) -> float:
    type_cfg = FSA_CONFIG[automaton_type]

    # ============================================================
    # 1. Generate and load automatons
    # ============================================================
    type_cfg["generate"](automaton, filename=type_cfg["reference_path"])
    reference = prepare_automaton_for_fsa_test(type_cfg["reference_path"])

    student_path = os.path.join(work_dir, type_cfg["student_fsa_filename"])
    student = prepare_automaton_for_fsa_test(student_path)

    # ============================================================
    # 2. Run all checks
    # ============================================================
    alphabet_passed = check_alphabet(reference, student)
    iso_passed = check_isomorphism(reference, student)
    iso_points = DKA_FSA_ISOMORPHISM if automaton_type == "DKA" else NKA_FSA_ISOMORPHISM
    ann_points = 0
    ann_passed = None
    ann_diff = None

    if type_cfg["check_annotations"]:
        ann_passed = check_annotations(reference, student)
        ann_points = DKA_FSA_ANNOTATIONS
        if not ann_passed:
            ann_diff = format_annotation_diff(reference, student)

    # ============================================================
    # 3. Calculate score
    # ============================================================
    score = 0.0

    if iso_passed:
        score += iso_points
        report.increase_score(iso_points)

    if ann_passed:
        score += ann_points
        report.increase_score(ann_points)

    # ============================================================
    # 4. Add to report
    # ============================================================
    report.section("1. FSA Specification Verification", (iso_points + ann_points))

    report.subsection(f"1.1 Alphabet correctness: {'PASSED' if alphabet_passed else 'FAILED'}")

    report.subsection("1.2 Isomorphism with Reference Automaton")
    report.add_result(
        "Isomorphism verification",
        iso_passed,
        points=iso_points,
    )

    if type_cfg["check_annotations"]:
        report.subsection("1.3 State Annotations")
        report.add_result(
            "State annotations verification",
            ann_passed,
            points=ann_points,
        )

        if not ann_passed:
            report.add_info("")
            report.add_info("Annotation mismatches detected:")
            report.add_info("")
            report.add_info(ann_diff)

    return score