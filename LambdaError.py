__author__ = 'Jason Childers'


class LambdaError(Exception):
    """Exception raised when encountering a generic issue in LambdaTerm.py.

        Attributes:
            value -- the msg of the exception
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)