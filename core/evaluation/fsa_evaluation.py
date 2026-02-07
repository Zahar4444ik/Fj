from core.evaluation.utils.difference_print import format_annotation_diff
from core.regex.automata.dka.dka_builder import DKA
from core.regex.automata.nka.nka_builder import NKA
from core.regex.generators.fsa_generator import fsa_from_dka, fsa_from_nka
from core.evaluation.report import AssignmentReport
from evaluation.evaluation_profile import EVALUATION_PROFILE
from tasks.task1_isomorphism.checker.compare import (
    prepare_automaton_for_fsa_test,
    check_isomorphism,
    check_annotations,
)

FSA_CONFIG = {
    "DKA": {
        "generate": fsa_from_dka,
        "reference_path": "output/fsa/dka.fsa",
        "student_path": "tasks/student_io/fsa/student_dka.fsa",
        "check_annotations": True,
    },
    "NKA": {
        "generate": fsa_from_nka,
        "reference_path": "output/fsa/nka.fsa",
        "student_path": "tasks/student_io/fsa/student_nka.fsa",
        "check_annotations": False,
    },
}


def evaluate_fsa(automaton: NKA | DKA, automaton_type: str, report: AssignmentReport) -> float:
    fsa_cfg = EVALUATION_PROFILE[automaton_type]["fsa"]
    type_cfg = FSA_CONFIG[automaton_type]

    # ============================================================
    # 1. Generate and load automatons
    # ============================================================
    type_cfg["generate"](automaton, filename=type_cfg["reference_path"])
    reference = prepare_automaton_for_fsa_test(type_cfg["reference_path"])
    student = prepare_automaton_for_fsa_test(type_cfg["student_path"])

    # ============================================================
    # 2. Run all checks
    # ============================================================
    iso_passed = check_isomorphism(reference, student)
    ann_passed = None
    ann_diff = None

    if type_cfg["check_annotations"]:
        ann_passed = check_annotations(reference, student)
        if not ann_passed:
            ann_diff = format_annotation_diff(reference, student)

    # ============================================================
    # 3. Calculate score
    # ============================================================
    score = 0.0

    if iso_passed:
        score += fsa_cfg["isomorphism"]
        report.increase_score(fsa_cfg["isomorphism"])

    if ann_passed:
        score += fsa_cfg["annotations"]
        report.increase_score(fsa_cfg["annotations"])

    # ============================================================
    # 4. Add to report
    # ============================================================
    report.section("1. FSA Specification Verification", max_points=fsa_cfg["total"])

    report.subsection("1.1 Structural Equivalence Verification")
    report.add_result(
        "Structural equivalence verification",
        iso_passed,
        points=fsa_cfg["isomorphism"],
    )

    if type_cfg["check_annotations"]:
        report.subsection("1.2 State Annotation Verification")
        report.add_result(
            "State annotation verification",
            ann_passed,
            points=fsa_cfg["annotations"],
        )

        if not ann_passed:
            report.add_info("")
            report.add_info("Annotation mismatches detected:")
            report.add_info("")
            report.add_info(ann_diff)

    return score