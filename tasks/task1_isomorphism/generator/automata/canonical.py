from collections import deque


def canonical_signature(automaton):
    queue = deque([automaton.start])
    state_id = {automaton.start: 0}
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

            for t in sorted(targets):
                if t not in state_id:
                    state_id[t] = len(state_id)
                    queue.append(t)
                ids.append(state_id[t])

            sig["transitions"][symbol] = ids[0] if automaton.is_dfa else ids

        signature[cid] = sig

    return signature
