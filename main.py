from core.assignment.assignment_description import get_assignment_description
from core.assignment.assignment_variables import generate_assignment_variables
from core.config.scoring import TITLE
from core.config.validation import validate_scoring_profile
from core.regex.generators.random_regex import generate_regex
from core.evaluation.fsa_evaluation import evaluate_fsa
from core.evaluation.implementation_evaluation import evaluate_implementation
from core.regex.automata.dka.dka_builder import build_DKA
from core.regex.automata.nka.nka_builder import build_NKA
from core.regex.frontend.lexer import Lexer
from core.regex.frontend.parser import Parser
from core.evaluation.report import AssignmentReport

RESULT_PATH = "output/results/assignment_report.txt"

AUTOMATON_BUILDERS = {
    "DKA": lambda ast, regex: build_DKA(ast, regex),
    "NKA": lambda ast, regex: build_NKA(ast),
}


def get_ast_from_regex(regex_str=None):
    if regex_str is None:
        regex_str = generate_regex()

    lexer = Lexer(regex_str)
    parser = Parser(lexer)
    return parser.parse()


if __name__ == "__main__":
    validate_scoring_profile()

    report = AssignmentReport(RESULT_PATH)
    report.header(TITLE, "zakhar.fesiuk@student.tuke.sk")

    assignment_variables = generate_assignment_variables()
    assignment_description = get_assignment_description(assignment_variables)

    # regex = assignment_variables["regex"]
    regex = "0|1{0|1}"  # Hardcoded for testing purposes

    # automaton_type = assignment_variables["automaton_type"]
    automaton_type = "NKA"  # Hardcoded for testing purposes

    # implementation = assignment_variables["implementation"]
    implementation = "iterative"  # Hardcoded for testing purposes

    report.add_info("Configuration")
    report.add_info("-" * 60)
    report.add_info(f"Regex: {regex}")
    report.add_info(f"Automaton type: {automaton_type}")
    report.add_info(f"Implementation: {implementation}")

    ast = get_ast_from_regex(regex)
    automaton = AUTOMATON_BUILDERS[automaton_type](ast, regex)

    score = 0.0
    score += evaluate_fsa(automaton, automaton_type, report)
    score += evaluate_implementation(ast, automaton_type, implementation, report)

    report.footer(score)
    report.save()
