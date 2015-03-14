__author__ = 'jchilders'

import unittest

from LambdaTerm import LambdaTerm


I = 'lambda x: x'

K = 'lambda x: (lambda y: x)'

S = 'lambda x: lambda y: lambda z: x(z)(y(z))'

debug = False


class TestLambdaTerm(unittest.TestCase):


    def setUp(self):
        LambdaTerm.reset()

    def tearDown(self):
        LambdaTerm.reset()


    def test_lambdaTermx(self):
        if debug: print('testing x')
        lt = LambdaTerm('x')
        self.assertEqual(lt.term, 'x')
        print('lambda-term: ' + lt.term)
        if debug: print('astTerms: ' + str(lt.astTerms))
        self.assertEqual(lt.astTerms, [{'_var_': 'x'}])
        self.assertEqual(lt.piProcessExpression, 'x!a')
        print('>  expected: ' + 'x!a')
        print('>>   actual: ' + lt.piProcessExpression)
        print('--------')


    def test_lambdaTermI(self):
        if debug: print('testing I')
        lt = LambdaTerm(I)
        self.assertEqual(lt.astTerms, [{'x': 'x'}])
        print('lambda-term - I: ' + lt.term)
        if debug: print(lt.astTerms)
        self.assertEqual(len(lt.astTerms), 1, 'Stack should have a depth equal to 1.')
        self.assertEqual(len(lt.astTerms), 1, 'keys length should be equal to 1.')
        term = lt.astTerms.pop()
        key = list(term.keys())[0]
        self.assertEqual(key, 'x', "the first key should equal 'x'.")
        value = term.get(key)
        self.assertEqual(value, 'x', "the value of the lambda term should equal 'x'")
        if debug: print(lt.piProcessExpression)
        self.assertEqual(lt.piProcessExpression, 'a?x.a?b.[x!c](b)')
        print('>      expected: ' + 'a?x.a?b.[x!c](b)')
        print('>>       actual: ' + lt.piProcessExpression)
        print('--------')


    def test_lambdaTermK(self):
        if debug: print('testing K')
        lt = LambdaTerm(K)
        self.assertEqual(lt.astTerms, [{'x': 'lambda y: x'}, {'y': 'x'}])
        print('lambda-term - K: ' + lt.term)
        if debug: print(lt.astTerms)
        self.assertEqual(len(lt.astTerms), 2, 'Stack should have a depth equal to 2.')
        term1 = lt.astTerms[0]
        key1 = list(term1.keys())[0]
        self.assertEqual(key1, 'x', "the 1st key for the first term should equal 'x'.")
        value1 = term1.get(key1)
        self.assertEqual(value1, 'lambda y: x', "the value of the 1st lambda term should equal 'lambda y: x'")

        term2 = lt.astTerms[1]
        key2 = list(term2.keys())[0]
        self.assertEqual(key2, 'y', "the 2nd key for the 2nd term should equal 'y'.")
        value2 = term2.get(key2)
        self.assertEqual(value2, 'x', "the value of the 2nd lambda term should equal 'x'")

        if debug: print(lt.piProcessExpression)
        self.assertEqual(lt.piProcessExpression, 'a?x.a?b.[c?y.c?d.[x!e](d)](b)')
        print('>      expected: ' + 'a?x.a?b.[c?y.c?d.[x!e](d)](b)')
        print('>>       actual: ' + lt.piProcessExpression)
        print('--------')


    def test_lambdaTermS(self):
        if debug: print('testing S')
        lt = LambdaTerm(S)
        self.assertEqual(lt.astTerms, [{'x': 'lambda y: lambda z: x(z)(y(z))'}, {'y': 'lambda z: x(z)(y(z))'},
                                       {'z': 'x(z)(y(z))'}])
        print('lambda-term - S: ' + lt.term)
        if debug: print(lt.astTerms)
        self.assertEqual(len(lt.astTerms), 3, 'Stack should have a depth equal to 3.')

        term1 = lt.astTerms[0]
        key1 = list(term1.keys())[0]
        self.assertEqual(key1, 'x', "the 1st key for the first term should equal 'x'.")
        value1 = term1.get(key1)
        self.assertEqual(value1, 'lambda y: lambda z: x(z)(y(z))', "the value of the 1st lambda term should equal "
                                                                   "'lambda y: lambda z: x(z)(y(z))'")
        term2 = lt.astTerms[1]
        key2 = list(term2.keys())[0]
        self.assertEqual(key2, 'y', "the 2nd key for the 2nd term should equal 'y'.")
        value2 = term2.get(key2)
        self.assertEqual(value2, 'lambda z: x(z)(y(z))', "the value of the 2nd lambda term should equal "
                                                         "'lambda z: x(z)(y(z))'")
        term3 = lt.astTerms[2]
        key3 = list(term3.keys())[0]
        self.assertEqual(key3, 'z', "the 3nd key for the 3nd term should equal 'z'.")
        value3 = term3.get(key3)
        self.assertEqual(value3, 'x(z)(y(z))', "the value of the 2nd lambda term should equal 'x(z)(y(z))'")

        if debug: print(lt.piProcessExpression)
        self.assertEqual(lt.piProcessExpression, 'a?x.a?b.[c?y.c?d.[e?z.e?f.[x(z)(y(z))!g](f)](d)](b)')
        print('>      expected: ' + 'a?x.a?b.[c?y.c?d.[e?z.e?f.[x(z)(y(z))!g](f)](d)](b)')
        print('>>       actual: ' + lt.piProcessExpression)
        print('--------')


    def test_lambdaTermKI(self):
        if debug: print('testing KI')
        lt = LambdaTerm('('+K+')'+'('+I+')')
        self.assertEqual(lt.astTerms, [[{'x': 'lambda y: x'}, {'y': 'x'}], [{'x': 'x'}]])
        print('lambda-term - KI: ' + lt.term)
        if debug: print(lt.astTerms)
        if debug: print(lt.astTerms)
        if debug: print(lt.piProcessExpression)
        self.assertEqual(lt.piProcessExpression, 'new(a,b).(([e?x.e?f.[g?y.g?h.[x!i](h)](f)](a)) | (a!b.b!c) |'
                                                 ' *((b?d).[j?x.j?k.[x!l](k)](d))')
        print('>       expected: ' + 'new(a,b).(([e?x.e?f.[g?y.g?h.[x!i](h)](f)](a)) | (a!b.b!c) |'
                                     ' *((b?d).[j?x.j?k.[x!l](k)](d))')
        print('>>        actual: ' + lt.piProcessExpression)
        print('--------')


    def test_lambdaTermSK(self):
        if debug: print('testing SK')
        lt = LambdaTerm('('+S+')'+'('+K+')')
        self.assertEqual(lt.astTerms, [[{'x': 'lambda y: lambda z: x(z)(y(z))'}, {'y': 'lambda z: x(z)(y(z))'},
                                        {'z': 'x(z)(y(z))'}], [{'x': 'lambda y: x'}, {'y': 'x'}]])
        print('lambda-term - SK: ' + lt.term)
        #print(lt.astTerms)
        if debug: print(lt.astTerms)
        if debug: print(lt.piProcessExpression)
        self.assertEqual(lt.piProcessExpression, 'new(a,b).(([e?x.e?f.[g?y.g?h.[i?z.i?j.[x(z)(y(z))!k](j)](h)](f)](a))'
                                                 ' | (a!b.b!c) | *((b?d).[l?x.l?m.[n?y.n?o.[x!p](o)](m)](d))')
        print('>       expected: ' + 'new(a,b).(([e?x.e?f.[g?y.g?h.[i?z.i?j.[x(z)(y(z))!k](j)](h)](f)](a)) | (a!b.b!c)'
                                     ' | *((b?d).[l?x.l?m.[n?y.n?o.[x!p](o)](m)](d))')
        print('>>        actual: ' + lt.piProcessExpression)
        print('--------')


    #TODO: wire this up
    @unittest.expectedFailure
    def test_lambdaTermSKI(self):
        if debug: print('testing SKI')
        lt = LambdaTerm('('+S+')'+'('+K+')'+'('+I+')')
        self.assertEqual(lt.astTerms, [[{'x': 'lambda y: lambda z: x(z)(y(z))'}, {'y': 'lambda z: x(z)(y(z))'},
                                        {'z': 'x(z)(y(z))'}], [{'x': 'lambda y: x'}, {'y': 'x'}], [{'x': 'x'}]])
        print('lambda-term - SKI: ' + lt.term)
        #print(lt.astTerms)
        if debug: print(lt.astTerms)
        if debug: print(lt.piProcessExpression)
        #self.assertEqual(lt.piProcessExpression, 'a?x.a?b.[c?y.c?d.[e?z.e?f.[x(z)(y(z))!g](f)](d)](b)')
        print('>        expected: ' + 'tbd - not yet wired up')
        print('>>         actual: ' + lt.piProcessExpression)
        print('--------')


    def test_lambdaChannelsLength(self):
        if debug: print('testing CHANNELS length')
        channelsLength = len(LambdaTerm.CHANNELS)
        self.assertEqual(channelsLength, 26, "only 26 channels should be available")


    def test_getNewChannel(self):
        if debug: print('testing newChannel()')
        channel = LambdaTerm.newChannel()
        channelReserved = LambdaTerm.CHANNELS.get(channel)
        if debug: print('channel: ' + channel + ', channelReserved: '+ str(channelReserved))
        self.assertEqual(channelReserved, 1, 'channel should be reserved (ie. = 1)')
        # get another new agent and assert it worked correctly too
        channel = LambdaTerm.newChannel()
        #self.assertEqual(channel, LambdaTerm.CHANNELS[1], 'channel should be the 2nd value in CHANNELS')
        channelReserved = LambdaTerm.CHANNELS.get(channel)
        self.assertEqual(channelReserved, 1, 'channel should be reserved (ie. = 1)')
        if debug: print('channel: ' + channel + ', channelReserved: '+ str(channelReserved))


    def test_lambdaAgentsLength(self):
        if debug: print('testing AGENTS length')
        agentsLength = len(LambdaTerm.AGENTS)
        self.assertEqual(agentsLength, 26, "only 26 agents should be available")


    def test_getNewAgent(self):
        if debug: print('testing newAgent()')
        agent = LambdaTerm.newAgent()
        agentReserved = LambdaTerm.AGENTS.get(agent)
        if debug: print('agent: ' + agent + ', agentReserved: ' + str(agentReserved))
        self.assertEqual(agentReserved, 1, 'agent should be reserved (ie. = 1)')
        # get another new agent and assert it worked correctly too
        agent = LambdaTerm.newAgent()
        agentReserved = LambdaTerm.AGENTS.get(agent)
        self.assertEqual(agentReserved, 1, 'agent should be reserved (ie. = 1)')
        if debug: print('agent: ' + agent + ', agentReserved: ' + str(agentReserved))


    # def test_lambdaI2Pi(self):
    #     if debug: print('testing I to Pi')
    #     lt = LambdaTerm(I)
    #     if debug: print(lt.astTerms)


if __name__ == '__main__':
    unittest.main()
