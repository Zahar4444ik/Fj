from datetime import datetime
from pathlib import Path

from evaluation.evaluation_profile import EVALUATION_PROFILE


class AssignmentReport:
    def __init__(self, path: str):
        self.path = Path(path)
        self.lines = []
        self.total_score = EVALUATION_PROFILE["global"]["total_score"]
        self.current_score = 0.0

        # --------------------------------------------------
        # Core helpers
        # --------------------------------------------------

    def _add_status_line(self, label: str, passed: bool):
        status = "PASSED" if passed else "FAILED"
        self.lines.append(f"{label}: {status}")

    def _add_points(self, points: float):
        if points > 0:
            self.current_score += points

    def _add_score_line(self):
        self.lines.append(
            f"[ {round(self.current_score, 2)}% / {self.total_score}% ]"
        )

    def header(self, title: str):
        self.lines.append("=" * 60)
        self.lines.append(title)
        self.lines.append(f"Generated: {datetime.now()}")
        self.lines.append("=" * 60)

    def section(self, title: str, max_score: int = 0):
        self.lines.append("")
        if max_score > 0:
            self.lines.append(f"[ {title} ] [ {max_score}% ]")
        else:
            self.lines.append(f"[ {title} ]")
        self.lines.append("-" * 60)

    def add_info(self, text):
        self.lines.append(str(text) if text is not None else "(no data)")

    def add_result(
        self,
        description: str,
        passed: bool,
        points: float = 0.0,
    ):
        self._add_status_line(description, passed)

        if passed:
            self._add_points(points)

        self._add_score_line()

    def footer(self, score):
        self.lines.append("")
        self.lines.append("=" * 60)
        self.lines.append(f"FINAL SCORE: {score}% / {self.total_score}%")
        self.lines.append("=" * 60)

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text("\n".join(self.lines), encoding="utf-8")

    def add_behavioral_group_result(
        self,
        group_index: int,
        words: list[str],
        passed: bool,
        points: float,
    ):
        self.lines.append("")
        self._add_status_line(f"Group {group_index}", passed)
        self.lines.append(f"Words: {', '.join(words)}")

        if passed:
            self._add_points(points)

        self._add_score_line()

