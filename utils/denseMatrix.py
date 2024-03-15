r"""
Dense Matrix Implementation
=============================
"""

from __future__ import annotations
from typing import Union

from numpy._typing import ArrayLike, NDArray
from utils.matrixInterface import matrixInterface

from numpy import array, allclose, matmul


class denseMatrix(matrixInterface):

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
    def matrix(self) -> NDArray:
        return self._matrix

    @matrix.setter
    def matrix(self, elements):

        if isinstance(elements, list):
            if self.vector:
                matrix = array(array(elements).reshape(len(elements), 1))
            else:
                matrix = array(array(elements).reshape(self.size, self.size))
        else:
            matrix = elements

        self._matrix = matrix
        return

    def tensor(self, other: denseMatrix) -> denseMatrix:
        product = []

        if self.vector or other.vector:
            for i in self.matrix:
                for j in other.matrix:
                    product.append(i * j)
            return denseMatrix(2, product, True)

        for rows in self.matrix:
            row = 0
            while row < self.matrix.ndim:
                for entry in rows:
                    column = 0
                    while column < self.matrix.ndim:
                        product.append(entry * other.matrix[row, column])
                        column += 1
                row += 1

        return denseMatrix(self.size * other.size, product)

    def __str__(self):
        return self.matrix.__str__()

    def reshape(self, rows: int, cols: int) -> denseMatrix:
        self.matrix.reshape(rows, cols)
        return self

    def update(self, row: int, col: int, value: float) -> denseMatrix:
        self.matrix[row][col] = value
        return self

    def negate(self) -> denseMatrix:
        self.matrix = -1 * self.matrix
        return self

    def equal(self, other: denseMatrix) -> bool:
        return allclose(self.matrix, other.matrix)

    def scale(self, factor: float) -> denseMatrix:
        self.matrix = factor * self.matrix
        return self

    def multiply(self, other: denseMatrix) -> denseMatrix:
        product = matmul(self.matrix, other.matrix)
        return denseMatrix(self.size, product, other.vector)

    def power(self, exponent: int) -> denseMatrix:
        initial = self
        i = 1
        while i < exponent:
            self.tensor(initial)
            i = i + 1
        return self

    def add(self, other: matrixInterface) -> denseMatrix:
        self.matrix = self.matrix + other.matrix
        return self

    def subtract(self, other: matrixInterface) -> denseMatrix:
        self.matrix = self.matrix - other.matrix
        return self

    def toVector(self) -> denseMatrix:
        self.matrix = self.matrix.reshape(self.matrix.shape[0], 1)
        return self

    def dimension(self) -> int:
        return self.matrix.shape[0]

    def flat(self) -> ArrayLike:
        return self.matrix.flatten()
