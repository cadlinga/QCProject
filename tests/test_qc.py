from math import sqrt
import unittest

import numpy

from qc import Circuit, Register
from utils.state_vector import makeStateVector
from utils.tensor import Operator


class TestBlocks(unittest.TestCase):

    def test_make_initial_zero_state_for_n_qubits(self):
        zero = makeStateVector(0)
        n = 3

        initialState = zero**n
        zero_3 = makeStateVector(0, 3)

        self.assertTrue(numpy.allclose(initialState.vector, zero_3.vector))

    def test_hadamard_fully_entangles(self):
        """2 States first"""
        initial = makeStateVector(0, 2)
        H_array = [1 / sqrt(2) * x for x in [1, 1, 1, -1]]
        H = Operator(2, H_array)
        H_2 = H**2

        product = numpy.matmul(H_2.matrix, initial.vector)

        """3 States"""

        initial = makeStateVector(0, 3)
        H_3 = H**3
        print(initial)
        print(H_3)

        product = numpy.matmul(H_3.matrix, initial.vector)
        print(product)

        # """ 5 States"""
        # H_5 = H**5
        # initial = makeStateVector(0, 5)
        #
        # product = numpy.matmul(H_5.matrix, initial.vector)
        # print(product)
        #
        self.assertTrue(False)

    def test_oracle_operator(self):
        initial = makeStateVector(0, 2)
        H_array = [1 / sqrt(2) * x for x in [1, 1, 1, -1]]
        H = Operator(2, H_array)
        H_2 = H**2
        Z = Operator(2, [1, 0, 0, -1])
        I = Operator(2, [1, 0, 0, 1])
        # print(numpy.matmul(H_2.matrix, initial.vector))

        CZ = I.tensor(makeStateVector(0).outer(makeStateVector(0))) + Z.tensor(
            makeStateVector(1).outer(makeStateVector(1))
        )

        # print(CZ)

        zero_outer_product = makeStateVector(0).outer(makeStateVector(0))
        one_outer_product = makeStateVector(1).outer(makeStateVector(1))

        CCZ = I.tensor(I).tensor(zero_outer_product) + \
            CZ.tensor(one_outer_product)
        # print(CCZ)

        """In 2D"""

        initial = makeStateVector(0, 2)

        entangled = numpy.matmul(H_2.matrix, initial.vector)

        # print(numpy.outer(entangled.transpose(), entangled))

        oracled = numpy.matmul(CZ.matrix, entangled)

        retangled = numpy.matmul(H_2.matrix, oracled)

        Z_2 = Z**2

        reflection = numpy.matmul(CZ.matrix, Z_2.matrix)
        print(reflection)

        # print(numpy.matmul(numpy.matmul(H_2.matrix, reflection), H_2.matrix))

        reflected = numpy.matmul(reflection, retangled)

        untangled = numpy.matmul(H_2.matrix, reflected)

        """Now, make a 3 state system, H^3, then CCZ and check result"""

        initial = makeStateVector(0, 3)
        H_3 = H**3
        #
        entangled = numpy.matmul(H_3.matrix, initial.vector)
        #
        # print(entangled)
        #

        CCZ = (Operator(2, [1, 0, 0, 1]) ** 3).update(3, 3, -1)

        oracled = numpy.matmul(CCZ.matrix, entangled)
        print(CCZ)
        #
        # print(oracled)
        #
        """Hadamard again"""
        #
        unentangled = numpy.matmul(H_3.matrix, oracled)
        # print(unentangled)
        #
        Z_3 = Z**3
        #
        reflection = Operator(
            8, numpy.matmul(CCZ.matrix, Z_3.matrix).flatten().tolist()
        )

        reflection = (Operator(2, [-1, 0, 0, -1]) ** 3).update(0, 0, 1)

        # reflection = Operator(
        #     8, (numpy.outer(entangled.transpose(), entangled)).flatten().tolist()
        # ) - (Operator(2, [1, 0, 0, 1]) ** 3)
        #
        # reflection = (Operator(2, [1, 0, 0, 1]) ** 3) - Operator(
        #     8, (2 * numpy.outer(entangled.transpose(), entangled)).flatten().tolist()
        # )

        # print(reflection.matrix)
        #
        print(reflection)
        #
        reflected = numpy.matmul(reflection.matrix, unentangled)

        # print(reflected)
        #
        retangled = numpy.matmul(H_3.matrix, reflected)
        #
        print(initial.vector)
        print(retangled)
        print("one iteration:")
        for i in [0, 1, 2, 3, 4, 5, 6, 7]:
            print(
                (numpy.dot(makeStateVector(i, 3).vector.flatten(), retangled.flatten()))
                ** 2
            )

        """Repeat the grover operator Oracle -> H -> Reflection -> H """
        #
        measurable = retangled
        for j in range(2, 20):

            oracled = numpy.matmul(CCZ.matrix, measurable)
            hadamarded = numpy.matmul(H_3.matrix, oracled)
            reflected = numpy.matmul(reflection.matrix, hadamarded)
            measurable = numpy.matmul(H_3.matrix, reflected)

            print(str(j) + " iteration:")
            for i in [0, 1, 2, 3, 4, 5, 6, 7]:
                print(
                    (
                        numpy.dot(
                            makeStateVector(
                                i, 3).vector.flatten(), measurable.flatten()
                        )
                    )
                    ** 2
                )

        #     print(measurable)
        #
        self.assertTrue(False)


# def test_two_oracle_construction(self):
#     ident = Operator(2, [1, 0, 0, 1])
#     zero_outer_product = Operator(2, [1, 0, 0, 0])
#     one_outer_product = Operator(2, [0, 0, 0, 1])
#     z = Operator(2, [1, 0, 0, -1])
#
#     print(ident.tensor(zero_outer_product))
#     print(z.tensor(one_outer_product))
#     print(ident.tensor(zero_outer_product) + z.tensor(one_outer_product))
#     self.assertTrue(False)
#
# def test_four_oracle_construction(self):
#     ident_2 = Operator(2, [1, 0, 0, 1])
#     # ident = ident_2.tensor(ident_2)
#     zero_outer_product = Operator(2, [1, 0, 0, 0])
#     # one_outer_product = Operator(2, [0, 0, 0, 1])
#     # z = Operator(2, [1, 0, 0, -1])
#
#     zero = makeStateVector(0, 3)
#     print(zero)
#
#     print(zero.tensor(one).tensor(two))
#
#     # print(ident_2.tensor(ident_2).tensor(zero_outer_product))
#     self.assertTrue(False)


class TestCircuit(unittest.TestCase):
    def test_vector_loading(self):
        circuit = Circuit(Register(3))
        print(circuit.register.bits[0])
        self.assertTrue(False)

    def test_h_application(self):
        circuit = Circuit(Register(1))
        circuit.h(0)

        print(circuit.register.bits[0])
        self.assertTrue(False)
