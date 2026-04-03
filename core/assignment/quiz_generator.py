"""
Quiz Generator for Moodle

Generates Moodle-compatible XML quiz files with FSA assignment questions.
Each question is generated from a template with a randomly chosen regex pattern,
automaton type (DFA/NFA), and implementation approach (iterative/recursive).

Workflow:
  1. Load question templates from resources
  2. Generate random assignment variables (regex, automaton type, implementation)
  3. Create unique questions by injecting regexes into templates
  4. Write complete quiz to XML file in output directory
"""

import base64
import copy
import io
import logging
import re
import xml.etree.ElementTree as ET
import zipfile
from importlib import resources
from pathlib import Path

from core.assignment.assignment_variables import generate_assignment_variables
from core.config.settings_parse import CATEGORY, NUMBER_OF_QUESTIONS, REGEX_LATEX_FORMAT

# -------------------------------------------------------------------------------
# CONFIGURATION
# -------------------------------------------------------------------------------

OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent / "output"
OUTPUT_FILE = OUTPUT_DIR / "quiz.xml"

SKELETON_DIR = Path(__file__).resolve().parent.parent.parent / "graders" / "behavioral" / "skeletons"
SKELETON_SHARED_DIR = SKELETON_DIR / "shared"

# Mapping from template key to (skeleton subdirectory name, zip filename)
SKELETON_MAP = {
    "dfa_iterative": ("skeleton_dfa_iter", "skeleton_dfa_iter.zip"),
    "dfa_recursive": ("skeleton_dfa_rec", "skeleton_dfa_rec.zip"),
    "nfa_iterative": ("skeleton_nfa_iter", "skeleton_nfa_iter.zip"),
    "nfa_recursive": ("skeleton_nfa_rec", "skeleton_nfa_rec.zip"),
}

# Mapping from template question names to template keys
TEMPLATE_KEY_MAP = {
    "dfa_iterative_template": "dfa_iterative",
    "dfa_recursive_template": "dfa_recursive",
    "nfa_iterative_template": "nfa_iterative",
    "nfa_recursive_template": "nfa_recursive",
}

# -------------------------------------------------------------------------------
# LOGGING
# -------------------------------------------------------------------------------

logger = logging.getLogger(__name__)


# -------------------------------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------------------------------

def _build_skeleton_zip(skeleton_dir: Path) -> bytes:
    """Zip skeleton files plus the shared syntax checker into a flat archive.

    Archive layout:
        automaton.py, main.py, specification.fsa  ← skeleton-specific files
        check_syntax.py                            ← shared, self-contained syntax checker
    """
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in skeleton_dir.iterdir():
            if file.is_file():
                zf.write(file, arcname=file.name)
        zf.write(SKELETON_SHARED_DIR / "check_fsa_syntax.py", arcname="check_fsa_syntax.py")
    return buffer.getvalue()


def _update_skeleton_file(question_element: ET.Element, zip_name: str, zip_bytes: bytes) -> None:
    """Replace (or create) the <file> element inside <questiontext> with the given zip."""
    questiontext = question_element.find("questiontext")
    if questiontext is None:
        raise ValueError("Question element missing <questiontext>")

    file_elem = questiontext.find("file")
    if file_elem is None:
        file_elem = ET.SubElement(questiontext, "file")

    file_elem.set("name", zip_name)
    file_elem.set("path", "/")
    file_elem.set("encoding", "base64")
    file_elem.text = base64.b64encode(zip_bytes).decode("ascii")


def _load_templates() -> dict:
    traversable_path = resources.files("core.assignment.templates").joinpath("templates.xml")

    with traversable_path.open("r", encoding="utf-8") as f:
        tree = ET.parse(f)

    root = tree.getroot()
    templates = {}

    for question in root.findall("question"):
        name_node = question.find("name/text")
        if name_node is None or not name_node.text:
            continue

        key = TEMPLATE_KEY_MAP.get(name_node.text.strip())
        if key:
            templates[key] = question

    if not templates:
        raise ValueError("No valid templates found in templates.xml")

    return templates


def _escape_regex_for_latex(regex: str) -> str:
    # Escape backslash first (order matters!)
    regex = regex.replace("\\", r"\textbackslash ")

    latex_special_chars = ['{', '}', '_', '^', '$', '&', '%']
    for char in latex_special_chars:
        regex = regex.replace(char, f"\\{char}")

    return regex


def _apply_regex_to_question(question_element: ET.Element, regex: str) -> None:
    questiontext = question_element.find("questiontext/text")
    if questiontext is None or not questiontext.text:
        raise ValueError("Question element missing questiontext/text")

    if REGEX_LATEX_FORMAT:
        replacement = f"$${_escape_regex_for_latex(regex)}$$"
    else:
        replacement = regex

    updated = re.sub(r"\$\$.*?\$\$", replacement, questiontext.text, flags=re.DOTALL)

    if updated == questiontext.text:
        raise ValueError(f"No LaTeX placeholder found in question template for regex: {regex}")

    questiontext.text = updated


def _set_question_id(question_element: ET.Element, question_id: int) -> None:
    idnumber_node = question_element.find("idnumber")
    if idnumber_node is None:
        idnumber_node = ET.SubElement(question_element, "idnumber")
    idnumber_node.text = str(question_id)


def _set_question_name(
    question_element: ET.Element,
    automaton_type: str,
    implementation: str,
    regex: str
) -> None:
    name_node = question_element.find("name/text")
    if name_node is None:
        name_elem = question_element.find("name")
        if name_elem is None:
            name_elem = ET.SubElement(question_element, "name")
        name_node = ET.SubElement(name_elem, "text")

    name_node.text = f"{automaton_type}_{implementation}_{regex}"


def _ensure_output_directory() -> None:
    """Create output directory if it doesn't exist."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Output directory ready: {OUTPUT_DIR}")


def _build_category_element(path: str) -> ET.Element:
    """
    Build a single Moodle category <question type="category"> element
    for the given full path, e.g. '$course$/top/Zapoctovka A/prakticka cast'.
    """
    category_q = ET.Element("question", type="category")

    category_node = ET.SubElement(category_q, "category")
    text = ET.SubElement(category_node, "text")
    text.text = path

    info = ET.SubElement(category_q, "info", format="html")
    ET.SubElement(info, "text")

    ET.SubElement(category_q, "idnumber")

    return category_q


def _build_category_elements(category: str) -> list[ET.Element]:
    """
    Build one category <question> element per path segment.

    A plain string like "Zapoctovka A" produces one element:
        $course$/top/Zapoctovka A

    A path like "Zapoctovka A/prakticka cast" produces two elements:
        $course$/top/Zapoctovka A
        $course$/top/Zapoctovka A/prakticka cast
    """
    segments = category.strip("/").split("/")
    elements = []
    for i in range(1, len(segments) + 1):
        path = "$course$/top/" + "/".join(segments[:i])
        elements.append(_build_category_element(path))
    return elements


def _build_quiz_xml(templates: dict, question_count: int) -> ET.Element:
    quiz = ET.Element("quiz")

    # Add category hierarchy — one element per path segment
    for category_element in _build_category_elements(CATEGORY):
        quiz.append(category_element)

    # Generate and add questions
    for i in range(question_count):
        assignment_vars = generate_assignment_variables()

        template_key = f"{assignment_vars['automaton_type']}_{assignment_vars['implementation']}"
        if template_key not in templates:
            logger.error(f"Template not found for: {template_key}")
            raise ValueError(f"Unknown automaton/implementation combination: {template_key}")

        template_question = templates[template_key]
        new_question = copy.deepcopy(template_question)

        # Embed fresh skeleton zip
        skeleton_subdir, zip_name = SKELETON_MAP[template_key]
        zip_bytes = _build_skeleton_zip(SKELETON_DIR / skeleton_subdir)
        _update_skeleton_file(new_question, zip_name, zip_bytes)

        # Apply assignments to question
        _apply_regex_to_question(new_question, assignment_vars["regex"])
        _set_question_id(new_question, i)
        _set_question_name(
            new_question,
            assignment_vars['automaton_type'],
            assignment_vars['implementation'],
            assignment_vars['regex']
        )

        quiz.append(new_question)

    return quiz


def _write_quiz_to_file(quiz_element: ET.Element, output_path: Path) -> None:
    tree = ET.ElementTree(quiz_element)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    logger.info(f"Quiz file written: {output_path}")


# -------------------------------------------------------------------------------
# PUBLIC API
# -------------------------------------------------------------------------------

def generate_quiz() -> None:
    try:
        # Step 1: Prepare output directory
        _ensure_output_directory()

        # Step 2: Load templates
        templates = _load_templates()
        logger.info(f"Loaded {len(templates)} question templates")

        # Step 3: Build quiz
        quiz_count = NUMBER_OF_QUESTIONS
        quiz_xml = _build_quiz_xml(templates, quiz_count)
        logger.info(f"Generated quiz structure with {quiz_count} questions")

        # Step 4: Write to file
        _write_quiz_to_file(quiz_xml, OUTPUT_FILE)

    except Exception as e:
        logger.error(f"Quiz generation failed: {e}", exc_info=True)
        raise
