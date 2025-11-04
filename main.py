from regex.generator import generate_valid_regex
from regex.lexer import Lexer
from regex.parser import Parser
from regex.nka.nka_builder import build_NKA, export_to_fsa
from regex.nka.nka_generator import generate_nka_py_file


def regex_to_fsa(regex_str):
    lexer = Lexer(regex_str)
    parser = Parser(lexer)
    ast = parser.parse()
    nka = build_NKA(ast)
    # generate_nka_py_file(ast)
    export_to_fsa(nka, filename="output/output.fsa")
    return nka


if __name__ == "__main__":
    regex = generate_valid_regex()
    print(f"Generated regex: {regex}")

    nka = regex_to_fsa(regex)
    print(f"Built NKA for: {regex}")

