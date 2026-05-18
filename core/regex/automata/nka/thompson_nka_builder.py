"""
Thompson's Construction NFA Builder

Implements Thompson's construction, which maintains the invariant that every
intermediate NFA has exactly one start state and one accept state.

Differences from nka_builder.py:
  - union:    adds a dedicated new accept state f; ε from both branches into f
  - kleene_star: adds new start AND new accept f; old accepts loop back and merge into f
  - optional: adds new start AND new accept f; old accepts merge into f

symbol_NKA and concat_NKA are identical to the custom builder.
"""

from core.regex.automata.nka.nka_builder import State, NKA


def symbol_NKA(symbol):
    start = State()
    accept = State()
    start.add_transition(symbol, accept)
    return NKA(start, {accept})


def concat_NKA(first, second):
    for a in first.accepts:
        a.add_transition('', second.start)
    return NKA(first.start, second.accepts)


def union_NKA(first, second):
    start = State()
    accept = State()
    start.add_transition('', first.start)
    start.add_transition('', second.start)
    for a in first.accepts:
        a.add_transition('', accept)
    for a in second.accepts:
        a.add_transition('', accept)
    return NKA(start, {accept})


def kleene_star_NKA(nka):
    start = State()
    accept = State()
    start.add_transition('', nka.start)
    start.add_transition('', accept)
    for a in nka.accepts:
        a.add_transition('', nka.start)
        a.add_transition('', accept)
    return NKA(start, {accept})


def optional_NKA(nka):
    start = State()
    accept = State()
    start.add_transition('', nka.start)
    start.add_transition('', accept)
    for a in nka.accepts:
        a.add_transition('', accept)
    return NKA(start, {accept})


def build_thompson_NKA(node):
    if node['type'] == 'regular':
        return build_thompson_NKA(node['children'][0])

    elif node['type'] == 'alternative':
        children = [build_thompson_NKA(child) for child in node['children'] if child['type'] != 'symbol']
        nka = children[0]
        for child_nka in children[1:]:
            nka = union_NKA(nka, child_nka)
        return nka

    elif node['type'] == 'sequence':
        elements = [build_thompson_NKA(child) for child in node['children']]
        nka = elements[0]
        for e in elements[1:]:
            nka = concat_NKA(nka, e)
        return nka

    elif node['type'] == 'element':
        children = node['children']

        if len(children) == 1 and children[0]['type'] == 'symbol':
            return symbol_NKA(children[0]['value'])

        if children[0]['value'] == '<LPAREN>':
            return build_thompson_NKA(children[1])
        elif children[0]['value'] == '<LBRACE>':
            return kleene_star_NKA(build_thompson_NKA(children[1]))
        elif children[0]['value'] == '<LBRACKET>':
            return optional_NKA(build_thompson_NKA(children[1]))

    raise ValueError("Unknown node structure: " + str(node))
