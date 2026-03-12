# Generated from C:/Users/Захар/Desktop/tuke/bakalarska/fj_assignments/tasks/task1_isomorphism/generator/grammar/FSA.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .FSAParser import FSAParser
else:
    from FSAParser import FSAParser

# This class defines a complete generic visitor for a parse tree produced by FSAParser.

class FSAVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by FSAParser#file.
    def visitFile(self, ctx:FSAParser.FileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FSAParser#section.
    def visitSection(self, ctx:FSAParser.SectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FSAParser#alphabet.
    def visitAlphabet(self, ctx:FSAParser.AlphabetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FSAParser#states.
    def visitStates(self, ctx:FSAParser.StatesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FSAParser#stateEntry.
    def visitStateEntry(self, ctx:FSAParser.StateEntryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FSAParser#start.
    def visitStart(self, ctx:FSAParser.StartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FSAParser#accepting.
    def visitAccepting(self, ctx:FSAParser.AcceptingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FSAParser#transitions.
    def visitTransitions(self, ctx:FSAParser.TransitionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FSAParser#transition.
    def visitTransition(self, ctx:FSAParser.TransitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FSAParser#symbol.
    def visitSymbol(self, ctx:FSAParser.SymbolContext):
        return self.visitChildren(ctx)



del FSAParser