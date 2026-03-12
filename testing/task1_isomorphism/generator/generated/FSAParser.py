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
        4,1,18,116,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,1,0,4,0,22,8,0,11,0,12,0,23,1,0,1,0,1,
        1,1,1,1,1,1,1,1,1,3,1,33,8,1,1,2,1,2,1,2,1,2,1,2,1,2,5,2,41,8,2,
        10,2,12,2,44,9,2,1,2,3,2,47,8,2,1,2,1,2,1,3,1,3,1,3,1,3,1,3,1,3,
        5,3,57,8,3,10,3,12,3,60,9,3,1,3,3,3,63,8,3,1,3,1,3,1,4,1,4,1,4,3,
        4,70,8,4,1,5,1,5,1,5,1,5,1,6,1,6,1,6,1,6,1,6,1,6,5,6,82,8,6,10,6,
        12,6,85,9,6,1,6,3,6,88,8,6,1,6,1,6,1,7,1,7,1,7,1,7,1,7,1,7,5,7,98,
        8,7,10,7,12,7,101,9,7,1,7,3,7,104,8,7,1,7,1,7,1,8,1,8,1,8,1,8,1,
        8,1,8,1,9,1,9,1,9,0,0,10,0,2,4,6,8,10,12,14,16,18,0,1,1,0,13,15,
        119,0,21,1,0,0,0,2,32,1,0,0,0,4,34,1,0,0,0,6,50,1,0,0,0,8,66,1,0,
        0,0,10,71,1,0,0,0,12,75,1,0,0,0,14,91,1,0,0,0,16,107,1,0,0,0,18,
        113,1,0,0,0,20,22,3,2,1,0,21,20,1,0,0,0,22,23,1,0,0,0,23,21,1,0,
        0,0,23,24,1,0,0,0,24,25,1,0,0,0,25,26,5,0,0,1,26,1,1,0,0,0,27,33,
        3,4,2,0,28,33,3,6,3,0,29,33,3,10,5,0,30,33,3,12,6,0,31,33,3,14,7,
        0,32,27,1,0,0,0,32,28,1,0,0,0,32,29,1,0,0,0,32,30,1,0,0,0,32,31,
        1,0,0,0,33,3,1,0,0,0,34,35,5,1,0,0,35,36,5,6,0,0,36,37,5,8,0,0,37,
        42,3,18,9,0,38,39,5,7,0,0,39,41,3,18,9,0,40,38,1,0,0,0,41,44,1,0,
        0,0,42,40,1,0,0,0,42,43,1,0,0,0,43,46,1,0,0,0,44,42,1,0,0,0,45,47,
        5,7,0,0,46,45,1,0,0,0,46,47,1,0,0,0,47,48,1,0,0,0,48,49,5,9,0,0,
        49,5,1,0,0,0,50,51,5,2,0,0,51,52,5,6,0,0,52,53,5,8,0,0,53,58,3,8,
        4,0,54,55,5,7,0,0,55,57,3,8,4,0,56,54,1,0,0,0,57,60,1,0,0,0,58,56,
        1,0,0,0,58,59,1,0,0,0,59,62,1,0,0,0,60,58,1,0,0,0,61,63,5,7,0,0,
        62,61,1,0,0,0,62,63,1,0,0,0,63,64,1,0,0,0,64,65,5,9,0,0,65,7,1,0,
        0,0,66,69,5,13,0,0,67,68,5,10,0,0,68,70,5,16,0,0,69,67,1,0,0,0,69,
        70,1,0,0,0,70,9,1,0,0,0,71,72,5,3,0,0,72,73,5,6,0,0,73,74,5,13,0,
        0,74,11,1,0,0,0,75,76,5,4,0,0,76,77,5,6,0,0,77,78,5,8,0,0,78,83,
        5,13,0,0,79,80,5,7,0,0,80,82,5,13,0,0,81,79,1,0,0,0,82,85,1,0,0,
        0,83,81,1,0,0,0,83,84,1,0,0,0,84,87,1,0,0,0,85,83,1,0,0,0,86,88,
        5,7,0,0,87,86,1,0,0,0,87,88,1,0,0,0,88,89,1,0,0,0,89,90,5,9,0,0,
        90,13,1,0,0,0,91,92,5,5,0,0,92,93,5,6,0,0,93,94,5,8,0,0,94,99,3,
        16,8,0,95,96,5,7,0,0,96,98,3,16,8,0,97,95,1,0,0,0,98,101,1,0,0,0,
        99,97,1,0,0,0,99,100,1,0,0,0,100,103,1,0,0,0,101,99,1,0,0,0,102,
        104,5,7,0,0,103,102,1,0,0,0,103,104,1,0,0,0,104,105,1,0,0,0,105,
        106,5,9,0,0,106,15,1,0,0,0,107,108,5,13,0,0,108,109,5,11,0,0,109,
        110,3,18,9,0,110,111,5,12,0,0,111,112,5,13,0,0,112,17,1,0,0,0,113,
        114,7,0,0,0,114,19,1,0,0,0,11,23,32,42,46,58,62,69,83,87,99,103
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
                      "EQUAL", "DASH", "ARROW", "ID", "SYMBOL", "EPSILON", 
                      "STRING", "COMMENT", "WS" ]

    RULE_file = 0
    RULE_section = 1
    RULE_alphabet = 2
    RULE_states = 3
    RULE_stateEntry = 4
    RULE_start = 5
    RULE_accepting = 6
    RULE_transitions = 7
    RULE_transition = 8
    RULE_symbol = 9

    ruleNames =  [ "file", "section", "alphabet", "states", "stateEntry", 
                   "start", "accepting", "transitions", "transition", "symbol" ]

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
    ID=13
    SYMBOL=14
    EPSILON=15
    STRING=16
    COMMENT=17
    WS=18

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

        def EOF(self):
            return self.getToken(FSAParser.EOF, 0)

        def section(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FSAParser.SectionContext)
            else:
                return self.getTypedRuleContext(FSAParser.SectionContext,i)


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
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 21 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 20
                self.section()
                self.state = 23 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 62) != 0)):
                    break

            self.state = 25
            self.match(FSAParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SectionContext(ParserRuleContext):
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


        def getRuleIndex(self):
            return FSAParser.RULE_section

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSection" ):
                listener.enterSection(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSection" ):
                listener.exitSection(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSection" ):
                return visitor.visitSection(self)
            else:
                return visitor.visitChildren(self)




    def section(self):

        localctx = FSAParser.SectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_section)
        try:
            self.state = 32
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 27
                self.alphabet()
                pass
            elif token in [2]:
                self.enterOuterAlt(localctx, 2)
                self.state = 28
                self.states()
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 3)
                self.state = 29
                self.start()
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 4)
                self.state = 30
                self.accepting()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 5)
                self.state = 31
                self.transitions()
                pass
            else:
                raise NoViableAltException(self)

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
        self.enterRule(localctx, 4, self.RULE_alphabet)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 34
            self.match(FSAParser.ALPHABET)
            self.state = 35
            self.match(FSAParser.COLON)
            self.state = 36
            self.match(FSAParser.LBRACE)
            self.state = 37
            self.symbol()
            self.state = 42
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 38
                    self.match(FSAParser.COMMA)
                    self.state = 39
                    self.symbol() 
                self.state = 44
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

            self.state = 46
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==7:
                self.state = 45
                self.match(FSAParser.COMMA)


            self.state = 48
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
        self.enterRule(localctx, 6, self.RULE_states)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 50
            self.match(FSAParser.STATES)
            self.state = 51
            self.match(FSAParser.COLON)
            self.state = 52
            self.match(FSAParser.LBRACE)
            self.state = 53
            self.stateEntry()
            self.state = 58
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,4,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 54
                    self.match(FSAParser.COMMA)
                    self.state = 55
                    self.stateEntry() 
                self.state = 60
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,4,self._ctx)

            self.state = 62
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==7:
                self.state = 61
                self.match(FSAParser.COMMA)


            self.state = 64
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
        self.enterRule(localctx, 8, self.RULE_stateEntry)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 66
            self.match(FSAParser.ID)
            self.state = 69
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==10:
                self.state = 67
                self.match(FSAParser.EQUAL)
                self.state = 68
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
        self.enterRule(localctx, 10, self.RULE_start)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 71
            self.match(FSAParser.START)
            self.state = 72
            self.match(FSAParser.COLON)
            self.state = 73
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
        self.enterRule(localctx, 12, self.RULE_accepting)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 75
            self.match(FSAParser.ACCEPTING)
            self.state = 76
            self.match(FSAParser.COLON)
            self.state = 77
            self.match(FSAParser.LBRACE)
            self.state = 78
            self.match(FSAParser.ID)
            self.state = 83
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,7,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 79
                    self.match(FSAParser.COMMA)
                    self.state = 80
                    self.match(FSAParser.ID) 
                self.state = 85
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,7,self._ctx)

            self.state = 87
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==7:
                self.state = 86
                self.match(FSAParser.COMMA)


            self.state = 89
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
        self.enterRule(localctx, 14, self.RULE_transitions)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 91
            self.match(FSAParser.TRANSITIONS)
            self.state = 92
            self.match(FSAParser.COLON)
            self.state = 93
            self.match(FSAParser.LBRACE)
            self.state = 94
            self.transition()
            self.state = 99
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,9,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 95
                    self.match(FSAParser.COMMA)
                    self.state = 96
                    self.transition() 
                self.state = 101
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,9,self._ctx)

            self.state = 103
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==7:
                self.state = 102
                self.match(FSAParser.COMMA)


            self.state = 105
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
        self.enterRule(localctx, 16, self.RULE_transition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 107
            self.match(FSAParser.ID)
            self.state = 108
            self.match(FSAParser.DASH)
            self.state = 109
            self.symbol()
            self.state = 110
            self.match(FSAParser.ARROW)
            self.state = 111
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
        self.enterRule(localctx, 18, self.RULE_symbol)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 113
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





