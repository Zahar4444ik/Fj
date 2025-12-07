from collections import defaultdict


class State:
    def __init__(self):
        self.transitions = defaultdict(set)  # Using defaultdict(set) for transitions handles nondeterminism
        # (multiple transitions on the same symbol).

    def add_transition(self, symbol, state):
        self.transitions[symbol].add(state)

    def __repr__(self):
        return f"State({id(self)})"


class NKA:
    def __init__(self, start, accepts):
        self.start = start
        self.accepts = set(accepts)

    def __repr__(self):
        return f"NKA(start={self.start}, accepts={self.accepts})"


def symbol_NKA(symbol):
    start = State()
    accept = State()
    start.add_transition(symbol, accept)  # start → symbol → accept
    return NKA(start, {accept})


def concat_NKA(first, second):
    for a in first.accepts:
        a.add_transition('', second.start)  # first.accept → ε → second.start
    return NKA(first.start, second.accepts)


def union_NKA(first, second):
    start = State()

    start.add_transition('', first.start)  # start → ε → first.start
    start.add_transition('', second.start)  # start → ε → second.start

    return NKA(start, first.accepts | second.accepts)  # | combines accepts


def kleene_star_NKA(nka):
    start = State()
    accepts = {start} | nka.accepts

    start.add_transition('', nka.start)  # start → ε → nka.start

    for a in nka.accepts:
        a.add_transition('', nka.start)  # nka.accepts → ε → nka.start (allows multiple occurrences)
    return NKA(start, accepts)


# The same as union_NKA but with an empty transition to accept state
def optional_NKA(nka):
    start = State()

    accepts = start | nka.acceptss
    start.add_transition('', nka.start)

    return NKA(start, accepts)


def build_NKA(node):
    if node['type'] == 'regular':
        return build_NKA(node['children'][0])

    elif node['type'] == 'alternative':
        children = [build_NKA(child) for child in node['children'] if child['type'] != 'symbol']
        nka = children[0]
        for child_nka in children[1:]:
            nka = union_NKA(nka, child_nka)
        return nka

    elif node['type'] == 'sequence':
        elements = [build_NKA(child) for child in node['children']]
        nka = elements[0]
        for e in elements[1:]:
            nka = concat_NKA(nka, e)
        return nka

    elif node['type'] == 'element':
        children = node['children']

        if len(children) == 1 and children[0]['type'] == 'symbol':
            return symbol_NKA(children[0]['value'])

        if children[0]['value'] == '<LPAREN>':
            return build_NKA(children[1])
        elif children[0]['value'] == '<LBRACE>':
            return kleene_star_NKA(build_NKA(children[1]))
        elif children[0]['value'] == '<LBRACKET>':
            return optional_NKA(build_NKA(children[1]))

    raise ValueError("Unknown node structure: " + str(node))
