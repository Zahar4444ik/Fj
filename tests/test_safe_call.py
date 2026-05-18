"""
Tests for _safe_call timeout guard in implementation_evaluation.
"""

import pytest
from core.evaluation.implementation_evaluation import _safe_call, STUDENT_TIMEOUT


def _normal(word: str) -> bool:
    return len(word) % 2 == 0


def _infinite_loop(word: str) -> bool:
    while True:
        pass


def _raises(word: str) -> bool:
    raise ValueError("student code crashed")


def test_normal_function_returns_result():
    assert _safe_call(_normal, "ab") is True
    assert _safe_call(_normal, "a") is False


def test_infinite_loop_raises_timeout():
    with pytest.raises(TimeoutError, match="timed out"):
        _safe_call(_infinite_loop, "x")


def test_student_exception_propagates():
    with pytest.raises(ValueError, match="student code crashed"):
        _safe_call(_raises, "x")


def test_timeout_constant_is_positive():
    assert STUDENT_TIMEOUT > 0
