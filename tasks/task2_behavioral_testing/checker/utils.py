import ast
from pathlib import Path

from tasks.task2_behavioral_testing.checker.iteration_checker import IterationChecker
from tasks.task2_behavioral_testing.checker.recursion_checker import RecursionChecker


def check_no_iteration(path: str | Path) -> list[str]:
    path = Path(path)

    try:
        code = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return [f"File not found: {path}"]
    except UnicodeDecodeError:
        return [f"Cannot read file (encoding error): {path}"]

    try:
        tree = ast.parse(code, filename=str(path))
    except SyntaxError as e:
        return [f"Syntax error in {path} at line {e.lineno}: {e.msg}"]

    checker = IterationChecker()
    checker.visit(tree)
    return checker.errors


def check_no_recursion(path: str | Path) -> list[str]:
    path = Path(path)

    try:
        code = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return [f"File not found: {path}"]
    except UnicodeDecodeError:
        return [f"Cannot read file (encoding error): {path}"]

    try:
        tree = ast.parse(code, filename=str(path))
    except SyntaxError as e:
        return [f"Syntax error in {path} at line {e.lineno}: {e.msg}"]

    checker = RecursionChecker()
    checker.visit(tree)
    checker.detect_recursion()
    return checker.errors
