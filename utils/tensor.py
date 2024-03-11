from typing import Union
import numpy
from numpy._typing import _ArrayLikeUnknown

from utils.gate import squareMatrix

### IGNORE THIS TEXT: GIT DESKTOP TEST - KEVIN ###
class Operator:
    def __init__(self, size: int, elements: list):
        self.matrix = squareMatrix(size, elements)
        self.size = size

    def tensor(self, target):
        product = []

        for rows in self.matrix:
            row = 0
            while row < self.matrix.ndim:
                for entry in rows:
                    column = 0
                    while column < self.matrix.ndim:
                        product.append(entry * target.matrix[row, column])
                        column += 1
                row += 1
        return Operator(self.size * target.size, product)

    def __str__(self):
        return self.matrix.__str__()

    def __add__(self, target):
        sum = self.matrix + target.matrix
        # print(sum)
        # print(sum.flatten().tolist())

        return Operator(self.size, sum.flatten().tolist())

    def __sub__(self, target):
        diff = self.matrix - target.matrix
        # print(sum)
        # print(sum.flatten().tolist())

        return Operator(self.size, diff.flatten().tolist())

    def __pow__(self, n):
        i = 1
        product = self
        while i < n:
            product = product.tensor(self)
            i = i + 1

        return product

    def update(self, row, column, value):
        self.matrix[row][column] = value
        return self

    def __mul__(self, other):
        self.matrix = numpy.matmul(other.matrix, self.matrix)
        return self

    def negate(self):
        self.matrix = -1 * self.matrix
        return self


class Vector:
    def __init__(self, elements: Union[list[int], int]):
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

            if elements == 1:
                elements = [0, 1]

        self.vector = numpy.resize(elements, [len(elements), 1])
        self.dimension = self.vector.size

    def tensor(self, target):
        product = []
        for i in self.vector:
            for j in target.vector:
                product.append(i * j)
        return Vector(product)

    def outer(self, target):
        outer = numpy.outer(self.vector.transpose(), target.vector)
        return Operator(self.vector.size, outer.tolist())

    def __add__(self, other):
        return Vector(numpy.add(self.vector, other.vector))

    def __sub__(self, other):
        return Vector(numpy.subtract(self.vector, other.vector))

    def __mul__(self, other):
        # Scalar multiplication only at the moment.
        return Vector((self.vector * other))

    __rmul__ = __mul__

    def __pow__(self, n):
        i = 1
        product = self
        while i < n:
            product = product.tensor(self)
            i = i + 1

        return product

    def __repr__(self):
        return self.vector.__rep__()

    def __str__(self):
        return self.vector.__str__()

    def apply(self, operator: Operator):
        product = numpy.matmul(operator.matrix, self.vector)
        return Vector(product.flatten().tolist())


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
