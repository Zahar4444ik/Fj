from core.regex.frontend.lexer import Lexer
from core.regex.frontend.parser import Parser
from core.regex.generators.regex.random_regex import generate_regex


def get_ast_from_regex(regex_str=None):
    if regex_str is None:
        regex_str = generate_regex()

    lexer = Lexer(regex_str)
    parser = Parser(lexer)
    return parser.parse()
