"""
moodle_downloader.py
--------------------
Downloads student .zip submissions from a Moodle quiz question,
auto-grades missing submissions as 0, and saves progress so the
run can be safely resumed if it crashes.

Output layout (all flat in download_path):
    <download_path>/
        student@email.com.zip      # downloaded submission
        progress.json              # resume checkpoint
        grading.csv                # summary: email, status, grade
"""

import os
import re
import csv
import json
import time
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# ─────────────────────────── CONFIGURATION ───────────────────────────────────

USERNAME      = "zf687mr"                        # TUKE login  e.g. "FL123XX"
PASSWORD      = "Zahar19%03"                        # TUKE password
ASSIGNMENT_LINK = "https://moodle.fei.tuke.sk/mod/quiz/view.php?id=14339"
STUDENT_GROUP = "Všetci účastníci"        # or e.g. "01 Pondelok 07:30 (Novotný)"
QUESTION      = 1                         # question number to download
DOWNLOAD_PATH = r"C:\Users\Захар\Desktop\tuke\bakalarska\fj_assignments\tasks\student_io"

# How many seconds to wait for a .zip file to appear on disk after clicking download
DOWNLOAD_TIMEOUT = 30

# ─────────────────────────── LOGGING SETUP ───────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(DOWNLOAD_PATH, "downloader.log"), encoding="utf-8"),
    ],
)
log = logging.getLogger(__name__)

# ─────────────────────────── HELPERS ─────────────────────────────────────────

PROGRESS_FILE = os.path.join(DOWNLOAD_PATH, "progress.json")
GRADING_FILE  = os.path.join(DOWNLOAD_PATH, "grading.csv")


def load_progress() -> dict:
    """Return {email: status} dict from a previous run, or empty dict."""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_progress(progress: dict) -> None:
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


def append_grading_row(email: str, status: str, grade) -> None:
    write_header = not os.path.exists(GRADING_FILE)
    with open(GRADING_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["email", "status", "grade", "timestamp"])
        writer.writerow([email, status, grade, datetime.now().isoformat(timespec="seconds")])


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
    """XPath that matches a question div whose id ends with the question number."""
    sw  = "starts-with(@id, 'question')"
    ew  = f"substring(@id, string-length(@id) - string-length('{question_num}')+1) = '{question_num}'"
    return f"//div[{sw} and {ew}]"


# ─────────────────────────── BROWSER SETUP ───────────────────────────────────

def create_driver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--start-maximized")
    options.add_argument("--safebrowsing-disable-download-protection")
    options.add_experimental_option("prefs", {
        "download.default_directory": DOWNLOAD_PATH,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": False,
    })
    return webdriver.Chrome(options=options)


# ─────────────────────────── CORE STEPS ──────────────────────────────────────

def login(driver: webdriver.Chrome, wait: WebDriverWait) -> None:
    log.info("Logging in…")
    driver.get(
        "https://moodle.fei.tuke.sk/login/index.php"
    )
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    driver.find_element(By.ID, "username").send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.ID, "loginbtn").click()
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    log.info("Login complete.")


def open_attempts_page(driver: webdriver.Chrome, wait: WebDriverWait) -> int:
    """Navigate to the attempts overview and return total student count."""
    driver.get(ASSIGNMENT_LINK)
    wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Pokusy:"))).click()

    # Optional: filter by group
    if STUDENT_GROUP != "Všetci účastníci":
        wait.until(EC.element_to_be_clickable((
            By.XPATH,
            f"//select[@name='group']/option[contains(text(),'{STUDENT_GROUP}')]"
        ))).click()
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    count_text = driver.find_element(By.CLASS_NAME, "quizattemptcounts").text
    numbers = re.findall(r"\d+", count_text)
    count = int(numbers[0 if STUDENT_GROUP == "Všetci účastníci" else 1])

    # Show all students on one page
    page_size_input = driver.find_element(By.ID, "id_pagesize")
    page_size_input.clear()
    page_size_input.send_keys(str(count))
    driver.find_element(By.ID, "id_submitbutton").click()   # explicit button, not .submit()
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    log.info("Total students: %d", count)
    return count


def get_student_email(driver: webdriver.Chrome, wait: WebDriverWait, idx: int) -> str:
    return wait.until(EC.visibility_of_element_located((
        By.XPATH,
        f"//tbody/tr[@class='gradedattempt' or @class='']"
        f"[@id='mod-quiz-report-overview-report_r{idx}']/td[4]"
    ))).text.strip()


def open_attempt_detail(driver: webdriver.Chrome, idx: int) -> None:
    driver.find_element(
        By.XPATH,
        f"//tbody/tr[@class='gradedattempt' or @class='']"
        f"[@id='mod-quiz-report-overview-report_r{idx}']/td[3]/a[2]"
    ).click()


def download_submission(driver: webdriver.Chrome, wait: WebDriverWait, email: str) -> bool:
    """
    Try to find and download the .zip attachment for QUESTION.
    Returns True on success, False if no attachment found.
    """
    q_xpath = build_question_xpath(QUESTION)
    attachment_xpath = f"{q_xpath}//div[@class='attachments']//a"

    try:
        link_elem = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, attachment_xpath))
        )
        file_name   = link_elem.text.strip()
        download_url = link_elem.get_attribute("href")

        driver.get(download_url)

        original_path  = os.path.join(DOWNLOAD_PATH, file_name)
        final_path     = os.path.join(DOWNLOAD_PATH, f"{email}.zip")

        if wait_for_file(original_path):
            # Remove existing destination if present (re-run scenario)
            if os.path.exists(final_path):
                os.remove(final_path)
            os.rename(original_path, final_path)
            log.info("  ✔ Downloaded → %s.zip", email)
            return True
        else:
            log.warning("  ✘ Download timed out for %s (file: %s)", email, file_name)
            return False

    except TimeoutException:
        return False  # no attachment present


def grade_zero(driver: webdriver.Chrome, wait: WebDriverWait, parent_handle: str) -> None:
    """Open the manual grading popup and submit 0 for the question."""
    q_xpath = build_question_xpath(QUESTION)
    comment_link_xpath = f"{q_xpath}//div[@class='commentlink']/a"

    try:
        driver.find_element(By.XPATH, comment_link_xpath).click()
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

        # Switch to the newly opened popup window
        all_windows = driver.window_handles
        popup = next(w for w in all_windows if w != parent_handle)
        driver.switch_to.window(popup)

        # Set grade to 0
        grade_input_xpath = f"{q_xpath}//div[@class='felement ftext']/input[1]"
        grade_input = wait.until(EC.visibility_of_element_located((By.XPATH, grade_input_xpath)))
        grade_input.clear()
        grade_input.send_keys("0")
        driver.find_element(By.ID, "id_submitbutton").click()

        # Close popup and return to main window
        driver.close()
        driver.switch_to.window(parent_handle)
        log.info("  → Graded 0 (no submission)")

    except (TimeoutException, NoSuchElementException) as exc:
        log.error("  ✘ Could not grade 0: %s", exc)
        # Make sure we're back on the parent window regardless
        driver.switch_to.window(parent_handle)


# ─────────────────────────── MAIN LOOP ───────────────────────────────────────

def run() -> None:
    os.makedirs(DOWNLOAD_PATH, exist_ok=True)

    progress = load_progress()
    log.info("Loaded %d previously processed students from checkpoint.", len(progress))

    driver = create_driver()
    wait   = WebDriverWait(driver, 20)
    parent = driver.current_window_handle

    try:
        login(driver, wait)
        total = open_attempts_page(driver, wait)
        parent = driver.current_window_handle  # refresh after navigation

        for idx in range(total):
            email = get_student_email(driver, wait, idx)

            # ── Resume: skip already-processed students ──────────────────────
            if email in progress:
                log.info("[%d/%d] Skipping %s (already done: %s)", idx + 1, total, email, progress[email])
                continue

            log.info("[%d/%d] Processing %s", idx + 1, total, email)
            open_attempt_detail(driver, idx)

            downloaded = download_submission(driver, wait, email)

            if downloaded:
                status, grade = "downloaded", None
            else:
                log.info("  No attachment found — grading 0")
                grade_zero(driver, wait, parent)
                status, grade = "no_submission", 0

            # ── Save progress ────────────────────────────────────────────────
            progress[email] = status
            save_progress(progress)
            append_grading_row(email, status, grade)

            # ── Navigate back to the attempts list ───────────────────────────
            driver.execute_script("window.history.go(-1)")
            wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    except Exception as exc:
        log.exception("Fatal error: %s", exc)

    finally:
        driver.quit()   # closes the whole browser, not just the tab
        log.info("Done. Check %s for results.", GRADING_FILE)


if __name__ == "__main__":
    run()