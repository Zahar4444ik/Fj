"""
FSA Generator

Generates .fsa format files from DFA and NFA automata.
Outputs properly formatted finite automaton specifications.
"""

import logging
from pathlib import Path

from core.regex.automata.utils.automata_operations import get_state_name, get_transitions

# ============================================================================
# CONFIGURATION
# ============================================================================

OUTPUT_DIR = Path(__file__).resolve().parent / "output"
FSA_DIR = OUTPUT_DIR / "fsa"

FSA_DIR.mkdir(parents=True, exist_ok=True)

EPSILON_SYMBOL = 'eps'

logger = logging.getLogger(__name__)


def write_fsa(filename, alphabet, states, start, accepting, transitions):
    """
    Write a fully formatted .fsa file.

    Args:
        filename: Output file path
        alphabet: Iterable of symbols
        states: List of state names
        start: Initial state name
        accepting: List of accepting state names
        transitions: List of (from_state, symbol, to_state) tuples

    Returns:
        str: Filename written
    """
    with open(filename, "w", encoding="utf-8") as f:
        # Alphabet
        f.write(f"alphabet: {{{', '.join(sorted(alphabet))}}}\n\n")

        # States
        f.write("states: {\n")
        f.write("    " + ",\n    ".join(states) + "\n")
        f.write("}\n\n")

        # Start state
        f.write(f"initial_state: {start}\n")

        # Accepting states
        f.write(f"accepting_states: {{{', '.join(sorted(accepting))}}}\n\n")

        # Transitions
        f.write("transitions: {\n")
        for i, (frm, sym, to) in enumerate(transitions):
            sym_out = sym if sym != '' else EPSILON_SYMBOL
            comma = "," if i < len(transitions) - 1 else ""
            f.write(f"    {frm} -{sym_out}-> {to}{comma}\n")
        f.write("}\n")

    logger.debug(f"Written FSA file: {filename}")
    return filename


# ============================================================================
# NFA TO FSA CONVERSION
# ============================================================================

def fsa_from_nka(nka, filename="output.fsa", alphabet=None, pretty=True):
    """
    Generate FSA file from NFA automaton.

    Args:
        nka: NFA automaton object
        filename: Output file path
        alphabet: Optional alphabet. Auto-computed if not provided
        pretty: Use pretty printing for transitions

    Returns:
        str: Filename written
    """
    state_names = get_state_name(nka)

    # Sort states by numeric suffix
    ordered = sorted(state_names.items(), key=lambda kv: int(kv[1][1:]))
    state_list = [name for _, name in ordered]

    # Get transitions
    transitions = get_transitions(nka, pretty=pretty)

    # Get accepting states
    if isinstance(nka.accepts, (set, list, tuple)):
        accepting = sorted({state_names[s] for s in nka.accepts})
    else:
        accepting = [state_names.get(nka.accepts)]

    # Get start state
    start = state_names[nka.start]

    # Compute alphabet if not provided
    if alphabet is None:
        alphabet = {
            sym for _, sym, _ in transitions
            if sym != '' and sym != EPSILON_SYMBOL
        }

    logger.debug(f"Converting NFA to FSA: {len(state_list)} states, {len(alphabet)} symbols")

    return write_fsa(
        filename=filename,
        alphabet=alphabet,
        states=state_list,
        start=start,
        accepting=accepting,
        transitions=transitions
    )


# ============================================================================
# DFA TO FSA CONVERSION
# ============================================================================

def fsa_from_dka(dka, filename):
    """
    Generate FSA file from DFA automaton.

    Args:
        dka: DFA automaton object
        filename: Output file path

    Returns:
        str: Filename written
    """
    # Build state list
    states = []
    for s in sorted(dka.name_map, key=lambda x: dka.name_map[x]):
        states.append(f'{dka.name_map[s]}="{dka.visual_map[s]}"')

    # Get start and accepting states
    start = dka.name_map[dka.start]
    accepting = sorted(dka.name_map[a] for a in dka.accepts)

    # Build transitions and alphabet
    transitions = []
    alphabet = set()

    for state in dka.name_map:
        for sym, targets in state.transitions.items():
            for t in targets:
                transitions.append(
                    (dka.name_map[state], sym, dka.name_map[t])
                )
                alphabet.add(sym)

    transitions.sort()

    logger.debug(f"Converting DFA to FSA: {len(states)} states, {len(alphabet)} symbols")

    return write_fsa(
        filename=filename,
        alphabet=alphabet,
        states=states,
        start=start,
        accepting=accepting,
        transitions=transitions
    )