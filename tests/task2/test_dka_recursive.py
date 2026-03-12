from task2.data.dka_recursive import student_b, student_a, student_random
import importlib.util
import sys

from testing.task2_behavioral_testing.generator.utils.safe_call import safe_call
from testing.task2_behavioral_testing.word_generation.testing_words_generator import generate_accepted_words, \
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
    from testing.task2_behavioral_testing.generator.dka.recursive import generate_recursive_dka

    lexer = Lexer(pattern)
    parser = Parser(lexer)
    ast = parser.parse()

    generate_recursive_dka(ast, path=path)

    return load_module_from_path(module_name, path), ast


def test_student_a():
    reference, ast = prepare_reference_automaton(
        "0",
        module_name="reference_a",
        path="tests/task2/data/dka_recursive/reference_a.py"
    )

    stu = safe_call(student_a.q0, '0')
    ref = safe_call(reference.q0, '0')
    assert stu == ref


def test_student_b():
    reference, ast = prepare_reference_automaton(
        "{0}",
        module_name="reference_b",
        path="tests/task2/data/dka_recursive/reference_b.py"
    )

    stu = safe_call(student_b.q0, '0000')
    ref = safe_call(reference.q0, '0000')
    assert stu == ref


def test_student_random():
    reference, tree = prepare_reference_automaton(
        "0|1{0|1}",
        module_name="reference_random",
        path="tests/task2/data/dka_recursive/reference_random.py"
    )

    words = generate_accepted_words(tree,  count=5, max_iterations=3)
    words.extend(generate_rejected_words(tree,  count=5))

    for w in words:
        ref = safe_call(reference.q0, w)
        stu = safe_call(student_random.q0, w)

        assert ref is not None
        assert stu is not None
        assert ref == stu, f"Mismatch on word '{w}'"

