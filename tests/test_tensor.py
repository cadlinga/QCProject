r"""
Tensor Module Test Suite
##############################

This module tests the classes included in the tensor module.
"""

import unittest
import numpy
from utils.gate import squareMatrix
from math import sqrt
from utils.state_vector import makeStateVector
from utils.tensor import Operator, Vector


class TestVector(unittest.TestCase):
    """
    This class aims to provide end to end testing of the
    Vector class within the tensor module.

    The purpose of each test and the method by which it
    is validated is outlined below.
    """

    def test_vector_construction(self):
        """
        This test aims to check...
        """

        elements = [1, 0, 1]
        vector = Vector(elements)
        self.assertEqual(vector.dimension, 3)

    def test_vector_element_access(self):
        elements = [1, 0, 1]
        vector = Vector(elements)
        first = vector.vector.flat[0]
        second = vector.vector.flat[1]
        third = vector.vector.flat[2]
        self.assertEqual(first, 1)
        self.assertEqual(second, 0)
        self.assertEqual(third, 1)

    def test_scalar_multiplication(self):
        vector = Vector([1, 2, 3])
        double = vector * 2
        self.assertTrue(numpy.array_equal(
            double.vector, Vector([2, 4, 6]).vector))

    def test_vector_tensor_product(self):
        v1 = Vector([1, 0, 1])
        v2 = Vector([1, 1, 1])
        v3 = Vector([1, 1, 1, 0, 0, 0, 1, 1, 1])
        self.assertTrue(numpy.array_equal(v1.tensor(v2).vector, v3.vector))

    # def test_vector_addition(self):
    #     v1 = 1 / sqrt(2) * Vector([0, 1])
    #     v2 = 1 / sqrt(2) * Vector([1, 0])
    #     print((v1 + v2).tensor(Vector([1, 0])))
    #     self.assertTrue(False)


class TestOperator(unittest.TestCase):

    def test_operator_tensor_product(self):
        op1 = Operator(2, [0, 1, 1, 0])
        op2 = Operator(2, [1, 0, 0, 1])

        self.assertTrue(
            numpy.array_equal(
                op1.tensor(op2).matrix,
                squareMatrix(4, [0, 0, 1, 0, 0, 0, 0, 1,
                             1, 0, 0, 0, 0, 1, 0, 0]),
            )
        )

    def test_operator_tensor_product_vs_notes(self):
        r"""Tensor Product of Hadamard, Identity and Hadamard, as presented in
        the slides - :math:`H \otimes \mathbb{I} \otimes H`.

        This manually creates the hadamard gates and performs the tensor
        product using the :meth:`~Vector.tensor()` method.

        The result is compared against the result in the slides:

        .. math::

            H \otimes \mathbb{I} \otimes H = \frac{1}{2}
                \begin{pmatrix}
                    1 & 1 & 0 & 0 & 1 & 1 & 0 & 0 \\
                    1 & -1 & 0 & 0 & 1 & -1 & 0 & 0 \\
                    0 & 0 & 1 & 1 & 0 & 0 & 1 & 1 \\
                    0 & 0 & 1 & -1 & 0 & 0 & 1 & -1 \\
                    1 & 1 & 0 & 0 & -1 & -1 & 0 & 0 \\
                    1 & -1 & 0 & 0 & 1 & -1 & 0 & 0 \\
                    0 & 0 & 1 & 1 & 0 & 0 & -1 & -1 \\
                    0 & 0 & 1 & -1 & 0 & 0 & -1 & 1
                \end{pmatrix}
        """

        H_array = [1 / sqrt(2) * x for x in [1, 1, 1, -1]]
        H = Operator(2, H_array)
        I = Operator(2, [1, 0, 0, 1])

        """Checked against slides from Tony"""
        correct_list = [
            1.0,
            1.0,
            0.0,
            0.0,
            1.0,
            1.0,
            0.0,
            0.0,
            1.0,
            -1.0,
            0.0,
            -0.0,
            1.0,
            -1.0,
            0.0,
            -0.0,
            0.0,
            0.0,
            1.0,
            1.0,
            0.0,
            0.0,
            1.0,
            1.0,
            0.0,
            -0.0,
            1.0,
            -1.0,
            0.0,
            -0.0,
            1.0,
            -1.0,
            1.0,
            1.0,
            0.0,
            0.0,
            -1.0,
            -1.0,
            -0.0,
            -0.0,
            1.0,
            -1.0,
            0.0,
            -0.0,
            -1.0,
            1.0,
            -0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            1.0,
            -0.0,
            -0.0,
            -1.0,
            -1.0,
            0.0,
            -0.0,
            1.0,
            -1.0,
            -0.0,
            0.0,
            -1.0,
            1.0,
        ]

        scaledProduct = H.tensor(I).tensor(H).matrix / 0.5
        correctMatrix = squareMatrix(8, correct_list)
        print(scaledProduct)
        print(correctMatrix)

        self.assertTrue(numpy.allclose(scaledProduct, correctMatrix))

    def test_product_of_H_gates(self):
        H_array = [1 / sqrt(2) * x for x in [1, 1, 1, -1]]
        H = Operator(2, H_array)

        product = H.tensor(H).tensor(H).tensor(H).tensor(H)
        print(product.matrix)
        self.assertEqual(product.size, 32)

    def test_operator_tensor_vector(self):
        from gates import H

        hadamard = Operator(2, H().matrix)
        ident = Operator(2, [1, 0, 0, 1])
        product = hadamard.tensor(ident).tensor(hadamard)

        # vector = makeStateVector(7, 3)
        # expected = (
        #     makeStateVector(2, 3)
        #     - makeStateVector(3, 3)
        #     - makeStateVector(6, 3)
        #     + makeStateVector(7, 3)
        # ) * 0.5
        vector = makeStateVector(0, 3)
        expected = (
            makeStateVector(0, 3)
            + makeStateVector(1, 3)
            + makeStateVector(4, 3)
            + makeStateVector(5, 3)
        ) * 0.5

        result = numpy.matmul(product.matrix, vector.vector)
        self.assertTrue(numpy.allclose(result, expected.vector))
