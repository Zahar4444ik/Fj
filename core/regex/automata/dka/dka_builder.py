from collections import defaultdict
from core.regex.automata.dka.ast_converter import parser_ast_to_regex_ast


class State:
    def __init__(self):
        self.transitions = defaultdict(set)

    def add_transition(self, symbol, state):
        self.transitions[symbol].add(state)

    def __repr__(self):
        return f"State({id(self)})"


class DKA:
    def __init__(self, start, accepts):
        self.start = start
        self.accepts = set(accepts)


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

    start_pos_set = frozenset(root["firstpos"])

    dfa_state_map = {}
    dfa_start_state = State()
    dfa_state_map[start_pos_set] = dfa_start_state

    unprocessed = [start_pos_set]

    # find end marker
    end_marker_pos = None
    for pos, sym in pos_map.items():
        if sym == "#":
            end_marker_pos = pos
            break

    dfa_accept_states = set()

    while unprocessed:
        current = unprocessed.pop()
        current_state_obj = dfa_state_map[current]

        if end_marker_pos in current:
            dfa_accept_states.add(current_state_obj)

        symbols = set(pos_map[p] for p in current if pos_map[p] != "#")

        for sym in symbols:
            positions_with_sym = [p for p in current if pos_map[p] == sym]

            target_set = set()
            for p in positions_with_sym:
                target_set |= followpos[p]

            target_set = frozenset(target_set)

            if not target_set:
                continue

            if target_set not in dfa_state_map:
                dfa_state_map[target_set] = State()
                unprocessed.append(target_set)

            target_state_obj = dfa_state_map[target_set]

            current_state_obj.add_transition(sym, target_state_obj)

    dka = DKA(dfa_start_state, dfa_accept_states)

    # ✔️ attach the mapping for later
    dka.state_map = dfa_state_map

    return dka


def build_DKA(ast, regex):
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

    # 6) creates states visual
    name_map, visual_map = name_dfa_states(dka, pos_map, regex)

    return dka, name_map, visual_map


def visualize_state_positions(regex_str, pos_map, pos_set):
    """
    regex_str : original regex string
    pos_map   : {pos: symbol}
    pos_set   : active positions in the DFA state

    Returns the regex string with '.' inserted before active symbol positions.
    """

    # Collect indexes of symbol-characters (non-operators)
    symbol_indexes = [
        i for i, ch in enumerate(regex_str)
        if ch not in "()*+?|{}[]"
    ]

    # Convert pos_set (positions) → real character indexes in regex_str
    marked_indexes = []
    for pos in pos_set:
        if pos <= len(symbol_indexes):
            marked_indexes.append(symbol_indexes[pos - 1])
        else:
            # Position outside regex_str (shouldn’t normally happen)
            marked_indexes.append(len(regex_str))

    # Insert '.' before each symbol, process from right to left
    result = regex_str
    for idx in sorted(marked_indexes, reverse=True):
        result = result[:idx] + "." + result[idx:]

    return result


def name_dfa_states(dka, pos_map, original_regex):
    """
    Assign q0, q1, q2 ... and compute visual token per DFA state.
    """
    if original_regex is None:
        return None, None

    name_map = {}
    visual_map = {}

    queue = [dka.start]
    visited = set([dka.start])
    counter = 0

    while queue:
        st = queue.pop(0)
        name = f"q{counter}"
        name_map[st] = name

        # find position-set behind this state
        # invert the mapping from dfa_state_map
        pos_set = None
        for k, v in dka.state_map.items():
            if v is st:
                pos_set = k
                break

        visual = visualize_state_positions(original_regex, pos_map, pos_set)
        visual_map[st] = visual

        counter += 1

        # BFS for next
        for sym, targets in st.transitions.items():
            for t in targets:
                if t not in visited:
                    visited.add(t)
                    queue.append(t)

    return name_map, visual_map