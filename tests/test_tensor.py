"""
Tensor Module Test Suite
##############################

This module tests the classes included in the tensor module.
"""

import unittest
from gates import Gate
from utils.state_vector import makeStateVector
from utils.tensor import Operator, Vector


class TestVector(unittest.TestCase):
    r"""
    This class aims to provide end to end testing of the
    Vector class within the tensor module.

    The purpose of each test and the method by which it
    is validated is outlined below.
    """

    def test_vector_construction(self):
        """
        This test checks that the `Vector` is correctly constructed
        when the `init` method is called.
        """
        elements = [1, 0, 1]
        vector = Vector(elements)
        self.assertEqual(vector.dimension, 3)

    # def test_vector_element_access(self):
    #     elements = [1, 0, 1]
    #     vector = Vector(elements)
    #     first = vector.vector.flat[0]
    #     second = vector.vector.flat[1]
    #     third = vector.vector.flat[2]
    #     self.assertEqual(first, 1)
    #     self.assertEqual(second, 0)
    #     self.assertEqual(third, 1)

    def test_scalar_multiplication(self):
        r"""
        This test checks the scalar multiplication method behaves
        as expected.
        """
        vector = Vector([1, 2, 3])
        double = vector.scale(2)
        print(double)
        self.assertTrue(double.equal(Vector([2, 4, 6])))

        # self.assertTrue(numpy.array_equal(
        # double.vector, Vector([2, 4, 6]).vector))

    def test_vector_tensor_product(self):
        r"""
        This test checks that the tensor product of two `Vector` is computed
        correctly.
        """
        v1 = Vector([1, 0, 1])
        v2 = Vector([1, 1, 1])
        v3 = Vector([1, 1, 1, 0, 0, 0, 1, 1, 1])
        self.assertTrue(v3.equal(v1.tensor(v2)))
        # self.assertTrue(numpy.array_equal(v1.tensor(v2).vector, v3.vector))

    # def test_vector_addition(self):
    #     v1 = 1 / sqrt(2) * Vector([0, 1])
    #     v2 = 1 / sqrt(2) * Vector([1, 0])
    #     print((v1 + v2).tensor(Vector([1, 0])))
    #     self.assertTrue(False)


class TestOperator(unittest.TestCase):
    r"""
    This class aims to provide end to end testing of the
    Operator class within the tensor module.

    The purpose of each test and the method by which it
    is validated is outlined below.
    """

    def test_operator_tensor_product(self):
        r"""
        This test checks that the tensor product of two operators
        is computed correctly.
        """
        op1 = Operator(2, [0, 1, 1, 0])
        op2 = Operator(2, [1, 0, 0, 1])

        product = op1.tensor(op2)
        print(product)

        result = Operator(4, [0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0])
        self.assertTrue(op1.tensor(op2).equal(result))

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

        gates = Gate(1)
        H = gates.h()
        I = gates.i()

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
        scaledProduct = H.tensor(I).tensor(H)
        print(scaledProduct)
        correctOperator = Operator(8, correct_list).scale(0.5)

        self.assertTrue(scaledProduct.equal(correctOperator))

    def test_product_of_H_gates(self):
        """
        This test confirms that raising a Hadamard gate to a power
        correctly computes the tensor product and provides the
        correct dimension of `Operator`.
        """
        gates = Gate(1)
        H = gates.h()
        product = H.tensor(H).tensor(H).tensor(H).tensor(H)
        self.assertEqual(product.matrix.size, 32)

    def test_operator_applied_to_vector(self):
        """
        This test confirms that `Operator`s are correctly applied
        to `Vector`s when the `apply()` method is used.
        """
        gates = Gate(1)
        h = gates.h()
        i = gates.i()
        op = h.tensor(i).tensor(h)

        vector = makeStateVector(0, 3)

        expected = (
            makeStateVector(0, 3)
            + makeStateVector(1, 3)
            + makeStateVector(4, 3)
            + makeStateVector(5, 3)
        ).scale(0.5)

        result = vector.apply(op)

        # self.assertTrue(False)

        self.assertTrue(result.equal(expected))

    def test_update(self):
        r"""
        This test confirms that when the update method is used on an `Operator`
        the correct element is updated to the correct value.
        """
        op = Gate(2).i()
        op.update(0, 0, -1)
        target = Operator(4, [-1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])
        self.assertTrue(op.equal(target))
