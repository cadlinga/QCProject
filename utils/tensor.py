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

    def __add__(self, other):
        return Vector(numpy.add(self.vector, other.vector))

    def __sub__(self, other):
        return Vector(numpy.subtract(self.vector, other.vector))

    def __mul__(self, other):
        # Scalar multiplication only at the moment.
        return Vector((self.vector * other))

    __rmul__ = __mul__

    def __repr__(self):
        return self.vector.__repr__()


def tensorDot(a: _ArrayLikeUnknown, b):
    """
    This function, when written will compute the tensor product of two
    array like objects. Currently it is tested against numpy.tensordot
    in order to confirm the validity of our home-rolled function.
    """

    # return [1, 2, 3, 4]
    return numpy.tensordot(a, b, 0)
