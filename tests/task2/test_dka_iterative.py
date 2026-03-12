from task2.data.dka_iterative import student_b, student_a, student_random
import importlib.util
import sys

from tasks.task2_behavioral_testing.word_generation.testing_words_generator import generate_accepted_words, \
    generate_rejected_words


def load_module_from_path(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def prepare_reference_automaton(pattern, module_name, path):
    from core.regex.frontend.lexer import Lexer
    from core.regex.frontend.parser import Parser
    from tasks.task2_behavioral_testing.generator.dka.iterative import generate_iterative_dka

    lexer = Lexer(pattern)
    parser = Parser(lexer)
    ast = parser.parse()

    generate_iterative_dka(ast, path=path)

    return load_module_from_path(module_name, path), ast


def test_student_a():
    reference, ast = prepare_reference_automaton(
        "{0}",
        module_name="reference_a",
        path="task2/data/dka_iterative/reference_a.py"
    )

    assert reference.DFA().check("000") == student_a.DFA().check("000")
    assert reference.DFA().check("1") == student_a.DFA().check("1")


def test_student_b():
    reference, ast = prepare_reference_automaton(
        "{01}1",
        module_name="reference_b",
        path="task2/data/dka_iterative/reference_b.py"
    )

    assert reference.DFA().check("011") == student_b.DFA().check("011")
    assert reference.DFA().check("010") == student_b.DFA().check("010")


def test_student_random():
    reference, tree = prepare_reference_automaton(
        "0|1{0|1}",
        module_name="reference_random",
        path="task2/data/dka_iterative/reference_random.py"
    )

    words = generate_accepted_words(tree, count=5, max_iterations=5)
    words.extend(generate_rejected_words(tree, count=5))

    for word in words:
        assert reference.DFA().check(word) == student_random.DFA().check(word)

