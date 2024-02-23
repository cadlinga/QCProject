import unittest

from qc import Circuit, Register


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
