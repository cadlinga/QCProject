r"""
Tensor Module
=============
This module provides classes for working with operators and vectors in a quantum computing context.
It includes the `Operator` class for representing quantum operators and the `Vector` class for
representing quantum state vectors.

The `Operator` class supports operations tensor products, addition, subtraction,
exponentiation, and matrix multiplication. It also provides methods for updating matrix elements,
negating the matrix, and scaling the matrix by a value.

The `Vector` class supports operations tensor products,  addition, subtraction,
scalar multiplication, and exponentiation. It also provides methods for applying an operator to a
vector and checking equality between vectors.

This is all achieved abstractly through the implementation of a `Matrix` property of each 
object. See `matrixInterface` for more details on available methods. 
"""

from __future__ import annotations
from utils.matrixInterface import matrixInterface
from typing import Union
import numpy

sparsity = "dense"  # "sparse" or "dense"


if sparsity == "dense":
    from utils.denseMatrix import denseMatrix as Matrix
else:
    from utils.sparseMatrix import sparseMatrix as Matrix


class Operator:
    r"""
    This class represents a quantum operator as a sparse matrix.

    It may take a list or `matrixInterface` in the constructor.
    """

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
        r"""
        Computes the tensor product of the operator with another operator.

        Args:
            target (Operator): The operator to compute the tensor product with.

        Returns:
            Operator: The tensor product operator.
        """

        matrix = self.matrix.tensor(target.matrix).matrix
        size = self.matrix.size * target.matrix.size
        return Operator(size, matrix)

    def __str__(self):
        return self.matrix.__str__()

    def __add__(self, target: Operator):
        r"""
        Adds the operator with another operator.

        Args:
            target (Operator): The operator to add.

        Returns:
            Operator: The sum of the operators.
        """

        self.matrix = self.matrix + target.matrix
        return self

    def __sub__(self, target):
        r"""
        Subtracts another operator from the operator.

        Args:
            target (Operator): The operator to subtract.

        Returns:
            Operator: The difference of the operators.
        """

        self.matrix = self.matrix - target.matrix
        return self

    def __pow__(self, n: int):
        r"""
        Computes the n-th power of the operator.

        Args:
            n (int): The exponent.

        Returns:
            Operator: The operator raised to the n-th power.
        """

        product = self
        i = 1
        while i < n:
            product = product.tensor(self)
            i = i + 1
        return product

    def update(self, row, column, value):
        r"""
        Updates a specific element of the operator matrix.

        Args:
            row (int): The row index of the element to update.
            column (int): The column index of the element to update.
            value (float): The new value of the element.

        Returns:
            Operator: The updated operator.
        """

        self.matrix = self.matrix.update(row, column, value)
        return self

    def __mul__(self, other):
        r"""
        Multiplies the operator with another operator.

        Args:
            other (Operator): The operator to multiply with.

        Returns:
            Operator: The product of the operators.
        """

        matrix = other.matrix.multiply(self.matrix).matrix
        size = self.matrix.size
        return Operator(size, matrix)

    def negate(self):
        r"""
        Negates the operator matrix.

        Returns:
            Operator: The negated operator.
        """

        self.matrix = self.matrix.negate()
        return self

    def equal(self, target):
        r"""
        Checks if the operator is equal to another operator.

        Args:
            target (Operator): The operator to compare with.

        Returns:
            bool: True if the operators are equal, False otherwise.
        """

        return self.matrix.equal(target.matrix)

    def scale(self, value: float):
        r"""
        Scales the operator matrix by a value.

        Args:
            value (float): The scaling factor.

        Returns:
            Operator: The scaled operator.

        ----
        """

        self.matrix = self.matrix.scale(value)
        return self


class Vector:
    r"""
    This class represents a quantum state vector.

    It may take the integer 1 or 0 to create a single qubit in the given state,
    a list or `matrixInterface` in the constructor.
    """

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
        r"""
        Computes the tensor product of the vector with another vector.

        Args:
            target (Vector): The vector to compute the tensor product with.

        Returns:
            Vector: The tensor product vector.
        """
        self.vector = self.vector.tensor(target.vector)
        return self

    def scale(self, scalar: float):
        r"""
        Scales the vector by a value.

        Args:
            value (float): The scaling factor.

        Returns:
            Vector: The scaled vector.
        """
        self.vector = self.vector.scale(scalar)
        return self

    def __add__(self, other: Vector):
        r"""
        Adds the vector with another vector.

        Args:
            other (Vector): The vector to add.

        Returns:
            Vector: The sum of the vectors.
        """

        self.vector = self.vector + other.vector
        return self

    def __sub__(self, other):
        r"""
        Subtracts another vector from the vector.

        Args:
            other (Vector): The vector to subtract.

        Returns:
            Vector: The difference of the vectors.
        """

        self.vector = self.vector - other.vector
        return self

    def __pow__(self, n: int):
        r"""
        Computes the n-th tensor power of the vector.

        Args:
            n (int): The exponent.

        Returns:
            Vector: The vector raised to the n-th tensor power.
        """
        self.vector = self.vector**n
        return self

    def __str__(self):
        return self.vector.__str__()

    def apply(self, operator: Operator):
        r"""
        Applies an operator to the vector.

        Args:
            operator (Operator): The operator to apply.

        Returns:
            Vector: The resulting vector after applying the operator.
        """

        product = operator.matrix.multiply(self.vector)
        return Vector(product)

    def equal(self, target: Vector):
        r"""
        Checks if the vector is equal to another vector.

        Args:
            target (Vector): The vector to compare with.

        Returns:
            bool: True if the vectors are equal, False otherwise.
        """

        return self.vector.equal(target.vector)

    def measure(self, basis: Vector):
        r"""
        Measures the vector with respect to a basis vector.

        Args:
            basis (Vector): The basis vector to measure against.

        Returns:
            float: The measurement result.

        ----
        """

        value = numpy.dot(
            basis.vector.flat(),
            self.vector.flat(),
        )

        return value
