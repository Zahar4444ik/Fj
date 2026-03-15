"""
solution_evaluation.py
---------
Testing pipeline for student submissions.

For each student .zip in SOLUTIONS_PATH:
  1. Extract into a working directory
  2. Validate required files are present
  3. Build the automaton from the student's task metadata
  4. Run evaluate_fsa + evaluate_implementation
  5. Save the report to RESULT_PATH

Directory layout assumed:
    SOLUTIONS_PATH/
        student@email.com.zip
        students.json               ← produced by download_solutions.py

Output:
    RESULT_PATH/
        student@email.com_report.txt
"""

import os
import json
import shutil
import zipfile
import logging
from pathlib import Path

from core.config.settings_parse import TITLE
from core.evaluation.fsa_evaluation import evaluate_fsa
from core.evaluation.implementation_evaluation import evaluate_implementation
from core.evaluation.report import AssignmentReport
from core.regex.automata.dka.dka_builder import build_DKA
from core.regex.automata.nka.nka_builder import build_NKA
from core.regex.frontend.helper import get_ast_from_regex

# ─────────────────────────── CONFIGURATION ───────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

SOLUTIONS_PATH = BASE_DIR / "downloads"
SOLUTIONS_PATH.mkdir(parents=True, exist_ok=True)
RESULT_PATH = BASE_DIR / "output" / "results"
OUTPUT_DIR =  BASE_DIR / "output"
RESULT_PATH.mkdir(parents=True, exist_ok=True)

AUTOMATON_BUILDERS = {
    "dfa": lambda ast, regex: build_DKA(ast, regex),
    "nfa": lambda ast, regex: build_NKA(ast),
}

# ─────────────────────────── LOGGING SETUP ───────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
)
log = logging.getLogger(__name__)

# ─────────────────────────── FILE PATHS ──────────────────────────────────────

STUDENTS_FILE = os.path.join(OUTPUT_DIR, "students.json")


# ─────────────────────────── HELPERS ─────────────────────────────────────────


def load_students() -> dict:
    if not os.path.exists(STUDENTS_FILE):
        raise FileNotFoundError(
            f"students.json not found at {STUDENTS_FILE}. Run download_solutions.py first."
        )
    with open(STUDENTS_FILE, encoding="utf-8") as f:
        return json.load(f)


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
    required = ["specification.fsa"]
    return [f for f in required if not os.path.exists(os.path.join(work_dir, f))]


def cleanup_student_files(email: str) -> None:
    """Remove student's zip file and extracted directory."""
    zip_path = os.path.join(SOLUTIONS_PATH, f"{email}.zip")
    work_dir = os.path.join(SOLUTIONS_PATH, email)

    try:
        if os.path.exists(zip_path):
            os.remove(zip_path)
            log.info("  Cleaned up zip file")
        if os.path.exists(work_dir):
            shutil.rmtree(work_dir)
            log.info("  Cleaned up working directory")
    except Exception as e:
        log.warning("  Cleanup failed: %s", e)


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


def build_report_footer(report: AssignmentReport, score: float) -> None:
    """Add final score to the report footer."""
    report.footer(score)
    report.save()


# ─────────────────────────── MAIN PIPELINE ───────────────────────────────────

def process_student(email: str, metadata: dict) -> None:
    zip_path = os.path.join(SOLUTIONS_PATH, f"{email}.zip")
    work_dir = os.path.join(SOLUTIONS_PATH, email)

    # ── Always build report first ────────────────────────────────────────────
    report = build_report(email, metadata)
    score = 0.0

    def fail(reason: str, failed: bool = True):
        nonlocal score
        log.error("  " + reason)
        report.add_info("-" * 60)
        report.add_info("\nERROR")
        report.add_info("-" * 60)
        report.add_info(reason)
        if failed:
            score = 0.0
            build_report_footer(report, score)
        return

    # ── No submission ────────────────────────────────────────────────────────
    if metadata.get("status") == "no_submission":
        fail("No submission provided.")
        return

    # ── Check zip exists ─────────────────────────────────────────────────────
    if not os.path.exists(zip_path):
        fail("Zip file not found.")
        return

    # ── Extract ──────────────────────────────────────────────────────────────
    os.makedirs(work_dir, exist_ok=True)
    if not extract_zip(zip_path, work_dir):
        fail("Bad zip file — extraction failed.")
        return

    flatten_if_single_subdir(work_dir)

    # ── Validate required files ──────────────────────────────────────────────
    missing = check_required_files(work_dir)
    if missing:
        fail(f"Missing required files: {missing}")
        return

    # ── Build automaton ──────────────────────────────────────────────────────
    try:
        regex = metadata["regex"]
        automaton_type = metadata["automaton_type"]
        variant = metadata["implementation_type"]

        ast = get_ast_from_regex(regex)
        automaton = AUTOMATON_BUILDERS[automaton_type](ast, regex)

    except Exception as e:
        fail(f"Automaton build failed: {e}")
        return

    # ── Evaluate ─────────────────────────────────────────────────────────────
    try:
        score += evaluate_fsa(automaton, automaton_type, report, work_dir)
        # score += evaluate_implementation(ast, automaton_type, variant, report, work_dir)

        if os.path.exists(os.path.join(work_dir, "automaton.py")):
            score += evaluate_implementation(ast, automaton_type, variant, report, work_dir)
        else:
            fail("Missing file: automaton.py", failed=False)
    except Exception as e:
        fail(f"Evaluation failed: {e}", failed=False)

    # ── Success ──────────────────────────────────────────────────────────────
    build_report_footer(report, score)
    log.info("  ✔ Score: %s", score)


def run() -> None:
    students = load_students()
    total = len(students)
    log.info("Starting grader — %d students", total)

    for idx, (email, metadata) in enumerate(students.items(), 1):
        log.info("[%d/%d] %s", idx, total, email)
        try:
            process_student(email, metadata)
            cleanup_student_files(email)
        except Exception as exc:
            log.exception("  Unexpected error for %s: %s", email, exc)


if __name__ == "__main__":
    run()
