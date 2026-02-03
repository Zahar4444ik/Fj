import random

from core.assignment.utils import load_module_from_path
from core.evaluation.report import AssignmentReport
from core.evaluation.utils.difference_print import format_acceptance_diff
from core.evaluation.utils.helpers import bad_word_ratio, split_into_groups
from core.regex.automata.utils.automata_operations import get_regex_alphabet
from evaluation.evaluation_profile import EVALUATION_PROFILE
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


def evaluate_implementation(ast: dict, automaton_type: str, variant: str, report: AssignmentReport) -> int:
    """
    Unified evaluation for both iterative and recursive implementations.

    :param ast: Syntax tree of the regex
    :param automaton_type: "DKA" or "NKA"
    :param variant: "iterative" or "recursive"
    :param report: Assignment report
    :return: Score earned
    """
    cfg = IMPLEMENTATION_CONFIG[(automaton_type, variant)]
    implementation_total = EVALUATION_PROFILE[automaton_type]["implementation"]["total"]

    report.section("2. Automaton Implementation Testing", implementation_total)

    # Static analysis
    errors = cfg["static_check"](cfg["student_path"])

    if errors:
        report.add_info(f"Skipping behavioral testing due to {cfg['static_error_reason']}.")
        for err in errors:
            report.add_info(err)
        report.add_info(f'[ 0% / {implementation_total}% ]')
        return 0

    # Generate reference and load both modules
    cfg["generate"](ast)

    reference = load_module_from_path(cfg["module_name"], cfg["reference_path"])
    student = load_module_from_path(cfg["student_module_name"], cfg["student_path"])

    reference_fn = cfg["get_check_fn"](reference)
    student_fn = cfg["get_check_fn"](student)

    words = generate_test_words(ast)

    random.shuffle(words)

    # 2.1 Behavioral testing
    report.section(f"2.1 Behavioral Testing ({variant})")

    return behavioral_group_test(
        words,
        reference_fn,
        student_fn,
        report,
        implementation_total,
    )


def generate_test_words(ast):
    cfg = EVALUATION_PROFILE["global"]["test_words"]

    total = cfg["count"]
    ratio = bad_word_ratio(cfg["bad_word_ratio_level"])

    rejected_count = int(total * ratio)
    accepted_count = total - rejected_count

    alphabet = get_regex_alphabet(ast)

    words = []

    words.extend(
        generate_accepted_words(
            ast,
            alphabet,
            count=accepted_count,
            max_iterations=3,
        )
    )

    words.extend(
        generate_rejected_words(
            ast,
            alphabet,
            count=rejected_count,
            max_iterations=3,
        )
    )

    return words


def behavioral_test(
    words,
    reference_fn,
    student_fn,
    report,
    max_points,
):

    points_per_word = max_points / len(words)
    score = 0.0

    for word in words:
        passed = reference_fn(word) == student_fn(word)

        report.add_result(
            f"Word '{word}'",
            passed,
            points=points_per_word if passed else 0,
        )

        if passed:
            score += points_per_word

    return round(score, 2)


def behavioral_group_test(
    words,
    reference_fn,
    student_fn,
    report,
    max_points,
):
    group_cfg = EVALUATION_PROFILE["global"]["group_testing"]
    group_size = group_cfg["group_size"]

    groups = split_into_groups(words, group_size)
    points_per_group = max_points / len(groups)

    score = 0.0

    for idx, group in enumerate(groups, start=1):
        group_passed = True
        mismatches = []

        for word in group:
            ref = reference_fn(word)
            stu = student_fn(word)

            if ref != stu:
                group_passed = False
                mismatches.append({
                    "word": word,
                    "expected": ref,
                    "got": stu,
                })

        report.add_behavioral_group_result(
            group_index=idx,
            words=group,
            passed=group_passed,
            points=points_per_group if group_passed else 0,
        )

        if group_passed:
            score += points_per_group
        else:
            report.add_info(format_acceptance_diff(mismatches))

    return round(score, 2)

