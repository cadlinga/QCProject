r"""
Quantum Circuit Module
======================
This module provides the implementation of a quantum circuit simulator.
It defines the `Circuit` class which represents a quantum circuit and
provides methods for applying quantum gates and running Grover's algorithm.
"""
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
    r"""
    This is the quantum circuit class which represents a quantum circuit with a 
    specified register size. It provides methods for applying quantum gates, 
    running Grover's algorithm, and measuring the result.
    """

    def __init__(self, register_size: int):
        r"""
        Initializes a new quantum circuit with the given register size.

        Params:
            register_size (int): The number of qubits in the quantum register.
        """
        self.register_size = int(register_size)
        self.register = makeStateVector(0, register_size)
        self.groverOperator = None
        self.gates = Gate(register_size)

        pass

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__qualname__, self.register_size)

    def h(self):
        r"""
        Applies the Hadamard gate to all qubits in the quantum register.

        This method retrieves the Hadamard gate matrix from the `gates` object,
        raises it to the power of the register size to create a tensor product,
        and then applies the resulting operator to the quantum register.

        The quantum register is updated with the new state after applying the
        Hadamard gate.
        """
        h = self.gates.h()
        product = h ** int(self.register_size)
        self.register = self.register.apply(product)
        return

    def grover(self, target: int):
        r"""
        Runs Grover's algorithm on the quantum circuit to find the target state.

        This method calculates the number of iterations required for Grover's
        algorithm based on the register size and the target state. It then
        constructs the Grover operator by combining the oracle, Hadamard gates,
        and reflection operator.

        The Grover operator is applied to the quantum register for the calculated
        number of iterations to amplify the amplitude of the target state.

        Params:
            target (int): The target state to find using Grover's algorithm.
        """

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
        r"""
        Measures the quantum circuit and prints the probability of the target state.

        This method performs a measurement on the quantum circuit to determine the
        probability of observing the target state. It calculates the inner product
        between the target state vector and the current state vector of the quantum
        register.

        Params:
            target (int): The target state to measure the probability for.
        """
        target = int(target)

        print("I think I've found it!")
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
