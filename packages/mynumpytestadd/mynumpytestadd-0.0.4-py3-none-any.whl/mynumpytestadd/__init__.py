import numpy
from types import MethodType

def test_add(self, i, j):
    return i + j

numpy.test_add = MethodType(test_add, numpy)