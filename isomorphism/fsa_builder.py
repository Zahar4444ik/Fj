from collections import defaultdict
from gen.FSAListener import FSAListener
from collections import deque


class Automaton:
    def __init__(self):
        self.is_dfa = True
        self.states = set()
        self.annotations = {}
        self.start = None
        self.accepting = set()
        self.transitions = defaultdict(lambda: defaultdict(set))


def is_dfa(automaton):
    for src in automaton.transitions:
        for sym, targets in automaton.transitions[src].items():
            if sym == 'ε':
                return False
            if len(targets) != 1:
                return False
    return True


def print_automaton(a):
    print("States:", a.states)
    print("Start:", a.start)
    print("Accepting:", a.accepting)
    print("Transitions:")
    for s in sorted(a.transitions):
        for sym, tgts in a.transitions[s].items():
            print(f"  {s} -{sym}-> {tgts}")


class FSABuilder(FSAListener):
    def __init__(self):
        self.automaton = Automaton()

    def exitStateEntry(self, ctx):
        state = ctx.ID().getText()
        self.automaton.states.add(state)

    def exitStart(self, ctx):
        self.automaton.start = ctx.ID().getText()

    def exitAccepting(self, ctx):
        for id_ctx in ctx.ID():
            self.automaton.accepting.add(id_ctx.getText())

    def exitTransition(self, ctx):
        src = ctx.ID(0).getText()
        sym = ctx.symbol().getText()
        dst = ctx.ID(1).getText()

        self.automaton.transitions[src][sym].add(dst)


# Ensure states from transitions are included
def normalize_states(automaton):
    for src in automaton.transitions:
        automaton.states.add(src)
        for sym in automaton.transitions[src]:
            automaton.states |= automaton.transitions[src][sym]


# Find all reachable states from the start state
def reachable_states(automaton):
    visited = set()
    queue = deque([automaton.start])

    while queue:
        s = queue.popleft()
        if s in visited:
            continue
        visited.add(s)

        for targets in automaton.transitions.get(s, {}).values():
            queue.extend(targets)

    return visited