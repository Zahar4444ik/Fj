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
    score = 0.0

    report.section("1. FSA Specification Verification", fsa_cfg["total"])

    # Generate and load
    type_cfg["generate"](automaton, filename=type_cfg["reference_path"])
    reference = prepare_automaton_for_fsa_test(type_cfg["reference_path"])
    student = prepare_automaton_for_fsa_test(type_cfg["student_path"])

    # 1.1 Isomorphism
    report.section("1.1 Structural Equivalence Verification")

    iso = check_isomorphism(reference, student)
    report.add_result(
        "Structural equivalence verification",
        iso,
        points=float(fsa_cfg["isomorphism"]),
    )

    if iso:
        score += fsa_cfg["isomorphism"]

    # 1.2 Annotations (DKA only)
    if type_cfg["check_annotations"]:
        report.section("1.2 State Annotation Verification")

        ann = check_annotations(reference, student)
        report.add_result(
            "State annotation verification",
            ann,
            points=float(fsa_cfg["annotations"]),
        )

        if ann:
            score += fsa_cfg["annotations"]
        else:
            report.add_info("")
            report.add_info("Annotation mismatches detected:")
            report.add_info("")
            report.add_info(format_annotation_diff(reference, student))

    return score
