from task2.data.nka_iterative import student_b, student_c, student_a
import importlib.util
import sys


def load_module_from_path(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def prepare_reference_automaton(pattern, module_name, path):
    from core.regex.frontend.lexer import Lexer
    from core.regex.frontend.parser import Parser
    from tasks.task2_behavioral_testing.generator.nka.iterative import generate_iterative_nka

    lexer = Lexer(pattern)
    parser = Parser(lexer)
    ast = parser.parse()

    generate_iterative_nka(ast, path=path)

    return load_module_from_path(module_name, path)


def test_student_a():
    reference = prepare_reference_automaton(
        "0",
        module_name="reference_a",
        path="task2/data/nka_iterative/reference_a.py"
    ).nfa

    student = student_a.nfa
    assert reference.check("0") == student.check("0")


def test_student_b():
    reference = prepare_reference_automaton(
        "{0|1}01",
        module_name="reference_b",
        path="task2/data/nka_iterative/reference_b.py"
    ).nfa

    student = student_b.nfa
    assert reference.check("0101") == student.check("0101")


def test_wrong_student_c():
    reference = prepare_reference_automaton(
        "{0}1",
        module_name="reference_c",
        path="task2/data/nka_iterative/reference_c.py"
    ).nfa

    student = student_c.nfa
    assert reference.check("0001") != student.check("0001")
