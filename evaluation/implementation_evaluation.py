from core.assignment.utils import load_module_from_path
from core.regex.frontend.syntax import ALPHABET
from tasks.task2_behavioral_testing.checker.utils import check_no_iteration
from tasks.task2_behavioral_testing.generator.dka.iterative import generate_iterative_dka
from tasks.task2_behavioral_testing.generator.dka.recursive import generate_recursive_dka
from tasks.task2_behavioral_testing.generator.nka.iterative import generate_iterative_nka
from tasks.task2_behavioral_testing.generator.nka.recursive import generate_recursive_nka
from tasks.task2_behavioral_testing.word_generation.testing_words_generator import generate_accepted_words, \
    generate_rejected_words


def evaluate_iterative(ast, automaton_type):
    score = 0

    if automaton_type == "DKA":
        generate_iterative_dka(ast)

        reference = load_module_from_path("dka_iterative", "output/automata/dka_iterative.py").dfa
        student = load_module_from_path("student_dka_iterative", "tasks/student_io/automaton/student_dka_iterative.py").dfa
    else:
        generate_iterative_nka(ast)

        reference = load_module_from_path("nka_iterative", "output/automata/nka_iterative.py").nfa
        student = load_module_from_path("student_nka_iterative", "tasks/student_io/automaton/student_nka_iterative.py").nfa

    words = generate_accepted_words(ast, ALPHABET, count=5, max_iterations=3)
    words.extend(generate_rejected_words(ast, ALPHABET, count=5, max_iterations=3))

    for word in words:
        print(f"Testing word: '{word}'")
        if reference.check(word) == student.check(word):
            print("PASSED! +1 point")
            score += 1
        else:
            print("FAILED!")

    return score


def evaluate_recursive(ast, automaton_type):
    score = 0

    errors = check_no_iteration("tasks/student_io/automaton/student_dka_recursive.py")

    if errors:
        print("❌ Iteration rule violated:")
        for e in errors:
            print("  -", e)
        return score
    else:
        print("✅ No forbidden iteration detected")

    if automaton_type == "DKA":
        generate_recursive_dka(ast)

        reference = load_module_from_path("dka_recursive", "output/automata/dka_recursive.py")
        student = load_module_from_path("student_dka_recursive", "tasks/student_io/automaton/student_dka_recursive.py")
    else:
        generate_recursive_nka(ast)

        reference = load_module_from_path("nka_recursive", "output/automata/nka_recursive.py")
        student = load_module_from_path("student_nka_recursive", "tasks/student_io/automaton/student_nka_recursive.py")

    words = generate_accepted_words(ast, ALPHABET, count=5, max_iterations=3)
    words.extend(generate_rejected_words(ast, ALPHABET, count=5, max_iterations=3))

    for word in words:
        print(f"Testing word: '{word}'")
        if reference.q0(word) == student.q0(word):
            print("PASSED! +1 point")
            score += 1
        else:
            print("FAILED!")

    return score
