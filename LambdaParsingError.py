__author__ = 'Jason Childers'


from LambdaError import LambdaError


class LambdaParsingError(LambdaError):
    """Exception raised when unable to parse a lambda term.

        Attributes:
            value -- the value of the lambda term that couldn't be parsed
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)