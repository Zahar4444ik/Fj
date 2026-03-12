def print_automaton(a):
    print("States:", a.states)
    print("Start:", a.start)
    print("Accepting:", a.accepting)
    print("Transitions:")
    for s in sorted(a.transitions):
        for sym, tgts in a.transitions[s].items():
            print(f"  {s} -{sym}-> {tgts}")
