"""
Tests for static analysis checkers used in the grading pipeline.

Before running any behavioral tests the grader applies two categories of
static analysis to student code:

  1. Import restrictions — only 'from enum import Enum/auto' is permitted.
     Any other import (stdlib, third-party, bare 'import X') is forbidden
     to prevent students from bypassing the automaton requirement.

  2. Structural enforcement — the implementation type declared in the
     assignment determines which construct is forbidden:
       * iterative submissions must not contain recursion
       * recursive  submissions must not use loops or comprehensions

These tests verify that each checker reports violations on non-conforming
code and returns an empty list for conforming code.
"""

import tempfile
import textwrap
from pathlib import Path

import pytest

from graders.behavioral.checker.check_imports import check_imports
from graders.behavioral.checker.utils import check_no_iteration, check_no_recursion


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _write(code: str) -> Path:
    """Write dedented source code to a temporary .py file, return its Path."""
    f = tempfile.NamedTemporaryFile(
        suffix=".py", delete=False, mode="w", encoding="utf-8"
    )
    f.write(textwrap.dedent(code))
    f.flush()
    return Path(f.name)


# ---------------------------------------------------------------------------
# Import checker
# ---------------------------------------------------------------------------

class TestCheckImports:
    def test_file_with_no_imports_is_clean(self):
        f = _write("""
            def accept(word):
                return True
        """)
        assert check_imports(str(f)) == []

    def test_allowed_enum_import_is_accepted(self):
        f = _write("""
            from enum import Enum, auto
            class State(Enum):
                Q0 = auto()
        """)
        assert check_imports(str(f)) == []

    def test_bare_import_of_stdlib_is_forbidden(self):
        f = _write("""
            import sys
            def accept(word):
                return True
        """)
        errors = check_imports(str(f))
        assert any("sys" in e for e in errors)

    def test_from_os_import_is_forbidden(self):
        f = _write("""
            from os import path
        """)
        errors = check_imports(str(f))
        assert any("os" in e for e in errors)

    def test_from_collections_import_is_forbidden(self):
        f = _write("""
            from collections import deque
        """)
        errors = check_imports(str(f))
        assert len(errors) > 0

    def test_multiple_forbidden_imports_all_reported(self):
        f = _write("""
            import sys
            import os
            from collections import deque
        """)
        errors = check_imports(str(f))
        assert len(errors) >= 3

    def test_error_message_includes_line_number(self):
        f = _write("""
            x = 1
            import sys
        """)
        errors = check_imports(str(f))
        # The import is on line 2 (after dedent); error must reference a line
        assert any(any(ch.isdigit() for ch in e) for e in errors)

    def test_partial_enum_import_is_accepted(self):
        f = _write("""
            from enum import Enum
        """)
        assert check_imports(str(f)) == []


# ---------------------------------------------------------------------------
# Iteration checker  (recursive submissions must not use loops)
# ---------------------------------------------------------------------------

class TestCheckNoIteration:
    def test_pure_recursive_function_is_clean(self):
        f = _write("""
            def accept(word, index=0):
                if index == len(word):
                    return True
                return accept(word, index + 1)
        """)
        assert check_no_iteration(f) == []

    def test_for_loop_is_forbidden(self):
        f = _write("""
            def accept(word):
                for ch in word:
                    pass
                return True
        """)
        errors = check_no_iteration(f)
        assert any("For" in e or "for" in e.lower() for e in errors)

    def test_while_loop_is_forbidden(self):
        f = _write("""
            def accept(word):
                i = 0
                while i < len(word):
                    i += 1
                return True
        """)
        errors = check_no_iteration(f)
        assert any("While" in e or "while" in e.lower() for e in errors)

    def test_list_comprehension_is_forbidden(self):
        f = _write("""
            def accept(word):
                return [ch for ch in word]
        """)
        errors = check_no_iteration(f)
        assert len(errors) > 0

    def test_generator_expression_is_forbidden(self):
        f = _write("""
            def accept(word):
                return any(ch == "a" for ch in word)
        """)
        errors = check_no_iteration(f)
        assert len(errors) > 0

    def test_loop_inside_main_guard_is_allowed(self):
        """Loops inside if __name__ == '__main__' must not be flagged."""
        f = _write("""
            def accept(word):
                return True

            if __name__ == "__main__":
                for w in ["a", "b"]:
                    print(accept(w))
        """)
        assert check_no_iteration(f) == []


# ---------------------------------------------------------------------------
# Recursion checker  (iterative submissions must not call themselves)
# ---------------------------------------------------------------------------

class TestCheckNoRecursion:
    def test_pure_iterative_function_is_clean(self):
        f = _write("""
            def accept(word):
                state = "q0"
                for ch in word:
                    if state == "q0" and ch == "a":
                        state = "q1"
                return state == "q1"
        """)
        assert check_no_recursion(f) == []

    def test_direct_self_call_is_forbidden(self):
        f = _write("""
            def accept(word, index=0):
                if index == len(word):
                    return True
                return accept(word, index + 1)
        """)
        errors = check_no_recursion(f)
        assert len(errors) > 0

    def test_mutual_recursion_is_forbidden(self):
        f = _write("""
            def step_a(word, i):
                if i >= len(word):
                    return False
                return step_b(word, i + 1)

            def step_b(word, i):
                if i >= len(word):
                    return True
                return step_a(word, i + 1)
        """)
        errors = check_no_recursion(f)
        assert len(errors) > 0

    def test_method_self_call_in_class_is_forbidden(self):
        f = _write("""
            class Automaton:
                def accept(self, word, index=0):
                    if index == len(word):
                        return True
                    return self.accept(word, index + 1)
        """)
        errors = check_no_recursion(f)
        assert len(errors) > 0

    def test_helper_call_without_cycle_is_clean(self):
        f = _write("""
            def next_state(state, ch):
                return "q1" if ch == "a" else "q0"

            def accept(word):
                state = "q0"
                for ch in word:
                    state = next_state(state, ch)
                return state == "q1"
        """)
        assert check_no_recursion(f) == []

    def test_nonexistent_file_returns_error(self):
        errors = check_no_recursion(Path("/nonexistent/file.py"))
        assert len(errors) > 0
        assert any("not found" in e.lower() or "nonexistent" in e for e in errors)
