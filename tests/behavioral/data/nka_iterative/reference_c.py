
"""
============================================================
Rekurzívna implementácia nedeterministického konečného automatu
Automat je generovaný automaticky zo syntaxového stromu regexu.
============================================================
"""

from enum import Enum, auto


# ============================================================
# States of the NFA
# ============================================================
class State(Enum):
    q0 = auto()
    q1 = auto()
    q2 = auto()
    q3 = auto()
    q4 = auto()


class NFA:
    def __init__(self):
        self.transition_table = {
            (State.q0, 'eps'): {State.q1, State.q3},
            (State.q1, '1'): {State.q2},
            (State.q3, '0'): {State.q4},
            (State.q4, 'eps'): {State.q1, State.q3},
        }
        self.accepted_states = {
            State.q2,
        }
        self.init_state = State.q0
        self.stack = None

    def expand_actual_configuration(self, actual_state: State, string: str) -> None:
        # Transition by input symbol
        if string != "" and (actual_state, string[0]) in self.transition_table:
            for state in self.transition_table[(actual_state, string[0])]:
                self.stack.append((state, string[1:]))

        # Epsilon transitions
        if (actual_state, "eps") in self.transition_table:
            for state in self.transition_table[(actual_state, "eps")]:
                self.stack.append((state, string))

    def check(self, string: str) -> bool:
        self.stack = [(self.init_state, string)]
        visited = set()

        while self.stack:
            actual_state, string_rest = self.stack.pop()

            if (actual_state, string_rest) in visited:
                continue
            visited.add((actual_state, string_rest))

            if actual_state in self.accepted_states and string_rest == "":
                return True

            self.expand_actual_configuration(actual_state, string_rest)

        return False


nfa = NFA()


if __name__ == "__main__":
    input_string = input ("Zadaj vstupný reťazec> ")
    while input_string != "quit":
        print (f"Reťazec '{ input_string }' " 
               f"{'JE ' if nfa.check(input_string) else 'NIE JE '}akceptovaný!")
        input_string = input ("Zadaj vstupný reťazec> ")
