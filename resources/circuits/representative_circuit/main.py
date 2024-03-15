from math import floor, pi, sqrt
from numpy import arcsin
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister

"""
Use this script as a template.

Create a directory and copy this script into it.
Edit the circuit however you like and in the director run `python3 main.py`
to generate the described circuit as a .png for inclusion in the report
"""

register = 3
measure = 1
# Build a quantum circuit
circuit = QuantumCircuit(register, 1)


oracle = QuantumCircuit(register, name="oracle")
oracle.to_gate()

reflection = QuantumCircuit(register, name="refelction")
reflection.to_gate()


circuit.h(range(register))
N = 2**register
theta = arcsin(sqrt(1 / N))
iterations = floor(pi / (4 * theta))

i = 0
while i < iterations:
    circuit.append(oracle, range(register))
    circuit.h(range(register))
    circuit.append(reflection, range(register))
    circuit.h(range(register))
    i = i + 1

# circuit.cx(0, 1)
circuit.measure(measure, 0)
# circuit.measure(range(register), range(1))

# Matplotlib drawing
fig = circuit.draw(output="mpl")
# save the figure to file
fig.savefig("circuit.png")
