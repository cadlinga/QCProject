import argparse
from qc import Circuit

parser = argparse.ArgumentParser(description="Quantum Computer Simulator")

parser.add_argument(
    "Register Size",
    help="Please enter an integer for the size of the register",
)

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


# Create circuit and register of correct size
circuit = Circuit(register_size)

# Apply the hadamard to all states initially
circuit.h()

# Loop over the grover cycle (oracle -> h -> refelct -> h)
# number of times specified
circuit.grover(target)

circuit.measure(target)
