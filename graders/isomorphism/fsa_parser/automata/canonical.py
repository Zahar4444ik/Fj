from collections import deque


def canonical_signature(automaton):
    """
    BFS from start state, assigns canonical ids (0, 1, 2, ...).
    Caches result on the automaton instance so repeated calls are free.

    Returns:
        signature: structure for equivalence check
        annotations: annotations mapped to canonical ids
    """
    if hasattr(automaton, '_canonical_cache'):
        return automaton._canonical_cache

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
            targets = automaton.transitions[current][symbol]
            ids = []

            # Sort by structural properties rather than arbitrary state names.
            # Two levels of lookahead breaks ties between siblings whose immediate
            # properties are identical but whose children differ (e.g. symmetric
            # NFA branches where one child is accepting and the other is not).
            def _struct_key(state_name):
                accepting = state_name in automaton.accepting
                out_symbols = tuple(sorted(automaton.transitions.get(state_name, {}).keys()))
                child_sigs = []
                for sym in out_symbols:
                    raw = automaton.transitions[state_name][sym]
                    children = list(raw) if isinstance(raw, (list, set, frozenset)) else [raw]
                    for child in children:
                        child_acc = child in automaton.accepting
                        child_out = tuple(sorted(automaton.transitions.get(child, {}).keys()))
                        child_sigs.append((sym, child_acc, child_out))
                child_sigs.sort()
                return (accepting, out_symbols, tuple(child_sigs), state_name)

            for t in sorted(targets, key=_struct_key):
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
