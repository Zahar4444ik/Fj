"""
download_solutions.py
---------------------
Downloads student .zip submissions from a Moodle quiz question,
scrapes per-student task metadata (regex, automaton_type, implementation_type)
from the question description, and auto-grades missing submissions as 0.

students.json is the single source of truth — it acts as both the metadata
store for the grader and the resume checkpoint if the run is interrupted.

Output layout (all flat in DOWNLOAD_PATH):
    <DOWNLOAD_PATH>/
        student@email.com.zip      # downloaded submission
        students.json              # per-student metadata + status for grader
"""

import os
import re
import json
import time
import logging
from pathlib import Path

import requests

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from core.config.settings_parse import PASSWORD, USERNAME, ASSIGNMENT_LINK, QUESTION_NUMBER

# ─────────────────────────── CONFIGURATION ───────────────────────────────────

BASE_DIR = Path(__file__).resolve().parent.parent

# Settings from environment
MOODLE_USERNAME = USERNAME
MOODLE_PASSWORD = PASSWORD
MOODLE_ASSIGNMENT_LINK = ASSIGNMENT_LINK

# Local settings
STUDENT_GROUP = "Všetci účastníci"  # or e.g. "01 Pondelok 07:30 (Novotný)"
QUESTION = QUESTION_NUMBER  # question number to download
DOWNLOAD_PATH = BASE_DIR / "downloads"
DOWNLOAD_PATH.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DOWNLOAD_TIMEOUT = 30  # seconds to wait for a .zip to appear on disk

# ─────────────────────────── LOGGING SETUP ───────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
)
log = logging.getLogger(__name__)

# ─────────────────────────── STUDENTS.JSON ───────────────────────────────────

STUDENTS_FILE = os.path.join(OUTPUT_DIR, "students.json")


def load_students() -> dict:
    """Return {email: metadata} from a previous run, or empty dict."""
    if os.path.exists(STUDENTS_FILE):
        with open(STUDENTS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_students(students: dict) -> None:
    with open(STUDENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(students, f, ensure_ascii=False, indent=2)


# ─────────────────────────── HELPERS ─────────────────────────────────────────

def wait_for_file(path: str, timeout: int = DOWNLOAD_TIMEOUT) -> bool:
    """Block until file exists and is fully written (size stable for 1 s)."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        if os.path.exists(path):
            size_before = os.path.getsize(path)
            time.sleep(1)
            if os.path.getsize(path) == size_before and size_before > 0:
                return True
        time.sleep(0.5)
    return False


def build_question_xpath(question_num: int) -> str:
    """XPath that matches the question div whose id ends with question_num."""
    sw = "starts-with(@id, 'question')"
    ew = f"substring(@id, string-length(@id) - string-length('{question_num}')+1) = '{question_num}'"
    return f"//div[{sw} and {ew}]"


def get_question_name(driver: webdriver.Chrome, wait: WebDriverWait) -> str | None:
    """
    Read the question name from the attempt review summary table.
    Moodle renders it as a <td class="cell"> next to <th>Otázka</th>.
    """
    try:
        name_elem = wait.until(EC.presence_of_element_located((
            By.XPATH, "//th[@scope='row'][.='Otázka']/following-sibling::td[@class='cell']"
        )))
        return name_elem.text.strip()
    except TimeoutException:
        log.warning("  Could not find question name element on page")
        return None


def parse_metadata_from_name(question_name: str) -> dict:
    """
    Parse automaton_type, implementation_type, and regex from the question name.

    Expected format: "<automaton_type>_<implementation_type>_<regex>"
    Example:         "DKA_iterative_{c[a]|ab}b"

    Uses maxsplit=2 so the regex part (which may itself contain '_') is
    always preserved intact as the third element.
    """
    automatons = {"DKA": "dfa", "NKA": "nfa"}

    empty = {"regex": None, "automaton_type": None, "implementation_type": None}

    parts = question_name.split("_", maxsplit=2)
    if len(parts) != 3:
        log.warning("  Unexpected question name format: %r (expected 3 parts, got %d)", question_name, len(parts))
        return empty

    automaton_raw, implementation_raw, regex = parts

    automaton_type = automaton_raw
    if automaton_type in ("DKA", "NKA"):
        automaton_type = automatons[automaton_type]
    if automaton_type not in ("dfa", "nfa"):
        log.warning("  Unknown automaton type %r in question name %r", automaton_raw, question_name)
        automaton_type = None

    implementation_type = implementation_raw.lower()
    if implementation_type not in ("iterative", "recursive"):
        log.warning("  Unknown implementation %r in question name %r", implementation_raw, question_name)
        implementation_type = None

    log.info("  Metadata → regex=%s  automaton=%s  impl=%s", regex, automaton_type, implementation_type)
    return {
        "regex": regex,
        "automaton_type": automaton_type,
        "implementation_type": implementation_type,
    }


def get_metadata(driver: webdriver.Chrome, wait: WebDriverWait) -> dict:
    """Read the question name from the page and parse metadata from it."""
    name = get_question_name(driver, wait)
    if not name:
        return {"regex": None, "automaton_type": None, "implementation_type": None}
    return parse_metadata_from_name(name)


# ─────────────────────────── BROWSER SETUP ───────────────────────────────────

def create_driver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--start-maximized")
    options.add_argument("--safebrowsing-disable-download-protection")
    options.add_experimental_option("prefs", {
        "download.default_directory": str(DOWNLOAD_PATH),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": False,
    })
    return webdriver.Chrome(options=options)


# ─────────────────────────── CORE STEPS ──────────────────────────────────────

def _is_logged_in(driver: webdriver.Chrome) -> bool:
    """Check if login succeeded by verifying we left the login page."""
    url = driver.current_url
    return "moodle.fei.tuke.sk" in url and "login" not in url


def login(driver: webdriver.Chrome, wait: WebDriverWait) -> None:
    log.info("Logging in…")

    # ── Attempt 1: SSO (KPI) login ───────────────────────────────────────────
    try:
        driver.get(
            "https://sso.kpi.fei.tuke.sk/login"
            "?service=https%3A%2F%2Fmoodle.fei.tuke.sk%2Flogin%2Findex.php%3FauthCAS%3DCAS"
        )
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        driver.find_element(By.ID, "username").send_keys(MOODLE_USERNAME)
        driver.find_element(By.ID, "password").send_keys(MOODLE_PASSWORD)
        driver.find_element(By.NAME, "submit").click()
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

        if _is_logged_in(driver):
            log.info("Login successful (SSO).")
            return
        log.warning("SSO login failed — trying direct Moodle login…")
    except Exception as exc:
        log.warning("SSO login error (%s) — trying direct Moodle login…", exc)

    # ── Attempt 2: direct Moodle login ───────────────────────────────────────
    driver.get("https://moodle.fei.tuke.sk/login/index.php")
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    username_field = driver.find_element(By.ID, "username")
    username_field.clear()
    username_field.send_keys(MOODLE_USERNAME)
    driver.find_element(By.ID, "password").send_keys(MOODLE_PASSWORD)
    driver.find_element(By.ID, "loginbtn").click()
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    if _is_logged_in(driver):
        log.info("Login successful (direct).")
    else:
        raise RuntimeError("Both login methods failed — check credentials or Moodle availability.")


def open_attempts_page(driver: webdriver.Chrome, wait: WebDriverWait) -> int:
    """Navigate to the attempts overview and return total student count."""
    driver.get(MOODLE_ASSIGNMENT_LINK)
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


def open_attempt_detail(driver: webdriver.Chrome, wait: WebDriverWait, idx: int, parent: str) -> None:
    """Click the 'Zhodnotiť odpoveď' grading link and switch focus to the new window."""

    wait.until(EC.element_to_be_clickable((  # HARDCODED FOR 2 solution
        By.XPATH,
        f"//tbody/tr[@class='gradedattempt' or @class='']"
        f"[@id='mod-quiz-report-overview-report_r{idx}']"
        f"//a[contains(@href,'slot={QUESTION}') and contains(@title,'Zhodnoti')]"
    ))).click()

    # Wait for the new window to appear and switch to it
    wait.until(lambda d: len(d.window_handles) > 1)
    new_window = next(w for w in driver.window_handles if w != parent)
    driver.switch_to.window(new_window)
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")


def download_submission(driver: webdriver.Chrome, email: str) -> bool:
    q_xpath = build_question_xpath(QUESTION)
    attachment_xpath = f"{q_xpath}//div[@class='attachments']//a"

    try:
        link_elem = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, attachment_xpath))
        )
        download_url = link_elem.get_attribute("href")

        # Copy session cookies from Selenium into requests
        session = requests.Session()
        for cookie in driver.get_cookies():
            session.cookies.set(cookie["name"], cookie["value"])

        response = session.get(download_url, stream=True, timeout=30)

        if response.status_code == 200 and "zip" in response.headers.get("Content-Type", ""):
            final_path = os.path.join(DOWNLOAD_PATH, f"{email}.zip")
            with open(final_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            log.info("  ✔ Downloaded → %s.zip", email)
            return True
        else:
            log.warning("  ✘ Unexpected response for %s: %s %s",
                        email, response.status_code, response.headers.get("Content-Type"))
            return False

    except TimeoutException:
        return False


# ─────────────────────────── MAIN LOOP ───────────────────────────────────────

def run() -> None:
    students = load_students()
    log.info("Loaded %d previously processed students from students.json.", len(students))

    driver = create_driver()
    wait = WebDriverWait(driver, 20)

    try:
        login(driver, wait)
        total = open_attempts_page(driver, wait)
        parent = driver.current_window_handle

        for idx in range(total):
            email = get_student_email(driver, wait, idx)

            # ── Resume: skip students already in students.json ───────────────
            if email in students:
                log.info("[%d/%d] Skipping %s (already done: %s)", idx + 1, total, email, students[email].get("status"))
                continue

            log.info("[%d/%d] Processing %s", idx + 1, total, email)
            open_attempt_detail(driver, wait, idx, parent)

            metadata = get_metadata(driver, wait)
            downloaded = download_submission(driver, email)

            if downloaded:
                metadata["status"] = "downloaded"
            else:
                log.info("  No attachment found — grading 0")
                metadata["status"] = "no_submission"

            # ── Save immediately so a crash mid-run is resumable ─────────────
            students[email] = metadata
            save_students(students)

            # ── Close grading window and return to attempts list ─────────────
            driver.close()
            driver.switch_to.window(parent)
            wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    except Exception as exc:
        log.exception("Fatal error: %s", exc)

    finally:
        driver.quit()
        log.info("Done. students.json saved to %s", STUDENTS_FILE)


if __name__ == "__main__":
    run()
