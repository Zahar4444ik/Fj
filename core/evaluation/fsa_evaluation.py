"""
FSA Specification Evaluation

Evaluates FSA specifications from student submissions against reference automatons.
Checks for isomorphism and state annotations correctness.
"""

import logging
import os
from pathlib import Path

from core.config.settings_parse import DKA_FSA_ISOMORPHISM, DKA_FSA_ANNOTATIONS, NKA_FSA_ISOMORPHISM
from core.evaluation.utils.difference_print import format_annotation_diff
from core.regex.automata.dka.dka_builder import DKA
from core.regex.automata.nka.nka_builder import NKA
from core.regex.generators.fsa.fsa_generator import fsa_from_dka, fsa_from_nka
from core.evaluation.report import AssignmentReport
from graders.isomorphism.checker.compare import (
    prepare_automaton_for_fsa_test,
    check_isomorphism,
    check_annotations,
    check_alphabet,
)

# ============================================================================
# CONFIGURATION
# ============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = BASE_DIR / "output"
FSA_DIR = OUTPUT_DIR / "fsa"

# Ensure FSA directory exists
FSA_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# LOGGING
# ============================================================================

logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURATION DATA
# ============================================================================

FSA_CONFIG = {
    "dfa": {
        "generate": fsa_from_dka,
        "reference_path": FSA_DIR / "dka.fsa",
        "student_fsa_filename": "specification.fsa",
        "check_annotations": True,
    },
    "nfa": {
        "generate": fsa_from_nka,
        "reference_path": FSA_DIR / "nka.fsa",
        "student_fsa_filename": "specification.fsa",
        "check_annotations": False,
    },
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def _generate_reference_fsa(automaton: NKA | DKA, reference_path: Path) -> None:
    """Generate reference FSA file."""
    reference_path.parent.mkdir(parents=True, exist_ok=True)

    if "dka" in reference_path.name.lower():
        fsa_from_dka(automaton, filename=str(reference_path))
    else:
        fsa_from_nka(automaton, filename=str(reference_path))

    logger.debug(f"Generated reference FSA: {reference_path}")


def _load_reference_fsa(reference_path: Path) -> object:
    """Load reference FSA from file."""
    return prepare_automaton_for_fsa_test(str(reference_path))


def _load_student_fsa(work_dir: str, student_filename: str) -> tuple[object, list[str]]:
    """Load student FSA from submission, returning automaton and any syntax errors."""
    student_path = os.path.join(work_dir, student_filename)
    return prepare_automaton_for_fsa_test(student_path)


def _run_alphabet_check(reference: object, student: object) -> bool:
    """Check alphabet correctness."""
    return check_alphabet(reference, student)


def _run_isomorphism_check(reference: object, student: object) -> bool:
    """Check isomorphism with reference automaton."""
    return check_isomorphism(reference, student)


def _run_annotations_check(reference: object, student: object) -> tuple:
    correct, total = check_annotations(reference, student)
    passed = correct == total
    diff = format_annotation_diff(reference, student) if not passed else None
    return correct, total, passed, diff


def _get_scoring_points(automaton_type: str, check_type: str) -> int:
    """Get points for specific check type."""
    points_map = {
        "dfa": {
            "isomorphism": DKA_FSA_ISOMORPHISM,
            "annotations": DKA_FSA_ANNOTATIONS,
        },
        "nfa": {
            "isomorphism": NKA_FSA_ISOMORPHISM,
            "annotations": 0,
        }
    }
    return points_map.get(automaton_type, {}).get(check_type, 0)


def _add_to_report(report: AssignmentReport,
                   syntax_passed: bool,
                   syntax_errors: list,
                   iso_passed: bool,
                   iso_points: int,
                   ann_passed: bool = None,
                   ann_points: int = 0,
                   ann_correct: int = 0,
                   ann_total: int = 0,
                   ann_diff: str = None) -> None:
    """Add evaluation results to report."""
    total_points = iso_points + ann_points

    report.section("1. FSA Specification Verification", total_points)

    report.subsection(f"1.1 Syntactic Validation: {'PASSED' if syntax_passed else 'FAILED'}")

    if not syntax_passed:
        report.add_info("Skipping further checks due to syntax errors:")
        for err in syntax_errors:
            report.add_info(err)
        return

    report.subsection("1.2 Isomorphism with Reference Automaton")
    report.add_result(
        "Isomorphism verification",
        iso_passed,
        points=iso_points if iso_passed else 0,
        total_points=iso_points
    )

    if ann_passed is not None:
        report.subsection("1.3 State Annotations")
        report.add_result(
            f"State annotations verification ({ann_correct}/{ann_total} correct)",
            ann_passed,
            points=round(ann_points / ann_total * ann_correct, 2) if ann_total > 0 else 0,
            total_points=ann_points
        )

        if not ann_passed and ann_diff:
            report.add_info("")
            report.add_info("Annotation mismatches detected:")
            report.add_info("")
            report.add_info(ann_diff)


# ============================================================================
# PUBLIC API
# ============================================================================

def evaluate_fsa(automaton: NKA | DKA, automaton_type: str, report: AssignmentReport, work_dir: str) -> float:
    """
    Evaluate FSA specification from student submission.

    Args:
        automaton: Built automaton (DFA or NFA)
        automaton_type: "dfa" or "nfa"
        report: Assignment report object
        work_dir: Directory containing student submission

    Returns:
        float: Points earned for FSA evaluation
    """
    type_cfg = FSA_CONFIG[automaton_type]

    if not os.path.exists(os.path.join(work_dir, type_cfg["student_fsa_filename"])):
        report.section("1. FSA Specification Verification", 0)
        report.add_info("\nERROR")
        report.add_info("-" * 60)
        report.add_info(f"Missing required file: specification.fsa")

        logger.error(f"Missing required file: specification.fsa")
        return 0.0

    try:
        # Step 1: Generate and load automatons
        logger.debug(f"Generating reference FSA for {automaton_type}")
        _generate_reference_fsa(automaton, type_cfg["reference_path"])
        reference, error = _load_reference_fsa(type_cfg["reference_path"])
        student, syntax_errors = _load_student_fsa(work_dir, type_cfg["student_fsa_filename"])
        syntax_passed = not syntax_errors

        # Step 2: Run all checks
        logger.debug(f"Running checks for {automaton_type} FSA")

        iso_passed = False
        iso_points = _get_scoring_points(automaton_type, "isomorphism")
        ann_points = _get_scoring_points(automaton_type, "annotations")
        ann_passed = None
        ann_correct = 0
        ann_total = 0
        ann_diff = None

        if syntax_passed:
            iso_passed = _run_isomorphism_check(reference, student)

            if type_cfg["check_annotations"]:
                ann_correct, ann_total, ann_passed, ann_diff = _run_annotations_check(reference, student)

        # Step 3: Calculate score
        score = 0.0

        if iso_passed:
            score += iso_points
            report.increase_score(iso_points)

        if ann_total > 0:
            per_state = ann_points / ann_total
            ann_score = round(per_state * ann_correct, 2)
            score += ann_score
            report.increase_score(ann_score)

        # Step 4: Add to report
        _add_to_report(report, syntax_passed=syntax_passed, syntax_errors=syntax_errors,
                       iso_passed=iso_passed, iso_points=iso_points,
                       ann_passed=ann_passed, ann_points=ann_points,
                       ann_correct=ann_correct, ann_total=ann_total, ann_diff=ann_diff)

        logger.info(f"FSA evaluation for {automaton_type} complete: {score} points")
        return score
    except Exception as e:
        report.section("1. FSA Specification Verification", 0)
        report.add_info("\nERROR")
        report.add_info("-" * 60)
        report.add_info(f"Evaluation failed: {e}")

        logger.error(f"Evaluation failed: {e}")
        return 0.0
