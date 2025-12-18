from isomorphism.automata.compare import compare
from regex.automata.dka.dka_builder import build_DKA
from regex.generate.generator import generate_valid_regex
from regex.frontend.lexer import Lexer
from regex.frontend.parser import Parser
from regex.automata.nka.nka_builder import build_NKA
from regex.io.exporter import export_to_fsa, export_dfa_to_fsa


def regex_to_fsa(regex_str):
    lexer = Lexer(regex_str)
    parser = Parser(lexer)
    ast = parser.parse()

    # Generate NKA
    nka = build_NKA(ast)
    export_to_fsa(nka, filename="output/fsa/nka.fsa")

    # Generate DKA
    dka, name_map, visual_map = build_DKA(ast, regex_str)
    export_dfa_to_fsa(dka, name_map, visual_map, filename="output/fsa/dka.fsa")


if __name__ == "__main__":
    regex = generate_valid_regex()
    regex = '0|1{0|1}'
    print(f"Generated regex: {regex}")

    regex_to_fsa(regex)

    print(compare("output/fsa/dka.fsa", "output/fsa/test.fsa"))

