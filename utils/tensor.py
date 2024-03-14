from __future__ import annotations
from typing import Union
import numpy

# from utils.gate import squareMatrix
from utils.matrix import sparseMatrix
import scipy
from scipy.sparse import coo_array

from utils.matrixInterface import matrixInterface


class Operator:
    def __init__(self, size: int, elements: Union[list, matrixInterface]):
        self.matrix = sparseMatrix(size, elements)
        # self.matrix = denseMatrix(size, elements)

    @property
    def matrix(self) -> matrixInterface:
        return self._matrix

    @matrix.setter
    def matrix(self, matrix: matrixInterface):
        self._matrix = matrix
        return

    def tensor(self, target: Operator):
        matrix = self.matrix.tensor(target.matrix).matrix
        size = self.matrix.size * target.matrix.size
        return Operator(size, matrix)
        self.matrix = self.matrix.tensor(target.matrix)
        return self

    def __str__(self):
        return self.matrix.__str__()

    def __add__(self, target: Operator):
        self.matrix = self.matrix + target.matrix
        return self

    def __sub__(self, target):
        self.matrix = self.matrix - target.matrix
        return self

    def __pow__(self, n: int):
        product = self
        i = 1
        while i < n:
            product = product.tensor(self)
            i = i + 1
        return product

        self.matrix = self.matrix.power(n)
        return self

    def update(self, row, column, value):
        self.matrix = self.matrix.update(row, column, value)
        return self

    def __mul__(self, other):
        matrix = other.matrix.multiply(self.matrix).matrix
        size = self.matrix.size
        return Operator(size, matrix)

        # self.matrix = self.matrix * other.matrix
        # self.matrix = numpy.matmul(other.matrix, self.matrix)
        # return self

    def negate(self):
        self.matrix = self.matrix.negate()
        return self

    def equal(self, target):
        return self.matrix.equal(target.matrix)

    def scale(self, value: float):
        self.matrix = self.matrix.scale(value)
        return self


class Vector:
    # def __init__(self, elements: Union[int, list, matrixInterface]):
    # self.matrix = sparseMatrix(size, elements)
    # self.matrix = denseMatrix(size, elements)

    @property
    def matrix(self) -> matrixInterface:
        return self._matrix

    @matrix.setter
    def matrix(self, matrix: matrixInterface):
        self._matrix = matrix
        return

    def __init__(self, elements: Union[list[int], int, matrixInterface]):
        if isinstance(elements, int):
            while elements not in [0, 1]:
                raise Exception(
                    """
                    If passing an int to this class it must be
                    0 or 1.
                    """
                )
            if elements == 0:
                elements = [1, 0]
            elif elements == 1:
                elements = [0, 1]

        if isinstance(elements, list):
            # THIS IS LIKELY TO BUG!
            self.vector = sparseMatrix(len(elements), elements, True)
            self.dimension = self.vector.dimension()
            return

        if isinstance(elements, matrixInterface):
            self.vector = elements.toVector()
        # else:
        #     self.length = elements.size
        #     size = elements.get_shape()[0] * elements.get_shape()[1]
        #     # print(elements.get_shape())
        #     self.vector = elements.reshape(size, 1)
        #     self.dimension = self.vector.get_shape()[0]

    def tensor(self, target: Vector):
        self.vector = self.vector.tensor(target.vector)
        return self

    def scale(self, scalar: float):
        self.vector = self.vector.scale(scalar)
        return self
        # try:
        #     # print(self.vector)
        #     # print(target.vector)
        #     product = scipy.sparse.kron(self.vector, target.vector)
        #
        #     return Vector(product)
        # except:
        #
        #     product = []
        #     for i in self.vector:
        #         for j in target.vector:
        #             product.append(i * j)
        #     return Vector(product)

    # def outer(self, target):
    #     outer = numpy.outer(self.vector.transpose(), target.vector)
    #     return Operator(self.vector.size, outer.tolist())

    def __add__(self, other: Vector):
        self.vector = self.vector + other.vector
        return self
        # return Vector(numpy.add(self.vector, other.vector))

    def __sub__(self, other):
        self.vector = self.vector - other.vector
        return self
        return Vector(numpy.subtract(self.vector, other.vector))

    # def __mul__(self, other):
    #     self.vector = self.vector * other.matrix
    #     return self
    # return Vector((self.vector * other))

    #
    # __rmul__ = __mul__

    def __pow__(self, n: int):
        self.vector = self.vector**n
        return self
        # i = 1
        # product = self
        # while i < n:
        #     product = product.tensor(self)
        #     i = i + 1
        #
        # return product

    # def __repr__(self):
    #     return self.vector.__rep__()

    def __str__(self):
        return self.vector.__str__()

    def apply(self, operator: Operator):
        # self.vector = self.vector * operator.matrix
        product = operator.matrix.multiply(self.vector)

        return Vector(product)
        return self
        # product = numpy.matmul(operator.matrix, self.vector)
        # product = operator.matrix.dot(coo_array(self.vector))
        # return Vector(product)

    def equal(self, target: Vector):
        return self.vector.equal(target.vector)
        return numpy.allclose(self.vector.todense(), target.vector.todense())

    def measure(self, basis: Vector):
        value = numpy.dot(
            basis.vector.flat(),
            self.vector.flat(),
        )

        return value
        # numpy.dot(
        #         makeStateVector(target, self.register_size)
        #         .vector.todense()
        #         .flatten(),
        #         self.register.vector.todense().flatten(),
        #     )


#
# def tensorDot(a: _ArrayLikeUnknown, b):
#     """
#     This function, when written will compute the tensor product of two
#     array like objects. Currently it is tested against numpy.tensordot
#     in order to confirm the validity of our home-rolled function.
#     """
#
#     # return [1, 2, 3, 4]
#     return numpy.tensordot(a, b, 0)
