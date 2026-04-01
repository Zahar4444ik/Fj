"""
Tests for the student-facing FSA syntax checker (check_syntax.py).

Imports check_fsa_syntax directly from the shared skeleton script so that
the tests always run against the exact code students receive in the zip.
"""

import importlib.util
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Load check_fsa_syntax from the shared skeleton script
# ---------------------------------------------------------------------------

_CHECKER_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "graders" / "behavioral" / "skeletons" / "shared" / "check_syntax.py"
)

_spec = importlib.util.spec_from_file_location("check_syntax", _CHECKER_PATH)
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
check_fsa_syntax = _module.check_fsa_syntax

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

DATA_DIR = Path(__file__).parent / "data"


def errors(filename: str) -> list[str]:
    return check_fsa_syntax(str(DATA_DIR / filename))


def assert_valid(filename: str):
    errs = errors(filename)
    assert errs == [], f"Expected no errors in {filename}, got:\n" + "\n".join(errs)


def assert_invalid(filename: str, *expected_fragments: str):
    """Assert the file has errors and that each fragment appears in at least one error."""
    errs = errors(filename)
    assert errs, f"Expected errors in {filename} but got none"
    combined = "\n".join(errs).lower()
    for fragment in expected_fragments:
        assert fragment.lower() in combined, (
            f"Expected '{fragment}' in errors for {filename}.\nActual errors:\n" + "\n".join(errs)
        )


# ---------------------------------------------------------------------------
# Valid files
# ---------------------------------------------------------------------------


def test_valid_dfa():
    assert_valid("valid_dfa.fsa")


def test_valid_dfa_with_annotations_and_trailing_comma():
    """Annotations (state = "label") and trailing commas are legal."""
    assert_valid("valid_dfa_annotated.fsa")


def test_valid_nfa_with_epsilon_transitions():
    """eps and epsilon are both valid epsilon symbols."""
    assert_valid("valid_nfa.fsa")


def test_comments_are_ignored():
    """Lines starting with # must not produce errors."""
    assert_valid("valid_dfa_annotated.fsa")


# ---------------------------------------------------------------------------
# Missing / misspelled sections
# ---------------------------------------------------------------------------


def test_missing_section_accepting_states():
    assert_invalid("missing_section.fsa", "accepting_states")


def test_misspelled_keyword():
    """'alphabt' is not a valid keyword — should report it and flag missing alphabet."""
    assert_invalid("misspelled_keyword.fsa", "alphabt", "alphabet")


# ---------------------------------------------------------------------------
# Transition errors
# ---------------------------------------------------------------------------


def test_transition_missing_symbol():
    """q0 -> q1 is invalid — symbol between dashes is required."""
    assert_invalid("bad_transition_no_symbol.fsa")


def test_transition_wrong_arrow():
    """q0 -a- q1 is invalid — '->' is required after the symbol."""
    assert_invalid("bad_transition_wrong_arrow.fsa", "->")


# ---------------------------------------------------------------------------
# Structural errors
# ---------------------------------------------------------------------------


def test_missing_closing_brace():
    assert_invalid("missing_brace.fsa", "}")


def test_annotation_without_quotes():
    """state = start is invalid — annotation must be a quoted string."""
    assert_invalid("bad_annotation.fsa", "quoted string")


# ---------------------------------------------------------------------------
# Multiple errors in one file
# ---------------------------------------------------------------------------


def test_multiple_errors_reported():
    """A file with several errors should report all of them, not stop at the first."""
    errs = errors("multiple_errors.fsa")
    assert len(errs) >= 2, (
        f"Expected at least 2 errors, got {len(errs)}:\n" + "\n".join(errs)
    )


# ---------------------------------------------------------------------------
# Error message quality
# ---------------------------------------------------------------------------


def test_errors_include_line_numbers():
    """Inline errors (token-level) must contain a line reference.
    File-level errors like 'Missing required section' don't have a line and are excluded."""
    errs = errors("misspelled_keyword.fsa")
    inline = [e for e in errs if not e.lower().startswith("missing required")]
    assert inline, "Expected at least one inline error"
    for err in inline:
        assert "line" in err.lower(), f"Inline error missing line number: {err}"
