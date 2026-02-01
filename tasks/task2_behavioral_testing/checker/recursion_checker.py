import ast


class RecursionChecker(ast.NodeVisitor):
    def __init__(self):
        self.errors = []
        self.in_main = False
        self.current_function = None
        self.functions = set()

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.functions.add(node.name)

        old = self.current_function
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = old

    def visit_If(self, node: ast.If):
        # if __name__ == "__main__":
        if (
            isinstance(node.test, ast.Compare)
            and isinstance(node.test.left, ast.Name)
            and node.test.left.id == "__name__"
            and isinstance(node.test.comparators[0], ast.Constant)
            and node.test.comparators[0].value == "__main__"
        ):
            old = self.in_main
            self.in_main = True
            for stmt in node.body:
                self.visit(stmt)
            self.in_main = old
            for stmt in node.orelse:
                self.visit(stmt)
        else:
            self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        if (
            not self.in_main
            and self.current_function
            and isinstance(node.func, ast.Name)
            and node.func.id in self.functions
        ):
            self.errors.append(
                f"Forbidden recursion: function '{self.current_function}' "
                f"calls '{node.func.id}' at line {node.lineno}"
            )
        self.generic_visit(node)
