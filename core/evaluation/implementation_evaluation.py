from core.assignment.utils import load_module_from_path
from core.evaluation.report import AssignmentReport
from core.regex.frontend.syntax import ALPHABET
from evaluation.evaluation_profile import EVALUATION_PROFILE
from tasks.task2_behavioral_testing.checker.utils import check_no_iteration
from tasks.task2_behavioral_testing.generator.dka.iterative import generate_iterative_dka
from tasks.task2_behavioral_testing.generator.dka.recursive import generate_recursive_dka
from tasks.task2_behavioral_testing.generator.nka.iterative import generate_iterative_nka
from tasks.task2_behavioral_testing.generator.nka.recursive import generate_recursive_nka
from tasks.task2_behavioral_testing.word_generation.testing_words_generator import (
    generate_accepted_words,
    generate_rejected_words,
)


# ---------------------------------------------------------------------
# Common helpers
# ---------------------------------------------------------------------

def generate_test_words(ast):
    words = generate_accepted_words(ast, ALPHABET, count=5, max_iterations=3)
    words.extend(generate_rejected_words(ast, ALPHABET, count=5, max_iterations=3))
    return words


def behavioral_test(words, reference_fn, student_fn, report, section_name):
    score = 0
    report.section(section_name)

    for word in words:
        passed = reference_fn(word) == student_fn(word)
        report.add_result(
            f"Word '{word}'",
            passed,
            points=1 if passed else 0,
        )
        if passed:
            score += 1

    return score


def evaluate_iterative(ast: dict, automaton_type: str, report: AssignmentReport) -> int:
    implementation_total = EVALUATION_PROFILE[automaton_type]["implementation"]["total"]
    score = 0

    report.section("2. Automaton Implementation Testing", implementation_total)

    if automaton_type == "DKA":
        generate_iterative_dka(ast)

        reference = load_module_from_path(
            "dka_iterative", "output/automata/dka_iterative.py"
        ).dfa
        student = load_module_from_path(
            "student_dka_iterative",
            "tasks/student_io/automaton/student_dka_iterative.py",
        ).dfa

        reference_fn = reference.check
        student_fn = student.check

    else:  # NKA
        generate_iterative_nka(ast)

        reference = load_module_from_path(
            "nka_iterative", "output/automata/nka_iterative.py"
        ).nfa
        student = load_module_from_path(
            "student_nka_iterative",
            "tasks/student_io/automaton/student_nka_iterative.py",
        ).nfa

        reference_fn = reference.check
        student_fn = student.check

    words = generate_test_words(ast)

    return behavioral_test(
        words,
        reference_fn,
        student_fn,
        report,
        section_name="2.1 Behavioral Testing (iterative)",
    )


def evaluate_recursive(ast: dict, automaton_type: str, report: AssignmentReport) -> int:
    implementation_total = EVALUATION_PROFILE[automaton_type]["implementation"]["total"]
    score = 0

    report.section("2. Automaton Implementation Testing", implementation_total)

    student_path = (
        "tasks/student_io/automaton/student_dka_recursive.py"
        if automaton_type == "DKA"
        else "tasks/student_io/automaton/student_nka_recursive.py"
    )

    # Static analysis
    errors = check_no_iteration(student_path)

    if errors:
        report.add_info(f"Skipping behavioral testing due to use of iteration.")
        for err in errors:
            report.add_info(err)
        report.add_info(f'[ 0% / {implementation_total}% ]')
        return 0

    # Generate reference automaton
    if automaton_type == "DKA":
        generate_recursive_dka(ast)

        reference = load_module_from_path(
            "dka_recursive", "output/automata/dka_recursive.py"
        )
        student = load_module_from_path(
            "student_dka_recursive", student_path
        )

    else:
        generate_recursive_nka(ast)

        reference = load_module_from_path(
            "nka_recursive", "output/automata/nka_recursive.py"
        )
        student = load_module_from_path(
            "student_nka_recursive", student_path
        )

    words = generate_test_words(ast)

    # 2.3 Behavioral testing
    return behavioral_test(
        words,
        reference.q0,
        student.q0,
        report,
        section_name="2.3 Behavioral Testing (recursive)",
    )
