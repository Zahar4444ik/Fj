from core.regex.automata.dka.dka_builder import DKA
from core.regex.automata.nka.nka_builder import NKA
from core.regex.generators.fsa_generator import fsa_from_dka, fsa_from_nka
from evaluation.report import AssignmentReport
from tasks.task1_isomorphism.checker.compare import prepare_automaton_for_fsa_test, check_isomorphism, check_annotations


def evaluate_fsa(automaton: NKA | DKA, automaton_type: str, report: AssignmentReport) -> int:
    score = 0
    report.section("1. FSA Specification Verification")

    if automaton_type == "DKA":
        fsa_from_dka(automaton, filename="output/fsa/dka.fsa")

        reference = prepare_automaton_for_fsa_test("output/fsa/dka.fsa")
        student = prepare_automaton_for_fsa_test("tasks/student_io/fsa/student_dka.fsa")

        # ------------------------------------------------------------------
        # 1.1 Structural equivalence
        # ------------------------------------------------------------------
        iso = check_isomorphism(reference, student)

        report.section("1.1 Structural Equivalence Verification")

        report.add_result("Structural equivalence", iso, points=8)
        if iso:
            score += 8

        # ------------------------------------------------------------------
        # 1.2 Annotation verification
        # ------------------------------------------------------------------
        ann = check_annotations(reference, student)

        report.add_info("\n[ 1.2 State Annotation Verification ]")
        report.add_info("Verified properties:")
        report.add_info("  - Correct annotation of states")
        report.add_info("  - Consistency with reference automaton")

        report.add_result("State annotations", ann, points=2)
        if ann:
            score += 2
        else:
            report.add_info("")
            report.add_info("Annotation mismatches detected:")
            report.add_info("")
            report.add_info("Expected annotations:")
            report.add_info(reference.annotations_as_string())
            report.add_info("Received annotations:")
            report.add_info(student.annotations_as_string())

    else:
        # NKA version (simpler)
        fsa_from_nka(automaton, filename="output/fsa/nka.fsa")

        reference = prepare_automaton_for_fsa_test("output/fsa/nka.fsa")
        student = prepare_automaton_for_fsa_test("tasks/student_io/fsa/student_nka.fsa")

        report.section("1.1 Structural Equivalence Verification")

        iso = check_isomorphism(reference, student)
        report.add_result("Structural equivalence (NKA)", iso, points=10)

        if iso:
            score += 10

    return score
