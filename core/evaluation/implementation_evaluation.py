from core.assignment.utils import load_module_from_path
from core.regex.frontend.syntax import ALPHABET
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


def test_words(words, reference_fn, student_fn, report, section_name):
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


# ---------------------------------------------------------------------
# Iterative evaluation
# ---------------------------------------------------------------------

def evaluate_iterative(ast, automaton_type, report):
    report.section("2. Automaton Implementation Testing")

    if automaton_type == "DKA":
        generate_iterative_dka(ast)

        ref = load_module_from_path(
            "dka_iterative", "output/automata/dka_iterative.py"
        ).dfa
        stu = load_module_from_path(
            "student_dka_iterative",
            "tasks/student_io/automaton/student_dka_iterative.py",
        ).dfa

        reference_fn = ref.check
        student_fn = stu.check

    else:  # NKA
        generate_iterative_nka(ast)

        ref = load_module_from_path(
            "nka_iterative", "output/automata/nka_iterative.py"
        ).nfa
        stu = load_module_from_path(
            "student_nka_iterative",
            "tasks/student_io/automaton/student_nka_iterative.py",
        ).nfa

        reference_fn = ref.check
        student_fn = stu.check

    words = generate_test_words(ast)
    return test_words(
        words,
        reference_fn,
        student_fn,
        report,
        section_name="2.1 Behavioral Testing (iterative)",
    )


# ---------------------------------------------------------------------
# Recursive evaluation
# ---------------------------------------------------------------------

def evaluate_recursive(ast, automaton_type, report):
    report.section("2. Automaton Implementation Testing")

    student_path = (
        "tasks/student_io/automaton/student_dka_recursive.py"
        if automaton_type == "DKA"
        else "tasks/student_io/automaton/student_nka_recursive.py"
    )

    errors = check_no_iteration(student_path)
    if errors:
        report.add_result(
            "[ 2.1 Static Code Analysis ]",
            passed=False,
            points=0,
        )
        for e in errors:
            report.add_info(e)
        return 0

    report.add_result(
        "[ 2.1 Static Code Analysis ]",
        passed=True,
        points=0,
    )

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
    return test_words(
        words,
        reference.q0,
        student.q0,
        report,
        section_name="[ 2.2 Behavioral Testing ]",
    )
