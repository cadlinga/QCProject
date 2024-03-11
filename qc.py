from typing import Union

import numpy
from numpy.lib import math
from gates import Gate

from utils.state_vector import makeStateVector
from utils.tensor import Operator

import matplotlib as plt


#
# class Qubit:
#     """Quantum Bit Implementation"""
#
#     def __init__(self, register=None, index: int = None):
#         if (register, index) == (None, None):
#             self._register = None
#             self._index = None
#         else:
#
#             if index < 0:
#                 """
#                 If the index is negative, place bit
#                 that many places from the end of the register.
#                 """
#                 index += register.size
#
#             if index >= register.size:
#                 """
#                 If the index is larger than the register size
#                 throw an exception.
#                 """
#                 raise Exception(
#                     """
#                     Index must `fit` within the register.
#                     The index provided was too large.
#                     (Remember 0 based indexing)
#                     """
#                 )
#
#             self._register = register
#             self._index = index
#
#     def __repr__(self) -> str:
#         return f"Qubit({self._register, self._index})"
#
#
# class Register:
#     """Quantum Register Implementation."""
#
#     def __init__(self, size: int):
#         if size < 0:
#             raise Exception(
#                 """
#                 Size of register must be a positive int.
#                 %s is not a acceptable.
#                 """
#                 % size
#             )
#
#         self._size = size
#         self._bits = [Qubit(self, i) for i in range(size)]
#
#     @property
#     def size(self):
#         return self._size
#
#     @property
#     def bits(self):
#         return self._bits
#
#     def __repr__(self):
#         return "%s(%d)" % (self.__class__.__qualname__, self.size)
#
#
class Circuit:

    def __init__(self, register_size: int):
        self.register_size = int(register_size)
        self.register = makeStateVector(0, register_size)
        self.groverOperator = None
        self.gates = Gate(register_size)

        pass

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__qualname__, self.register_size)

    def h(self):
        h = self.gates.h()
        product = h ** int(self.register_size)
        self.register = self.register.apply(product)
        return

    def grover(self, target: int):

        N = 2**self.register_size
        theta = numpy.arcsin(numpy.sqrt(1 / N))
        iterations = math.floor(numpy.pi / (4 * theta))

        print(
            "I've calculated that I need to use "
            + str(iterations)
            + " iterations to be likely to succeed."
        )

        if self.groverOperator is None:
            self.groverOperator = (
                self.gates.oracle(target)
                * (self.gates.h() ** int(self.register_size))
                * self.gates.reflection()
                * (self.gates.h() ** int(self.register_size))
            )

        i = 0
        while i < int(iterations):
            self.register = self.register.apply(self.groverOperator)
            i = i + 1

    def measure(self, target: int):
        target = int(target)

        print(
            "P("
            + str(target)
            + ") = "
            + str(
                (
                    numpy.dot(
                        makeStateVector(target, self.register_size)
                        .vector.todense()
                        .flatten(),
                        self.register.vector.todense().flatten(),
                    )
                )
                ** 2
            )
        )
        return
