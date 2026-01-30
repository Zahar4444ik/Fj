from collections import defaultdict


class Automaton:
    def __init__(self):
        self.states = set()
        self.annotations = {}
        self.start = None
        self.accepting = set()
        self.transitions = defaultdict(lambda: defaultdict(set))
        self.is_dfa = None

    def format_annotation_diff(self, other) -> str:
        lines = [
            "State   Expected                    Received",
            "-" * 60
        ]

        for state in sorted(self.annotations):
            exp = self.annotations.get(state, "")
            got = other.annotations.get(state, "")
            if exp != got:
                lines.append(f"{state:<6} {exp:<27} {got}")

        return "\n".join(lines)
