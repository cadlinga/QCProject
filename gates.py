r"""
Gates Module
=======================
This module provides the implementation of quantum gates used in Grover's algorithm.
The `Gate` class contains methods for creating the Hadamard gate, oracle gate,
reflection gate, and identity gate.

"""

from math import sqrt

from utils.tensor import Operator


class Gate(object):
    r"""
    This is the gate class which contains the gates we need to implement
    Grover's algorithm.

    When we initialise, we declare the dimension of the quantum
    register so that the gates (except the Hadamard) can be provided in
    the correct dimension.

    The Hadamard gate is scaled (using tensor products) at the point
    of implementation to make the application more obvious.

    """

    def __init__(self, dimension: int):
        """
        Comments here wont make it into the docs.
        """
        self.dimension = int(dimension)
        pass

    def h(self):
        r""" 
        Single-qubit Hadamard gate.

        This gate is a :math:`\pi` rotation about the X+Z axis, and has the effect
        of changing computation basis from :math:`|0\rangle,|1\rangle` to
        :math:`|+\rangle,|-\rangle` and vice-versa.

        **Matrix Representation:**

        .. math::

            H = \frac{1}{\sqrt{2}}
                \begin{pmatrix}
                    1 & 1 \\
                    1 & -1
                \end{pmatrix}
        """

        array = [1 / sqrt(2) * x for x in [1, 1, 1, -1]]
        return Operator(2, array)

    def oracle(self, target: int):
        r"""
        Oracle gate for Grover's algorithm.

        The oracle gate marks the target state by flipping its phase. It is a
        diagonal matrix with all elements on the diagonal equal to 1, except for
        the element corresponding to the target state, which is -1.

        **Matrix Representation when targeting the second state:**

        .. math::

            O = 
                \begin{pmatrix}
                    1 & 0 \\
                    0 & -1
                \end{pmatrix}

        Params:
            target (int): The target state to be marked by the oracle in little endian convention.

        Returns:
            Operator: The oracle gate as an `Operator` object.

        """
        target = int(target)
        return (Operator(2, [1, 0, 0, 1]) ** self.dimension).update(target, target, -1)

    def reflection(self):
        r"""
        Reflection gate for Grover's algorithm.

        The reflection gate reflects the quantum register in the direction 
        of the initial state. 
        It is a diagonal matrix with the first element on the diagonal
        equal to 1 and all other elements equal to -1.

        **Matrix Representation:**

        .. math::

            R = 
                \begin{pmatrix}
                    1 & 0 \\
                    0 & -1
                \end{pmatrix}

        Returns:
            Operator: The reflection gate as an `Operator` object
        """
        return (Operator(2, [1, 0, 0, 1]) ** self.dimension).negate().update(0, 0, 1)

    def i(self):
        r"""
        Identity gate.

        The identity gate performs no operation on the quantum state. It is
        represented by the identity matrix of size determined by the dimension
        of the quantum register.

        **Matrix Representation:**

        .. math::

            I = 
                \begin{pmatrix}
                    1 & 0 \\
                    0 & 1
                \end{pmatrix}

        Returns:
            Operator: The identity gate as an `Operator` object.

        ----
        """
        return Operator(2, [1, 0, 0, 1]) ** self.dimension


#
# class H(Gate):
#     r"""Single-qubit Hadamard gate.
#
#     This gate is a :math:`\pi` rotation about the X+Z axis, and has the effect
#     of changing computation basis from :math:`|0\rangle,|1\rangle` to
#     :math:`|+\rangle,|-\rangle` and vice-versa.
#
#     **Matrix Representation:**
#
#     .. math::
#
#         H = \frac{1}{\sqrt{2}}
#             \begin{pmatrix}
#                 1 & 1 \\
#                 1 & -1
#             \end{pmatrix}
#
#     """
#
#     def __init__(self):
#         matrix = squareMatrix(
#             2,
#             1
#             / sqrt(2)
#             * numpy.array(
#                 [[1, 1], [1, -1]]
#                 # , dtype=numpy.complex128
#             ),
#         ).tolist()
#         super().__init__(matrix)
