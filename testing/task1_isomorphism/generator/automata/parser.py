from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener

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


class FSASyntaxErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(f"line {line}:{column} {msg}")


def parse_fsa(path):
    stream = FileStream(path, encoding="utf-8")
    lexer = FSALexer(stream)

    error_listener = FSASyntaxErrorListener()

    # Remove default stderr listener, attach ours to both lexer and parser
    lexer.removeErrorListeners()
    lexer.addErrorListener(error_listener)

    tokens = CommonTokenStream(lexer)
    parser = FSAParser(tokens)
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)

    tree = parser.file_()

    builder = FSABuilder()
    ParseTreeWalker().walk(builder, tree)

    return builder.automaton, error_listener.errors
