r"""
Dense Matrix Implementation
=============================
This module provides an implementation of a dense matrix using the `matrixInterface`.
It supports various matrix operations such as tensor product, multiplication, addition,
subtraction, negation, scaling, and equality comparison.

The dense matrix can be constructed from a list of elements or another matrix.
It also supports vector representation.
"""

from __future__ import annotations
from typing import Union

from numpy._typing import ArrayLike, NDArray
from utils.matrixInterface import matrixInterface

from numpy import array, allclose, matmul


class denseMatrix(matrixInterface):
    r"""
    This class represents a dense matrix and provides methods for performing various
    matrix operations.
    """

    def __init__(self, size: int, elements: Union[list, matrixInterface], vector=False):
        r"""
        Args:
            size (int): The size of the matrix.
            elements (Union[list, matrixInterface]): The matrix elements as a list or another matrix.
            vector (bool): Indicates if the matrix represents a vector.

        Attributes:
            size (int): The size of the matrix.
            vector (bool): Indicates if the matrix represents a vector.
            matrix (NDArray): The underlying `numpy` array representing the matrix.
        """

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
        r"""
        Sets the matrix elements for the dense matrix.

        Args:
            elements (Union[list, matrixInterface]): The matrix elements as a list or another matrix.
        """

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
        r"""
        Dense matrix implementation to compute the tensor product of the matrix with another matrix.

        Args:
            other (denseMatrix): The other matrix to compute the tensor product with.

        Returns:
            denseMatrix: The tensor product matrix.
        """

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
        r"""
        Dense matrix implementation to reshape the matrix to the specified dimensions.

        Args:
            rows (int): The number of rows in the reshaped matrix.
            cols (int): The number of columns in the reshaped matrix.

        Returns:
            denseMatrix: The reshaped matrix.
        """

        self.matrix.reshape(rows, cols)
        return self

    def update(self, row: int, col: int, value: float) -> denseMatrix:
        r"""
        Dense matrix implementation to update a specific element of the matrix.

        Args:
            row (int): The row index of the element to update.
            col (int): The column index of the element to update.
            value (float): The new value of the element.

        Returns:
            denseMatrix: The updated matrix.
        """
        self.matrix[row][col] = value
        return self

    def negate(self) -> denseMatrix:
        r"""
        Negates the dense matrix.

        Returns:
            denseMatrix: The negated matrix.
        """

        self.matrix = -1 * self.matrix
        return self

    def equal(self, other: denseMatrix) -> bool:
        r"""
        Checks if the dense matrix is equal to another dense matrix.

        Args:
            other (denseMatrix): The other matrix to compare with.

        Returns:
            bool: True if the matrices are equal, False otherwise.
        """

        return allclose(self.matrix, other.matrix)

    def scale(self, factor: float) -> denseMatrix:
        r"""
        Scales the dense matrix by a factor.

        Args:
            factor (float): The scaling factor.

        Returns:
            denseMatrix: The scaled matrix.
        """

        self.matrix = factor * self.matrix
        return self

    def multiply(self, other: denseMatrix) -> denseMatrix:
        r"""
        Multiplies dense matrix with another dense matrix.

        Args:
            other (denseMatrix): The other matrix to multiply with.

        Returns:
            denseMatrix: The product matrix.
        """

        product = matmul(self.matrix, other.matrix)
        return denseMatrix(self.size, product, other.vector)

    def power(self, exponent: int) -> denseMatrix:
        r"""
        Raises the dense matrix to a power.

        Args:
            exponent (int): The exponent to raise the matrix to.

        Returns:
            denseMatrix: The matrix raised to the specified power.
        """

        initial = self
        i = 1
        while i < exponent:
            self.tensor(initial)
            i = i + 1
        return self

    def add(self, other: matrixInterface) -> denseMatrix:
        r"""
        Adds another matrix to the dense matrix.

        Args:
            other (matrixInterface): The other matrix to add.

        Returns:
            denseMatrix: The sum of the matrices.
        """

        self.matrix = self.matrix + other.matrix
        return self

    def subtract(self, other: matrixInterface) -> denseMatrix:
        r"""
        Subtracts another matrix from the dense matrix.

        Args:
            other (matrixInterface): The other matrix to subtract.

        Returns:
            denseMatrix: The difference matrix.
        """

        self.matrix = self.matrix - other.matrix
        return self

    def toVector(self) -> denseMatrix:
        r"""
        Converts the dense matrix to a vector.

        Returns:
            denseMatrix: The matrix reshaped as a vector.
        """

        self.matrix = self.matrix.reshape(self.matrix.shape[0], 1)
        return self

    def dimension(self) -> int:
        r"""
        Returns the dimension of the matrix.
        """

        return self.matrix.shape[0]

    def flat(self) -> ArrayLike:
        r"""
        Returns the matrix flattened into a 1D array.
        """

        return self.matrix.flatten()
