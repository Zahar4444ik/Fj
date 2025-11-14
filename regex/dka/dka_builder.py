from collections import defaultdict
from regex.dka.ast_converter import parser_ast_to_regex_ast


def annotate_positions(root):
    """
    Walk the tree and assign unique integer 'position' to every symbol leaf.
    Returns: position_map (pos -> symbol)
    """
    pos_counter = 1
    position_map = {}

    def helper(node):
        nonlocal pos_counter
        t = node['type']
        if t == 'symbol':
            # assign position
            node['position'] = pos_counter
            position_map[pos_counter] = node['value']
            pos_counter += 1
            # initialize placeholders (useful later)
            node['nullable'] = (node.get('value', '') == '')
            node['firstpos'] = {node['position']}
            node['lastpos'] = {node['position']}
        elif t == 'union' or t == 'concat':
            helper(node['left'])
            helper(node['right'])
        elif t == 'star' or t == 'optional':
            helper(node['child'])
        else:
            raise ValueError(f"Unknown node type in annotate: {t}")

    helper(root)
    return position_map


# ---------------------------------------------------
# Compute nullable, firstpos and lastpos (bottom-up)
# ---------------------------------------------------
def compute_nullable_first_last(node):
    """
    Mutates node in-place adding:
      node['nullable'] -> bool
      node['firstpos'] -> set of positions
      node['lastpos'] -> set of positions
    Must be called after annotate_positions (so symbol leaves have 'position').
    """
    t = node['type']
    if t == 'symbol':
        # leaves already initialized by annotate_positions, but ensure fields exist
        node.setdefault('nullable', node.get('value', '') == '')
        node.setdefault('firstpos', {node['position']})
        node.setdefault('lastpos', {node['position']})
        return

    if t == 'union':
        compute_nullable_first_last(node['left'])
        compute_nullable_first_last(node['right'])
        node['nullable'] = node['left']['nullable'] or node['right']['nullable']
        node['firstpos'] = set(node['left']['firstpos']) | set(node['right']['firstpos'])
        node['lastpos'] = set(node['left']['lastpos']) | set(node['right']['lastpos'])
        return

    if t == 'concat':
        compute_nullable_first_last(node['left'])
        compute_nullable_first_last(node['right'])
        node['nullable'] = node['left']['nullable'] and node['right']['nullable']
        # firstpos: left.firstpos, and if left nullable include right.firstpos
        node['firstpos'] = set(node['left']['firstpos'])
        if node['left']['nullable']:
            node['firstpos'] |= set(node['right']['firstpos'])
        # lastpos: right.lastpos, and if right nullable include left.lastpos
        node['lastpos'] = set(node['right']['lastpos'])
        if node['right']['nullable']:
            node['lastpos'] |= set(node['left']['lastpos'])
        return

    if t == 'star':
        compute_nullable_first_last(node['child'])
        node['nullable'] = True
        node['firstpos'] = set(node['child']['firstpos'])
        node['lastpos'] = set(node['child']['lastpos'])
        return

    if t == 'optional':
        compute_nullable_first_last(node['child'])
        node['nullable'] = True
        node['firstpos'] = set(node['child']['firstpos'])
        node['lastpos'] = set(node['child']['lastpos'])
        return

    raise ValueError(f"Unknown node type in compute_nullable_first_last: {t}")

class State:
    def __init__(self):
        self.transitions = defaultdict(set)

    def add_transition(self, symbol, state):
        self.transitions[symbol].add(state)

    def __repr__(self):
        return f"State({id(self)})"


class DKA:
    def __init__(self, start, accept):
        self.start = start
        self.accept = accept


# -----------------------------------------
# Compute followpos using standard rules
# -----------------------------------------
def compute_followpos(root):
    """
    Returns followpos: dict mapping position -> set(positions)
    Must be called after compute_nullable_first_last (so first/last sets exist).
    """
    followpos = defaultdict(set)

    def helper(node):
        t = node['type']
        if t == 'concat':
            # for every i in lastpos(left): add firstpos(right) to followpos[i]
            left = node['left']; right = node['right']
            for i in left['lastpos']:
                followpos[i] |= set(right['firstpos'])
            # recurse
            helper(left)
            helper(right)
        elif t == 'union':
            helper(node['left'])
            helper(node['right'])
        elif t == 'star':
            # for every i in lastpos(child): add firstpos(child) to followpos[i]
            child = node['child']
            for i in child['lastpos']:
                followpos[i] |= set(child['firstpos'])
            helper(child)
        elif t == 'optional':
            helper(node['child'])
        elif t == 'symbol':
            return
        else:
            raise ValueError(f"Unknown node type in compute_followpos: {t}")

    helper(root)
    return followpos


def build_dka_from_followpos(root, pos_map, followpos):
    """
    Convert followpos automaton to your DKA structure.
    root      – AST root (must have firstpos computed)
    pos_map   – {pos: symbol}
    followpos – {pos: set_of_positions}
    """

    # 1) initial state = firstpos(root)
    start_pos_set = frozenset(root["firstpos"])

    # Mapping: set_of_positions → State()
    dfa_state_map = {}
    dfa_start_state = State()
    dfa_state_map[start_pos_set] = dfa_start_state

    # Queue for BFS
    unprocessed = [start_pos_set]

    # End marker position (#)
    end_marker_pos = None
    for pos, sym in pos_map.items():
        if sym == "#":
            end_marker_pos = pos
            break

    # Collect accepting states (State() objects)
    dfa_accept_states = set()

    while unprocessed:
        current = unprocessed.pop()
        current_state_obj = dfa_state_map[current]

        # If contains end marker → accepting DFA state
        if end_marker_pos in current:
            dfa_accept_states.add(current_state_obj)

        # Transitions by real alphabet symbols
        symbols = set(pos_map[p] for p in current if pos_map[p] != "#")

        for sym in symbols:
            # All positions in current where symbol = sym
            positions_with_sym = [p for p in current if pos_map[p] == sym]

            # Union of followpos over these positions
            target_set = set()
            for p in positions_with_sym:
                target_set |= followpos[p]

            target_set = frozenset(target_set)

            if not target_set:
                continue  # no target

            # Create new state if needed
            if target_set not in dfa_state_map:
                dfa_state_map[target_set] = State()
                unprocessed.append(target_set)

            target_state_obj = dfa_state_map[target_set]

            # Add transition
            current_state_obj.add_transition(sym, target_state_obj)

    # Final result
    if len(dfa_accept_states) == 1:
        accept = next(iter(dfa_accept_states))
    else:
        accept = dfa_accept_states  # if multiple

    return DKA(dfa_start_state, accept)


def build_DKA(ast):
    """
    Build DKA from parsed AST
    Returns: DKA object
    """
    regex_ast = parser_ast_to_regex_ast(ast)

    # 1) Append end marker '#': concat(regex_ast, symbol '#')
    root = {'type': 'concat', 'left': regex_ast, 'right': {'type': 'symbol', 'value': '#'}}

    # 2) annotate positions
    pos_map = annotate_positions(root)

    # 3) compute nullable, firstpos, lastpos
    compute_nullable_first_last(root)

    # 4) compute followpos
    followpos = compute_followpos(root)

    # 5) build DKA from followpos
    dka = build_dka_from_followpos(root, pos_map, followpos)

    return dka


# ---------------------------
# Small demo using the regex:
#   a | b{c|d}
# (you can replace this with parser_ast_to_regex_ast(parser_tree))
# ---------------------------
if __name__ == "__main__":
    # Build normalized regex AST for: a | b{c|d}
    # Equivalent normalization:
    # union( symbol 'a', concat(symbol 'b', star(union(symbol 'c', symbol 'd'))) )
    regex_ast = {
        'type': 'regular',
        'children': [{
            'type': 'alternative',
            'children': [
                {'type': 'sequence', 'children': [
                    {'type': 'element', 'children': [
                        {'type': 'symbol', 'value': 'a'}
                    ]}
                ]},
                {'type': 'symbol', 'value': '<PIPE>'},
                {'type': 'sequence', 'children': [
                    {'type': 'element', 'children': [
                        {'type': 'symbol', 'value': 'b'}
                    ]}
                ]}
            ]
        }]
    }

    regex_ast = parser_ast_to_regex_ast(regex_ast)  # just to illustrate usage; regex_ast is already in regex AST form

    # Append end marker '#': concat(regex_ast, symbol '#')
    root = {'type': 'concat', 'left': regex_ast, 'right': {'type': 'symbol', 'value': '#'}}

    # 1) annotate positions (assign integers to every symbol leaf)
    pos_map = annotate_positions(root)
    print("Position map:", pos_map)  # e.g. {1:'a', 2:'b', 3:'c', 4:'d', 5:'#'}

    # 2) compute nullable, firstpos, lastpos
    compute_nullable_first_last(root)

    # Walk tree and print interesting nodes for clarity
    def dump(node, name='root'):
        t = node['type']
        print(f"\nNode {name}: type={t}")
        if t == 'symbol':
            print(f"  symbol={node['value']} pos={node['position']}")
        if 'nullable' in node:
            print(f"  nullable: {node['nullable']}")
        if 'firstpos' in node:
            print(f"  firstpos: {sorted(node['firstpos'])}")
        if 'lastpos' in node:
            print(f"  lastpos: {sorted(node['lastpos'])}")
        if t in ('union','concat'):
            dump(node['left'], name + '.left')
            dump(node['right'], name + '.right')
        elif t in ('star','optional'):
            dump(node['child'], name + '.child')

    dump(root)

    # 3) compute followpos
    followpos = compute_followpos(root)
    print("\nfollowpos:")
    for p in sorted(followpos.keys()):
        print(f"  pos {p} -> {sorted(followpos[p])}")