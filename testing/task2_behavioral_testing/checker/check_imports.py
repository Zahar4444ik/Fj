import ast
import sys


ALLOWED_IMPORTS = [
    ("from", "enum", {"Enum", "auto"}),
]


def check_imports(filepath: str) -> list[str]:
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return [f"SyntaxError while parsing file: {e}"]

    errors = []

    for node in ast.walk(tree):
        # import something  /  import something as x
        if isinstance(node, ast.Import):
            for alias in node.names:
                errors.append(
                    f"Line {node.lineno}: forbidden import 'import {alias.name}'"
                )

        # from something import ...
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            names = {alias.name for alias in node.names}

            # Check against every allowed "from X import Y, Z" rule
            allowed = False
            for _, allowed_module, allowed_names in ALLOWED_IMPORTS:
                if module == allowed_module and names <= allowed_names:
                    allowed = True
                    break

            if not allowed:
                imported = ", ".join(sorted(names))
                errors.append(
                    f"Line {node.lineno}: forbidden import 'from {module} import {imported}'"
                )

    return errors
