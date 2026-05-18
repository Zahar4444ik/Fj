
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
    def __init__(self):
        self.transition_table = {
            (State.q0, '0'): State.q1,
            (State.q0, '1'): State.q2,
            (State.q1, '1'): State.q0,
        }
        self.accepted_states = {
            State.q2,
        }
        self.init_state = State.q0
        self.actual_state = None

    def check(self, string: str) -> bool:
        self.actual_state = self.init_state

        for idx, symbol in enumerate(string):
            if (self.actual_state, symbol) not in self.transition_table:
                return False
            self.actual_state = self.transition_table[(self.actual_state, symbol)]

        return self.actual_state in self.accepted_states


if __name__ == "__main__":
    dfa = DFA()

    input_string = input("Zadaj vstupný reťazec> ")
    while input_string != "quit":
        print(
            f"Reťazec '{input_string}' "
            f"{'JE ' if dfa.check(input_string) else 'NIE JE '}akceptovaný!"
        )
        input_string = input("Zadaj vstupný reťazec> ")
