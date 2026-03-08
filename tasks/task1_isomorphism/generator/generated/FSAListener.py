# Generated from C:/Users/Захар/Desktop/tuke/bakalarska/fj_assignments/tasks/task1_isomorphism/generator/grammar/FSA.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .FSAParser import FSAParser
else:
    from FSAParser import FSAParser

# This class defines a complete listener for a parse tree produced by FSAParser.
class FSAListener(ParseTreeListener):

    # Enter a parse tree produced by FSAParser#file.
    def enterFile(self, ctx:FSAParser.FileContext):
        pass

    # Exit a parse tree produced by FSAParser#file.
    def exitFile(self, ctx:FSAParser.FileContext):
        pass


    # Enter a parse tree produced by FSAParser#section.
    def enterSection(self, ctx:FSAParser.SectionContext):
        pass

    # Exit a parse tree produced by FSAParser#section.
    def exitSection(self, ctx:FSAParser.SectionContext):
        pass


    # Enter a parse tree produced by FSAParser#alphabet.
    def enterAlphabet(self, ctx:FSAParser.AlphabetContext):
        pass

    # Exit a parse tree produced by FSAParser#alphabet.
    def exitAlphabet(self, ctx:FSAParser.AlphabetContext):
        pass


    # Enter a parse tree produced by FSAParser#states.
    def enterStates(self, ctx:FSAParser.StatesContext):
        pass

    # Exit a parse tree produced by FSAParser#states.
    def exitStates(self, ctx:FSAParser.StatesContext):
        pass


    # Enter a parse tree produced by FSAParser#stateEntry.
    def enterStateEntry(self, ctx:FSAParser.StateEntryContext):
        pass

    # Exit a parse tree produced by FSAParser#stateEntry.
    def exitStateEntry(self, ctx:FSAParser.StateEntryContext):
        pass


    # Enter a parse tree produced by FSAParser#start.
    def enterStart(self, ctx:FSAParser.StartContext):
        pass

    # Exit a parse tree produced by FSAParser#start.
    def exitStart(self, ctx:FSAParser.StartContext):
        pass


    # Enter a parse tree produced by FSAParser#accepting.
    def enterAccepting(self, ctx:FSAParser.AcceptingContext):
        pass

    # Exit a parse tree produced by FSAParser#accepting.
    def exitAccepting(self, ctx:FSAParser.AcceptingContext):
        pass


    # Enter a parse tree produced by FSAParser#transitions.
    def enterTransitions(self, ctx:FSAParser.TransitionsContext):
        pass

    # Exit a parse tree produced by FSAParser#transitions.
    def exitTransitions(self, ctx:FSAParser.TransitionsContext):
        pass


    # Enter a parse tree produced by FSAParser#transition.
    def enterTransition(self, ctx:FSAParser.TransitionContext):
        pass

    # Exit a parse tree produced by FSAParser#transition.
    def exitTransition(self, ctx:FSAParser.TransitionContext):
        pass


    # Enter a parse tree produced by FSAParser#symbol.
    def enterSymbol(self, ctx:FSAParser.SymbolContext):
        pass

    # Exit a parse tree produced by FSAParser#symbol.
    def exitSymbol(self, ctx:FSAParser.SymbolContext):
        pass



del FSAParser