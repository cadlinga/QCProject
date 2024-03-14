from __future__ import annotations
from typing import Union

from numpy._typing import ArrayLike
from utils.matrixInterface import matrixInterface

from scipy.sparse import coo_array, kron
from numpy import array, allclose


class sparseMatrix(matrixInterface):

    def __init__(self, size: int, elements: Union[list, matrixInterface], vector=False):
        self.size = size
        self.vector = vector
        self.matrix = elements

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
        return

    @property
    def matrix(self) -> coo_array:
        return self._matrix

    @matrix.setter
    def matrix(self, elements):

        if isinstance(elements, list):
            if self.vector:
                matrix = coo_array(array(elements).reshape(len(elements), 1))
            else:
                matrix = coo_array(
                    array(elements).reshape(self.size, self.size))
        else:
            matrix = elements

        self._matrix = matrix
        return

    def tensor(self, other: matrixInterface) -> sparseMatrix:
        product = kron(self.matrix, other.matrix)
        size = self.size * other.size
        return sparseMatrix(size, product, self.vector)

    def __str__(self):
        return self.matrix.todense().__str__()

    def reshape(self, rows: int, cols: int) -> sparseMatrix:
        self.matrix.reshape(rows, cols)
        return self

    def update(self, row: int, col: int, value: float) -> sparseMatrix:
        matrix = self.matrix.todense()
        matrix[row][col] = value
        self.matrix = coo_array(matrix)
        return self

    def negate(self) -> sparseMatrix:
        self.matrix = -1 * self.matrix
        return self

    def equal(self, other: matrixInterface) -> bool:
        return allclose(self.matrix.todense(), other.matrix.todense())

    def scale(self, factor: float) -> sparseMatrix:
        self.matrix = factor * self.matrix
        return self

    def multiply(self, other: matrixInterface) -> sparseMatrix:
        product = self.matrix.dot(other.matrix)
        return sparseMatrix(1, product, other.vector)

    def power(self, exponent: int) -> sparseMatrix:
        initial = self
        i = 1
        while i < exponent:
            self.tensor(initial)
            i = i + 1
        return self

    def add(self, other: matrixInterface) -> sparseMatrix:
        self.matrix = self.matrix + other.matrix
        return self

    def subtract(self, other: matrixInterface) -> sparseMatrix:
        self.matrix = self.matrix - other.matrix
        return self

    def toVector(self) -> sparseMatrix:
        self.matrix = self.matrix.reshape(self.matrix.get_shape()[0], 1)
        return self

    def dimension(self) -> int:
        return self.matrix.get_shape()[0]

    def flat(self) -> ArrayLike:
        return self.matrix.todense().flatten()
