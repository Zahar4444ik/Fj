def parser_ast_to_regex_ast(parser_tree):
    """
    Convert the parser AST dict (from your parser.py) to a normalized regex AST.
    Normalized node types: 'symbol', 'concat', 'union', 'star', 'optional'.
    """

    # --- Step 1: ensure root is regular
    if parser_tree["type"] != "regular":
        raise ValueError("Expected 'regular' root node")

    alt_node = parser_tree["children"][0]  # 'alternative'
    if alt_node["type"] != "alternative":
        raise ValueError("Expected 'alternative' child under 'regular'")

    return _convert_alternative(alt_node)


def _convert_alternative(node):
    """Convert 'alternative' node to chain of unions."""
    children = node["children"]
    parts = []
    current_seq = None
    for child in children:
        if child["type"] == "symbol" and child["value"] == "<PIPE>":
            continue
        if child["type"] == "sequence":
            parts.append(_convert_sequence(child))

    # multiple parts => chain them with union
    if not parts:
        raise ValueError("Empty alternative")
    expr = parts[0]
    for right in parts[1:]:
        expr = {"type": "union", "left": expr, "right": right}
    return expr


def _convert_sequence(node):
    """Convert 'sequence' node to chain of concats."""
    elements = [_convert_element(el) for el in node["children"] if el["type"] == "element"]
    if not elements:
        raise ValueError("Empty sequence")
    expr = elements[0]
    for right in elements[1:]:
        expr = {"type": "concat", "left": expr, "right": right}
    return expr


def _convert_element(node):
    """Convert 'element' node to its corresponding operation."""
    children = node["children"]
    if not children:
        raise ValueError("Empty element")

    first = children[0]

    # Plain symbol
    if first["type"] == "symbol" and first["value"].startswith("<SYMBOL"):
        symbol_val = first["value"][len("<SYMBOL,"):-1]  # extract real symbol
        return {"type": "symbol", "value": symbol_val}

    # Literal symbol like 'a' (without <SYMBOL,> format)
    if first["type"] == "symbol" and not first["value"].startswith("<"):
        return {"type": "symbol", "value": first["value"]}

    # Bracketed/grouped forms
    if first["type"] == "symbol":
        token = first["value"]
        if token == "<LPAREN>":   # ( regular )
            inner = children[1]
            return parser_ast_to_regex_ast(inner)
        elif token == "<LBRACE>":  # { regular }  → star
            inner = children[1]
            return {"type": "star", "child": parser_ast_to_regex_ast(inner)}
        elif token == "<LBRACKET>":  # [ regular ] → optional
            inner = children[1]
            return {"type": "optional", "child": parser_ast_to_regex_ast(inner)}

    raise ValueError(f"Unhandled element node: {node}")


if __name__ == "__main__":
    # Example parser AST for regex: a | b{c|d}
    parser_ast = {
        'type': 'regular',
        'children': [{
            'type': 'alternative',
            'children': [
                {'type': 'sequence', 'children': [
                    {'type': 'element', 'children': [
                        {'type': 'symbol', 'value': 'a'}
                    ]}
                ]},
                {'type': 'symbol', 'value': '<PIPE>'},
                {'type': 'sequence', 'children': [
                    {'type': 'element', 'children': [
                        {'type': 'symbol', 'value': 'b'}
                    ]}
                ]}
            ]
        }]
    }

    regex_ast = parser_ast_to_regex_ast(parser_ast)
    import pprint
    pprint.pprint(regex_ast)

    print(regex_ast)