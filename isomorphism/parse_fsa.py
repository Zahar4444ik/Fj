from antlr4 import *
from gen.FSALexer import FSALexer
from gen.FSAParser import FSAParser
from fsa_builder import FSABuilder, is_dfa
from fsa_builder import print_automaton, normalize_states, reachable_states


def parse_fsa(path):
    stream = FileStream(path, encoding="utf-8")
    lexer = FSALexer(stream)
    tokens = CommonTokenStream(lexer)
    parser = FSAParser(tokens)
    tree = parser.file_()

    builder = FSABuilder()
    walker = ParseTreeWalker()
    walker.walk(builder, tree)

    automaton = builder.automaton

    # Added normalization and reachability filtering
    normalize_states(automaton)
    automaton.is_dfa = is_dfa(automaton)
    reachable = reachable_states(automaton)
    automaton.states &= reachable
    automaton.accepting &= reachable
    automaton.transitions = {
        s: automaton.transitions[s]
        for s in automaton.transitions
        if s in reachable
    }
    print_automaton(automaton)

    return automaton
