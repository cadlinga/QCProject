from __future__ import annotations
from typing import Union
import numpy

# from utils.sparseMatrix import sparseMatrix as Matrix
from utils.denseMatrix import denseMatrix as Matrix

from utils.matrixInterface import matrixInterface


class Operator:
    def __init__(self, size: int, elements: Union[list, matrixInterface]):
        self.matrix = Matrix(size, elements)

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

    def update(self, row, column, value):
        self.matrix = self.matrix.update(row, column, value)
        return self

    def __mul__(self, other):
        matrix = other.matrix.multiply(self.matrix).matrix
        size = self.matrix.size
        return Operator(size, matrix)

    def negate(self):
        self.matrix = self.matrix.negate()
        return self

    def equal(self, target):
        return self.matrix.equal(target.matrix)

    def scale(self, value: float):
        self.matrix = self.matrix.scale(value)
        return self


class Vector:

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
            self.vector = Matrix(len(elements), elements, True)
            self.dimension = self.vector.dimension()
            return

        if isinstance(elements, matrixInterface):
            self.vector = elements.toVector()

    def tensor(self, target: Vector):
        self.vector = self.vector.tensor(target.vector)
        return self

    def scale(self, scalar: float):
        self.vector = self.vector.scale(scalar)
        return self

    def __add__(self, other: Vector):
        self.vector = self.vector + other.vector
        return self
        # return Vector(numpy.add(self.vector, other.vector))

    def __sub__(self, other):
        self.vector = self.vector - other.vector
        return self

    def __pow__(self, n: int):
        self.vector = self.vector**n
        return self

    def __str__(self):
        return self.vector.__str__()

    def apply(self, operator: Operator):
        product = operator.matrix.multiply(self.vector)
        return Vector(product)

    def equal(self, target: Vector):
        return self.vector.equal(target.vector)

    def measure(self, basis: Vector):
        value = numpy.dot(
            basis.vector.flat(),
            self.vector.flat(),
        )

        return value
