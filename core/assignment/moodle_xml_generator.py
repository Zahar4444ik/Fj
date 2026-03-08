import copy
import re
import xml.etree.ElementTree as ET

from core.assignment.assignment_variables import generate_assignment_variables
from core.config.settings_parse import CATEGORY


TEMPLATE_NAME_MAP = {
    "dfa_iterative_template": "dfa_iterative",
    "dfa_recursive_template": "dfa_recursive",
    "nfa_iterative_template": "nfa_iterative",
    "nfa_recursive_template": "nfa_recursive",
}


def load_templates(template_path: str) -> dict:
    tree = ET.parse(template_path)
    root = tree.getroot()

    templates = {}

    for question in root.findall("question"):
        name_node = question.find("name/text")
        if name_node is None or not name_node.text:
            continue

        key = TEMPLATE_NAME_MAP.get(name_node.text.strip())
        if key:
            templates[key] = question

    return templates


def escape_regex_for_moodle(regex: str) -> str:
    """
    Escape only LaTeX-sensitive characters inside $$...$$.
    """

    # Order matters: escape backslash first
    regex = regex.replace("\\", r"\textbackslash ")

    latex_special = ['{', '}', '_', '^', '$', '&', '%']

    for ch in latex_special:
        regex = regex.replace(ch, f"\\{ch}")

    return regex


def inject_regex(question_element: ET.Element, regex: str):
    questiontext = question_element.find("questiontext/text")
    if questiontext is None or not questiontext.text:
        return

    escaped = escape_regex_for_moodle(regex)

    updated = re.sub(
        r"\$\$.*?\$\$",
        f"$${escaped}$$",
        questiontext.text,
        flags=re.DOTALL,
    )

    questiontext.text = updated


def set_question_id(question_element: ET.Element, id_value: int):
    idnumber_node = question_element.find("idnumber")
    if idnumber_node is None:
        idnumber_node = ET.SubElement(question_element, "idnumber")
    idnumber_node.text = str(id_value)


def set_question_name(question_element: ET.Element, automaton_type: str, implementation: str, regex: str):
    """Set the question name to format: automaton_type_implementation_regex"""
    name_node = question_element.find("name/text")
    if name_node is None:
        name_elem = question_element.find("name")
        if name_elem is None:
            name_elem = ET.SubElement(question_element, "name")
        name_node = ET.SubElement(name_elem, "text")

    name_node.text = f"{automaton_type}_{implementation}_{regex}"


def generate_moodle_xml(count: int, template_path: str, output_path: str):
    templates = load_templates(template_path)

    quiz = ET.Element("quiz")

    # Add category
    category = ET.SubElement(quiz, "question", type="category")
    cat_node = ET.SubElement(category, "category")
    text = ET.SubElement(cat_node, "text")
    text.text = f"$course$/top/{CATEGORY}"

    for i in range(count):
        assignment = generate_assignment_variables()

        key = f"{assignment['automaton_type']}_{assignment['implementation']}"
        template_question = templates[key]

        new_question = copy.deepcopy(template_question)

        inject_regex(new_question, assignment["regex"])
        set_question_id(new_question, i)
        set_question_name(new_question, assignment['automaton_type'], assignment['implementation'], assignment['regex'])

        quiz.append(new_question)

    tree = ET.ElementTree(quiz)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)

    print(f"Generated {count} questions → {output_path}")
