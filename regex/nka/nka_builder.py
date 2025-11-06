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
    def __init__(self, start, accept):
        self.start = start
        self.accept = accept

    def __repr__(self):
        return f"NKA(start={self.start}, accept={self.accept})"


def symbol_NKA(symbol):
    start = State()
    accept = State()
    start.add_transition(symbol, accept)  # start → symbol → accept
    return NKA(start, accept)


def concat_NKA(first, second):
    first.accept.add_transition('', second.start)  # first.accept → ε → second.start
    return NKA(first.start, second.accept)


def union_NKA(first, second):
    start = State()
    accept = State()
    start.add_transition('', first.start)  # start → ε → first.start
    start.add_transition('', second.start)  # start → ε → second.start
    first.accept.add_transition('', accept)  # first.accept ε → accept
    second.accept.add_transition('', accept)  # second.accept → ε → accept
    return NKA(start, accept)


def kleene_star_NKA(nka):
    start = State()
    accept = State()
    start.add_transition('', nka.start)  # start → ε → nka.start
    start.add_transition('', accept)  # start → ε → accept (allows zero occurrences)
    nka.accept.add_transition('', nka.start)  # nka.accept → ε → nka.start (allows multiple occurrences)
    nka.accept.add_transition('', accept)  # nka.accept → ε → accept
    return NKA(start, accept)


# The same as union_NKA but with an empty transition to accept state
def optional_NKA(nka):
    start = State()
    accept = State()
    start.add_transition('', nka.start)
    start.add_transition('', accept)
    nka.accept.add_transition('', accept)
    return NKA(start, accept)


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
