#!/usr/local/bin/python3

__author__ = 'Jason Childers'


import argparse

from LambdaTerm import LambdaTerm


parser = argparse.ArgumentParser()
parser.add_argument("lambdaterm", type=str, help="a lambda term [ex: 'lambda x: x']")
parser.add_argument("-d", "--debug", help="show debug info", action="store_true")
args = parser.parse_args()
if args.debug:
    LambdaTerm.debug = True
    if args.debug: print('(debug) debug is turned on')


def main(args):
    if (args is not None):
        if args.debug: print('(debug) args: ' + str(args))
        lambdaTerm = LambdaTerm(args.lambdaterm)
        print('\n>>> lambda term: ' + lambdaTerm.term + '\n')
        if args.debug: print('(debug) astTerms: ' + str(lambdaTerm.astTerms))
        print('>>> pi-calculus process: ' + lambdaTerm.piProcessExpression + '\n')
    else:
        print('no args');


if __name__ == '__main__':
    main(args)
    exit()
