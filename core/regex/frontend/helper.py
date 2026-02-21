from core.regex.frontend.lexer import Lexer
from core.regex.frontend.parser import Parser


def get_ast_from_regex(regex_str=None):
    lexer = Lexer(regex_str)
    parser = Parser(lexer)
    return parser.parse()


def regex_from_tree(node: dict) -> str:
    node_type = node.get("type")

    if node_type == "symbol":
        value = node.get("value", "")
        return "" if value.startswith("<") else value

    if node_type in ("regular", "sequence"):
        return "".join(regex_from_tree(child) for child in node.get("children", []))

    if node_type == "alternative":
        branches = [
            regex_from_tree(child)
            for child in node.get("children", [])
            if child.get("type") != "symbol"
        ]
        return "|".join(branches)

    if node_type == "element":
        children = node.get("children", [])
        if len(children) >= 3:
            first = children[0].get("value", "")
            inner = regex_from_tree(children[1])
            if first == "<LBRACE>":
                return f"{{{inner}}}"
            if first == "<LBRACKET>":
                return f"[{inner}]"
            if first == "<LPAREN>":
                return f"({inner})"
        return "".join(regex_from_tree(child) for child in children)

    return ""


if __name__ == "__main__":
    test_regex = "{$|8}e[D|e~]"
    ast = get_ast_from_regex(test_regex)
    print(ast)
    reconstructed = regex_from_tree(ast)
    print(reconstructed)