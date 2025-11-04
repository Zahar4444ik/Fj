from textwrap import dedent
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
            return nka.accept in current_states


        # Build NKA structure
        """))

        state_names = get_state_name(nka)
        for states in state_names.values():
            f.write(f"{states} = State()\n")

        transitions = get_transitions(nka)
        for from_state, symbol, to_state in sorted(transitions):
            f.write(f"{from_state}.add_transition({repr(symbol)}, {to_state})\n")

        f.write(f"\nnka = NKA({state_names[nka.start]}, {state_names[nka.accept]})\n")

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


def get_state_name(nka):
    state_names = {}
    counter = 0
    stack = [nka.start]
    visited = set()
    while stack:
        state = stack.pop()
        if state in visited:
            continue
        visited.add(state)
        state_names[state] = f"q{counter}"
        counter += 1
        for next_states in state.transitions.values():
            stack.extend(next_states - visited)
    return state_names


def get_transitions(nka):
    state_names = get_state_name(nka)
    transitions = []
    visited = set()
    stack = [(nka.start, [])]
    while stack:
        state, path = stack.pop()
        if state in visited:
            continue
        visited.add(state)
        for symbol, next_states in state.transitions.items():
            for next_state in next_states:
                transitions.append((state_names[state], symbol, state_names[next_state]))
                stack.append((next_state, path + [(state, symbol, next_state)]))
    return transitions


def visualize_nka(nka):
    # Assign state names (q0, q1, etc.)
    state_names = {}
    counter = 0
    stack = [nka.start]
    visited = set()
    while stack:
        state = stack.pop()
        if state in visited:
            continue
        visited.add(state)
        state_names[state] = f"q{counter}"
        counter += 1
        for next_states in state.transitions.values():
            stack.extend(next_states - visited)

    print("NFA Structure:")
    print(f"States: {', '.join(sorted(state_names[state] for state in visited))}")
    print(f"Start State: {state_names[nka.start]}")
    print(f"Accept State: {state_names[nka.accept]}")

    # Collect transitions and ε-transitions
    transitions = []
    epsilon_transitions = []
    visited = set()
    stack = [(nka.start, [])]
    while stack:
        state, path = stack.pop()
        if state in visited:
            continue
        visited.add(state)
        for symbol, next_states in state.transitions.items():
            for next_state in next_states:
                if symbol == '':
                    epsilon_transitions.append((state_names[state], state_names[next_state]))
                else:
                    transitions.append((state_names[state], symbol, state_names[next_state]))
                stack.append((next_state, path + [(state, symbol, next_state)]))

    # Print transitions
    print("Transitions:")
    if transitions:
        for from_state, symbol, to_state in sorted(transitions):
            symbol = symbol.replace('<SYMBOL_', '').replace('>', '')
            print(f"  {from_state} --{symbol}--> {to_state}")
    else:
        print("  (none)")

    # Print ε-transitions
    print("Epsilon Transitions:")
    if epsilon_transitions:
        for from_state, to_state in sorted(epsilon_transitions):
            print(f"  {from_state} --eps--> {to_state}")
    else:
        print("  (none)")
