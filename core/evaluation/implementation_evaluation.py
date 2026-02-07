import random

from core.assignment.utils import load_module_from_path
from core.config.scoring import DKA_IMPLEMENTATION, NKA_IMPLEMENTATION, TEST_WORDS_COUNT, BAD_WORD_RATIO_LEVEL, \
    GROUP_SIZE
from core.evaluation.report import AssignmentReport
from core.evaluation.utils.difference_print import format_acceptance_diff
from core.evaluation.utils.helpers import split_into_groups
from core.regex.automata.utils.automata_operations import get_regex_alphabet
from tasks.task2_behavioral_testing.checker.utils import check_no_iteration, check_no_recursion
from tasks.task2_behavioral_testing.generator.dka.iterative import generate_iterative_dka
from tasks.task2_behavioral_testing.generator.dka.recursive import generate_recursive_dka
from tasks.task2_behavioral_testing.generator.nka.iterative import generate_iterative_nka
from tasks.task2_behavioral_testing.generator.nka.recursive import generate_recursive_nka
from tasks.task2_behavioral_testing.word_generation.testing_words_generator import (
    generate_accepted_words,
    generate_rejected_words,
)

IMPLEMENTATION_CONFIG = {
    ("DKA", "iterative"): {
        "student_path": "tasks/student_io/automaton/student_dka_iterative.py",
        "reference_path": "output/automata/dka_iterative.py",
        "module_name": "dka_iterative",
        "student_module_name": "student_dka_iterative",
        "static_check": check_no_recursion,
        "static_error_reason": "use of recursion",
        "generate": generate_iterative_dka,
        "get_check_fn": lambda mod: mod.dfa.check,
    },
    ("DKA", "recursive"): {
        "student_path": "tasks/student_io/automaton/student_dka_recursive.py",
        "reference_path": "output/automata/dka_recursive.py",
        "module_name": "dka_recursive",
        "student_module_name": "student_dka_recursive",
        "static_check": check_no_iteration,
        "static_error_reason": "use of iteration",
        "generate": generate_recursive_dka,
        "get_check_fn": lambda mod: mod.q0,
    },
    ("NKA", "iterative"): {
        "student_path": "tasks/student_io/automaton/student_nka_iterative.py",
        "reference_path": "output/automata/nka_iterative.py",
        "module_name": "nka_iterative",
        "student_module_name": "student_nka_iterative",
        "static_check": check_no_recursion,
        "static_error_reason": "use of recursion",
        "generate": generate_iterative_nka,
        "get_check_fn": lambda mod: mod.nfa.check,
    },
    ("NKA", "recursive"): {
        "student_path": "tasks/student_io/automaton/student_nka_recursive.py",
        "reference_path": "output/automata/nka_recursive.py",
        "module_name": "nka_recursive",
        "student_module_name": "student_nka_recursive",
        "static_check": check_no_iteration,
        "static_error_reason": "use of iteration",
        "generate": generate_recursive_nka,
        "get_check_fn": lambda mod: mod.q0,
    },
}


def evaluate_implementation(
        ast: dict,
        automaton_type: str,
        variant: str,
        report: AssignmentReport
) -> float:
    """
    Unified evaluation for both iterative and recursive implementations.

    :param ast: Syntax tree of the regex
    :param automaton_type: "DKA" or "NKA"
    :param variant: "iterative" or "recursive"
    :param report: Assignment report
    :return: Score earned
    """
    report.set_current_score(0)
    cfg = IMPLEMENTATION_CONFIG[(automaton_type, variant)]
    impl_point = DKA_IMPLEMENTATION if automaton_type == "DKA" else NKA_IMPLEMENTATION

    # ============================================================
    # 1. Static analysis
    # ============================================================
    static_errors = cfg["static_check"](cfg["student_path"])
    static_passed = not static_errors

    # ============================================================
    # 2. Behavioral testing (only if static passed)
    # ============================================================
    group_results = []
    score = 0.0

    if static_passed:
        # Generate reference and load modules
        cfg["generate"](ast)
        reference = load_module_from_path(cfg["module_name"], cfg["reference_path"])
        student = load_module_from_path(cfg["student_module_name"], cfg["student_path"])

        reference_fn = cfg["get_check_fn"](reference)
        student_fn = cfg["get_check_fn"](student)

        # Generate and shuffle test words
        words = generate_test_words(ast)
        random.shuffle(words)

        # Run group testing
        group_results, score = run_group_tests(words, reference_fn, student_fn, impl_point)

        report.increase_score(score)

    # ============================================================
    # 3. Add to report
    # ============================================================
    report.section("2. FSA Implementation Testing", max_points=impl_point)
    report.subsection(f"2.1 Static Analysis: {'PASSED' if static_passed else 'FAILED'}")

    if not static_passed:
        report.add_info(f"Skipping behavioral testing due to {cfg['static_error_reason']}.")
        for err in static_errors:
            report.add_info(err)
        return 0.0

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

    return score


def generate_test_words(ast: dict) -> list[str]:
    """Generate test words based on configuration."""

    total = TEST_WORDS_COUNT
    ratio = BAD_WORD_RATIO_LEVEL

    rejected_count = int(total * ratio)

    accepted_count = total - rejected_count

    alphabet = get_regex_alphabet(ast)

    words = []
    words.extend(
        generate_accepted_words(ast, alphabet, count=accepted_count, max_iterations=3)
    )
    words.extend(
        generate_rejected_words(ast, alphabet, count=rejected_count, max_iterations=3)
    )

    return words


def run_group_tests(words: list[str], reference_fn, student_fn, impl_points: int) -> tuple[list[dict], float]:
    """
    Run behavioral testing on groups of words.

    Returns:
        (group_results, total_score)
    """
    group_size = GROUP_SIZE

    groups = split_into_groups(words, group_size)
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

    return results, round(score, 2)