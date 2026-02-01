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


def evaluate_fsa(automaton: NKA | DKA, automaton_type: str, report: AssignmentReport) -> float:
    fsa_cfg = EVALUATION_PROFILE[automaton_type]["fsa"]
    score = 0.0

    report.section("1. FSA Specification Verification", fsa_cfg["total"])

    if automaton_type == "DKA":
        fsa_from_dka(automaton, filename="output/fsa/dka.fsa")

        reference = prepare_automaton_for_fsa_test("output/fsa/dka.fsa")
        student = prepare_automaton_for_fsa_test("tasks/student_io/fsa/student_dka.fsa")

        # 1.1 Isomorphism
        report.section("1.1 Structural Equivalence Verification")

        iso = check_isomorphism(reference, student)  # computes and caches
        report.add_result(
            "Structural equivalence verification",
            iso,
            points=float(fsa_cfg["isomorphism"]),
        )

        if iso:
            score += fsa_cfg["isomorphism"]

        # 1.2 Annotations
        report.section("1.2 State Annotation Verification")

        ann = check_annotations(reference, student)  # uses cache, no recomputation
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
            report.add_info(format_annotation_diff(reference, student))  # uses cache

    else:
        fsa_from_nka(automaton, filename="output/fsa/nka.fsa")

        reference = prepare_automaton_for_fsa_test("output/fsa/nka.fsa")
        student = prepare_automaton_for_fsa_test("tasks/student_io/fsa/student_nka.fsa")

        # 1.1 Isomorphism
        report.section("1.1 Structural Equivalence Verification")

        iso = check_isomorphism(reference, student)  # computes and caches
        report.add_result(
            "Structural equivalence verification",
            iso,
            points=float(fsa_cfg["isomorphism"]),
        )

        if iso:
            score += fsa_cfg["isomorphism"]

    report.current_score_report()
    return score
