# '{0}

from enum import Enum, auto


# ============================================================
# States of the DFA
# ============================================================
class State(Enum):
    q0 = auto()


class DFA:
    def __init__(self):
        self.transition_table = {
            (State.q0, '0'): State.q0,
        }
        self.accepted_states = {
            State.q0,
        }
        self.init_state = State.q0
        self.actual_state = None

    def check(self, string: str) -> bool:
        self.actual_state = self.init_state

        for symbol in string:
            if (self.actual_state, symbol) not in self.transition_table:
                return False
            self.actual_state = self.transition_table[(self.actual_state, symbol)]

        return self.actual_state in self.accepted_states
