r"""
Gate Module
===========
This module provides utility functions and the `Gate` class for working with quantum gates.

The `squareMatrix` function creates a square matrix from a list of elements, and the `vector`
function creates a column vector from a list of elements.

The `Gate` class represents a quantum gate and provides methods for gathering and scattering
bits, as well as applying the gate to a vector.
"""

import numpy


def squareMatrix(size: int, elements: list[int]):
    r"""
    Creates a square matrix from a list of elements.

    Args:
        size (int): The size of the square matrix.
        elements (list[int]): The list of elements to populate the matrix.

    Returns:
        numpy.ndarray: The square matrix created from the elements.
    """

    return numpy.array(elements).reshape(size, size)


def vector(elements: list[int]):
    r"""
    Creates a column vector from a list of elements.

    Args:
        elements (list[int]): The list of elements to populate the vector.

    Returns:
        numpy.ndarray: The column vector created from the elements.
    """

    return numpy.array(elements).reshape(len(elements), 1)


class Gate:  # LazyMatrix to be implemented later
    r"""
    Represents a quantum gate.

    The `Gate` class provides methods for gathering and scattering bits, as well as
    applying the gate to a vector.

    Args:
        qubitPosition (list[int]): The positions of the qubits the gate acts on.
    """

    def __init__(self, qubitPosition: list[int]) -> None:
        self._smallMatrix = squareMatrix(2, [1, 2, 3, 4])
        self._qbpos = qubitPosition

    def gather(self, i: int):
        """
        Gathers the bits of the input integer `i` at the positions specified
        by the `qbpos` list and packs them into a new integer.

        Args:
            i: The input integer.

        Returns:
            An integer with the bits of `i` at the positions specified by
            `qbpos` packed together.
        """
        j = 0
        k = 0
        bit = 0
        for k in range(len(self._qbpos)):
            # Extract the bit at position `qbpos[k]` of `i`.
            # cast to integers explicitly to allow bitwise manipulation
            bit = (int(i) >> int(self._qbpos[k])) & 1
            # Pack the bit into position `k` of `j`.
        j |= bit << k
        return j

    def scatter(self, j: int):
        """
         Scatters the bits of the input integer `j` into the
         positions specified by the `qbpos` list and packs them into a new
         integer.

        Args:
            j: The input integer.

        Returns:
            An integer with the bits of `j` scattered into the positions
            specified by `qbpos`.
        """

        i = 0
        k = 0
        for k in range(len(self._qbpos)):
            # Extract the bit at position `k` of `j`.
            bit = (j >> k) & 1
            # Pack the bit into position `qbpos[k]` of `i`.
            i |= bit << self._qbpos[k]
        return i

    def apply(self, v: list):
        r"""
        Applies the gate to the input vector `v`.

        This method gathers the bits of each element in `v`, applies the gate matrix
        to the gathered bits, and then scatters the bits back into the original positions.

        Args:
            v (list): The input vector to apply the gate to.

        Returns:
            list: The resulting vector after applying the gate.
        
        ----
        """
        
        w: list = [0] * len(v)
        for i in range(len(w)):
            r = self.gather(i)
            i0 = i & ~self.scatter(r)
            for c in range(self._smallMatrix.ndim):
                j = i0 | self.scatter(c)
                w[i] += self._smallMatrix[r, c] * v[j]
        return w
