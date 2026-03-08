import ast


class RecursionChecker(ast.NodeVisitor):
    def __init__(self):
        self.functions = set()
        self.call_graph = {}
        self.call_lines = {}

        self.current_function = None
        self.current_class = None
        self.in_main = False

        self.errors = []
        self.pass_num = 0
        self.tree = None

    # ------------------------
    # Helpers
    # ------------------------

    def full_name(self, name):
        if self.current_class:
            return f"{self.current_class}.{name}"
        return name

    # ------------------------
    # AST visitors
    # ------------------------

    def visit_ClassDef(self, node):
        old = self.current_class
        self.current_class = node.name

        self.generic_visit(node)

        self.current_class = old

    def visit_FunctionDef(self, node):
        name = self.full_name(node.name)

        self.functions.add(name)
        self.call_graph.setdefault(name, set())

        old = self.current_function
        self.current_function = name

        self.generic_visit(node)

        self.current_function = old

    def visit_If(self, node):
        # ignore main section
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

    def visit_Call(self, node):
        if self.in_main or not self.current_function:
            self.generic_visit(node)
            return

        target = None

        # foo()
        if isinstance(node.func, ast.Name):
            name = node.func.id
            if name in self.functions:
                target = name

        # self.foo()
        elif isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name) and node.func.value.id == "self":
                name = node.func.attr
                full = f"{self.current_class}.{name}"

                if full in self.functions:
                    target = full

        if target:
            self.call_graph[self.current_function].add(target)
            self.call_lines[(self.current_function, target)] = node.lineno

        self.generic_visit(node)

    def visit(self, node):
        """Override visit to implement two-pass approach on the root node"""
        # First pass: collect all function names
        if self.pass_num == 0 and isinstance(node, ast.Module):
            self.pass_num = 1
            self._collect_functions(node)
            self.pass_num = 2

        # Second pass: build call graph
        return super().visit(node)

    def _collect_functions(self, node):
        """Pre-pass to collect all function names in the tree"""
        for child in ast.walk(node):
            if isinstance(child, ast.FunctionDef):
                # Handle class methods
                for parent in ast.walk(node):
                    if isinstance(parent, ast.ClassDef):
                        for item in parent.body:
                            if item == child:
                                name = f"{parent.name}.{child.name}"
                                self.functions.add(name)
                                self.call_graph.setdefault(name, set())
                                break
                        else:
                            continue
                        break
                else:
                    # Not in a class, it's a module-level function
                    self.functions.add(child.name)
                    self.call_graph.setdefault(child.name, set())

    # ------------------------
    # Recursion detection
    # ------------------------

    def detect_recursion(self):
        """Detect all cycles using DFS with per-path visited tracking"""
        visited_global = set()

        def dfs(func, stack, visited_path):
            """
            DFS to detect cycles.
            - stack: current path being explored
            - visited_path: nodes visited in current path
            """
            if func in visited_path:
                # Found a cycle
                cycle = stack[stack.index(func) :] + [func]
                self.report_cycle(cycle)
                return

            if func in visited_global:
                # Already fully explored this branch
                return

            visited_path.add(func)
            stack.append(func)

            for nxt in self.call_graph.get(func, []):
                dfs(nxt, stack, visited_path)

            stack.pop()
            visited_path.remove(func)
            visited_global.add(func)

        for f in self.functions:
            if f not in visited_global:
                dfs(f, [], set())

    def report_cycle(self, cycle):
        path = " -> ".join(cycle)

        lines = []
        for a, b in zip(cycle, cycle[1:]):
            line = self.call_lines.get((a, b))
            if line:
                lines.append(f"{a} calls {b} at line {line}")

        msg = f"Recursion detected: {path}"
        if lines:
            msg += "\n  " + "\n  ".join(lines)

        self.errors.append(msg)
