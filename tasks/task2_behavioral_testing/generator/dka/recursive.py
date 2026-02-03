from textwrap import dedent

from core.regex.automata.dka.dka_builder import build_DKA
from core.regex.automata.utils.automata_operations import get_transitions
from core.regex.generators.fsa_generator import get_state_name


def generate_recursive_dka(syntax_tree, path="output/automata/dka_recursive.py"):
    dka = build_DKA(syntax_tree, None)

    # Assign names q0, q1, ...
    state_names = {state: f"q{i}" for i, state in enumerate(get_state_name(dka))}

    # Collect transitions: (state, symbol) -> state
    transitions = {}
    alphabet = set()

    for from_state, symbol, to_state in get_transitions(dka):
        transitions[(from_state, symbol)] = to_state
        alphabet.add(symbol)

    with open(path, "w", encoding="utf-8") as f:
        # Header
        f.write(dedent('''
        """
        ============================================================
        Rekurzívna implementácia deterministického konečného automatu
        Automat je generovaný automaticky zo syntaxového stromu regexu.
        ============================================================
        """
        '''))

        # Generate each state as a function
        for state, state_name in state_names.items():
            f.write(f"\n\ndef {state_name}(string: str) -> bool:\n")

            # Handle empty string (base case)
            is_accepting = state in dka.accepts
            f.write("    if len(string) == 0:\n")
            f.write(f"        return {is_accepting}\n")

            # Handle non-empty string (transitions)
            f.write("    else:\n")
            f.write("        match string[0]:\n")

            for symbol in sorted(alphabet):
                key = (state_name, symbol)
                if key in transitions:
                    target = transitions[key]
                    f.write(f"            case {repr(symbol)}:\n")
                    f.write(f"                return {target}(string[1:])\n")

            # Default case for invalid symbols
            f.write("            case _:\n")
            f.write("                return False\n")

        # Main loop
        f.write(dedent(f"""

        if __name__ == "__main__":
            input_string = input("Zadaj vstupný reťazec> ")
            while input_string != "quit":
                print(
                    f"Reťazec '{{input_string}}' "
                    f"{{'JE ' if {state_names[dka.start]}(input_string) else 'NIE JE '}}akceptovaný!"
                )
                input_string = input("Zadaj vstupný reťazec> ")
        """))
