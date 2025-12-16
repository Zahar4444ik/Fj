from collections import deque

from isomorphism.parse_fsa import parse_fsa


def canonical_signature(automaton):
    queue = deque()
    state_id = {}          # original_state -> canonical_number
    signature = []         # list of state descriptors

    # initialize
    state_id[automaton.start] = 0
    queue.append(automaton.start)

    while queue:
        current = queue.popleft()
        current_id = state_id[current]

        # ensure signature list is long enough
        while len(signature) <= current_id:
            signature.append(None)

        # accepting flag
        state_sig = {
            "accepting": current in automaton.accepting,
            "transitions": {}
        }

        # process transitions
        transitions = automaton.transitions.get(current, {})

        for symbol in sorted(transitions.keys()):
            targets = transitions[symbol]

            target_ids = []
            for tgt in sorted(targets):
                if tgt not in state_id:
                    state_id[tgt] = len(state_id)
                    queue.append(tgt)
                target_ids.append(state_id[tgt])

            # DFA vs NFA handling
            if automaton.is_dfa:
                state_sig["transitions"][symbol] = target_ids[0]
            else:
                state_sig["transitions"][symbol] = sorted(target_ids)

        signature[current_id] = state_sig

    return signature


def structurally_equivalent(a1, a2):
    if a1.is_dfa != a2.is_dfa:
        return False

    sig1 = canonical_signature(a1)
    sig2 = canonical_signature(a2)

    return sig1 == sig2


if __name__ == "__main__":
    a1 = parse_fsa("test.fsa")
    a2 = parse_fsa("test2.fsa")
    print(structurally_equivalent(a1, a2))