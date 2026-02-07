from datetime import datetime
from pathlib import Path


class AssignmentReport:
    def __init__(self, path: str):
        self.path = Path(path)
        self.lines = []
        self.total_score = 100
        self._current_score = 0.0

    def header(self, title: str, student_email: str):
        """Add report header with title and metadata."""
        self.lines.extend([
            "=" * 60,
            f"{title} – Evaluation Report",
            f"Student: {student_email}",
            f"Generated: {datetime.now()}",
            "=" * 60,
        ])

    def section(self, title: str, max_points: int = None):
        """
        Add a section header.
        If max_points provided, shows as: [ title ] [ X pts / Y pts ]
        Otherwise just: [ title ]
        """
        self.lines.append("")
        self.lines.append("-" * 60)
        if max_points is not None:
            self.lines.append(f"{title:<40} [ {int(self._current_score)} pts / {max_points} pts ]")
        else:
            self.lines.append(title)
        self.lines.append("-" * 60)

    def subsection(self, title: str):
        """Add a subsection (no separator line)."""
        self.lines.append("")
        self.lines.append(title)

    def add_info(self, text: str):
        """Add informational text."""
        self.lines.append(str(text) if text is not None else "(no data)")

    def add_result(self, description: str, passed: bool, points: float = 0.0):
        """
        Add a test result with status and points.
        Format: "description: PASSED/FAILED"
        Followed by: "[ X pts / Y pts ]"
        """
        self.lines.append("")
        status = "PASSED" if passed else "FAILED"
        self.lines.append(f"{description}: {status}")

        self.lines.append(f"[ {int(points) if passed else 0} pts / {int(points)} pts ]")

    def add_group_result(
            self,
            group_index: int,
            words: list[str],
            passed: bool,
            points: float,
    ):
        """
        Add a behavioral test group result.

        :param group_index: Group number
        :param words: List of test words
        :param passed: Whether group passed
        :param points: Points for this group
        """
        status = "PASSED" if passed else "FAILED"
        self.lines.append(f"Group {group_index}: {status}")
        self.lines.append(f"Words: {', '.join(words)}")

        self.lines.append(f"[ {points if passed else 0} pts / {points} pts ]\n")

    def increase_score(self, points: float):
        """Manually increase score (for partial credit)."""
        self._current_score += points

    def footer(self, score):
        """Add final score footer."""
        self.lines.extend([
            "=" * 60,
            f"FINAL SCORE:{' ' * 27} [ {int(score)} pts / {self.total_score} pts ]",
            "=" * 60,
        ])

    def set_current_score(self, score: float):
        """Set current score to a specific value (for manual adjustments)."""
        self._current_score = score

    def save(self):
        """Write report to file."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text("\n".join(self.lines), encoding="utf-8")