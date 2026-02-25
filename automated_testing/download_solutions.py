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
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# ─────────────────────────── CONFIGURATION ───────────────────────────────────

USERNAME        = ""                   # TUKE login e.g. "FL123XX"
PASSWORD        = ""                   # TUKE password
ASSIGNMENT_LINK = "https://moodle.fei.tuke.sk/mod/quiz/view.php?id=14339"
STUDENT_GROUP   = "Všetci účastníci"  # or e.g. "01 Pondelok 07:30 (Novotný)"
QUESTION        = 1                    # question number to download
DOWNLOAD_PATH   = r"C:\Users\Захар\Desktop\tuke\bakalarska\fj_assignments\tasks\student_io\solutions"

DOWNLOAD_TIMEOUT = 30  # seconds to wait for a .zip to appear on disk

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

# ─────────────────────────── STUDENTS.JSON ───────────────────────────────────

STUDENTS_FILE = os.path.join(DOWNLOAD_PATH, "students.json")


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


def scrape_task_metadata(driver: webdriver.Chrome, wait: WebDriverWait) -> dict:
    """
    Extract regex, automaton_type, and implementation_type from the question text.

    - automaton_type:      first sentence contains 'DFA'/'NFA' → mapped to 'DKA'/'NKA'
    - implementation_type: first sentence contains iterative/recursive keyword
    - regex:               centered paragraph (3-stage fallback)
    """
    try:
        question_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".qtext")))
        full_text = question_div.text
    except NoSuchElementException:
        log.warning("  Could not locate .qtext for metadata scraping")
        return {"regex": None, "automaton_type": None, "implementation_type": None}

    first_sentence = full_text.split(".")[0]

    # ── Automaton type ────────────────────────────────────────────────────────
    if "NFA" in first_sentence or "NKA" in first_sentence:
        automaton_type = "NKA"
    elif "DFA" in first_sentence or "DKA" in first_sentence:
        automaton_type = "DKA"
    else:
        automaton_type = None
        log.warning("  Could not detect automaton type in: %s", first_sentence)

    # ── Implementation type ───────────────────────────────────────────────────
    if any(kw in first_sentence.lower() for kw in ("rekurzívnu", "recursive", "rekurzivnu")):
        implementation_type = "recursive"
    elif any(kw in first_sentence.lower() for kw in ("iteratívnu", "iterative", "iterativnu")):
        implementation_type = "iterative"
    else:
        implementation_type = None
        log.warning("  Could not detect implementation type in: %s", first_sentence)

    # ── Regex (3-stage fallback) ──────────────────────────────────────────────
    regex = None
    try:
        q_xpath = build_question_xpath(QUESTION)

        # Stage 1: centered element inside question body
        centered = driver.find_elements(
            By.XPATH,
            f"{q_xpath}//*[contains(@style,'center') or contains(@class,'text-center')]"
        )
        if centered:
            regex = centered[0].text.strip() or None

        # Stage 2: short space-free <p> — regex expressions have no spaces
        if not regex:
            for p in driver.find_elements(By.XPATH, f"{q_xpath}//p"):
                txt = p.text.strip()
                if txt and len(txt) < 60 and " " not in txt:
                    regex = txt
                    break

        # Stage 3: token in full text containing regex special characters
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
    driver.get("https://moodle.fei.tuke.sk/login/index.php")
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


def open_attempt_detail(driver: webdriver.Chrome, idx: int) -> None:
    driver.find_element(
        By.XPATH,
        f"//tbody/tr[@class='gradedattempt' or @class='']"
        f"[@id='mod-quiz-report-overview-report_r{idx}']/td[3]/a[2]"
    ).click()


def download_submission(driver: webdriver.Chrome, email: str) -> bool:
    """Try to find and download the .zip attachment. Returns True on success."""
    q_xpath = build_question_xpath(QUESTION)
    attachment_xpath = f"{q_xpath}//div[@class='attachments']//a"

    try:
        link_elem = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, attachment_xpath))
        )
        file_name    = link_elem.text.strip()
        download_url = link_elem.get_attribute("href")

        driver.get(download_url)

        original_path = os.path.join(DOWNLOAD_PATH, file_name)
        final_path    = os.path.join(DOWNLOAD_PATH, f"{email}.zip")

        if wait_for_file(original_path):
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


# ─────────────────────────── MAIN LOOP ───────────────────────────────────────

def run() -> None:
    os.makedirs(DOWNLOAD_PATH, exist_ok=True)

    students = load_students()
    log.info("Loaded %d previously processed students from students.json.", len(students))

    driver = create_driver()
    wait   = WebDriverWait(driver, 20)

    try:
        login(driver, wait)
        total  = open_attempts_page(driver, wait)
        parent = driver.current_window_handle

        for idx in range(total):
            email = get_student_email(driver, wait, idx)

            # ── Resume: skip students already in students.json ───────────────
            if email in students:
                log.info("[%d/%d] Skipping %s (already done: %s)", idx + 1, total, email, students[email].get("status"))
                continue

            log.info("[%d/%d] Processing %s", idx + 1, total, email)
            open_attempt_detail(driver, idx)

            metadata = scrape_task_metadata(driver, wait)
            downloaded = download_submission(driver, email)

            if downloaded:
                metadata["status"] = "downloaded"
            else:
                log.info("  No attachment found — grading 0")
                metadata["status"] = "no_submission"

            # ── Save immediately so a crash mid-run is resumable ─────────────
            students[email] = metadata
            save_students(students)

            driver.execute_script("window.history.go(-1)")
            wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    except Exception as exc:
        log.exception("Fatal error: %s", exc)

    finally:
        driver.quit()
        log.info("Done. students.json saved to %s", STUDENTS_FILE)


if __name__ == "__main__":
    run()