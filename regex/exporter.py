EPSILON_SYMBOL = 'ε'


def get_state_name(nka):
    """
    Traverse reachable states and assign deterministic names q0, q1, ...
    Uses DFS-like stack but deterministic enumeration order.
    Returns dict: {State_object: "qN"}
    """
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
        # push children in deterministic order: flatten all next states
        # convert to list to have deterministic iteration order (insertion order of set is arbitrary)
        for next_states in state.transitions.values():
            # next_states is a set; extend with a stable ordering (list)
            for ns in list(next_states):
                if ns not in visited:
                    stack.append(ns)
    return state_names


def get_transitions(nka, pretty=True):
    """
    Return list of (from_name, symbol, to_name) tuples for all reachable transitions.
    pretty: if True, maps '' -> EPSILON_SYMBOL and strips '<SYMBOL,x>' decorations if present.
    """
    state_names = get_state_name(nka)
    transitions = []
    visited = set()
    stack = [(nka.start, None)]
    while stack:
        state, _ = stack.pop()
        if state in visited:
            continue
        visited.add(state)
        for symbol, next_states in state.transitions.items():
            for next_state in next_states:
                from_name = state_names[state]
                to_name = state_names[next_state]
                sym = symbol
                if pretty:
                    if sym == '':
                        sym = EPSILON_SYMBOL
                    else:
                        # clean up token-like symbols <SYMBOL,x> -> x
                        if sym.startswith('<SYMBOL,') and sym.endswith('>'):
                            sym = sym[len('<SYMBOL,'):-1]
                transitions.append((from_name, sym, to_name))
                stack.append((next_state, None))
    # stable sort for deterministic output: by from_name, symbol, to_name
    transitions.sort(key=lambda t: (int(t[0][1:]) if t[0].startswith('q') else t[0], str(t[1]), int(t[2][1:]) if t[2].startswith('q') else t[2]))
    return transitions


def visualize_nka(nka, pretty=True):
    """
    Print a readable overview of the NKA (states, start, accept, transitions).
    """
    state_names = get_state_name(nka)
    # sort visited states by their q number for nicer printing
    visited_states = sorted(state_names.items(), key=lambda kv: int(kv[1][1:]))  # list of (state, name)

    print("NFA Structure:")
    print("States:", ", ".join(name for _, name in visited_states))
    print("Start State:", state_names[nka.start])

    # Accepting may be single state or a collection
    if isinstance(nka.accepts, (set, list, tuple)):
        accepting_names = sorted({state_names[s] for s in nka.accepts})
        print("Accepting States:", ", ".join(accepting_names))
    else:
        print("Accept State:", state_names.get(nka.accepts, "UNKNOWN"))

    # Collect transitions
    transitions = []
    epsilon_transitions = []
    visited = set()
    stack = [(nka.start, None)]
    while stack:
        state, _ = stack.pop()
        if state in visited:
            continue
        visited.add(state)
        for symbol, next_states in state.transitions.items():
            for next_state in next_states:
                from_name = state_names[state]
                to_name = state_names[next_state]
                if symbol == '':
                    epsilon_transitions.append((from_name, to_name))
                else:
                    sym = symbol
                    if pretty and sym.startswith('<SYMBOL,') and sym.endswith('>'):
                        sym = sym[len('<SYMBOL,'):-1]
                    transitions.append((from_name, sym, to_name))
                stack.append((next_state, None))

    print("\nTransitions:")
    if transitions:
        for frm, sym, to in transitions:
            print(f"  {frm} --{sym}--> {to}")
    else:
        print("  (none)")

    print("\nEpsilon Transitions:")
    if epsilon_transitions:
        for frm, to in epsilon_transitions:
            print(f"  {frm} --eps--> {to}")
    else:
        print("  (none)")


def export_to_fsa(nka, filename="output.fsa", alphabet=None, pretty=True):
    """
    Write a .fsa file for the given NKA.
    - alphabet: optional iterable of symbols to print in header
    - pretty: format symbols for readability (ε for epsilon, strip <SYMBOL,x> wrapper)
    """
    state_names = get_state_name(nka)
    # order states by their assigned q index
    ordered = sorted(state_names.items(), key=lambda kv: int(kv[1][1:]))  # [(state, 'q0'), ...]
    state_list = [name for _, name in ordered]

    # transitions as (from, symbol, to)
    transitions = get_transitions(nka, pretty=pretty)

    # compute accepting set names
    if isinstance(nka.accepts, (set, list, tuple)):
        accepting = sorted({state_names[s] for s in nka.accepts})
    else:
        accepting = [state_names.get(nka.accepts)]

    with open(filename, "w", encoding="utf-8") as f:
        # alphabet header
        if alphabet:
            f.write(f"alphabet: {{{', '.join(sorted(alphabet))}}}\n")
        # states header
        f.write(f"states: {{{', '.join(state_list)}}}\n")
        # start and accepting
        f.write(f"start: {state_names[nka.start]}\n")
        f.write(f"accepting: {{{', '.join(accepting)}}}\n\n")

        f.write("transitions:\n")
        for frm, sym, to in transitions:
            sym_out = sym if sym != '' else EPSILON_SYMBOL
            # ensure epsilon uses EPSILON_SYMBOL
            if sym_out == '':
                sym_out = EPSILON_SYMBOL
            f.write(f"  {frm} -{sym_out}-> {to}\n")

    return filename
