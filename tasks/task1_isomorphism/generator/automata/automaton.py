# automaton.py
from collections import defaultdict


class Automaton:
    def __init__(self):
        self.states = set()
        self.annotations = {}
        self.start = None
        self.accepting = set()
        self.transitions = defaultdict(lambda: defaultdict(set))
        self.is_dfa = None
