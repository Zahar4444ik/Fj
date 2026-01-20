# "0"

from enum import Enum, auto


class State(Enum):
    q0 = auto()
    q1 = auto()


class NFA:
    def __init__(self, transition_table, accepted_states, init_state):
        self.transition_table = transition_table
        self.accepted_states = accepted_states
        self.init_state = init_state
        self.stack = None

    def expand_actual_configuration(self, actual_state, string):
        if string != "" and (actual_state, string[0]) in self.transition_table:
            for s in self.transition_table[(actual_state, string[0])]:
                self.stack.append((s, string[1:]))

    def check(self, string):
        self.stack = [(self.init_state, string)]
        visited = set()

        while self.stack:
            state, rest = self.stack.pop()
            if (state, rest) in visited:
                continue
            visited.add((state, rest))

            if state in self.accepted_states and rest == "":
                return True

            self.expand_actual_configuration(state, rest)
        return False


transition_table = {
    (State.q0, '0'): {State.q1},
}

accepted_states = {State.q1}
init_state = State.q0

nfa = NFA(transition_table, accepted_states, init_state)
