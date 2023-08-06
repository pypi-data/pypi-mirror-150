# Generated from mongoengine_dsl/lexer/MongoEngineDSL.g4 by ANTLR 4.10.1
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
        4,1,24,68,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,1,0,1,
        0,1,1,1,1,1,1,1,1,1,1,1,1,3,1,21,8,1,1,1,1,1,1,1,1,1,1,1,1,1,5,1,
        29,8,1,10,1,12,1,32,9,1,1,2,1,2,1,2,1,2,1,3,1,3,1,3,5,3,41,8,3,10,
        3,12,3,44,9,3,1,4,1,4,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,3,
        5,58,8,5,4,5,60,8,5,11,5,12,5,61,1,5,1,5,3,5,66,8,5,1,5,0,1,2,6,
        0,2,4,6,8,10,0,1,1,0,7,14,74,0,12,1,0,0,0,2,20,1,0,0,0,4,33,1,0,
        0,0,6,37,1,0,0,0,8,45,1,0,0,0,10,65,1,0,0,0,12,13,3,2,1,0,13,1,1,
        0,0,0,14,15,6,1,-1,0,15,21,3,4,2,0,16,17,5,1,0,0,17,18,3,2,1,0,18,
        19,5,2,0,0,19,21,1,0,0,0,20,14,1,0,0,0,20,16,1,0,0,0,21,30,1,0,0,
        0,22,23,10,4,0,0,23,24,5,5,0,0,24,29,3,2,1,5,25,26,10,3,0,0,26,27,
        5,6,0,0,27,29,3,2,1,4,28,22,1,0,0,0,28,25,1,0,0,0,29,32,1,0,0,0,
        30,28,1,0,0,0,30,31,1,0,0,0,31,3,1,0,0,0,32,30,1,0,0,0,33,34,3,6,
        3,0,34,35,3,8,4,0,35,36,3,10,5,0,36,5,1,0,0,0,37,42,5,19,0,0,38,
        39,5,3,0,0,39,41,5,19,0,0,40,38,1,0,0,0,41,44,1,0,0,0,42,40,1,0,
        0,0,42,43,1,0,0,0,43,7,1,0,0,0,44,42,1,0,0,0,45,46,7,0,0,0,46,9,
        1,0,0,0,47,66,5,15,0,0,48,66,5,16,0,0,49,66,5,17,0,0,50,66,5,18,
        0,0,51,66,5,20,0,0,52,66,5,21,0,0,53,66,5,19,0,0,54,59,5,22,0,0,
        55,57,3,10,5,0,56,58,5,4,0,0,57,56,1,0,0,0,57,58,1,0,0,0,58,60,1,
        0,0,0,59,55,1,0,0,0,60,61,1,0,0,0,61,59,1,0,0,0,61,62,1,0,0,0,62,
        63,1,0,0,0,63,64,5,23,0,0,64,66,1,0,0,0,65,47,1,0,0,0,65,48,1,0,
        0,0,65,49,1,0,0,0,65,50,1,0,0,0,65,51,1,0,0,0,65,52,1,0,0,0,65,53,
        1,0,0,0,65,54,1,0,0,0,66,11,1,0,0,0,7,20,28,30,42,57,61,65
    ]

class MongoEngineDSLParser ( Parser ):

    grammarFileName = "MongoEngineDSL.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "'.'", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "'!='", "'<'", "'<='", "'>'", 
                     "'>='", "'@'", "'!@'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "DOT", "COMMA", 
                      "AND", "OR", "EQ", "NE", "LT", "LE", "GT", "GE", "IN", 
                      "NIN", "BOOL", "INT", "DOUBLE", "QSTR", "TOKEN", "WILDCARD", 
                      "DENIED", "ARR_LPOS", "ARR_RPOS", "WS" ]

    RULE_process = 0
    RULE_expression = 1
    RULE_filterexpr = 2
    RULE_field = 3
    RULE_operator = 4
    RULE_value = 5

    ruleNames =  [ "process", "expression", "filterexpr", "field", "operator", 
                   "value" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    DOT=3
    COMMA=4
    AND=5
    OR=6
    EQ=7
    NE=8
    LT=9
    LE=10
    GT=11
    GE=12
    IN=13
    NIN=14
    BOOL=15
    INT=16
    DOUBLE=17
    QSTR=18
    TOKEN=19
    WILDCARD=20
    DENIED=21
    ARR_LPOS=22
    ARR_RPOS=23
    WS=24

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.10.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProcessContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(MongoEngineDSLParser.ExpressionContext,0)


        def getRuleIndex(self):
            return MongoEngineDSLParser.RULE_process

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProcess" ):
                listener.enterProcess(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProcess" ):
                listener.exitProcess(self)




    def process(self):

        localctx = MongoEngineDSLParser.ProcessContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_process)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 12
            self.expression(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return MongoEngineDSLParser.RULE_expression

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class BracketExpressionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MongoEngineDSLParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expression(self):
            return self.getTypedRuleContext(MongoEngineDSLParser.ExpressionContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBracketExpression" ):
                listener.enterBracketExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBracketExpression" ):
                listener.exitBracketExpression(self)


    class AndExpressionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MongoEngineDSLParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MongoEngineDSLParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(MongoEngineDSLParser.ExpressionContext,i)

        def AND(self):
            return self.getToken(MongoEngineDSLParser.AND, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAndExpression" ):
                listener.enterAndExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAndExpression" ):
                listener.exitAndExpression(self)


    class FilterExpressionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MongoEngineDSLParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def filterexpr(self):
            return self.getTypedRuleContext(MongoEngineDSLParser.FilterexprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFilterExpression" ):
                listener.enterFilterExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFilterExpression" ):
                listener.exitFilterExpression(self)


    class OrExpressionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MongoEngineDSLParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MongoEngineDSLParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(MongoEngineDSLParser.ExpressionContext,i)

        def OR(self):
            return self.getToken(MongoEngineDSLParser.OR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOrExpression" ):
                listener.enterOrExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOrExpression" ):
                listener.exitOrExpression(self)



    def expression(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = MongoEngineDSLParser.ExpressionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 2
        self.enterRecursionRule(localctx, 2, self.RULE_expression, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 20
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [MongoEngineDSLParser.TOKEN]:
                localctx = MongoEngineDSLParser.FilterExpressionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 15
                self.filterexpr()
                pass
            elif token in [MongoEngineDSLParser.T__0]:
                localctx = MongoEngineDSLParser.BracketExpressionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 16
                self.match(MongoEngineDSLParser.T__0)
                self.state = 17
                self.expression(0)
                self.state = 18
                self.match(MongoEngineDSLParser.T__1)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 30
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 28
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
                    if la_ == 1:
                        localctx = MongoEngineDSLParser.AndExpressionContext(self, MongoEngineDSLParser.ExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 22
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 23
                        self.match(MongoEngineDSLParser.AND)
                        self.state = 24
                        self.expression(5)
                        pass

                    elif la_ == 2:
                        localctx = MongoEngineDSLParser.OrExpressionContext(self, MongoEngineDSLParser.ExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 25
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 26
                        self.match(MongoEngineDSLParser.OR)
                        self.state = 27
                        self.expression(4)
                        pass

             
                self.state = 32
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class FilterexprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def field(self):
            return self.getTypedRuleContext(MongoEngineDSLParser.FieldContext,0)


        def operator(self):
            return self.getTypedRuleContext(MongoEngineDSLParser.OperatorContext,0)


        def value(self):
            return self.getTypedRuleContext(MongoEngineDSLParser.ValueContext,0)


        def getRuleIndex(self):
            return MongoEngineDSLParser.RULE_filterexpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFilterexpr" ):
                listener.enterFilterexpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFilterexpr" ):
                listener.exitFilterexpr(self)




    def filterexpr(self):

        localctx = MongoEngineDSLParser.FilterexprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_filterexpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 33
            self.field()
            self.state = 34
            self.operator()
            self.state = 35
            self.value()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FieldContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TOKEN(self, i:int=None):
            if i is None:
                return self.getTokens(MongoEngineDSLParser.TOKEN)
            else:
                return self.getToken(MongoEngineDSLParser.TOKEN, i)

        def DOT(self, i:int=None):
            if i is None:
                return self.getTokens(MongoEngineDSLParser.DOT)
            else:
                return self.getToken(MongoEngineDSLParser.DOT, i)

        def getRuleIndex(self):
            return MongoEngineDSLParser.RULE_field

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField" ):
                listener.enterField(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField" ):
                listener.exitField(self)




    def field(self):

        localctx = MongoEngineDSLParser.FieldContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_field)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 37
            self.match(MongoEngineDSLParser.TOKEN)
            self.state = 42
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==MongoEngineDSLParser.DOT:
                self.state = 38
                self.match(MongoEngineDSLParser.DOT)
                self.state = 39
                self.match(MongoEngineDSLParser.TOKEN)
                self.state = 44
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OperatorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LE(self):
            return self.getToken(MongoEngineDSLParser.LE, 0)

        def GE(self):
            return self.getToken(MongoEngineDSLParser.GE, 0)

        def NE(self):
            return self.getToken(MongoEngineDSLParser.NE, 0)

        def LT(self):
            return self.getToken(MongoEngineDSLParser.LT, 0)

        def GT(self):
            return self.getToken(MongoEngineDSLParser.GT, 0)

        def EQ(self):
            return self.getToken(MongoEngineDSLParser.EQ, 0)

        def IN(self):
            return self.getToken(MongoEngineDSLParser.IN, 0)

        def NIN(self):
            return self.getToken(MongoEngineDSLParser.NIN, 0)

        def getRuleIndex(self):
            return MongoEngineDSLParser.RULE_operator

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOperator" ):
                listener.enterOperator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOperator" ):
                listener.exitOperator(self)




    def operator(self):

        localctx = MongoEngineDSLParser.OperatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_operator)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 45
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << MongoEngineDSLParser.EQ) | (1 << MongoEngineDSLParser.NE) | (1 << MongoEngineDSLParser.LT) | (1 << MongoEngineDSLParser.LE) | (1 << MongoEngineDSLParser.GT) | (1 << MongoEngineDSLParser.GE) | (1 << MongoEngineDSLParser.IN) | (1 << MongoEngineDSLParser.NIN))) != 0)):
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


    class ValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return MongoEngineDSLParser.RULE_value

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class DoubleValueContext(ValueContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MongoEngineDSLParser.ValueContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def DOUBLE(self):
            return self.getToken(MongoEngineDSLParser.DOUBLE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDoubleValue" ):
                listener.enterDoubleValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDoubleValue" ):
                listener.exitDoubleValue(self)


    class BooleanValueContext(ValueContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MongoEngineDSLParser.ValueContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def BOOL(self):
            return self.getToken(MongoEngineDSLParser.BOOL, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBooleanValue" ):
                listener.enterBooleanValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBooleanValue" ):
                listener.exitBooleanValue(self)


    class IntegerValueContext(ValueContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MongoEngineDSLParser.ValueContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def INT(self):
            return self.getToken(MongoEngineDSLParser.INT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIntegerValue" ):
                listener.enterIntegerValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIntegerValue" ):
                listener.exitIntegerValue(self)


    class DeniedValueContext(ValueContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MongoEngineDSLParser.ValueContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def DENIED(self):
            return self.getToken(MongoEngineDSLParser.DENIED, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeniedValue" ):
                listener.enterDeniedValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeniedValue" ):
                listener.exitDeniedValue(self)


    class WildcardValueContext(ValueContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MongoEngineDSLParser.ValueContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def WILDCARD(self):
            return self.getToken(MongoEngineDSLParser.WILDCARD, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWildcardValue" ):
                listener.enterWildcardValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWildcardValue" ):
                listener.exitWildcardValue(self)


    class ArrayValueContext(ValueContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MongoEngineDSLParser.ValueContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ARR_LPOS(self):
            return self.getToken(MongoEngineDSLParser.ARR_LPOS, 0)
        def ARR_RPOS(self):
            return self.getToken(MongoEngineDSLParser.ARR_RPOS, 0)
        def value(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MongoEngineDSLParser.ValueContext)
            else:
                return self.getTypedRuleContext(MongoEngineDSLParser.ValueContext,i)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(MongoEngineDSLParser.COMMA)
            else:
                return self.getToken(MongoEngineDSLParser.COMMA, i)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArrayValue" ):
                listener.enterArrayValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArrayValue" ):
                listener.exitArrayValue(self)


    class QuoteStringValueContext(ValueContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MongoEngineDSLParser.ValueContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def QSTR(self):
            return self.getToken(MongoEngineDSLParser.QSTR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuoteStringValue" ):
                listener.enterQuoteStringValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuoteStringValue" ):
                listener.exitQuoteStringValue(self)


    class TokenValueContext(ValueContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MongoEngineDSLParser.ValueContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def TOKEN(self):
            return self.getToken(MongoEngineDSLParser.TOKEN, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTokenValue" ):
                listener.enterTokenValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTokenValue" ):
                listener.exitTokenValue(self)



    def value(self):

        localctx = MongoEngineDSLParser.ValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_value)
        self._la = 0 # Token type
        try:
            self.state = 65
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [MongoEngineDSLParser.BOOL]:
                localctx = MongoEngineDSLParser.BooleanValueContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 47
                self.match(MongoEngineDSLParser.BOOL)
                pass
            elif token in [MongoEngineDSLParser.INT]:
                localctx = MongoEngineDSLParser.IntegerValueContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 48
                self.match(MongoEngineDSLParser.INT)
                pass
            elif token in [MongoEngineDSLParser.DOUBLE]:
                localctx = MongoEngineDSLParser.DoubleValueContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 49
                self.match(MongoEngineDSLParser.DOUBLE)
                pass
            elif token in [MongoEngineDSLParser.QSTR]:
                localctx = MongoEngineDSLParser.QuoteStringValueContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 50
                self.match(MongoEngineDSLParser.QSTR)
                pass
            elif token in [MongoEngineDSLParser.WILDCARD]:
                localctx = MongoEngineDSLParser.WildcardValueContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 51
                self.match(MongoEngineDSLParser.WILDCARD)
                pass
            elif token in [MongoEngineDSLParser.DENIED]:
                localctx = MongoEngineDSLParser.DeniedValueContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 52
                self.match(MongoEngineDSLParser.DENIED)
                pass
            elif token in [MongoEngineDSLParser.TOKEN]:
                localctx = MongoEngineDSLParser.TokenValueContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 53
                self.match(MongoEngineDSLParser.TOKEN)
                pass
            elif token in [MongoEngineDSLParser.ARR_LPOS]:
                localctx = MongoEngineDSLParser.ArrayValueContext(self, localctx)
                self.enterOuterAlt(localctx, 8)
                self.state = 54
                self.match(MongoEngineDSLParser.ARR_LPOS)
                self.state = 59 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 55
                    self.value()
                    self.state = 57
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==MongoEngineDSLParser.COMMA:
                        self.state = 56
                        self.match(MongoEngineDSLParser.COMMA)


                    self.state = 61 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << MongoEngineDSLParser.BOOL) | (1 << MongoEngineDSLParser.INT) | (1 << MongoEngineDSLParser.DOUBLE) | (1 << MongoEngineDSLParser.QSTR) | (1 << MongoEngineDSLParser.TOKEN) | (1 << MongoEngineDSLParser.WILDCARD) | (1 << MongoEngineDSLParser.DENIED) | (1 << MongoEngineDSLParser.ARR_LPOS))) != 0)):
                        break

                self.state = 63
                self.match(MongoEngineDSLParser.ARR_RPOS)
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



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[1] = self.expression_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expression_sempred(self, localctx:ExpressionContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 3)
         




