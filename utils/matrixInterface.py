r"""
Matrix Interface
================
The matrix interface relies on the pipeline pattern whereby, with few exceptions, the methods
should all return an object of the matrixInterface. This allows for methods to be chained 
for more readable code. 

The parent class and available methods are described.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Union

from numpy._typing import ArrayLike
from scipy.sparse import coo_array


class matrixInterface(ABC):
    r"""
    This class serves as the Abstract Base Class (ABC or interface) for the
    concrete implementations of the matrix object.
    """

    def __init__(self, size, elements):
        pass

    @property
    @abstractmethod
    def matrix(
        self,
    ) -> Union[coo_array, ArrayLike]:
        r"""
        The matrix property stores the array like object which handles the state
        of the object.
        """

        pass

    @property
    @abstractmethod
    def size(self) -> int:
        r"""
        The size property is used when the parent object is an operator and casts the
        array into a size x size matrix.
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        r"""This magic method defines how the object is cast into a string, which will vary depending
        on the type of object used for the matrix property.
        """
        pass

    @abstractmethod
    def tensor(self, other: matrixInterface) -> matrixInterface:
        r"""
        Computes the tensor product of the matrix with another matrix.
        """

        # Below is ignored by Sphinx
        """
        Args:
            other (matrixInterface): The other matrix to compute the tensor product with.

        Returns:
            matrixInterface: The tensor product two matrices.
        """

        pass

    @abstractmethod
    def reshape(self, rows: int, cols: int) -> matrixInterface:
        r"""
        Casts the matrix object into a specific shape e.g. into a column for vectors or
        a square for operators.
        """
        pass

    @abstractmethod
    def update(self, row: int, col: int, value: float) -> matrixInterface:
        r"""
        Updates a specific index of the matrix to the provided value.
        """
        pass

    @abstractmethod
    def multiply(self, other: matrixInterface) -> matrixInterface:
        r"""
        Performs matrix multiplication of two matrices. The order should be provided as it would
        be written.
        """
        pass

    @abstractmethod
    def power(self, exponent: int) -> matrixInterface:
        r"""
        Iteratively performs a tensor product as many times required. Useful for example when raising a
        gate to the power of the size of the quantum register to fully entangle the register.
        """
        pass

    @abstractmethod
    def add(self, other: matrixInterface) -> matrixInterface:
        r"""
        Performs elementwise addition of two matrices of the same size.
        """
        pass

    @abstractmethod
    def subtract(self, other: matrixInterface) -> matrixInterface:
        r"""
        Performs elementwise subtraction of two matrices of the same size.
        """
        pass

    @abstractmethod
    def equal(self, other: matrixInterface) -> matrixInterface:
        r"""
        Compares two matrices to check for equality, this will be a costly operation so
        should be reserved for testing.
        """
        pass

    @abstractmethod
    def negate(self) -> matrixInterface:
        r"""
        Returns the original matrix with each element set to its own negative.
        """
        pass

    @abstractmethod
    def scale(self, factor: float) -> matrixInterface:
        r"""
        Performs elementwise scalar multiplication by the supplied factor.
        """
        pass

    @abstractmethod
    def toVector(self) -> matrixInterface:
        r"""
        Convenience method to cast a matrix into a column i.e. 1 column and as many rows as elements.
        """
        pass

    @abstractmethod
    def dimension(self) -> matrixInterface:
        r"""
        Returns the number of rows in a column matrix or the number of rows and columns for a square matrix.
        """
        pass

    @abstractmethod
    def flat(self) -> ArrayLike:
        r"""
        Returns a flattened version of the matrix, this is equivalent to the transpose for column matrices
        so can be used during measurement.
        """
        pass

    #            CONCRETE            #
    def __mul__(self, other: matrixInterface) -> matrixInterface:
        self.multiply(other)
        return self

    def __pow__(self, exponent: int) -> matrixInterface:
        self.power(exponent)
        return self

    def __add__(self, other: matrixInterface) -> matrixInterface:
        self.add(other)
        return self

    def __sub__(self, other: matrixInterface) -> matrixInterface:
        self.subtract(other)
        return self
