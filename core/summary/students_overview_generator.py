import json
import csv
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent
STUDENTS_FILE = BASE_DIR / "output" / "students.json"
OUTPUT_FILE   = BASE_DIR / "output" / "students_overview.csv"


def generate():
    if not os.path.exists(STUDENTS_FILE):
        raise FileNotFoundError(f"No such file: '{STUDENTS_FILE}'")

    with open(STUDENTS_FILE, encoding="utf-8") as f:
        students = json.load(f)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["email", "automaton_type", "implementation_type", "regex"])
        for email, data in students.items():
            writer.writerow([
                email,
                data.get("automaton_type", ""),
                data.get("implementation_type", ""),
                data.get("regex", ""),
            ])

    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    generate()
