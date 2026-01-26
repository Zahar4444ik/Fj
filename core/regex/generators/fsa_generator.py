from core.regex.automata.utils.automata_operations import get_state_name, get_transitions

EPSILON_SYMBOL = 'ε'


def fsa_from_nka(nka, filename="output.fsa", alphabet=None, pretty=True):
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


def fsa_from_dka(dka, filename):
    lines = []

    # states line
    list_states = [f'{dka.name_map[s]}="{dka.visual_map[s]}"' for s in dka.name_map]
    lines.append("states: {\n\t" + ", \n\t".join(list_states) + "\n}")

    # start
    lines.append(f"start: {dka.name_map[dka.start]}")

    # accepting
    acc_names = [dka.name_map[a] for a in dka.accepts]
    lines.append("accepting: {" + ", ".join(acc_names) + "}")

    # transitions
    lines.append("\ntransitions:")
    for state in dka.name_map:
        for sym, targets in state.transitions.items():
            for t in targets:
                lines.append(f"  {dka.name_map[state]} -{sym}-> {dka.name_map[t]}")

    result = "\n".join(lines)
    with open(filename, "w") as f:
        f.write(result)