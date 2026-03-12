from antlr4 import *
from testing.task1_isomorphism.generator.generated.FSALexer import FSALexer
from testing.task1_isomorphism.generator.generated.FSAListener import FSAListener
from testing.task1_isomorphism.generator.generated.FSAParser import FSAParser
from testing.task1_isomorphism.generator.automata.automaton import Automaton


class FSABuilder(FSAListener):
    def __init__(self):
        self.automaton = Automaton()

    def exitAlphabet(self, ctx):
        for sym_ctx in ctx.symbol():
            self.automaton.alphabet.add(sym_ctx.getText())

    def exitStateEntry(self, ctx):
        state = ctx.ID().getText()
        self.automaton.states.add(state)

        if ctx.STRING() is not None:
            annotation = ctx.STRING().getText()[1:-1]
            self.automaton.annotations[state] = annotation

    def exitStart(self, ctx):
        self.automaton.start = ctx.ID().getText()

    def exitAccepting(self, ctx):
        for id_ctx in ctx.ID():
            self.automaton.accepting.add(id_ctx.getText())

    def exitTransition(self, ctx):
        if ctx.ID(0) is None or ctx.ID(1) is None:
            raise ValueError(f"Invalid transition syntax: {ctx.getText()}")

        src = ctx.ID(0).getText()
        sym = ctx.symbol().getText()
        dst = ctx.ID(1).getText()

        self.automaton.transitions[src][sym].add(dst)


def parse_fsa(path):
    stream = FileStream(path, encoding="utf-8")
    lexer = FSALexer(stream)
    tokens = CommonTokenStream(lexer)
    parser = FSAParser(tokens)
    tree = parser.file_()

    builder = FSABuilder()
    ParseTreeWalker().walk(builder, tree)

    return builder.automaton
