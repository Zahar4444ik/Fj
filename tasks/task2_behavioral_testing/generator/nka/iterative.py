from collections import defaultdict
from textwrap import dedent

from core.regex.automata.utils.automata_operations import get_state_name, get_transitions
from core.regex.automata.nka.nka_builder import build_NKA


def generate_iterative_nka(syntax_tree, path="output/automata/nka_iterative.py"):
    # Build NKA from syntax tree
    nka = build_NKA(syntax_tree)

    with open(path, "w", encoding="utf-8") as f:
        f.write(dedent('''
                """
                ============================================================
                Rekurzívna implementácia nedeterministického konečného automatu
                Automat je generovaný automaticky zo syntaxového stromu regexu.
                ============================================================
                """
                '''))

        f.write(dedent("""
        from enum import Enum, auto


        # ============================================================
        # States of the NFA
        # ============================================================
        class State(Enum):
        """))

        # Generate enum states
        state_names = get_state_name(nka)
        for name in sorted(state_names.values()):
            f.write(f"    {name} = auto()\n")

        f.write(dedent("""

        class NFA:
            def __init__(self):
                self.transition_table = {
        """))

        # Generate transitions
        transition_dict = defaultdict(set)

        for from_state, symbol, to_state in get_transitions(nka):
            transition_dict[(from_state, symbol)].add(to_state)

        for (from_state, symbol), to_states in sorted(transition_dict.items()):
            symbol_repr = repr(symbol) if symbol != "ε" else "''"
            targets = ", ".join(f"State.{s}" for s in sorted(to_states))
            f.write(
                f"            (State.{from_state}, {symbol_repr}): {{{targets}}},\n"
            )

        f.write("        }\n")
        f.write("        self.accepted_states = {\n")

        for acc_state in nka.accepts:
            f.write(f"            State.{state_names[acc_state]},\n")
        f.write("        }\n")

        # Initial state
        f.write(f"        self.init_state = State.{state_names[nka.start]}")

        # Instantiate automaton
        f.write(dedent("""
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
        """))
