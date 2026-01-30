from core.regex.automata.dka.dka_builder import DKA
from core.regex.automata.nka.nka_builder import NKA
from core.regex.generators.fsa_generator import fsa_from_dka, fsa_from_nka
from core.evaluation.report import AssignmentReport
from evaluation.evaluation_profile import EVALUATION_PROFILE
from tasks.task1_isomorphism.checker.compare import prepare_automaton_for_fsa_test, check_isomorphism, check_annotations


def evaluate_fsa(automaton: NKA | DKA, automaton_type: str, report: AssignmentReport) -> int:
    fsa_cfg = EVALUATION_PROFILE[automaton_type]["fsa"]
    score = 0

    report.section("1. FSA Specification Verification", fsa_cfg["total"])

    if automaton_type == "DKA":
        fsa_from_dka(automaton, filename="output/fsa/dka.fsa")

        reference = prepare_automaton_for_fsa_test("output/fsa/dka.fsa")
        student = prepare_automaton_for_fsa_test("tasks/student_io/fsa/student_dka.fsa")

        # 1.1 Isomorphism
        report.section("1.1 Structural Equivalence Verification")

        iso, iso_map = check_isomorphism(reference, student)
        report.add_result(
            "Structural equivalence verification",
            iso,
            points=fsa_cfg["isomorphism"],
            max_points=fsa_cfg["total"]
        )

        if iso:
            score += fsa_cfg["isomorphism"]

        # 1.2 Annotations
        report.section("1.2 State Annotation Verification")

        ann = check_annotations(reference, student, iso_map)
        report.add_result(
            "State annotation verification",
            ann,
            points=fsa_cfg["annotations"],
            max_points=fsa_cfg["total"]
        )

        if ann:
            score += fsa_cfg["annotations"]
        else:
            report.add_info("")
            report.add_info("Annotation mismatches detected:")
            report.add_info("")
            report.add_info(
                reference.format_annotation_diff(student)
            )

    else:
        fsa_from_nka(automaton, filename="output/fsa/nka.fsa")

        reference = prepare_automaton_for_fsa_test("output/fsa/nka.fsa")
        student = prepare_automaton_for_fsa_test("tasks/student_io/fsa/student_nka.fsa")

        # 1.1 Isomorphism
        report.section("1.1 Structural Equivalence Verification")

        iso = check_isomorphism(reference, student)
        report.add_result(
            "Structural equivalence verification",
            iso,
            points=fsa_cfg["isomorphism"],
            max_points=fsa_cfg["total"]
        )

        if iso:
            score += fsa_cfg["isomorphism"]

    report.current_score_report()
    return score
