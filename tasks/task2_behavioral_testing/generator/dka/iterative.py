from textwrap import dedent

from core.regex.automata.dka.dka_builder import build_DKA
from core.regex.automata.utils.automata_operations import get_transitions
from core.regex.generators.fsa_generator import get_state_name


def generate_iterative_dka(syntax_tree, path="output/automata/dka_iterative.py"):
    dka = build_DKA(syntax_tree, None)

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
        # States of the DFA
        # ============================================================
        class State(Enum):
        """))

        state_names = {state: f"q{i}" for i, state in enumerate(get_state_name(dka))}

        for name in state_names.values():
            f.write(f"    {name} = auto()\n")

        f.write(dedent("""

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
                    print(f'({self.actual_state}, "{string[idx:]}")')
                    self.actual_state = self.transition_table[(self.actual_state, symbol)]

                return self.actual_state in self.accepted_states


        # ============================================================
        # Transition table
        # ============================================================
        transition_table = {
        """))

        transition_table = {}
        for from_state, symbol, to_state in get_transitions(dka):
            transition_table[(from_state, symbol)] = to_state

        for (from_state, symbol), to_state in transition_table.items():
            f.write(
                f"    (State.{from_state}, {repr(symbol)}): "
                f"State.{to_state},\n"
            )

        f.write(dedent("""
        }


        # ============================================================
        # Accepting states
        # ============================================================
        accepted_states = {
        """))

        for acc in dka.accepts:
            f.write(f"    State.{state_names[acc]},\n")

        f.write("}\n\n")

        f.write(f"init_state = State.{state_names[dka.start]}\n\n")

        f.write(dedent("""
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
        """))
