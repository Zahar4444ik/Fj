from core.regex.frontend.lexer import Lexer
from core.regex.frontend.parser import Parser


def get_ast_from_regex(regex_str=None):
    lexer = Lexer(regex_str)
    parser = Parser(lexer)
    return parser.parse()
