from tasks.task1_isomorphism.checker.compare import compare
from core.regex.automata.dka.dka_builder import build_DKA
from tasks.task2_behavioral_testing.generator.nka.iterative import generate_iterative_nka
from core.regex.generators.random_regex import generate_valid_regex
from core.regex.frontend.lexer import Lexer
from core.regex.frontend.parser import Parser
from core.regex.automata.nka.nka_builder import build_NKA
from core.regex.generators.fsa_generator import fsa_from_nka, fsa_from_dka


def regex_to_fsa(regex_str):
    lexer = Lexer(regex_str)
    parser = Parser(lexer)
    ast = parser.parse()
    # print(ast)

    # Generate NKA
    nka = build_NKA(ast)
    fsa_from_nka(nka, filename="output/fsa/nka.fsa")
    generate_iterative_nka(ast)

    # Generate DKA
    dka, name_map, visual_map = build_DKA(ast, regex_str)
    fsa_from_dka(dka, name_map, visual_map, filename="output/fsa/dka.fsa")


if __name__ == "__main__":
    regex = generate_valid_regex()
    regex = '0|1{0|1}'
    print(f"Generated regex: {regex}")

    regex_to_fsa(regex)

    print(compare("output/fsa/test.fsa", "output/fsa/test2.fsa"))

