from antlr4 import *
from isomorphism.generated.FSALexer import FSALexer
from isomorphism.generated.FSAListener import FSAListener
from isomorphism.generated.FSAParser import FSAParser
from isomorphism.automata.automaton import Automaton


class FSABuilder(FSAListener):
    def __init__(self):
        self.automaton = Automaton()

    def exitStateEntry(self, ctx):
        self.automaton.states.add(ctx.ID().getText())

    def exitStart(self, ctx):
        self.automaton.start = ctx.ID().getText()

    def exitAccepting(self, ctx):
        for id_ctx in ctx.ID():
            self.automaton.accepting.add(id_ctx.getText())

    def exitTransition(self, ctx):
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
