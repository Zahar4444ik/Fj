from datetime import datetime
from pathlib import Path

from evaluation.evaluation_profile import EVALUATION_PROFILE


class AssignmentReport:
    def __init__(self, path: str):
        self.path = Path(path)
        self.lines = []
        self.total_score = EVALUATION_PROFILE["global"]["total_score"]
        self.current_score = 0

    def header(self, title: str):
        self.lines.append("=" * 60)
        self.lines.append(title)
        self.lines.append(f"Generated: {datetime.now()}")
        self.lines.append("=" * 60)
        # self.lines.append("")

    def section(self, title: str, max_score: int = 0):
        self.lines.append("")
        self.lines.append(f"[ {title} ] [ {max_score}% ]" if max_score > 0 else f"[ {title} ]")
        self.lines.append("-" * 60)

    def add_result(self, description: str, passed: bool, points: int = 0, max_points: int = 0):
        description = str(description)
        status = "PASSED" if passed else "FAILED"
        self.lines.append(f"{description}: {status}")
        if passed and points > 0:
            self.current_score += points
        self.lines.append(f"[ {self.current_score}% / {max_points}% ]")

    def add_info(self, text):
        if text is None:
            self.lines.append("(no data)")
        else:
            self.lines.append(str(text))

    def current_score_report(self):
        self.lines.append("")
        self.lines.append(f"CURRENT SCORE: {self.current_score}% / {self.total_score}%")

    def footer(self):
        self.lines.append("")
        self.lines.append("=" * 60)
        self.lines.append(f"FINAL SCORE: {self.current_score}% / {self.total_score}%")
        self.lines.append("=" * 60)

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text("\n".join(self.lines), encoding="utf-8")

    def add_property_check(self, description: str, passed: bool, points: int = 0):
        """Add a single property check with optional points"""
        symbol = "✔" if passed else "✘"
        self.lines.append(
            f"[{symbol}] {description} (+{points} pts)" if passed else f"[{symbol}] {description} (+0 pts)")
