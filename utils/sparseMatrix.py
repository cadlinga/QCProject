r"""
Sparse Matrix Implementation
=============================
This module provides an implementation of a sparse matrix using the `matrixInterface`.
It supports various matrix operations such as tensor product, multiplication, addition,
subtraction, negation, scaling, and equality comparison.

The sparse matrix can be constructed from a list of elements or another matrix.
It also supports vector representation.
"""

from __future__ import annotations
from typing import Union

from numpy._typing import ArrayLike
from utils.matrixInterface import matrixInterface

from scipy.sparse import coo_array, kron
from numpy import array, allclose


class sparseMatrix(matrixInterface):
    r"""
    This class represents a sparse matrix and provides methods for performing various matrix
    operations.
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
            matrix (coo_array): The underlying `scipy.sparse.coo_array` representing the matrix.
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
    def matrix(self) -> coo_array:
        return self._matrix

    @matrix.setter
    def matrix(self, elements):
        r"""
        Sets the matrix elements for the sparse matrix.

        Args:
            elements (Union[list, matrixInterface]): The matrix elements as a list or another matrix.
        """

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
        r"""
        Computes the tensor product of the sparse matrix with another matrix.

        Args:
            other (matrixInterface): The other matrix to compute the tensor product with.

        Returns:
            sparseMatrix: The tensor product matrix.
        """

        product = kron(self.matrix, other.matrix)
        size = self.size * other.size
        return sparseMatrix(size, product, self.vector)

    def __str__(self):
        return self.matrix.todense().__str__()

    def reshape(self, rows: int, cols: int) -> sparseMatrix:
        r"""
        Reshapes the sparse matrix to the specified dimensions.

        Args:
            rows (int): The number of rows in the reshaped matrix.
            cols (int): The number of columns in the reshaped matrix.

        Returns:
            sparseMatrix: The reshaped matrix.
        """
        self.matrix.reshape(rows, cols)
        return self

    def update(self, row: int, col: int, value: float) -> sparseMatrix:
        r"""
        Updates a specific element of the sparse matrix.

        Args:
            row (int): The row index of the element to update.
            col (int): The column index of the element to update.
            value (float): The new value of the element.

        Returns:
            sparseMatrix: The updated matrix.
        """

        matrix = self.matrix.todense()
        matrix[row][col] = value
        self.matrix = coo_array(matrix)
        return self

    def negate(self) -> sparseMatrix:
        r"""
        Negates the sparse matrix.

        Returns:
            sparseMatrix: The negated matrix.
        """
        self.matrix = -1 * self.matrix
        return self

    def equal(self, other: matrixInterface) -> bool:
        r"""
        Checks if the sparse matrix is equal to another matrix.

        Args:
            other (matrixInterface): The other matrix to compare with.

        Returns:
            bool: True if the matrices are equal, False otherwise.
        """
        return allclose(self.matrix.todense(), other.matrix.todense())

    def scale(self, factor: float) -> sparseMatrix:
        r"""
        Scales the sparse matrix by a factor.

        Args:
            factor (float): The scaling factor.

        Returns:
            sparseMatrix: The scaled matrix.
        """

        self.matrix = factor * self.matrix
        return self

    def multiply(self, other: matrixInterface) -> sparseMatrix:
        r"""
        Multiplies the sparse matrix with another matrix.

        Args:
            other (matrixInterface): The other matrix to multiply with.

        Returns:
            sparseMatrix: The product matrix.
        """
        product = self.matrix.dot(other.matrix)
        return sparseMatrix(1, product, other.vector)

    def power(self, exponent: int) -> sparseMatrix:
        r"""
        Raises the sparse matrix to a power.

        Args:
            exponent (int): The exponent to raise the matrix to.

        Returns:
            sparseMatrix: The matrix raised to the specified power.
        """

        initial = self
        i = 1
        while i < exponent:
            self.tensor(initial)
            i = i + 1
        return self

    def add(self, other: matrixInterface) -> sparseMatrix:
        r"""
        Adds another matrix to the sparse matrix.

        Args:
            other (matrixInterface): The other matrix to add.

        Returns:
            sparseMatrix: The sum of the matrices.
        """
        self.matrix = self.matrix + other.matrix
        return self

    def subtract(self, other: matrixInterface) -> sparseMatrix:
        r"""
        Subtracts another matrix from the sparse matrix.

        Args:
            other (matrixInterface): The other matrix to subtract.

        Returns:
            sparseMatrix: The difference matrix.
        """
        self.matrix = self.matrix - other.matrix
        return self

    def toVector(self) -> sparseMatrix:
        r"""
        Converts the sparse matrix to a vector.

        Returns:
            sparseMatrix: The matrix as a vector.
        """
        self.matrix = self.matrix.reshape(self.matrix.get_shape()[0], 1)
        return self

    def dimension(self) -> int:
        r"""
        Returns the dimensions of the sparse matrix
        """

        return self.matrix.get_shape()[0]

    def flat(self) -> ArrayLike:
        r"""
        Returns the flattened matrix as a 1D array
        """
        
        return self.matrix.todense().flatten()
