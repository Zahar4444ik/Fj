from core.assignment.assignment_description import get_assignment_description
from core.assignment.assignment_variables import generate_assignment_variables
from evaluation.fsa_evaluation import evaluate_fsa
from evaluation.implementation_evaluation import evaluate_iterative, evaluate_recursive
from core.regex.automata.dka.dka_builder import build_DKA
from core.regex.generators.random_regex import generate_valid_regex
from core.regex.frontend.lexer import Lexer
from core.regex.frontend.parser import Parser
from core.regex.automata.nka.nka_builder import build_NKA
from evaluation.report import AssignmentReport

RESULT_PATH = "output/results/assignment_report.txt"


def get_ast_from_regex(regex_str=None):
    if regex_str is None:
        regex_str = generate_valid_regex()
    # print(f"Using regex: {regex_str}")

    lexer = Lexer(regex)
    parser = Parser(lexer)
    ast = parser.parse()

    return ast


if __name__ == "__main__":
    report = AssignmentReport(RESULT_PATH)
    report.header("Automata Assignment – Evaluation Report")

    assignment_variables = generate_assignment_variables()
    assignment_description = get_assignment_description(assignment_variables)

    # report.section("Assignment Description")
    # report.add_info(assignment_description)

    regex = "0|1{0|1}"
    # automaton_type = assignment_variables["automaton_type"]
    automaton_type = "NKA"
    implementation = assignment_variables["implementation"]
    report.section("Configuration")
    report.add_info(f"Regex: {regex}")
    report.add_info(f"Automaton type: {automaton_type}")
    report.add_info(f"Implementation: {implementation}")

    ast = get_ast_from_regex(regex)

    score = 0

    if automaton_type == "NKA":
        nka = build_NKA(ast)
        score += evaluate_fsa(nka, automaton_type, report)

        if implementation == "iterative":
            score += evaluate_iterative(ast, automaton_type, report)
        else:
            score += evaluate_recursive(ast, automaton_type, report)

    else:
        dka = build_DKA(ast, regex)
        score += evaluate_fsa(dka, automaton_type, report)

        if implementation == "iterative":
            score += evaluate_iterative(ast, automaton_type, report)
        else:
            score += evaluate_recursive(ast, automaton_type, report)

    report.footer()
    report.save()

    # print("FINAL SCORE:", report.total_score)
    # print(f"Report saved to {RESULT_PATH}")
