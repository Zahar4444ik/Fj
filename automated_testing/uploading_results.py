"""
upload_results.py
-----------------
Reads each student's report .txt, parses the final score, then opens
the Moodle manual-grading popup for that student and:
  1. Pastes the full report into the comment box
  2. Enters the numeric score
  3. Submits

Requires:
    - students.json        (produced by download_solutions.py)
    - <email>_report.txt   (produced by grader.py, one per student)

Students with status 'no_submission' get score 0 and a short comment.
Students whose report is missing are logged and skipped.
"""

import os
import re
import json
import time
import logging
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# ─────────────────────────── CONFIGURATION ───────────────────────────────────

USERNAME        = ""
PASSWORD        = ""
ASSIGNMENT_LINK = "https://moodle.fei.tuke.sk/mod/quiz/view.php?id=14339"
STUDENT_GROUP   = "Všetci účastníci"
QUESTION        = 1

SUBMISSIONS_PATH = r"C:\Users\Захар\Desktop\tuke\bakalarska\fj_assignments\tasks\student_io\solutions"
RESULTS_PATH     = r"C:\Users\Захар\Desktop\tuke\bakalarska\fj_assignments\output\results"
STUDENTS_FILE    = os.path.join(SUBMISSIONS_PATH, "students.json")

# Pause every N students to avoid overwhelming Moodle (seconds)
BATCH_PAUSE_EVERY = 5
BATCH_PAUSE_SECS  = 3

# ─────────────────────────── LOGGING SETUP ───────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(SUBMISSIONS_PATH, "uploader.log"), encoding="utf-8"),
    ],
)
log = logging.getLogger(__name__)

# ─────────────────────────── HELPERS ─────────────────────────────────────────

def load_students() -> dict:
    if not os.path.exists(STUDENTS_FILE):
        raise FileNotFoundError(f"students.json not found at {STUDENTS_FILE}")
    with open(STUDENTS_FILE, encoding="utf-8") as f:
        return json.load(f)


def parse_score_from_report(report_text: str) -> float | None:
    """
    Extract score from the FINAL SCORE line, e.g.:
        FINAL SCORE:   [ 100 pts / 100 pts ]
    Returns the earned points as a float, or None if not found.
    """
    match = re.search(r"FINAL SCORE:.*?\[\s*([\d.]+)\s*pts", report_text)
    if match:
        return float(match.group(1))
    return None


def load_report(email: str) -> tuple[str | None, float | None]:
    """
    Load report text and parse score for a student.
    Returns (report_text, score) or (None, None) if file missing.
    """
    path = os.path.join(RESULTS_PATH, f"{email}_report.txt")
    if not os.path.exists(path):
        log.warning("  Report not found: %s", path)
        return None, None
    with open(path, encoding="utf-8") as f:
        text = f.read()
    score = parse_score_from_report(text)
    if score is None:
        log.warning("  Could not parse score from report for %s", email)
    return text, score


def build_question_xpath(question_num: int) -> str:
    sw = "starts-with(@id, 'question')"
    ew = f"substring(@id, string-length(@id) - string-length('{question_num}')+1) = '{question_num}'"
    return f"//div[{sw} and {ew}]"

# ─────────────────────────── BROWSER SETUP ───────────────────────────────────


def create_driver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)

# ─────────────────────────── CORE STEPS ──────────────────────────────────────


def login(driver: webdriver.Chrome, wait: WebDriverWait) -> None:
    log.info("Logging in…")
    driver.get("https://moodle.fei.tuke.sk/login/index.php")
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    driver.find_element(By.ID, "username").send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.ID, "loginbtn").click()
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    log.info("Login complete.")


def open_attempts_page(driver: webdriver.Chrome, wait: WebDriverWait) -> int:
    """Navigate to attempts overview, show all on one page, return student count."""
    driver.get(ASSIGNMENT_LINK)
    wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Pokusy:"))).click()

    if STUDENT_GROUP != "Všetci účastníci":
        wait.until(EC.element_to_be_clickable((
            By.XPATH,
            f"//select[@name='group']/option[contains(text(),'{STUDENT_GROUP}')]"
        ))).click()
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    count_text = driver.find_element(By.CLASS_NAME, "quizattemptcounts").text
    numbers = re.findall(r"\d+", count_text)
    count = int(numbers[0 if STUDENT_GROUP == "Všetci účastníci" else 1])

    page_size_input = driver.find_element(By.ID, "id_pagesize")
    page_size_input.clear()
    page_size_input.send_keys(str(count))
    driver.find_element(By.ID, "id_submitbutton").click()
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    log.info("Total students: %d", count)
    return count


def get_student_email(driver: webdriver.Chrome, wait: WebDriverWait, idx: int) -> str:
    return wait.until(EC.visibility_of_element_located((
        By.XPATH,
        f"//tbody/tr[@class='gradedattempt' or @class='']"
        f"[@id='mod-quiz-report-overview-report_r{idx}']/td[4]"
    ))).text.strip()


def open_grading_popup(driver: webdriver.Chrome, wait: WebDriverWait, idx: int, parent: str) -> bool:
    """
    Click the student's attempt, then open the grading popup for QUESTION.
    Switches driver focus to the popup window.
    Returns True on success.
    """
    # Open attempt detail
    driver.find_element(
        By.XPATH,
        f"//tbody/tr[@class='gradedattempt' or @class='']"
        f"[@id='mod-quiz-report-overview-report_r{idx}']/td[3]/a[2]"
    ).click()
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    # Click comment/grade link to open popup
    q_xpath = build_question_xpath(QUESTION)
    try:
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, f"{q_xpath}//div[@class='commentlink']/a")
        )).click()
    except TimeoutException:
        log.error("  Could not find grading link for question %d", QUESTION)
        return False

    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    popup = next(w for w in driver.window_handles if w != parent)
    driver.switch_to.window(popup)
    driver.set_window_size(1024, 768)
    return True


def paste_report_comment(driver: webdriver.Chrome, wait: WebDriverWait, report_text: str) -> None:
    """
    Paste report_text into Moodle's Atto editor line-by-line instead of one injection.
    Each line is appended individually, preserving formatting and editor behavior.
    """

    q_xpath = build_question_xpath(QUESTION)

    comment_box = wait.until(EC.visibility_of_element_located((
        By.XPATH, f"{q_xpath}//div[@class='editor_atto_content_wrap']//div"
    )))

    # Click to focus editor
    comment_box.click()

    driver.execute_script("arguments[0].innerHTML = '<br>';", comment_box)

    lines = report_text.split("\n")

    for i, line in enumerate(lines):
        safe_line = (
            line.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
        )

        # Append line
        driver.execute_script(
            "arguments[0].innerHTML += arguments[1];",
            comment_box,
            safe_line
        )

        # Add line break (except after last line)
        if i < len(lines) - 1:
            driver.execute_script(
                "arguments[0].innerHTML += '<br>';",
                comment_box
            )

        # Optional tiny delay to mimic human input (helps flaky editors)
        time.sleep(0.02)


def submit_grade(driver: webdriver.Chrome, wait: WebDriverWait, score: float) -> None:
    """Enter the numeric score and submit the grading form."""
    q_xpath = build_question_xpath(QUESTION)

    grade_input = wait.until(EC.visibility_of_element_located((
        By.XPATH, f"{q_xpath}//div[@class='felement ftext']/input[1]"
    )))

    grade_value = str(score / 10)  # HARDCODED

    grade_input.clear()
    grade_input.send_keys(grade_value)

    wait.until(lambda d: grade_input.get_attribute("value") == grade_value)

    submit_btn = wait.until(EC.element_to_be_clickable((By.ID, "id_submitbutton")))
    submit_btn.click()


# ─────────────────────────── MAIN PIPELINE ───────────────────────────────────

def upload_student(
    driver: webdriver.Chrome,
    wait: WebDriverWait,
    parent: str,
    idx: int,
    email: str,
    metadata: dict,
) -> None:
    status = metadata.get("status")

    # ── Determine report text and score ──────────────────────────────────────
    if status == "no_submission":
        report_text = "No submission — automatically graded 0."
        score = 0.0
    else:
        report_text, score = load_report(email)
        if report_text is None:
            log.error("  Skipping %s — report file missing", email)
            return
        if score is None:
            log.error("  Skipping %s — could not parse score from report", email)
            return

    log.info("  Score: %s", score)

    # ── Open grading popup ────────────────────────────────────────────────────
    if not open_grading_popup(driver, wait, idx, parent):
        driver.switch_to.window(parent)
        driver.execute_script("window.history.go(-1)")
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        return

    # ── Paste report and submit grade ─────────────────────────────────────────
    try:
        paste_report_comment(driver, wait, report_text)
        submit_grade(driver, wait, score)
        log.info("  ✔ Uploaded")
    except (TimeoutException, NoSuchElementException) as exc:
        log.error("  ✘ Upload failed: %s", exc)
    finally:
        driver.close()
        driver.switch_to.window(parent)

    driver.execute_script("window.history.go(-1)")
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")


def run() -> None:
    students = load_students()
    log.info("Loaded %d students from students.json", len(students))

    driver = create_driver()
    wait   = WebDriverWait(driver, 20)

    try:
        login(driver, wait)
        total  = open_attempts_page(driver, wait)
        parent = driver.current_window_handle

        for idx in range(total):
            email = get_student_email(driver, wait, idx)
            log.info("[%d/%d] %s", idx + 1, total, email)

            if email not in students:
                log.warning("  Not in students.json — skipping")
                continue

            upload_student(driver, wait, parent, idx, email, students[email])

            # Brief pause every N students to avoid hammering Moodle
            if (idx + 1) % BATCH_PAUSE_EVERY == 0:
                log.info("  Pausing %ds…", BATCH_PAUSE_SECS)
                time.sleep(BATCH_PAUSE_SECS)

    except Exception as exc:
        log.exception("Fatal error: %s", exc)

    finally:
        driver.quit()
        log.info("Upload complete.")


if __name__ == "__main__":
    run()