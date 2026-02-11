import random
import copy
import re
import xml.etree.ElementTree as ET

from core.regex.generators.random_regex import generate_valid_regex


# ---------------------------
# Your existing variable generator
# ---------------------------

def generate_assignment_variables(seed=None):
    random.seed(seed)

    automaton_type = random.choice(["NKA", "DKA"])
    implementation = random.choice(["iterative", "recursive"])

    regex = generate_valid_regex()  # <-- your function

    return {
        "regex": regex,
        "automaton_type": automaton_type,
        "implementation": implementation,
    }


# ---------------------------
# Load templates from XML
# ---------------------------

def load_templates(template_path: str) -> dict:
    tree = ET.parse(template_path)
    root = tree.getroot()

    templates = {}

    for question in root.findall("question"):
        name_node = question.find("name/text")
        if name_node is None:
            continue

        name = name_node.text.strip()

        if name == "dfa_iterative_template":
            templates["DKA_iterative"] = question
        elif name == "dfa_recursive_template":
            templates["DKA_recursive"] = question
        elif name == "nfa_iterative_template":
            templates["NKA_iterative"] = question
        elif name == "nfa_recursive_template":
            templates["NKA_recursive"] = question

    return templates


# ---------------------------
# Replace regex inside CDATA
# ---------------------------

def inject_regex(question_element: ET.Element, regex: str):
    questiontext = question_element.find("questiontext/text")
    if questiontext is None:
        return

    original = questiontext.text

    # Replace content inside $$ ... $$
    escaped = regex.replace("{", r"\{").replace("}", r"\}")
    updated = re.sub(r"\$\$.*?\$\$", f"$${escaped}$$", original, flags=re.DOTALL)

    questiontext.text = updated


# ---------------------------
# Main generator
# ---------------------------

def generate_moodle_xml(count: int, template_path: str, output_path: str):
    templates = load_templates(template_path)

    quiz = ET.Element("quiz")

    # Add category (copied manually once)
    category = ET.SubElement(quiz, "question", type="category")
    cat_node = ET.SubElement(category, "category")
    text = ET.SubElement(cat_node, "text")
    text.text = "$course$/top/generated_assignments"

    for i in range(count):
        assignment = generate_assignment_variables()

        key = f"{assignment['automaton_type']}_{assignment['implementation']}"
        template_question = templates[key]

        new_question = copy.deepcopy(template_question)

        inject_regex(new_question, assignment["regex"])

        # Set idnumber
        idnumber_node = new_question.find("idnumber")
        if idnumber_node is not None:
            idnumber_node.text = str(i)
        else:
            # If template doesn't contain idnumber (safety)
            idnumber_node = ET.SubElement(new_question, "idnumber")
            idnumber_node.text = str(i)

        quiz.append(new_question)

    tree = ET.ElementTree(quiz)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)

    print(f"Generated {count} questions → {output_path}")


if __name__ == "__main__":
    generate_moodle_xml(
        2,
        "output/templates.xml",
        "output/quiz.xml"
    )
