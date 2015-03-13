__author__ = 'jchilders'

import unittest

from LambdaTerm import LambdaTerm


I = 'lambda x: x'

K = 'lambda x: (lambda y: x)'

S = 'lambda x: lambda y: lambda z: x(z)(y(z))'


class TestLamdaTerm(unittest.TestCase):


    def test_lambdaTermx(self):
        print('testing x')
        lt = LambdaTerm('x')
        self.assertEqual(lt.term, 'x')
        print('astTerms: ' + str(lt.astTerms))
        self.assertEqual(lt.astTerms, [{'_var_': 'x'}])
        self.assertEqual(lt.piProcessExpression, 'x!a')



    def test_lambdaTermI(self):
        print('testing I')
        lt = LambdaTerm(I)
        self.assertEqual(lt.astTerms, [{'x': 'x'}])
        print(lt.astTerms)
        self.assertEqual(len(lt.astTerms), 1, 'Stack should have a depth equal to 1.')
        self.assertEqual(len(lt.astTerms), 1, 'keys length should be equal to 1.')
        term = lt.astTerms.pop()
        key = list(term.keys())[0]
        self.assertEqual(key, 'x', "the first key should equal 'x'.")
        value = term.get(key)
        self.assertEqual(value, 'x', "the value of the lambda term should equal 'x'")
        print(lt.piProcessExpression)
        self.assertEqual(lt.piProcessExpression, 'a?x.a?b.[x!c](b)')



    def test_lambdaTermK(self):
        print('testing K')
        lt = LambdaTerm(K)
        self.assertEqual(lt.astTerms, [{'x': 'lambda y: x'}, {'y': 'x'}])
        print(lt.astTerms)
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

        print(lt.piProcessExpression)
        self.assertEqual(lt.piProcessExpression, 'a?x.a?b.[c?y.c?d.[x!e](d)](b)')


    def test_lambdaTermS(self):
        print('testing S')
        lt = LambdaTerm(S)
        self.assertEqual(lt.astTerms, [{'x': 'lambda y: lambda z: x(z)(y(z))'}, {'y': 'lambda z: x(z)(y(z))'},
                                       {'z': 'x(z)(y(z))'}])
        print(lt.astTerms)
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

        print(lt.piProcessExpression)
        self.assertEqual(lt.piProcessExpression, 'a?x.a?b.[c?y.c?d.[e?z.e?f.[x(z)(y(z))!g](f)](d)](b)')


    def test_lambdaTermKI(self):
        print('testing KI')
        lt = LambdaTerm('('+K+')'+'('+I+')')
        print(lt.astTerms)


    def test_lambdaTermSK(self):
        print('testing SK')
        lt = LambdaTerm('('+S+')'+'('+K+')')
        print(lt.astTerms)


    def test_lambdaTermSKI(self):
        print('testing SKI')
        lt = LambdaTerm('('+S+')'+'('+K+')'+'('+I+')')
        print(lt.astTerms)


    def test_lambdaChannelsLength(self):
        print('testing CHANNELS length')
        channelsLength = len(LambdaTerm.CHANNELS)
        self.assertEqual(channelsLength, 26, "only 26 channels should be available")


    def test_getNewChannel(self):
        print('testing newChannel()')
        channel = LambdaTerm.newChannel()
        #ltChannels = LambdaTerm.CHANNELS
        channelReserved = LambdaTerm.CHANNELS.get(channel)
        print('channel: ' + channel + ', channelReserved: '+ str(channelReserved))
        self.assertEqual(channelReserved, 1, 'channel should be reserved (ie. = 1)')
        # get another new agent and assert it worked correctly too
        channel = LambdaTerm.newChannel()
        #self.assertEqual(channel, LambdaTerm.CHANNELS[1], 'channel should be the 2nd value in CHANNELS')
        channelReserved = LambdaTerm.CHANNELS.get(channel)
        self.assertEqual(channelReserved, 1, 'channel should be reserved (ie. = 1)')
        print('channel: ' + channel + ', channelReserved: '+ str(channelReserved))


    def test_lambdaAgentsLength(self):
        print('testing AGENTS length')
        agentsLength = len(LambdaTerm.AGENTS)
        self.assertEqual(agentsLength, 26, "only 26 agents should be available")


    def test_getNewAgent(self):
        print('testing newAgent()')
        agent = LambdaTerm.newAgent()
        agentReserved = LambdaTerm.AGENTS.get(agent)
        print('agent: ' + agent + ', agentReserved: ' + str(agentReserved))
        self.assertEqual(agentReserved, 1, 'agent should be reserved (ie. = 1)')
        # get another new agent and assert it worked correctly too
        agent = LambdaTerm.newAgent()
        agentReserved = LambdaTerm.AGENTS.get(agent)
        self.assertEqual(agentReserved, 1, 'agent should be reserved (ie. = 1)')
        print('agent: ' + agent + ', agentReserved: ' + str(agentReserved))


    def test_lambdaI2Pi(self):
        print('testing I to Pi')
        lt = LambdaTerm(I)
        print(lt.astTerms)




if __name__ == '__main__':
    unittest.main()
