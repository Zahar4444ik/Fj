from enum import Enum, auto


# ============================================================
# States of the NFA
# ============================================================
class State(Enum):
    q0 = auto()
    q1 = auto()
    q10 = auto()
    q11 = auto()
    q12 = auto()
    q2 = auto()
    q3 = auto()
    q4 = auto()
    q5 = auto()
    q6 = auto()
    q7 = auto()
    q8 = auto()
    q9 = auto()


class NFA:
    def __init__(self):
        self.transition_table = {
            (State.q0, 'j'): {State.q1},
            (State.q1, 'eps'): {State.q2},
            (State.q10, 'eps'): {State.q11},
            (State.q11, '*'): {State.q12},
            (State.q12, 'eps'): {State.q3, State.q9},
            (State.q2, 'eps'): {State.q3, State.q9},
            (State.q3, 'eps'): {State.q4},
            (State.q4, 'eps'): {State.q5, State.q7},
            (State.q5, 's'): {State.q6},
            (State.q7, 'E'): {State.q8},
            (State.q9, 't'): {State.q10},
        }
        self.accepted_states = {
            State.q8,
            State.q3,
            State.q6,
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
