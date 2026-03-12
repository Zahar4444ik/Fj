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

import copy
import logging
import re
import xml.etree.ElementTree as ET
from importlib import resources
from pathlib import Path

from core.assignment.assignment_variables import generate_assignment_variables
from core.config.settings_parse import CATEGORY, NUMBER_OF_QUESTIONS
from core.config.validation import validate_all_settings

# -------------------------------------------------------------------------------
# CONFIGURATION
# -------------------------------------------------------------------------------

OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent / "output"
OUTPUT_FILE = OUTPUT_DIR / "quiz.xml"

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

    escaped_regex = _escape_regex_for_latex(regex)

    updated = re.sub(
        r"\$\$.*?\$\$",
        f"$${escaped_regex}$$", # Finds the LaTeX placeholder ($$...$$) in the question text
        questiontext.text,
        flags=re.DOTALL,
    )

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


def _build_quiz_xml(templates: dict, question_count: int) -> ET.Element:
    quiz = ET.Element("quiz")

    # Add category definition
    category = ET.SubElement(quiz, "question", type="category")
    cat_node = ET.SubElement(category, "category")
    text = ET.SubElement(cat_node, "text")
    text.text = f"$course$/top/{CATEGORY}"

    # Generate and add questions
    for i in range(question_count):
        assignment_vars = generate_assignment_variables()

        template_key = f"{assignment_vars['automaton_type']}_{assignment_vars['implementation']}"
        if template_key not in templates:
            logger.error(f"Template not found for: {template_key}")
            raise ValueError(f"Unknown automaton/implementation combination: {template_key}")

        template_question = templates[template_key]
        new_question = copy.deepcopy(template_question)

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
