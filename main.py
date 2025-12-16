from regex.dka.dka_builder import build_DKA
from regex.generator import generate_valid_regex
from regex.lexer import Lexer
from regex.parser import Parser
from regex.nka.nka_builder import build_NKA
from regex.exporter import export_to_fsa, export_dfa_to_fsa


def regex_to_fsa(regex_str):
    lexer = Lexer(regex_str)
    parser = Parser(lexer)
    ast = parser.parse()

    # Generate NKA
    nka = build_NKA(ast)
    export_to_fsa(nka, filename="output/nka.fsa")

    # Generate DKA
    dka, name_map, visual_map = build_DKA(ast, regex_str)
    export_dfa_to_fsa(dka, name_map, visual_map, filename="output/dka.fsa")

    return nka


if __name__ == "__main__":
    regex = generate_valid_regex()
    regex = '0|1{0|1}'
    print(f"Generated regex: {regex}")

    nka = regex_to_fsa(regex)

