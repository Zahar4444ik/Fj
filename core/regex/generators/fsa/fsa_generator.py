from core.regex.automata.utils.automata_operations import get_state_name, get_transitions

EPSILON_SYMBOL = 'ε'


def write_fsa(
    filename,
    alphabet,
    states,
    start,
    accepting,
    transitions,
):
    """
    Write a fully formatted .fsa file.
    - alphabet: iterable[str]
    - states: list[str]
    - start: str
    - accepting: list[str]
    - transitions: list[(from, symbol, to)]
    """

    with open(filename, "w", encoding="utf-8") as f:
        # Alphabet
        f.write(f"alphabet: {{{', '.join(sorted(alphabet))}}}\n\n")

        # States
        f.write("states: {\n")
        f.write("    " + ",\n    ".join(states) + "\n")
        f.write("}\n\n")

        # Start
        f.write(f"start: {start}\n")

        # Accepting
        f.write(f"accepting: {{{', '.join(sorted(accepting))}}}\n\n")

        # Transitions
        f.write("transitions: {\n")
        for i, (frm, sym, to) in enumerate(transitions):
            sym_out = sym if sym != '' else EPSILON_SYMBOL
            comma = "," if i < len(transitions) - 1 else ""
            f.write(f"    {frm} -{sym_out}-> {to}{comma}\n")
        f.write("}\n")

    return filename


def fsa_from_nka(nka, filename="output.fsa", alphabet=None, pretty=True):
    state_names = get_state_name(nka)

    ordered = sorted(state_names.items(), key=lambda kv: int(kv[1][1:]))
    state_list = [name for _, name in ordered]

    transitions = get_transitions(nka, pretty=pretty)

    if isinstance(nka.accepts, (set, list, tuple)):
        accepting = sorted({state_names[s] for s in nka.accepts})
    else:
        accepting = [state_names.get(nka.accepts)]

    start = state_names[nka.start]

    # If alphabet not provided, compute from transitions
    if alphabet is None:
        alphabet = {
            sym for _, sym, _ in transitions
            if sym != '' and  sym != EPSILON_SYMBOL # exclude epsilon
        }

    return write_fsa(
        filename=filename,
        alphabet=alphabet,
        states=state_list,
        start=start,
        accepting=accepting,
        transitions=transitions
    )


def fsa_from_dka(dka, filename):
    states = []
    transitions = []

    # Build state list
    for s in sorted(dka.name_map, key=lambda x: dka.name_map[x]):
        states.append(f'{dka.name_map[s]}="{dka.visual_map[s]}"')

    start = dka.name_map[dka.start]

    accepting = sorted(dka.name_map[a] for a in dka.accepts)

    # Build transitions and alphabet
    alphabet = set()

    for state in dka.name_map:
        for sym, targets in state.transitions.items():
            for t in targets:
                transitions.append(
                    (dka.name_map[state], sym, dka.name_map[t])
                )
                alphabet.add(sym)

    transitions.sort()

    return write_fsa(
        filename=filename,
        alphabet=alphabet,
        states=states,
        start=start,
        accepting=accepting,
        transitions=transitions
    )