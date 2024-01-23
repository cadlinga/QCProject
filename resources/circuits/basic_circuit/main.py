from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister

'''
Use this script as a template.

Create a directory and copy this script into it.
Edit the circuit however you like and in the director run `python3 main.py`
to generate the described circuit as a .png for inclusion in the report
'''

# Build a quantum circuit
circuit = QuantumCircuit(3, 3)

circuit.x(1)
circuit.h(range(3))
# circuit.cx(0, 1)
circuit.measure(range(3), range(3))

# Matplotlib drawing
fig = circuit.draw(output='mpl')
# save the figure to file
fig.savefig('basic_circuit.png')
