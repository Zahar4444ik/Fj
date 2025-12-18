def is_dfa(automaton):
    for src in automaton.transitions:
        for sym, targets in automaton.transitions[src].items():
            if sym == 'ε':
                return False
            if len(targets) != 1:
                return False
    return True
