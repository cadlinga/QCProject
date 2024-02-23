import unittest

from utils.gate import Gate, squareMatrix


class TestGate(unittest.TestCase):
    def test_gather(self):
        gate = Gate(qubitPosition=[0, 2])
        gathered = gate.gather(13)
        self.assertEqual(gathered, 2)

    def test_scatter(self):
        gate = Gate(qubitPosition=[2, 0, 1])
        scattered = gate.scatter(28)
        # Best guess at correct output - needs to be checked.
        self.assertEqual(scattered, 2)

    def test_apply(self):
        gate = Gate(qubitPosition=[0, 2])
        print("Output:")
        print(gate.apply([1, 3]))
        """
        Intentional fail here until we can find some
        data to validate the implementation.
        """
        self.assertEqual(0, 1)


class TestSmallMatrix(unittest.TestCase):
    def test_matrix_dimension(self):
        sm = squareMatrix(2, [1, 2, 3, 4])
        self.assertEqual(2, sm.ndim)

    def test_smallMatrix_element_access(self):
        sm = squareMatrix(2, [1, 2, 3, 4])
        self.assertEqual(sm[0, 0], 1)
        self.assertEqual(sm[0, 1], 2)
        self.assertEqual(sm[1, 0], 3)
        self.assertEqual(sm[1, 1], 4)
