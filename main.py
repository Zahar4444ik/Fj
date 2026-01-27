from core.assignment.assignment_description import get_assignment_description
from core.assignment.assignment_variables import generate_assignment_variables
from evaluation.fsa_evaluation import evaluate_fsa
from evaluation.implementation_evaluation import evaluate_iterative, evaluate_recursive
from core.regex.automata.dka.dka_builder import build_DKA
from core.regex.generators.random_regex import generate_valid_regex
from core.regex.frontend.lexer import Lexer
from core.regex.frontend.parser import Parser
from core.regex.automata.nka.nka_builder import build_NKA


def get_ast_from_regex(regex_str=None):
    if regex_str is None:
        regex_str = generate_valid_regex()
    print(f"Using regex: {regex_str}")

    lexer = Lexer(regex)
    parser = Parser(lexer)
    ast = parser.parse()

    return ast


if __name__ == "__main__":
    assignment_variables = generate_assignment_variables()

    assignment_description = get_assignment_description(assignment_variables)

    # regex = assignment_variables["regex"]
    regex = "0|1{0|1}"
    automaton_type = assignment_variables["automaton_type"]
    # automaton_type = "NKA"
    implementation = assignment_variables["implementation"]
    # implementation = "recursive"

    ast = get_ast_from_regex()

    score = 0

    if automaton_type == "NKA":
        nka = build_NKA(ast)

        # FSA
        score += evaluate_fsa(nka, automaton_type)

        # Implementation
        if implementation == "iterative":
            score += evaluate_iterative(ast, automaton_type)
        else:
            score += evaluate_recursive(ast, automaton_type)

    else:
        dka = build_DKA(ast, regex)

        # FSA
        score += evaluate_fsa(dka, automaton_type)

        # Implementation
        if implementation == "iterative":
            score += evaluate_iterative(ast, automaton_type)

        else:
            score += evaluate_recursive(ast, automaton_type)

    print("FINAL SCORE:", score)