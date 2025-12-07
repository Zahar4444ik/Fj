from textwrap import dedent

from regex.exporter import visualize_nka, get_state_name, get_transitions
from regex.nka.nka_builder import build_NKA


def generate_nka_py_file(syntax_tree):
    # Build NKA from syntax tree
    nka = build_NKA(syntax_tree)
    visualize_nka(nka)

    # Generate nka.py
    with open("automata\\nka.py", "w", encoding="utf-8") as f:
        f.write(dedent("""
        from collections import defaultdict


        class State:
            def __init__(self):
                self.transitions = defaultdict(set)

            def add_transition(self, symbol, state):
                self.transitions[symbol].add(state)


        class NKA:
            def __init__(self, start, accept):
                self.start = start
                self.accept = accept


        def epsilon_closure(states):
            stack = list(states)
            closure = set(states)
            while stack:
                state = stack.pop()
                for next_state in state.transitions['']:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
            return closure


        def move(states, symbol):
            symbol = f"<SYMBOL,{symbol}>"
            result = set()
            for state in states:
                result.update(state.transitions[symbol])
            return result


        def matches(nka, input_str):
            current_states = epsilon_closure({nka.start})
            for symbol in input_str:
                current_states = epsilon_closure(move(current_states, symbol))
            return nka.accepts in current_states


        # Build NKA structure
        """))

        state_names = get_state_name(nka)
        for states in state_names.values():
            f.write(f"{states} = State()\n")

        transitions = get_transitions(nka)
        for from_state, symbol, to_state in sorted(transitions):
            f.write(f"{from_state}.add_transition({repr(symbol)}, {to_state})\n")

        f.write(f"\nnka = NKA({state_names[nka.start]}, {state_names[nka.accepts]})\n")

        f.write(dedent("""
        while True:
            try:
                input_str = input("Enter input word: ")
                if input_str.lower() == 'quit':
                    break
                if matches(nka, input_str):
                    print(f"Word '{input_str}' is ACCEPTED")
                else:
                    print(f"Word '{input_str}' is NOT ACCEPTED")
            except (KeyboardInterrupt, EOFError):
                print("\\nExiting...")
                break
        """))
