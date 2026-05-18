"""
Tests for core/evaluation/report.py — AssignmentReport

The report is the primary artefact produced per student: it is saved to
output/results/<email>_report.txt and its content is later pasted into
Moodle by the upload pipeline.  The upload script locates the final grade
via the regex r'FINAL SCORE:.*?\\[\\s*([\\d.]+)\\s*pts'.

These tests verify the formatting contract that the rest of the pipeline
depends on, as well as the file I/O guarantees of AssignmentReport.save().
"""

import re
import pytest

from core.evaluation.report import AssignmentReport


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------

@pytest.fixture
def report(tmp_path):
    return AssignmentReport(str(tmp_path / "report.txt"))


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

class TestHeader:
    def test_title_appears_in_output(self, report):
        report.header("FSA Credit Test A", "john@tuke.sk")
        assert any("FSA Credit Test A" in line for line in report.lines)

    def test_student_email_appears_in_output(self, report):
        report.header("Test", "john@tuke.sk")
        assert any("john@tuke.sk" in line for line in report.lines)


# ---------------------------------------------------------------------------
# add_result
# ---------------------------------------------------------------------------

class TestAddResult:
    def test_passed_result_contains_passed_keyword(self, report):
        report.add_result("Isomorphism check", passed=True, points=30, total_points=30)
        assert any("PASSED" in line for line in report.lines)

    def test_failed_result_contains_failed_keyword(self, report):
        report.add_result("Isomorphism check", passed=False, points=0, total_points=30)
        assert any("FAILED" in line for line in report.lines)

    def test_result_shows_awarded_points(self, report):
        report.add_result("Annotations", passed=True, points=20, total_points=20)
        assert any("20" in line for line in report.lines)

    def test_result_shows_total_points(self, report):
        report.add_result("Implementation", passed=False, points=0, total_points=50)
        text = "\n".join(report.lines)
        assert "50" in text


# ---------------------------------------------------------------------------
# Score tracking
# ---------------------------------------------------------------------------

class TestScoreTracking:
    def test_increase_score_accumulates_correctly(self, report):
        report.increase_score(30)
        report.increase_score(20)
        assert report._current_score == 50.0

    def test_set_current_score_overrides_accumulated(self, report):
        report.increase_score(30)
        report.set_current_score(75.0)
        assert report._current_score == 75.0

    def test_initial_score_is_zero(self, report):
        assert report._current_score == 0.0


# ---------------------------------------------------------------------------
# Footer — critical for the upload pipeline
# ---------------------------------------------------------------------------

class TestFooter:
    def test_footer_contains_final_score_label(self, report):
        report.footer(85)
        assert any("FINAL SCORE" in line for line in report.lines)

    def test_footer_score_matches_upload_parser_pattern(self, report):
        """The upload pipeline uses regex r'FINAL SCORE:.*?\\[\\s*([\\d.]+)\\s*pts'."""
        report.footer(73.5)
        text = "\n".join(report.lines)
        match = re.search(r"FINAL SCORE:.*?\[\s*([\d.]+)\s*pts", text)
        assert match is not None, "Upload parser pattern not found in footer"
        assert float(match.group(1)) == 73.5

    def test_zero_score_is_parseable(self, report):
        report.footer(0)
        text = "\n".join(report.lines)
        match = re.search(r"FINAL SCORE:.*?\[\s*([\d.]+)\s*pts", text)
        assert match is not None
        assert float(match.group(1)) == 0.0

    def test_full_score_is_parseable(self, report):
        report.footer(100)
        text = "\n".join(report.lines)
        match = re.search(r"FINAL SCORE:.*?\[\s*([\d.]+)\s*pts", text)
        assert match is not None
        assert float(match.group(1)) == 100.0


# ---------------------------------------------------------------------------
# Group result
# ---------------------------------------------------------------------------

class TestGroupResult:
    def test_passed_group_shows_passed(self, report):
        report.add_group_result(1, ["ab", "ba"], passed=True, points=5.0)
        assert any("PASSED" in line for line in report.lines)

    def test_failed_group_shows_failed(self, report):
        report.add_group_result(2, ["ab"], passed=False, points=5.0)
        assert any("FAILED" in line for line in report.lines)

    def test_empty_string_word_displayed_as_quoted_empty(self, report):
        report.add_group_result(1, [""], passed=True, points=5.0)
        text = "\n".join(report.lines)
        assert '""' in text

    def test_group_index_appears_in_output(self, report):
        report.add_group_result(3, ["xyz"], passed=True, points=5.0)
        assert any("3" in line for line in report.lines)


# ---------------------------------------------------------------------------
# File I/O
# ---------------------------------------------------------------------------

class TestSave:
    def test_save_creates_file_on_disk(self, tmp_path):
        path = tmp_path / "out.txt"
        r = AssignmentReport(str(path))
        r.header("T", "a@b.com")
        r.footer(100)
        r.save()
        assert path.exists()

    def test_saved_content_contains_all_added_lines(self, tmp_path):
        path = tmp_path / "out.txt"
        r = AssignmentReport(str(path))
        r.header("Test", "a@b.com")
        r.add_info("Custom info line")
        r.footer(42)
        r.save()
        content = path.read_text(encoding="utf-8")
        assert "Custom info line" in content
        assert "FINAL SCORE" in content

    def test_save_creates_missing_parent_directories(self, tmp_path):
        deep = tmp_path / "a" / "b" / "c" / "report.txt"
        r = AssignmentReport(str(deep))
        r.footer(0)
        r.save()
        assert deep.exists()
