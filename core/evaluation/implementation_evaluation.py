"""
Implementation Evaluation

Evaluates automata implementations from student submissions.
Performs static analysis and behavioral testing on iterative/recursive implementations.
"""

import logging
import os
from pathlib import Path

from core.assignment.utils import load_module_from_path
from core.config.settings_parse import DKA_IMPLEMENTATION, NKA_IMPLEMENTATION, TEST_WORDS_COUNT, BAD_WORD_RATIO_LEVEL, \
    GROUP_SIZE
from core.evaluation.report import AssignmentReport
from core.evaluation.utils.difference_print import format_acceptance_diff
from testing.task2_behavioral_testing.checker.check_imports import check_imports
from testing.task2_behavioral_testing.checker.utils import check_no_iteration, check_no_recursion
from testing.task2_behavioral_testing.generator.dka.iterative import generate_iterative_dka
from testing.task2_behavioral_testing.generator.dka.recursive import generate_recursive_dka
from testing.task2_behavioral_testing.generator.nka.iterative import generate_iterative_nka
from testing.task2_behavioral_testing.generator.nka.recursive import generate_recursive_nka
from testing.task2_behavioral_testing.generator.utils.resursive_helper import get_start_state_for_recursive
from testing.task2_behavioral_testing.word_generation.testing_words_generator import generate_accepted_words, \
    generate_rejected_words

# ============================================================================
# CONFIGURATION
# ============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = BASE_DIR / "output"
AUTOMATA_DIR = OUTPUT_DIR / "automata"

# Ensure automata directory exists
AUTOMATA_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# LOGGING
# ============================================================================

logger = logging.getLogger(__name__)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def _get_recursive_check_fn(mod, start_state):
    """Get check function from recursive automaton module."""
    try:
        fn = getattr(mod, start_state)
    except AttributeError:
        raise AttributeError(
            f"Student module does not implement function '{start_state}'"
        )

    if not callable(fn):
        raise TypeError(f"'{start_state}' exists but is not callable")

    return fn

# ============================================================================
# CONFIGURATION DATA
# ============================================================================


IMPLEMENTATION_CONFIG = {
    ("dfa", "iterative"): {
        "student_filename": "automaton.py",
        "reference_path": AUTOMATA_DIR / "dka_iterative.py",
        "module_name": "dka_iterative",
        "student_module_name": "automaton",
        "static_check": check_no_recursion,
        "generate": generate_iterative_dka,
        "get_check_fn": lambda mod, _: mod.DFA().check,
    },
    ("dfa", "recursive"): {
        "student_filename": "automaton.py",
        "reference_path": AUTOMATA_DIR / "dka_recursive.py",
        "module_name": "dka_recursive",
        "student_module_name": "automaton",
        "static_check": check_no_iteration,
        "generate": generate_recursive_dka,
        "get_check_fn": _get_recursive_check_fn,
    },
    ("nfa", "iterative"): {
        "student_filename": "automaton.py",
        "reference_path": AUTOMATA_DIR / "nka_iterative.py",
        "module_name": "nka_iterative",
        "student_module_name": "automaton",
        "static_check": check_no_recursion,
        "generate": generate_iterative_nka,
        "get_check_fn": lambda mod, _: mod.NFA().check,
    },
    ("nfa", "recursive"): {
        "student_filename": "automaton.py",
        "reference_path": AUTOMATA_DIR / "nka_recursive.py",
        "module_name": "nka_recursive",
        "student_module_name": "automaton",
        "static_check": check_no_iteration,
        "generate": generate_recursive_nka,
        "get_check_fn": _get_recursive_check_fn,
    },
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def _generate_reference_implementation(ast: dict, cfg: dict) -> None:
    """Generate reference implementation file."""
    cfg["reference_path"].parent.mkdir(parents=True, exist_ok=True)
    cfg["generate"](ast, str(cfg["reference_path"]))
    logger.debug(f"Generated reference implementation: {cfg['reference_path']}")


def _load_reference_module(cfg: dict) -> object:
    """Load reference implementation module."""
    return load_module_from_path(cfg["module_name"], str(cfg["reference_path"]))


def _load_student_module(work_dir: str, cfg: dict) -> object:
    """Load student implementation module."""
    student_path = os.path.join(work_dir, cfg["student_filename"])
    return load_module_from_path(cfg["student_module_name"], student_path)


def _get_check_functions(cfg: dict, variant: str, work_dir: str, reference_mod, student_mod):
    """Get check functions for reference and student modules."""
    if variant == "recursive":
        student_fsa_path = os.path.join(work_dir, "specification.fsa")
        start_state = get_start_state_for_recursive(student_fsa_path)
        student_fn = cfg["get_check_fn"](student_mod, start_state)
        reference_fn = cfg["get_check_fn"](reference_mod, "q0")
    else:
        reference_fn = cfg["get_check_fn"](reference_mod, None)
        student_fn = cfg["get_check_fn"](student_mod, None)

    return reference_fn, student_fn


def _create_groups(ast: dict) -> list[list[str]]:
    """
    Generate all words upfront to avoid repeats, then split into groups
    while preserving the bad word ratio per group.
    """
    full_groups, remainder = divmod(TEST_WORDS_COUNT, GROUP_SIZE)
    group_sizes = [GROUP_SIZE] * full_groups + ([remainder] if remainder else [])

    # Calculate total accepted/rejected across all groups
    total_rejected = sum(int(size * BAD_WORD_RATIO_LEVEL) for size in group_sizes)
    total_accepted = TEST_WORDS_COUNT - total_rejected

    # Generate full pools upfront — no repeats
    accepted_pool = generate_accepted_words(ast, count=total_accepted, max_iterations=5)
    accepted_pool.sort(key=lambda w: (len(w), w))
    rejected_pool = generate_rejected_words(ast, count=total_rejected)
    accepted_pool.sort(key=lambda w: (len(w), w))

    logger.info("Word pool: %d accepted, %d rejected", len(accepted_pool), len(rejected_pool))

    # Split pools into groups respecting ratio, sort each group by length
    groups = []
    acc_idx = rej_idx = 0

    for size in group_sizes:
        rejected = int(size * BAD_WORD_RATIO_LEVEL)
        accepted = size - rejected

        group = (
            accepted_pool[acc_idx : acc_idx + accepted] +
            rejected_pool[rej_idx : rej_idx + rejected]
        )
        group.sort(key=lambda w: (len(w), w))
        groups.append(group)

        acc_idx += accepted
        rej_idx += rejected

    return groups


def _run_group_tests(reference_fn, student_fn, impl_points: int, ast: dict) -> tuple[list[dict], float]:
    """
    Run behavioral testing on groups of words.

    Returns:
        (group_results, total_score)
    """
    groups = _create_groups(ast)
    points_per_group = float(impl_points / len(groups))

    results = []
    score = 0.0

    for idx, group in enumerate(groups, start=1):
        mismatches = []

        for word in group:
            ref = reference_fn(word)
            stu = student_fn(word)
            if ref != stu:
                mismatches.append({
                    "word": word,
                    "expected": ref,
                    "got": stu,
                })

        group_passed = len(mismatches) == 0
        results.append({
            "index": idx,
            "words": group,
            "passed": group_passed,
            "points": points_per_group,
            "mismatches": mismatches,
        })

        if group_passed:
            score += points_per_group

    logger.debug(f"Group testing complete: {len(groups)} groups, {score} points")
    return results, round(score, 2)


def _add_to_report(report: AssignmentReport, cfg: dict, variant: str, static_passed: bool,
                   static_errors: list, group_results: list, impl_points: int) -> None:
    """Add evaluation results to report."""
    report.section("2. FSA Implementation Testing", max_points=impl_points)
    report.subsection(f"2.1 Static Analysis: {'PASSED' if static_passed else 'FAILED'}")

    if not static_passed:
        types = {
            "import": "use of extra imports",
            "iteration": "use of iteration",
            "Recursion": "use of recursion"
        }

        error_type = next(
            (label for key, label in types.items() if any(key.lower() in err.lower() for err in static_errors)),
            "static analysis errors"
        )

        report.add_info(f"Skipping behavioral testing due to {error_type}:")
        for err in static_errors:
            report.add_info(err)
        return

    report.subsection(f"2.2 Functional Testing ({variant}):")
    report.add_info("")

    for result in group_results:
        report.add_group_result(
            group_index=result["index"],
            words=result["words"],
            passed=result["passed"],
            points=result["points"],
        )

        if not result["passed"]:
            report.add_info(format_acceptance_diff(result["mismatches"]))


# ============================================================================
# PUBLIC API
# ============================================================================

def evaluate_implementation(
        ast: dict,
        automaton_type: str,
        variant: str,
        report: AssignmentReport,
        work_dir: str,
) -> float:
    """
    Evaluate automata implementation from student submission.

    Args:
        ast: Syntax tree of the regex
        automaton_type: "dfa" or "nfa"
        variant: "iterative" or "recursive"
        report: Assignment report object
        work_dir: Directory containing student submission

    Returns:
        float: Points earned for implementation evaluation
    """
    report.set_current_score(0)
    cfg = IMPLEMENTATION_CONFIG[(automaton_type, variant)]
    impl_points = {
        "dfa": DKA_IMPLEMENTATION,
        "nfa": NKA_IMPLEMENTATION,
    }[automaton_type]

    if not os.path.exists(os.path.join(work_dir, cfg["student_filename"])):
        report.section("2. FSA Implementation Testing", 0)
        report.add_info("\nERROR")
        report.add_info("-" * 60)
        report.add_info(f"Missing required file: automaton.py")

        logger.error(f"Missing required file: automaton.py")
        return 0.0


    try:
        # Step 1: Static analysis
        logger.debug(f"Running static analysis for {automaton_type} {variant}")
        student_path = os.path.join(work_dir, cfg["student_filename"])
        static_errors = check_imports(student_path)
        static_errors.extend(cfg["static_check"](student_path))
        static_passed = not static_errors

        # Step 2: Behavioral testing (only if static passed)
        group_results = []
        score = 0.0

        if static_passed:
            logger.debug(f"Running behavioral testing for {automaton_type} {variant}")
            _generate_reference_implementation(ast, cfg)
            reference = _load_reference_module(cfg)
            student = _load_student_module(work_dir, cfg)

            reference_fn, student_fn = _get_check_functions(cfg, variant, work_dir, reference, student)

            group_results, score = _run_group_tests(reference_fn, student_fn, impl_points, ast)

            report.increase_score(score)

        # Step 3: Add to report
        _add_to_report(report, cfg, variant, static_passed, static_errors, group_results, impl_points)

        logger.info(f"Implementation evaluation for {automaton_type} {variant} complete: {score} points")
        return score
    except Exception as e:
        report.section("2. FSA Implementation Testing", 0)
        report.add_info("\nERROR")
        report.add_info("-" * 60)
        report.add_info(f"Evaluation failed: {e}")

        logger.error(f"Evaluation failed: {e}")
        return 0.0
