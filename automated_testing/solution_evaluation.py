"""
---------
Testing pipeline for student submissions.

For each student .zip in SUBMISSIONS_PATH:
  1. Extract into a working directory
  2. Validate required files are present
  3. Build the automaton from the student's task metadata
  4. Run evaluate_fsa + evaluate_implementation
  5. Save the report to RESULT_PATH

Directory layout assumed:
    SUBMISSIONS_PATH/
        student@email.com.zip
        students.json               ← produced by moodle_downloader.py

Output:
    RESULT_PATH/
        student@email.com_report.txt
"""

import os
import csv
import json
import shutil
import zipfile
import logging

from core.config.settings_parse import TITLE
from core.evaluation.fsa_evaluation import evaluate_fsa
from core.evaluation.implementation_evaluation import evaluate_implementation
from core.evaluation.report import AssignmentReport
from core.regex.automata.dka.dka_builder import build_DKA
from core.regex.automata.nka.nka_builder import build_NKA
from core.regex.frontend.helper import get_ast_from_regex

# ─────────────────────────── CONFIGURATION ───────────────────────────────────

SUBMISSIONS_PATH = r"/tasks/student_io/solutions"
RESULT_PATH      = r"/output/results"

AUTOMATON_BUILDERS = {
    "DKA": lambda ast, regex: build_DKA(ast, regex),
    "NKA": lambda ast, regex: build_NKA(ast),
}

# ─────────────────────────── LOGGING SETUP ───────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(SUBMISSIONS_PATH, "grader.log"), encoding="utf-8"),
    ],
)
log = logging.getLogger(__name__)

# ─────────────────────────── FILE PATHS ──────────────────────────────────────

STUDENTS_FILE = os.path.join(SUBMISSIONS_PATH, "students.json")
SUMMARY_FILE  = os.path.join(SUBMISSIONS_PATH, "grading_summary.csv")

# ─────────────────────────── HELPERS ─────────────────────────────────────────

def load_students() -> dict:
    if not os.path.exists(STUDENTS_FILE):
        raise FileNotFoundError(
            f"students.json not found at {STUDENTS_FILE}. Run moodle_downloader.py first."
        )
    with open(STUDENTS_FILE, encoding="utf-8") as f:
        return json.load(f)


def write_summary_row(email: str, status: str, score, error: str = "") -> None:
    write_header = not os.path.exists(SUMMARY_FILE)
    with open(SUMMARY_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["email", "status", "score", "error"])
        writer.writerow([email, status, score, error])


def extract_zip(zip_path: str, target_dir: str) -> bool:
    """Extract zip into target_dir. Returns False if zip is invalid."""
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            # Guard against zip slip (malicious paths like ../../etc)
            for member in zf.namelist():
                member_path = os.path.realpath(os.path.join(target_dir, member))
                if not member_path.startswith(os.path.realpath(target_dir)):
                    log.error("  Zip slip detected in %s, skipping", zip_path)
                    return False
            zf.extractall(target_dir)
        return True
    except zipfile.BadZipFile as exc:
        log.error("  Bad zip file: %s", exc)
        return False


def flatten_if_single_subdir(work_dir: str) -> None:
    """
    If the zip extracted into a single subdirectory (common student mistake),
    move its contents up so required files are at the top level.

    e.g. work_dir/solution/automaton.py  →  work_dir/automaton.py
    """
    entries = [e for e in os.listdir(work_dir) if not e.startswith(".")]
    if len(entries) == 1:
        subdir = os.path.join(work_dir, entries[0])
        if os.path.isdir(subdir):
            for item in os.listdir(subdir):
                shutil.move(os.path.join(subdir, item), work_dir)
            os.rmdir(subdir)
            log.info("  Flattened single subdirectory: %s/", entries[0])


def check_required_files(work_dir: str) -> list[str]:
    """Return list of missing required files."""
    required = ["automaton.py", "specification.fsa"]
    return [f for f in required if not os.path.exists(os.path.join(work_dir, f))]


def build_report(email: str, metadata: dict) -> AssignmentReport:
    """Initialise the report and write the configuration header."""
    os.makedirs(RESULT_PATH, exist_ok=True)
    path = os.path.join(RESULT_PATH, f"{email}_report.txt")
    report = AssignmentReport(path)

    report.header(TITLE, email)
    report.add_info("Configuration")
    report.add_info("-" * 60)
    report.add_info(f"Regex: {metadata['regex']}")
    report.add_info(f"Automaton type: {metadata['automaton_type']}")
    report.add_info(f"Implementation: {metadata['implementation_type']}")

    return report


# ─────────────────────────── MAIN PIPELINE ───────────────────────────────────

def process_student(email: str, metadata: dict) -> None:
    zip_path = os.path.join(SUBMISSIONS_PATH, f"{email}.zip")
    work_dir = os.path.join(SUBMISSIONS_PATH, email)

    # ── Skip students with no submission (already graded 0 during download) ──
    if metadata.get("status") == "no_submission":
        log.info("  Skipping — no submission (already graded 0)")
        write_summary_row(email, "no_submission", 0)
        return

    # ── Check zip exists ─────────────────────────────────────────────────────
    if not os.path.exists(zip_path):
        log.error("  Zip not found: %s", zip_path)
        write_summary_row(email, "missing_zip", 0, "zip file not found")
        return

    # ── Extract ──────────────────────────────────────────────────────────────
    os.makedirs(work_dir, exist_ok=True)
    if not extract_zip(zip_path, work_dir):
        write_summary_row(email, "bad_zip", 0, "could not extract zip")
        return

    flatten_if_single_subdir(work_dir)

    # ── Validate required files ───────────────────────────────────────────────
    missing = check_required_files(work_dir)
    if missing:
        log.error("  Missing required files: %s", missing)
        write_summary_row(email, "missing_files", 0, f"missing: {missing}")
        return

    # ── Build report header ───────────────────────────────────────────────────
    report = build_report(email, metadata)

    # ── Build automaton from task metadata ────────────────────────────────────
    regex          = metadata["regex"]
    automaton_type = metadata["automaton_type"]
    implementation = metadata["implementation_type"]

    ast       = get_ast_from_regex(regex)
    automaton = AUTOMATON_BUILDERS[automaton_type](ast, regex)

    # ── Evaluate and save ─────────────────────────────────────────────────────
    score = 0.0
    score += evaluate_fsa(automaton, automaton_type, report, work_dir)
    score += evaluate_implementation(ast, automaton_type, implementation, report, work_dir)

    report.footer(score)
    report.save()

    log.info("  ✔ Score: %s", score)
    write_summary_row(email, "graded", score)


def run() -> None:
    students = load_students()
    total = len(students)
    log.info("Starting grader — %d students", total)

    for idx, (email, metadata) in enumerate(students.items(), 1):
        log.info("[%d/%d] %s", idx, total, email)
        try:
            process_student(email, metadata)
        except Exception as exc:
            log.exception("  Unexpected error for %s: %s", email, exc)
            write_summary_row(email, "unexpected_error", 0, str(exc))

    log.info("Done. Summary → %s", SUMMARY_FILE)


if __name__ == "__main__":
    run()