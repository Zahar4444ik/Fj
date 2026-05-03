from collections import deque


def _stable_labels(automaton):
    """
    Iteratively refine state labels until stable (Weisfeiler-Leman style).

    Each round replaces a state's label with a signature derived from its
    accepting flag, its outgoing symbols, and the *current labels* of all
    children.  Repeating until convergence means that after k rounds every
    state's label encodes the full structural context up to depth k.  For a
    graph with N states, N rounds are always sufficient for convergence.
    """
    states = automaton.states

    # Round 0: label = (accepting, sorted out-symbols)
    labels = {
        s: (s in automaton.accepting,
            tuple(sorted(automaton.transitions.get(s, {}).keys())))
        for s in states
    }

    for _ in range(len(states) + 1):
        new_labels = {}
        for s in states:
            trans_sig = []
            for sym in sorted(automaton.transitions.get(s, {}).keys()):
                raw = automaton.transitions[s][sym]
                children = list(raw) if isinstance(raw, (list, set, frozenset)) else [raw]
                # Sort child labels so NFA non-determinism order doesn't matter
                child_labels = tuple(sorted(labels[c] for c in children))
                trans_sig.append((sym, child_labels))
            new_labels[s] = (s in automaton.accepting, tuple(trans_sig))

        if new_labels == labels:
            break
        labels = new_labels

    return labels


def canonical_signature(automaton):
    """
    BFS from start state, assigns canonical ids (0, 1, 2, ...).
    Caches result on the automaton instance so repeated calls are free.

    Returns:
        signature: structure for equivalence check
        annotations: annotations mapped to canonical ids
        id_to_state: mapping from canonical id back to original state name
    """
    if hasattr(automaton, '_canonical_cache'):
        return automaton._canonical_cache

    labels = _stable_labels(automaton)

    queue = deque([automaton.start])
    state_id = {automaton.start: 0}
    id_to_state = {0: automaton.start}
    signature = []

    while queue:
        current = queue.popleft()
        cid = state_id[current]

        while len(signature) <= cid:
            signature.append(None)

        sig = {
            "accepting": current in automaton.accepting,
            "transitions": {}
        }

        for symbol in sorted(automaton.transitions.get(current, {})):
            raw = automaton.transitions[current][symbol]
            targets = list(raw) if isinstance(raw, (list, set, frozenset)) else [raw]
            ids = []

            # Use stable label as sort key; state name only as last-resort tiebreaker
            # for truly isomorphic sibling subgraphs (same label = same structure).
            for t in sorted(targets, key=lambda s: (labels[s], s)):
                if t not in state_id:
                    state_id[t] = len(state_id)
                    id_to_state[state_id[t]] = t
                    queue.append(t)
                ids.append(state_id[t])

            sig["transitions"][symbol] = ids[0] if automaton.is_dfa else ids

        signature[cid] = sig

    annotations = {
        cid: automaton.annotations.get(state)
        for cid, state in id_to_state.items()
    }

    automaton._canonical_cache = (signature, annotations, id_to_state)
    return signature, annotations, id_to_state
