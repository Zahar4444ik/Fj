import ast

FORBIDDEN_NODES = (
    ast.For,
    ast.While,
    ast.AsyncFor,
    ast.Break,
    ast.Continue,
    ast.ListComp,
    ast.SetComp,
    ast.DictComp,
    ast.GeneratorExp,
)


class IterationChecker(ast.NodeVisitor):
    def __init__(self):
        self.errors = []
        self.in_main = False

    def visit_If(self, node: ast.If):
        # Detect: if __name__ == "__main__":
        if (
            isinstance(node.test, ast.Compare)
            and isinstance(node.test.left, ast.Name)
            and node.test.left.id == "__name__"
            and len(node.test.comparators) == 1
            and isinstance(node.test.comparators[0], ast.Constant)
            and node.test.comparators[0].value == "__main__"
        ):
            old = self.in_main
            self.in_main = True
            for stmt in node.body:
                self.visit(stmt)
            self.in_main = old

            # Still visit else normally
            for stmt in node.orelse:
                self.visit(stmt)
        else:
            self.generic_visit(node)

    def generic_visit(self, node):
        if isinstance(node, FORBIDDEN_NODES) and not self.in_main:
            self.errors.append(
                f"Forbidden iteration construct {type(node).__name__} "
                f"at line {node.lineno}"
            )
        super().generic_visit(node)
