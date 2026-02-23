
"""
============================================================
Rekurzívna implementácia nedeterministického konečného automatu
Automat je generovaný automaticky zo syntaxového stromu regexu.
============================================================
"""

from enum import Enum, auto


# ============================================================
# States of the DFA
# ============================================================
class State(Enum):
    q0 = auto()
    q1 = auto()
    q2 = auto()


class DFA:
    def __init__(self, transition_table: dict, accepted_states: set, init_state: State):
        self.transition_table = transition_table
        self.accepted_states = accepted_states
        self.init_state = init_state
        self.actual_state = None

    def check(self, string: str) -> bool:
        self.actual_state = self.init_state

        for idx, symbol in enumerate(string):
            if (self.actual_state, symbol) not in self.transition_table:
                return False
            self.actual_state = self.transition_table[(self.actual_state, symbol)]

        return self.actual_state in self.accepted_states


# ============================================================
# Transition table
# ============================================================
transition_table = {
    (State.q0, '0'): State.q2,
    (State.q0, '1'): State.q1,
    (State.q1, '0'): State.q1,
    (State.q1, '1'): State.q1,

}


# ============================================================
# Accepting states
# ============================================================
accepted_states = {
    State.q2,
    State.q1,
}

init_state = State.q0


dfa = DFA(
    transition_table=transition_table,
    accepted_states=accepted_states,
    init_state=init_state
)


if __name__ == "__main__":
    input_string = input("Zadaj vstupný reťazec> ")
    while input_string != "quit":
        print(
            f"Reťazec '{input_string}' "
            f"{'JE ' if dfa.check(input_string) else 'NIE JE '}akceptovaný!"
        )
        input_string = input("Zadaj vstupný reťazec> ")
