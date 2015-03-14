__author__ = 'Jason Childers'


import operator

import LambdaError
import LambdaParsingError


class LambdaTerm:
    """This class models lambda terms of the form:

        I = lambda x: x                                 // Identity: returns itself... given an argument x, returns x
                                                        // I(42); returns 42
        K = lambda x: (lambda y: x)                     // Constant: given any argument, always returns a constant
                                                        // K(3)(12); returns 3
        S = lambda x: lambda y: lambda z: x(z)(y(z))    // Substitution
                                                        // S(K)(K)(42); return 42

        lambda to Pi translations of the form are supported:

            ------------------------------------------------------------------------------------------------------------
            | lambda expression     |   Pi agent on port p      |   meaning                                            |
            ------------------------------------------------------------------------------------------------------------
            |       M               |       [M](p)              | Build an agent with a communication channel p        |
            ------------------------------------------------------------------------------------------------------------
            |     λx M              |    p?x.p?q.[M](q)         | Given a channel p, obtain the value of x and the     |
            |                       |                           | communication channel q; call agent [M] on channel   |
                                    |                           | q                                                    |
            ------------------------------------------------------------------------------------------------------------
            |       x               |        x!p                | A variable, when used, just publishes its channel    |
            ------------------------------------------------------------------------------------------------------------
            |      M N              |   new(a,b).(([M](a))|     | Applying M to N means: create control channels a and |
            |                       |   (a!b.a!f)|              | b, and launch in parallel: [M] on a (it will wait);  |
            |                       |   *((b?c).[N](c))         | pass b and f to M via channel a; read channel b on y,|
            |                       |                           | start [N] which will work with channel c; run it     |
            |                       |                           | forever, we may need result more than once.          |
            ------------------------------------------------------------------------------------------------------------

    """

    CHANNELS = {'a':0, 'b':0, 'c':0, 'd':0, 'e':0, 'f':0, 'g':0, 'h':0, 'i':0, 'j':0, 'k':0, 'l':0, 'm':0, 'n':0, 'o':0,
                'p':0, 'q':0, 'r':0, 's':0, 't':0, 'u':0, 'v':0, 'w':0, 'x':0, 'y':0, 'z':0}

    AGENTS = {'A':0, 'B':0, 'C':0, 'D':0, 'E':0, 'F':0, 'G':0, 'H':0, 'I':0, 'J':0, 'K':0, 'L':0, 'M':0, 'N':0, 'O':0,
              'P':0, 'Q':0, 'R':0, 'S':0, 'T':0, 'U':0, 'V':0, 'W':0, 'X':0, 'Y':0, 'Z':0}

    PI_EXPRESSIONS = ['_M_', 'x: _M_', '_var_', '_M_ _N_']

    EXPRESSION_MAP = {'_M_': '[_M_](_c_)',
                      'x: _M_': '_c1_?x._c1_?_c2_.[_M_](_c2_)',
                      '_var_': '_var_!_c_',
                      '_M_ _N_':'new(_c1_,_c2_).(([_M_](_c1_)) | '
                                          '(_c1_!_c2_._c2_!_c3_) | '
                                          '*((_c2_?_c4_).[_N_](_c4_))'}

    debug = False

    term = ''
    astTerms = []
    expressionKeys = []
    expressionValues = []
    piProcessExpression = ''

    def __init__(self, expr):
        try:
            self.term = expr
            self.astTerms = LambdaTerm.parseLambdaTerm(expr)
            self.createExpressionMap()
            if LambdaTerm.debug: print('(debug) ' + str(self.expressionKeys))
            self.evaluate()
            if LambdaTerm.debug: print('(debug) ' + str(self.piProcessExpression))
        except LambdaParsingError as e:
            print("Oops!  Could not parse LambdaExpression: ", e.value)


    @staticmethod
    def parseLambdaTerm(lambdaTerm):
        lstack = []
        lambdaTerm = str(lambdaTerm).strip()

        terms = LambdaTerm.getTerms(lambdaTerm)
        if len(terms) > 1:
            for term in terms:
                #lstack.extend(LambdaTerm.parseLambdaTerm(term))
                lstack.append(LambdaTerm.parseLambdaTerm(term))
                termIndex = lambdaTerm.rfind(term)
                if termIndex is not -1:
                    lambdaTerm = lambdaTerm[len(term):]

        if lambdaTerm.startswith('('):
            lambdaTerm = LambdaTerm.stripParens(lambdaTerm)

        if lambdaTerm.startswith('lambda'):
            colonIndex = lambdaTerm.find(':')

            if colonIndex != -1:
                key = lambdaTerm[colonIndex-1:colonIndex]
                value = lambdaTerm[colonIndex+1:].strip()
                if value.startswith('('):      # remove leading and trailing parens from the term
                    value = LambdaTerm.stripParens(value)

                lstack.append({key:value})
                ltItems = []
                if value.find('lambda') is not -1:
                    ltItems = LambdaTerm.parseLambdaTerm(value)

                if len(ltItems) > 0:
                    if isinstance(ltItems, list):
                        for item in ltItems:
                            lstack.append(item)
                    else:
                        lstack.append(ltItems)
        elif len(lambdaTerm) > 0:
            key = '_var_'
            value = lambdaTerm
            prevTerm = LambdaTerm.getPreviousValue(terms)
            if value is not LambdaTerm.getPreviousValue(terms):
                lstack.append({key:value})


        return lstack


    @staticmethod
    def getPreviousValue(termsTree):
        totalTerms = len(termsTree)
        term = termsTree
        if len(term) > 0:
            if isinstance(term, list):
                term = termsTree[totalTerms-1]
                term = LambdaTerm.getPreviousValue(term)

            if isinstance(term, dict):
                term = termsTree[totalTerms-1]
                key, value = term.popItem()
                term = value

        return term


    @staticmethod
    def stripParens(lambdaTerm):
        term = lambdaTerm[0:]
        counter = 0
        endparenindex = -1
        for i,c in enumerate(term):
            if c is '(':
                counter+=1
            elif c is ')':
                counter-=1
                if counter is 0:
                    endparenindex = i
                    break

        if endparenindex is -1:
            raise LambdaParsingError

        return lambdaTerm[1:endparenindex] + lambdaTerm[endparenindex+1:]


    @staticmethod
    def getTerms(lambdaTerm):
        terms = []

        if (lambdaTerm.find('(') is -1):
            return terms

        term = lambdaTerm[0:]
        counter = 0
        endparenindex = -1
        for i, c in enumerate(term):
            if c is '(':
                counter+=1
            elif c is ')':
                counter-=1
                if counter is 0:
                    endparenindex = i
                    break

        if endparenindex is -1:
            raise LambdaParsingError

        aTerm = lambdaTerm[0:endparenindex+1]
        terms.append(aTerm)
        ltLength = len(lambdaTerm)
        if endparenindex < len(lambdaTerm)-1:
            lambdaIndex = lambdaTerm[endparenindex+1:].find('lambda')
            if lambdaTerm[endparenindex+1:].find('lambda') is not 1:
                # replace the prior term with the entire term
                terms.remove(aTerm)
                terms.append(lambdaTerm[0:])
            else:
                terms.extend(LambdaTerm.getTerms(lambdaTerm[endparenindex+1:]))

        return terms


    def toPi(self):
        self.createExpressionMap()

    @staticmethod
    def newChannel():
        channelKeys = sorted(LambdaTerm.CHANNELS.items(), key=operator.itemgetter(0))
        channel = ''
        for ck in channelKeys:
            if ck[1] is 0:
                channel = ck[0]
                LambdaTerm.CHANNELS[channel] = 1
                break

        if channel is '':
            raise LambdaError

        return channel


    @staticmethod
    def newAgent():
        agentKeys = sorted(LambdaTerm.AGENTS.items(), key=operator.itemgetter(0))
        agent = ''
        for ak in agentKeys:
            if ak[1] is 0:
                agent = ak[0]
                LambdaTerm.AGENTS[agent] = 1
                break

        if agent is '':
            raise LambdaError

        return agent


    def createExpressionMap(self):
        if len(self.astTerms) is 2 and isinstance(self.astTerms[0], list):         # the case where M N
            self.expressionKeys.append(LambdaTerm.PI_EXPRESSIONS[3])

        elif len(self.astTerms) is 1 or isinstance(self.astTerms[0], dict):
            for term in self.astTerms:
                for key in term.keys():
                    if key is LambdaTerm.PI_EXPRESSIONS[2]:         # key is a variable
                        self.expressionKeys.append(LambdaTerm.PI_EXPRESSIONS[2])
                    else:
                        self.expressionKeys.append(LambdaTerm.PI_EXPRESSIONS[1])
                    value = term[key]
                    self.expressionValues.append(value)


    def evaluate(self):
        for i in range(len(self.expressionKeys)):
            if i is 0 or isinstance(self.expressionValues[i], list):
                exprKey = self.expressionKeys[i]
                if exprKey is LambdaTerm.PI_EXPRESSIONS[3]:
                    self.appendEvaluatedTerm(self.evaluateAgents(exprKey))
                else:
                    exprVal = self.expressionValues[i]
                    term = self.astTerms[i]
                    # TODO: perhaps here call evaluateAgent
                    if exprKey is LambdaTerm.PI_EXPRESSIONS[2]:
                        self.appendEvaluatedTerm(self.evaluateVar(exprKey, exprVal, i))
                    elif exprKey is LambdaTerm.PI_EXPRESSIONS[1]:
                        self.appendEvaluatedTerm(self.evaluateLambda(exprKey, exprVal, i))


    #  x  ==  x!p
    def evaluateVar(self, expressionKey, expressionValue, currentExpressionIndex, terms=None):
        mappedTerm = LambdaTerm.EXPRESSION_MAP.get(expressionKey)
        evaluatedTerm = mappedTerm.replace('_var_', expressionValue)
        evaluatedTerm = evaluatedTerm.replace('_c_', LambdaTerm.newChannel())

        return evaluatedTerm


    #  λx M  ==  p?x.p?q.[M](q)
    def evaluateLambda(self, expressionKey, expressionValue, currentExpressionIndex, terms=None, expressionValues=None):
        mappedTerm = LambdaTerm.EXPRESSION_MAP.get(expressionKey)
        # _c1_?x._c1_?_c2_.[_M_](_c2_)
        if terms is None:
            term = self.astTerms[currentExpressionIndex]
        else:
            term = terms[currentExpressionIndex]

        if LambdaTerm.debug: print('(debug) evaluating term: ' + str(term))
        termInput = list(term.keys())[0]
        termExpr = term.get(termInput)

        evaluatedTerm = mappedTerm.replace('x', termInput)
        evaluatedTerm = evaluatedTerm.replace('_c1_', LambdaTerm.newChannel())
        evaluatedTerm = evaluatedTerm.replace('_c2_', LambdaTerm.newChannel())
        evaluatedSubterm = ''
        if expressionValue.find('lambda') is -1:    # in this case the value is a var
            evaluatedSubterm = self.evaluateVar(LambdaTerm.PI_EXPRESSIONS[2], expressionValue, currentExpressionIndex+1, terms)
        else:                                       # in this case the value is another lambda
            if expressionValues is None:
                expressionValues = self.expressionValues
            evaluatedSubterm = self.evaluateLambda(LambdaTerm.PI_EXPRESSIONS[1],
                                                   expressionValues[currentExpressionIndex+1],
                                                   currentExpressionIndex+1, terms, expressionValues)
        if len(evaluatedSubterm) > 0:
            evaluatedTerm = evaluatedTerm.replace('_M_', evaluatedSubterm)

        if LambdaTerm.debug: print('(debug) evaluatedTerm: ' + evaluatedTerm)
        return evaluatedTerm


    # Evaluate an Agent.  Example
    #   For K:
    #       expressionKeys = ['x: _M_', 'x: _M_']
    #       expressionValues = ['lambda y: x', 'x']
    def evaluateAgent(self, terms):
        # determine expressionKeys for term
        expressionKeys, expressionValues = LambdaTerm.getTermExpressionKeysValues(terms)
        if LambdaTerm.debug: print('expressionKeys: ' + str(expressionKeys))
        if LambdaTerm.debug: print('expressionValues: ' + str(expressionValues))

        evaluatedTerm = ''
        for i in range(len(expressionKeys)):
            if i is 0 or isinstance(expressionValues[i], list):
                exprKey = expressionKeys[i]
                if exprKey is LambdaTerm.PI_EXPRESSIONS[3]:
                    self.evaluateAgents(exprKey)
                else:
                    exprVal = expressionValues[i]
                    term = terms[i]
                    if exprKey is LambdaTerm.PI_EXPRESSIONS[2]:
                        evaluatedTerm = self.evaluateVar(exprKey, exprVal, i, terms)
                    elif exprKey is LambdaTerm.PI_EXPRESSIONS[1]:
                        evaluatedTerm = self.evaluateLambda(exprKey, exprVal, i, terms, expressionValues)

        if LambdaTerm.debug: print('(debug) evaluatedTerm: ' + evaluatedTerm)
        return evaluatedTerm


    @staticmethod
    def getTermExpressionKeysValues(terms):
        expressionKeys = []
        expressionValues = []
        for term in terms:
            for key in term.keys():
                if key is LambdaTerm.PI_EXPRESSIONS[2]:         # key is a variable
                    expressionKeys.append(LambdaTerm.PI_EXPRESSIONS[2])
                else:
                    expressionKeys.append(LambdaTerm.PI_EXPRESSIONS[1])
                value = term[key]
                expressionValues.append(value)

        return expressionKeys, expressionValues



    # evaluate M N  ==  new(a,b).(([M](a)) | (a!b.a!f) | *((b?c).[N](c))
    def evaluateAgents(self, expressionKey, currentExpressionIndex=0):
        if expressionKey is LambdaTerm.PI_EXPRESSIONS[3]:
            mappedTerm = LambdaTerm.EXPRESSION_MAP.get(expressionKey)
            # new(_c1_,_c2_).(([_M_](_c1_)) | (_c1_!_c2_._c2_!_c3_) | *((_c2_?_c4_).[_N_](_c4_))
            evaluatedTerm = mappedTerm.replace('_c1_', LambdaTerm.newChannel())
            evaluatedTerm = evaluatedTerm.replace('_c2_', LambdaTerm.newChannel())
            evaluatedTerm = evaluatedTerm.replace('_c3_', LambdaTerm.newChannel())
            evaluatedTerm = evaluatedTerm.replace('_c4_', LambdaTerm.newChannel())
            evaluatedSubterm = ''

            for i in range(len(self.astTerms)):
                evaluatedSubterm = self.evaluateAgent(self.astTerms[i])
                if len(evaluatedSubterm) > 0:
                    if i is 0:
                        evaluatedTerm = evaluatedTerm.replace('_M_', evaluatedSubterm)
                    elif i is 1:
                        evaluatedTerm = evaluatedTerm.replace('_N_', evaluatedSubterm)

                if LambdaTerm.debug: print('(debug) evaluatedTerm: ' + evaluatedTerm)

        if LambdaTerm.debug: print('(debug) evaluatedTerm: ' + evaluatedTerm)
        return evaluatedTerm


    def appendEvaluatedTerm(self, evaluatedTerm):
        if len(evaluatedTerm) > 0:
            if len(self.piProcessExpression) > 0:
                self.piProcessExpression += '.' + evaluatedTerm
            else:
                self.piProcessExpression += evaluatedTerm
