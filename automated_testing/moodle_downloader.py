"""
moodle_downloader.py
--------------------
Downloads student .zip submissions from a Moodle quiz question,
scrapes per-student task metadata (regex, automaton_type, implementation_type)
from the question description, auto-grades missing submissions as 0,
and saves progress so the run can be safely resumed if it crashes.

Output layout (all flat in download_path):
    <download_path>/
        student@email.com.zip      # downloaded submission
        students.json              # per-student metadata for the grader
        progress.json              # resume checkpoint
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

# ─────────────────────────── CONFIGURATION ───────────────────────────────────

USERNAME      = ""                        # TUKE login  e.g. "FL123XX"
PASSWORD      = ""                        # TUKE password
ASSIGNMENT_LINK = "https://moodle.fei.tuke.sk/mod/quiz/view.php?id=14339"
STUDENT_GROUP = "Všetci účastníci"        # or e.g. "01 Pondelok 07:30 (Novotný)"
QUESTION      = 1                         # question number to download
DOWNLOAD_PATH = r"C:\Users\Захар\Desktop\tuke\bakalarska\fj_assignments\tasks\student_io\solutions"

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
STUDENTS_FILE = os.path.join(DOWNLOAD_PATH, "students.json")


def load_progress() -> dict:
    """Return {email: status} dict from a previous run, or empty dict."""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_progress(progress: dict) -> None:
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


def load_students() -> dict:
    """Return {email: metadata} dict from a previous run, or empty dict."""
    if os.path.exists(STUDENTS_FILE):
        with open(STUDENTS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_students(students: dict) -> None:
    with open(STUDENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(students, f, ensure_ascii=False, indent=2)


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


def scrape_task_metadata(driver: webdriver.Chrome, wait: WebDriverWait) -> dict:
    """
    Extract regex, automaton_type, and implementation_type from the question description.

    - automaton_type:      first sentence contains 'DFA' or 'NFA'
    - implementation_type: first sentence contains 'iteratívnu'/'iterative' or 'rekurzívnu'/'recursive'
    - regex:               a paragraph whose text-align is 'center', or the only
                           short (<60 chars) standalone <p> inside the question body,
                           falling back to a regex pattern scan of the full text
    """
    q_xpath = build_question_xpath(QUESTION)

    # ── Full question text for automaton/implementation detection ────────────
    try:
        question_div = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".qtext")
        ))
        full_text = question_div.text
    except TimeoutException:
        log.warning("  Could not locate question div for metadata scraping")
        return {"regex": None, "automaton_type": None, "implementation_type": None}

    first_sentence = full_text.split(".")[0]

    # automaton type
    if "NFA" in first_sentence:
        automaton_type = "NKA"
    elif "DFA" in first_sentence:
        automaton_type = "DKA"
    else:
        automaton_type = None
        log.warning("  Could not detect automaton type in: %s", first_sentence)

    # implementation type
    if any(kw in first_sentence.lower() for kw in ("rekurzívnu", "recursive", "rekurzivnu")):
        implementation_type = "recursive"
    elif any(kw in first_sentence.lower() for kw in ("iteratívnu", "iterative", "iterativnu")):
        implementation_type = "iterative"
    else:
        implementation_type = None
        log.warning("  Could not detect implementation type in: %s", first_sentence)

    # ── Regex: look for a centered <p> inside the question content ───────────
    regex = None
    try:
        # Moodle renders the centered line as a <p style="text-align:center"> or similar
        centered = driver.find_elements(
            By.XPATH,
            f"{q_xpath}//div[contains(@class,'qtext')]"
            f"//*[contains(@style,'center') or contains(@class,'text-center')]"
        )
        if centered:
            regex = centered[0].text.strip()

        # Fallback: find a short standalone paragraph (the regex line is typically <60 chars
        # and contains no spaces — it's the only such line in the question body)
        if not regex:
            paragraphs = driver.find_elements(By.XPATH, f"{q_xpath}//div[contains(@class,'qtext')]//p")
            for p in paragraphs:
                txt = p.text.strip()
                if txt and len(txt) < 60 and " " not in txt:
                    regex = txt
                    break

        # Last resort: scan full text for a token that looks like a formal regex
        # (contains special chars like {, }, |, *, + but no spaces)
        if not regex:
            for token in full_text.split():
                if any(c in token for c in ("{", "}", "|", "*", "+")) and len(token) < 60:
                    regex = token
                    break

    except Exception as exc:
        log.warning("  Regex scrape error: %s", exc)

    if regex:
        log.info("  Metadata → regex=%s  automaton=%s  impl=%s", regex, automaton_type, implementation_type)
    else:
        log.warning("  Could not extract regex from question text")

    return {
        "regex": regex,
        "automaton_type": automaton_type,
        "implementation_type": implementation_type,
    }


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
    students = load_students()
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

            # ── Scrape metadata FIRST, while the attempt page is open ────────
            metadata = scrape_task_metadata(driver, wait)

            downloaded = download_submission(driver, wait, email)

            if downloaded:
                status = "downloaded"
                metadata["status"] = "downloaded"
            else:
                log.info("  No attachment found — grading 0")
                grade_zero(driver, wait, parent)
                status = "no_submission"
                metadata["status"] = "no_submission"
                metadata["grade"]  = 0

            # ── Persist metadata and progress ────────────────────────────────
            students[email] = metadata
            save_students(students)

            progress[email] = status
            save_progress(progress)

            # ── Navigate back to the attempts list ───────────────────────────
            driver.execute_script("window.history.go(-1)")
            wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    except Exception as exc:
        log.exception("Fatal error: %s", exc)

    finally:
        driver.quit()   # closes the whole browser, not just the tab
        log.info("Done. Metadata saved to %s", STUDENTS_FILE)


if __name__ == "__main__":
    run()