#!/usr/local/bin/python3

__author__ = 'Jason Childers'


import argparse
from LambdaTerm import LambdaTerm


parser = argparse.ArgumentParser()
parser.add_argument("lambdaterm", type=str, help="a lambda term [ex: 'lambda x: x(42)']")
parser.add_argument("-d", "--debug", help="show debug info", action="store_true")
args = parser.parse_args()
if args.debug:
    print('debug is turned on');


def main(args):
    if (args is not None):
        print(args)
        print('args: ' + str(args))
        lambdaTerm = LambdaTerm(args.lambdaterm)
        print(lambdaTerm.astTerms)
    else:
        print('no args');


if __name__ == '__main__':
    main(args)
    exit()

