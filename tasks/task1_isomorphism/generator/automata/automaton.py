from collections import defaultdict


class Automaton:
    def __init__(self):
        self.states = set()
        self.annotations = {}
        self.start = None
        self.accepting = set()
        self.transitions = defaultdict(lambda: defaultdict(set))
        self.is_dfa = None

    def annotations_as_string(self):
        lines = []
        for state in sorted(self.states):
            annotation = self.annotations.get(state, "")
            lines.append(f"\t{state} = '{annotation}'")
        return "\n".join(lines)