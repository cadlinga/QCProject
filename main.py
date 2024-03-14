r"""
Quantum Computer Simulator
==========================
This module serves as the entry point for the Quantum Computer Simulator.
It takes command line arguments for the register size and target state,
creates a quantum circuit, applies the Hadamard gate to all states, runs
Grover's algorithm to find the target state, and measures the result.
"""

import argparse
from qc import Circuit
from utils.tensor import Operator, Vector

parser = argparse.ArgumentParser(description="Quantum Computer Simulator")

r"""
The 'Register Size' argument specifies the number of qubits in the quantum register.
"""
parser.add_argument(
    "Register Size",
    help="Please enter an integer for the size of the register",
)

r"""
The 'Target State' argument represents the state that Grover's algorithm should find.
"""
parser.add_argument(
    "Target State",
    help="The state you want Grovers algorithm to find, zero based indexing",
)

args = vars(parser.parse_args())

register_size = args["Register Size"]
target = args["Target State"]

print("Register Size: " + register_size)
print("Target State: " + target)

print(
    "I'm looking for the "
    + str(target)
    + " state (needle) state in the "
    + str((2 ** int(register_size)))
    + " possible "
    + "[0 - "
    + str((2 ** int(register_size)) - 1)
    + "]"
    + " states (haystack)"
)

r"""
This creates a quantum circuit with the specified register size.
"""

circuit = Circuit(register_size)

r"""
This applies the hadamard to all states initially.
"""
circuit.h()

r"""
This loops over the grover cycle (oracle -> h -> reflect -> h)
number of times specified.
"""
circuit.grover(target, True)


r"""
This measures the quantum circuit to retrieve the result of Grover's algorithm.
"""
circuit.measure(target)
