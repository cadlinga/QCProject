"""
#############
Gates Module
#############


.. note::
   This code is still under development and until the version
   is incremented to a 1.* you should not trust any of this
   documentation.
"""

from math import sqrt

from utils.tensor import Operator


class Gate(object):
    """
    This is the gate object which we will document properly now.

    """

    def __init__(self, dimension: int):
        self.dimension = int(dimension)
        pass

    def h(self):
        array = [1 / sqrt(2) * x for x in [1, 1, 1, -1]]
        return Operator(2, array)

    def oracle(self, target: int):
        target = int(target)
        return (Operator(2, [1, 0, 0, 1]) ** self.dimension).update(target, target, -1)

    def reflection(self):
        return (Operator(2, [1, 0, 0, 1]) ** self.dimension).negate().update(0, 0, 1)

    def i(self):
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
