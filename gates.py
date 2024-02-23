"""
#############
Gates Module
#############


.. note::
   This code is still under development and until the version 
   is incremented to a 1.* you should not trust any of this 
   documentation.
"""

import numpy
from math import sqrt, pi

from utils.gate import squareMatrix


class Gate(object):
    """
    This is the gate object which we will document properly now.

    .. note::
       This class should not be called directly. It is a super
       class for the gates below.
    """

    def __init__(self, matrix: numpy.ndarray):
        self.matrix = matrix


class H(Gate):
    r"""Single-qubit Hadamard gate.

    This gate is a :math:`\pi` rotation about the X+Z axis, and has the effect of
    changing computation basis from :math:`|0\rangle,|1\rangle` to
    :math:`|+\rangle,|-\rangle` and vice-versa.

    **Matrix Representation:**

    .. math::

        H = \frac{1}{\sqrt{2}}
            \begin{pmatrix}
                1 & 1 \\
                1 & -1
            \end{pmatrix}

    """

    def __init__(self):
        matrix = squareMatrix(
            2,
            1
            / sqrt(2)
            * numpy.array(
                [[1, 1], [1, -1]]
                # , dtype=numpy.complex128
            ),
        ).tolist()
        super().__init__(matrix)
