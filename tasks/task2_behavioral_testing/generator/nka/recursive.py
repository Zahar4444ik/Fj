from collections import defaultdict
from textwrap import dedent

from core.regex.generators.fsa_generator import get_state_name, get_transitions
from core.regex.automata.nka.nka_builder import build_NKA


def generate_recursive_nka(syntax_tree, path="output/automata/nka_recursive.py"):
    nka = build_NKA(syntax_tree)

    state_names = get_state_name(nka)
    transitions = get_transitions(nka)

    # group transitions: (from_state) -> [(symbol, to_state)]
    transition_dict = defaultdict(list)
    for from_state, symbol, to_state in transitions:
        transition_dict[from_state].append((symbol, to_state))

    with open(path, "w", encoding="utf-8") as f:
        f.write(dedent('''
        """
        ============================================================
        Rekurzívna implementácia nedeterministického konečného automatu
        Automat je generovaný automaticky zo syntaxového stromu regexu.
        ============================================================
        """
        '''))

        # ------------------------------------------------------------
        # Generate state functions
        # ------------------------------------------------------------
        for state in sorted(state_names.values()):
            f.write(f"\n\ndef {state}(string: str) -> bool:\n")

            clauses = []

            # accepting state
            original_state = next(k for k, v in state_names.items() if v == state)
            if original_state in nka.accepts:
                clauses.append("len(string) == 0")

            # transitions
            for symbol, to_state in transition_dict.get(state, []):
                to_name = to_state

                if symbol == "ε" or symbol == "":
                    clauses.append(f"{to_name}(string)")
                else:
                    clauses.append(
                        f"(len(string) > 0 and string[0] == '{symbol}' and {to_name}(string[1:]))"
                    )

            if clauses:
                f.write("    return " + " or ".join(clauses) + "\n")
            else:
                f.write("    return False\n")

        # ------------------------------------------------------------
        # Main entry point
        # ------------------------------------------------------------
        start_name = state_names[nka.start]

        f.write(dedent(f"""

        if __name__ == "__main__":
            input_string = input("Zadaj vstupný reťazec> ")
            while input_string != "quit":
                print(
                    f"Reťazec '{{input_string}}' "
                    f"{{'JE ' if {start_name}(input_string) else 'NIE JE '}}akceptovaný!"
                )
                input_string = input("Zadaj vstupný reťazec> ")
        """))
