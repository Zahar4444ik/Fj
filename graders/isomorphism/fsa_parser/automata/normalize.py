from collections import deque

from graders.isomorphism.fsa_parser.automata.classify import is_dfa


# Ensure states from transitions are included
def normalize_states(automaton):
    for src in automaton.transitions:
        automaton.states.add(src)
        for sym in automaton.transitions[src]:
            automaton.states |= automaton.transitions[src][sym]


# Find all reachable states from the start state
def reachable_states(automaton):
    visited = set()
    queue = deque([automaton.start])

    while queue:
        s = queue.popleft()
        if s in visited:
            continue
        visited.add(s)

        for targets in automaton.transitions.get(s, {}).values():
            queue.extend(targets)

    return visited


# Normalize the automaton by removing unreachable states
def normalize_automaton(automaton):
    normalize_states(automaton)
    reachable = reachable_states(automaton)

    automaton.states &= reachable
    automaton.accepting &= reachable

    automaton.transitions = {
        s: automaton.transitions[s]
        for s in automaton.transitions
        if s in reachable
    }

    automaton.is_dfa = is_dfa(automaton)
    return automaton
