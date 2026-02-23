# Generated from C:/Users/Захар/Desktop/tuke/bakalarska/fj_assignments/tasks/task1_isomorphism/generator/grammar/FSA.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,17,107,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,
        1,1,1,5,1,32,8,1,10,1,12,1,35,9,1,1,1,3,1,38,8,1,1,1,1,1,1,2,1,2,
        1,2,1,2,1,2,1,2,5,2,48,8,2,10,2,12,2,51,9,2,1,2,3,2,54,8,2,1,2,1,
        2,1,3,1,3,1,3,3,3,61,8,3,1,4,1,4,1,4,1,4,1,5,1,5,1,5,1,5,1,5,1,5,
        5,5,73,8,5,10,5,12,5,76,9,5,1,5,3,5,79,8,5,1,5,1,5,1,6,1,6,1,6,1,
        6,1,6,1,6,5,6,89,8,6,10,6,12,6,92,9,6,1,6,3,6,95,8,6,1,6,1,6,1,7,
        1,7,1,7,1,7,1,7,1,7,1,8,1,8,1,8,0,0,9,0,2,4,6,8,10,12,14,16,0,1,
        1,0,13,15,106,0,18,1,0,0,0,2,25,1,0,0,0,4,41,1,0,0,0,6,57,1,0,0,
        0,8,62,1,0,0,0,10,66,1,0,0,0,12,82,1,0,0,0,14,98,1,0,0,0,16,104,
        1,0,0,0,18,19,3,2,1,0,19,20,3,4,2,0,20,21,3,8,4,0,21,22,3,10,5,0,
        22,23,3,12,6,0,23,24,5,0,0,1,24,1,1,0,0,0,25,26,5,1,0,0,26,27,5,
        6,0,0,27,28,5,8,0,0,28,33,3,16,8,0,29,30,5,7,0,0,30,32,3,16,8,0,
        31,29,1,0,0,0,32,35,1,0,0,0,33,31,1,0,0,0,33,34,1,0,0,0,34,37,1,
        0,0,0,35,33,1,0,0,0,36,38,5,7,0,0,37,36,1,0,0,0,37,38,1,0,0,0,38,
        39,1,0,0,0,39,40,5,9,0,0,40,3,1,0,0,0,41,42,5,2,0,0,42,43,5,6,0,
        0,43,44,5,8,0,0,44,49,3,6,3,0,45,46,5,7,0,0,46,48,3,6,3,0,47,45,
        1,0,0,0,48,51,1,0,0,0,49,47,1,0,0,0,49,50,1,0,0,0,50,53,1,0,0,0,
        51,49,1,0,0,0,52,54,5,7,0,0,53,52,1,0,0,0,53,54,1,0,0,0,54,55,1,
        0,0,0,55,56,5,9,0,0,56,5,1,0,0,0,57,60,5,14,0,0,58,59,5,10,0,0,59,
        61,5,16,0,0,60,58,1,0,0,0,60,61,1,0,0,0,61,7,1,0,0,0,62,63,5,3,0,
        0,63,64,5,6,0,0,64,65,5,14,0,0,65,9,1,0,0,0,66,67,5,4,0,0,67,68,
        5,6,0,0,68,69,5,8,0,0,69,74,5,14,0,0,70,71,5,7,0,0,71,73,5,14,0,
        0,72,70,1,0,0,0,73,76,1,0,0,0,74,72,1,0,0,0,74,75,1,0,0,0,75,78,
        1,0,0,0,76,74,1,0,0,0,77,79,5,7,0,0,78,77,1,0,0,0,78,79,1,0,0,0,
        79,80,1,0,0,0,80,81,5,9,0,0,81,11,1,0,0,0,82,83,5,5,0,0,83,84,5,
        6,0,0,84,85,5,8,0,0,85,90,3,14,7,0,86,87,5,7,0,0,87,89,3,14,7,0,
        88,86,1,0,0,0,89,92,1,0,0,0,90,88,1,0,0,0,90,91,1,0,0,0,91,94,1,
        0,0,0,92,90,1,0,0,0,93,95,5,7,0,0,94,93,1,0,0,0,94,95,1,0,0,0,95,
        96,1,0,0,0,96,97,5,9,0,0,97,13,1,0,0,0,98,99,5,14,0,0,99,100,5,11,
        0,0,100,101,3,16,8,0,101,102,5,12,0,0,102,103,5,14,0,0,103,15,1,
        0,0,0,104,105,7,0,0,0,105,17,1,0,0,0,9,33,37,49,53,60,74,78,90,94
    ]

class FSAParser ( Parser ):

    grammarFileName = "FSA.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'alphabet'", "'states'", "'initial_state'", 
                     "'accepting_states'", "'transitions'", "':'", "','", 
                     "'{'", "'}'", "'='", "'-'", "'->'" ]

    symbolicNames = [ "<INVALID>", "ALPHABET", "STATES", "START", "ACCEPTING", 
                      "TRANSITIONS", "COLON", "COMMA", "LBRACE", "RBRACE", 
                      "EQUAL", "DASH", "ARROW", "SYMBOL", "ID", "EPSILON", 
                      "STRING", "WS" ]

    RULE_file = 0
    RULE_alphabet = 1
    RULE_states = 2
    RULE_stateEntry = 3
    RULE_start = 4
    RULE_accepting = 5
    RULE_transitions = 6
    RULE_transition = 7
    RULE_symbol = 8

    ruleNames =  [ "file", "alphabet", "states", "stateEntry", "start", 
                   "accepting", "transitions", "transition", "symbol" ]

    EOF = Token.EOF
    ALPHABET=1
    STATES=2
    START=3
    ACCEPTING=4
    TRANSITIONS=5
    COLON=6
    COMMA=7
    LBRACE=8
    RBRACE=9
    EQUAL=10
    DASH=11
    ARROW=12
    SYMBOL=13
    ID=14
    EPSILON=15
    STRING=16
    WS=17

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class FileContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def alphabet(self):
            return self.getTypedRuleContext(FSAParser.AlphabetContext,0)


        def states(self):
            return self.getTypedRuleContext(FSAParser.StatesContext,0)


        def start(self):
            return self.getTypedRuleContext(FSAParser.StartContext,0)


        def accepting(self):
            return self.getTypedRuleContext(FSAParser.AcceptingContext,0)


        def transitions(self):
            return self.getTypedRuleContext(FSAParser.TransitionsContext,0)


        def EOF(self):
            return self.getToken(FSAParser.EOF, 0)

        def getRuleIndex(self):
            return FSAParser.RULE_file

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFile" ):
                listener.enterFile(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFile" ):
                listener.exitFile(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFile" ):
                return visitor.visitFile(self)
            else:
                return visitor.visitChildren(self)




    def file_(self):

        localctx = FSAParser.FileContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_file)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 18
            self.alphabet()
            self.state = 19
            self.states()
            self.state = 20
            self.start()
            self.state = 21
            self.accepting()
            self.state = 22
            self.transitions()
            self.state = 23
            self.match(FSAParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AlphabetContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ALPHABET(self):
            return self.getToken(FSAParser.ALPHABET, 0)

        def COLON(self):
            return self.getToken(FSAParser.COLON, 0)

        def LBRACE(self):
            return self.getToken(FSAParser.LBRACE, 0)

        def symbol(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FSAParser.SymbolContext)
            else:
                return self.getTypedRuleContext(FSAParser.SymbolContext,i)


        def RBRACE(self):
            return self.getToken(FSAParser.RBRACE, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(FSAParser.COMMA)
            else:
                return self.getToken(FSAParser.COMMA, i)

        def getRuleIndex(self):
            return FSAParser.RULE_alphabet

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAlphabet" ):
                listener.enterAlphabet(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAlphabet" ):
                listener.exitAlphabet(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAlphabet" ):
                return visitor.visitAlphabet(self)
            else:
                return visitor.visitChildren(self)




    def alphabet(self):

        localctx = FSAParser.AlphabetContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_alphabet)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 25
            self.match(FSAParser.ALPHABET)
            self.state = 26
            self.match(FSAParser.COLON)
            self.state = 27
            self.match(FSAParser.LBRACE)
            self.state = 28
            self.symbol()
            self.state = 33
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,0,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 29
                    self.match(FSAParser.COMMA)
                    self.state = 30
                    self.symbol() 
                self.state = 35
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,0,self._ctx)

            self.state = 37
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==7:
                self.state = 36
                self.match(FSAParser.COMMA)


            self.state = 39
            self.match(FSAParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatesContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STATES(self):
            return self.getToken(FSAParser.STATES, 0)

        def COLON(self):
            return self.getToken(FSAParser.COLON, 0)

        def LBRACE(self):
            return self.getToken(FSAParser.LBRACE, 0)

        def stateEntry(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FSAParser.StateEntryContext)
            else:
                return self.getTypedRuleContext(FSAParser.StateEntryContext,i)


        def RBRACE(self):
            return self.getToken(FSAParser.RBRACE, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(FSAParser.COMMA)
            else:
                return self.getToken(FSAParser.COMMA, i)

        def getRuleIndex(self):
            return FSAParser.RULE_states

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStates" ):
                listener.enterStates(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStates" ):
                listener.exitStates(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStates" ):
                return visitor.visitStates(self)
            else:
                return visitor.visitChildren(self)




    def states(self):

        localctx = FSAParser.StatesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_states)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 41
            self.match(FSAParser.STATES)
            self.state = 42
            self.match(FSAParser.COLON)
            self.state = 43
            self.match(FSAParser.LBRACE)
            self.state = 44
            self.stateEntry()
            self.state = 49
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 45
                    self.match(FSAParser.COMMA)
                    self.state = 46
                    self.stateEntry() 
                self.state = 51
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

            self.state = 53
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==7:
                self.state = 52
                self.match(FSAParser.COMMA)


            self.state = 55
            self.match(FSAParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StateEntryContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(FSAParser.ID, 0)

        def EQUAL(self):
            return self.getToken(FSAParser.EQUAL, 0)

        def STRING(self):
            return self.getToken(FSAParser.STRING, 0)

        def getRuleIndex(self):
            return FSAParser.RULE_stateEntry

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStateEntry" ):
                listener.enterStateEntry(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStateEntry" ):
                listener.exitStateEntry(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStateEntry" ):
                return visitor.visitStateEntry(self)
            else:
                return visitor.visitChildren(self)




    def stateEntry(self):

        localctx = FSAParser.StateEntryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_stateEntry)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 57
            self.match(FSAParser.ID)
            self.state = 60
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==10:
                self.state = 58
                self.match(FSAParser.EQUAL)
                self.state = 59
                self.match(FSAParser.STRING)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StartContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def START(self):
            return self.getToken(FSAParser.START, 0)

        def COLON(self):
            return self.getToken(FSAParser.COLON, 0)

        def ID(self):
            return self.getToken(FSAParser.ID, 0)

        def getRuleIndex(self):
            return FSAParser.RULE_start

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStart" ):
                listener.enterStart(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStart" ):
                listener.exitStart(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStart" ):
                return visitor.visitStart(self)
            else:
                return visitor.visitChildren(self)




    def start(self):

        localctx = FSAParser.StartContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_start)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 62
            self.match(FSAParser.START)
            self.state = 63
            self.match(FSAParser.COLON)
            self.state = 64
            self.match(FSAParser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AcceptingContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ACCEPTING(self):
            return self.getToken(FSAParser.ACCEPTING, 0)

        def COLON(self):
            return self.getToken(FSAParser.COLON, 0)

        def LBRACE(self):
            return self.getToken(FSAParser.LBRACE, 0)

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(FSAParser.ID)
            else:
                return self.getToken(FSAParser.ID, i)

        def RBRACE(self):
            return self.getToken(FSAParser.RBRACE, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(FSAParser.COMMA)
            else:
                return self.getToken(FSAParser.COMMA, i)

        def getRuleIndex(self):
            return FSAParser.RULE_accepting

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAccepting" ):
                listener.enterAccepting(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAccepting" ):
                listener.exitAccepting(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAccepting" ):
                return visitor.visitAccepting(self)
            else:
                return visitor.visitChildren(self)




    def accepting(self):

        localctx = FSAParser.AcceptingContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_accepting)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 66
            self.match(FSAParser.ACCEPTING)
            self.state = 67
            self.match(FSAParser.COLON)
            self.state = 68
            self.match(FSAParser.LBRACE)
            self.state = 69
            self.match(FSAParser.ID)
            self.state = 74
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,5,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 70
                    self.match(FSAParser.COMMA)
                    self.state = 71
                    self.match(FSAParser.ID) 
                self.state = 76
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,5,self._ctx)

            self.state = 78
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==7:
                self.state = 77
                self.match(FSAParser.COMMA)


            self.state = 80
            self.match(FSAParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TransitionsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TRANSITIONS(self):
            return self.getToken(FSAParser.TRANSITIONS, 0)

        def COLON(self):
            return self.getToken(FSAParser.COLON, 0)

        def LBRACE(self):
            return self.getToken(FSAParser.LBRACE, 0)

        def transition(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FSAParser.TransitionContext)
            else:
                return self.getTypedRuleContext(FSAParser.TransitionContext,i)


        def RBRACE(self):
            return self.getToken(FSAParser.RBRACE, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(FSAParser.COMMA)
            else:
                return self.getToken(FSAParser.COMMA, i)

        def getRuleIndex(self):
            return FSAParser.RULE_transitions

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTransitions" ):
                listener.enterTransitions(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTransitions" ):
                listener.exitTransitions(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTransitions" ):
                return visitor.visitTransitions(self)
            else:
                return visitor.visitChildren(self)




    def transitions(self):

        localctx = FSAParser.TransitionsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_transitions)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 82
            self.match(FSAParser.TRANSITIONS)
            self.state = 83
            self.match(FSAParser.COLON)
            self.state = 84
            self.match(FSAParser.LBRACE)
            self.state = 85
            self.transition()
            self.state = 90
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,7,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 86
                    self.match(FSAParser.COMMA)
                    self.state = 87
                    self.transition() 
                self.state = 92
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,7,self._ctx)

            self.state = 94
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==7:
                self.state = 93
                self.match(FSAParser.COMMA)


            self.state = 96
            self.match(FSAParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TransitionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(FSAParser.ID)
            else:
                return self.getToken(FSAParser.ID, i)

        def DASH(self):
            return self.getToken(FSAParser.DASH, 0)

        def symbol(self):
            return self.getTypedRuleContext(FSAParser.SymbolContext,0)


        def ARROW(self):
            return self.getToken(FSAParser.ARROW, 0)

        def getRuleIndex(self):
            return FSAParser.RULE_transition

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTransition" ):
                listener.enterTransition(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTransition" ):
                listener.exitTransition(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTransition" ):
                return visitor.visitTransition(self)
            else:
                return visitor.visitChildren(self)




    def transition(self):

        localctx = FSAParser.TransitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_transition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 98
            self.match(FSAParser.ID)
            self.state = 99
            self.match(FSAParser.DASH)
            self.state = 100
            self.symbol()
            self.state = 101
            self.match(FSAParser.ARROW)
            self.state = 102
            self.match(FSAParser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SymbolContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYMBOL(self):
            return self.getToken(FSAParser.SYMBOL, 0)

        def ID(self):
            return self.getToken(FSAParser.ID, 0)

        def EPSILON(self):
            return self.getToken(FSAParser.EPSILON, 0)

        def getRuleIndex(self):
            return FSAParser.RULE_symbol

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSymbol" ):
                listener.enterSymbol(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSymbol" ):
                listener.exitSymbol(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSymbol" ):
                return visitor.visitSymbol(self)
            else:
                return visitor.visitChildren(self)




    def symbol(self):

        localctx = FSAParser.SymbolContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_symbol)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 104
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 57344) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





