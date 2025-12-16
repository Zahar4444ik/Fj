# Generated from C:/Users/Захар/Desktop/tuke/bakalarska/fj_assignments/isomorphism/FSA.g4 by ANTLR 4.13.2
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
        4,1,16,73,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,5,1,29,
        8,1,10,1,12,1,32,9,1,1,1,1,1,1,2,1,2,1,2,3,2,39,8,2,1,3,1,3,1,3,
        1,3,1,4,1,4,1,4,1,4,1,4,1,4,5,4,51,8,4,10,4,12,4,54,9,4,1,4,1,4,
        1,5,1,5,1,5,4,5,61,8,5,11,5,12,5,62,1,6,1,6,1,6,1,6,1,6,1,6,1,7,
        1,7,1,7,0,0,8,0,2,4,6,8,10,12,14,0,1,1,0,12,14,68,0,16,1,0,0,0,2,
        22,1,0,0,0,4,35,1,0,0,0,6,40,1,0,0,0,8,44,1,0,0,0,10,57,1,0,0,0,
        12,64,1,0,0,0,14,70,1,0,0,0,16,17,3,2,1,0,17,18,3,6,3,0,18,19,3,
        8,4,0,19,20,3,10,5,0,20,21,5,0,0,1,21,1,1,0,0,0,22,23,5,1,0,0,23,
        24,5,5,0,0,24,25,5,7,0,0,25,30,3,4,2,0,26,27,5,6,0,0,27,29,3,4,2,
        0,28,26,1,0,0,0,29,32,1,0,0,0,30,28,1,0,0,0,30,31,1,0,0,0,31,33,
        1,0,0,0,32,30,1,0,0,0,33,34,5,8,0,0,34,3,1,0,0,0,35,38,5,13,0,0,
        36,37,5,9,0,0,37,39,5,15,0,0,38,36,1,0,0,0,38,39,1,0,0,0,39,5,1,
        0,0,0,40,41,5,2,0,0,41,42,5,5,0,0,42,43,5,13,0,0,43,7,1,0,0,0,44,
        45,5,3,0,0,45,46,5,5,0,0,46,47,5,7,0,0,47,52,5,13,0,0,48,49,5,6,
        0,0,49,51,5,13,0,0,50,48,1,0,0,0,51,54,1,0,0,0,52,50,1,0,0,0,52,
        53,1,0,0,0,53,55,1,0,0,0,54,52,1,0,0,0,55,56,5,8,0,0,56,9,1,0,0,
        0,57,58,5,4,0,0,58,60,5,5,0,0,59,61,3,12,6,0,60,59,1,0,0,0,61,62,
        1,0,0,0,62,60,1,0,0,0,62,63,1,0,0,0,63,11,1,0,0,0,64,65,5,13,0,0,
        65,66,5,10,0,0,66,67,3,14,7,0,67,68,5,11,0,0,68,69,5,13,0,0,69,13,
        1,0,0,0,70,71,7,0,0,0,71,15,1,0,0,0,4,30,38,52,62
    ]

class FSAParser ( Parser ):

    grammarFileName = "FSA.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'states'", "'start'", "'accepting'", 
                     "'transitions'", "':'", "','", "'{'", "'}'", "'='", 
                     "'-'", "'->'", "<INVALID>", "<INVALID>", "'\\u03B5'" ]

    symbolicNames = [ "<INVALID>", "STATES", "START", "ACCEPTING", "TRANSITIONS", 
                      "COLON", "COMMA", "LBRACE", "RBRACE", "EQUAL", "DASH", 
                      "ARROW", "SYMBOL", "ID", "EPSILON", "STRING", "WS" ]

    RULE_file = 0
    RULE_states = 1
    RULE_stateEntry = 2
    RULE_start = 3
    RULE_accepting = 4
    RULE_transitions = 5
    RULE_transition = 6
    RULE_symbol = 7

    ruleNames =  [ "file", "states", "stateEntry", "start", "accepting", 
                   "transitions", "transition", "symbol" ]

    EOF = Token.EOF
    STATES=1
    START=2
    ACCEPTING=3
    TRANSITIONS=4
    COLON=5
    COMMA=6
    LBRACE=7
    RBRACE=8
    EQUAL=9
    DASH=10
    ARROW=11
    SYMBOL=12
    ID=13
    EPSILON=14
    STRING=15
    WS=16

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
            self.state = 16
            self.states()
            self.state = 17
            self.start()
            self.state = 18
            self.accepting()
            self.state = 19
            self.transitions()
            self.state = 20
            self.match(FSAParser.EOF)
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
        self.enterRule(localctx, 2, self.RULE_states)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 22
            self.match(FSAParser.STATES)
            self.state = 23
            self.match(FSAParser.COLON)
            self.state = 24
            self.match(FSAParser.LBRACE)
            self.state = 25
            self.stateEntry()
            self.state = 30
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==6:
                self.state = 26
                self.match(FSAParser.COMMA)
                self.state = 27
                self.stateEntry()
                self.state = 32
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 33
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
        self.enterRule(localctx, 4, self.RULE_stateEntry)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 35
            self.match(FSAParser.ID)
            self.state = 38
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==9:
                self.state = 36
                self.match(FSAParser.EQUAL)
                self.state = 37
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
        self.enterRule(localctx, 6, self.RULE_start)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 40
            self.match(FSAParser.START)
            self.state = 41
            self.match(FSAParser.COLON)
            self.state = 42
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
        self.enterRule(localctx, 8, self.RULE_accepting)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 44
            self.match(FSAParser.ACCEPTING)
            self.state = 45
            self.match(FSAParser.COLON)
            self.state = 46
            self.match(FSAParser.LBRACE)
            self.state = 47
            self.match(FSAParser.ID)
            self.state = 52
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==6:
                self.state = 48
                self.match(FSAParser.COMMA)
                self.state = 49
                self.match(FSAParser.ID)
                self.state = 54
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 55
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

        def transition(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FSAParser.TransitionContext)
            else:
                return self.getTypedRuleContext(FSAParser.TransitionContext,i)


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
        self.enterRule(localctx, 10, self.RULE_transitions)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 57
            self.match(FSAParser.TRANSITIONS)
            self.state = 58
            self.match(FSAParser.COLON)
            self.state = 60 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 59
                self.transition()
                self.state = 62 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==13):
                    break

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
        self.enterRule(localctx, 12, self.RULE_transition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 64
            self.match(FSAParser.ID)
            self.state = 65
            self.match(FSAParser.DASH)
            self.state = 66
            self.symbol()
            self.state = 67
            self.match(FSAParser.ARROW)
            self.state = 68
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
        self.enterRule(localctx, 14, self.RULE_symbol)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 70
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 28672) != 0)):
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





