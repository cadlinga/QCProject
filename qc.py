r"""
Quantum Circuit Module
======================
This module provides the implementation of a quantum circuit simulator.
It defines the `Circuit` class which represents a quantum circuit and
provides methods for applying quantum gates and running Grover's algorithm.
"""

import numpy
from numpy.lib import math
from gates import Gate

from utils.state_vector import makeStateVector

import matplotlib.pyplot as plt


class Circuit:
    r"""
    This is the quantum circuit class which represents a quantum circuit with a
    specified register size. It provides methods for applying quantum gates,
    running Grover's algorithm, and measuring the result.
    """

    def __init__(self, register_size: int):
        r"""
        Initializes a new quantum circuit with the given register size.

        Params:
            register_size (int): The number of qubits in the quantum register.
        """
        self.register_size = int(register_size)
        self.initial = makeStateVector(0, register_size)
        self.register = self.initial
        self.gates = Gate(register_size)

        pass

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__qualname__, self.register_size)

    def h(self):
        r"""
        Applies the Hadamard gate to all qubits in the quantum register.

        This method retrieves the Hadamard gate matrix from the `gates` object,
        raises it to the power of the register size to create a tensor product,
        and then applies the resulting operator to the quantum register.

        The quantum register is updated with the new state after applying the
        Hadamard gate.
        """
        h = self.gates.h()
        product = h ** int(self.register_size)
        self.register = self.register.apply(product)
        return

    def grover(self, target: int, plot=False):
        r"""
        Runs Grover's algorithm on the quantum circuit to find the target state.

        This method calculates the number of iterations required for Grover's
        algorithm based on the register size and the target state. It then
        constructs the Grover operator by combining the oracle, Hadamard gates,
        and reflection operator.

        The Grover operator is applied to the quantum register for the calculated
        number of iterations to amplify the amplitude of the target state.

        Params:
            target (int): The target state to find using Grover's algorithm.
        """

        N = 2**self.register_size
        theta = numpy.arcsin(numpy.sqrt(1 / N))
        iterations = math.floor(numpy.pi / (4 * theta))

        print(
            "I've calculated that I need to use "
            + str(iterations)
            + " iterations to be likely to succeed."
        )

        if plot:

            plt.figure(figsize=(12, 12))
            plt.title(
                "Projection of "
                + str(self.register_size)
                + " qubit Quantum Register State with Initial and Oracle State Over "
                + str(iterations)
                + " iterations"
            )
            # Manually adjust these to find the best axis
            plt.xlim((-0.005, 0.05))
            plt.ylim((-0.1, 1))
            plt.axis("off")

            plt.quiver(
                [1, 0, 1],
                [0, 0, 0],
                angles="xy",
                scale_units="xy",
                scale=1,
                label="Initial State",
                color="b",
                alpha=0.1,
            )
            plt.quiver(
                [0, 0, 0],
                [1, 0, 1],
                angles="xy",
                scale_units="xy",
                scale=1,
                label="Oracle State",
                color="g",
                alpha=0.1,
            )

            target_state = makeStateVector(int(target), self.register_size)

        i = 0

        G = (
            self.gates.oracle(target)
            * self.gates.h() ** int(self.register_size)
            * self.gates.reflection()
            * self.gates.h() ** int(self.register_size)
        )

        while i < int(iterations):
            self.register = self.register.apply(G)

            i = i + 1

            if plot:
                target_projection = self.register.measure(target_state)
                initial_projection = self.register.measure(self.initial)
                plt.quiver(
                    [initial_projection, 0, initial_projection],
                    [target_projection, 0, target_projection],
                    angles="xy",
                    scale_units="xy",
                    scale=1,
                    alpha=target_projection,
                    label="Iteration " + str(i),
                )

        if plot:
            plt.legend()
            plt.savefig(
                str(self.register_size) + "qubits_" +
                str(iterations) + "iterations",
                dpi=400,
            )
            plt.show()

    def measure(self, target: int):
        r"""
        Measures the quantum circuit and prints the probability of the target state.

        This method performs a measurement on the quantum circuit to determine the
        probability of observing the target state. It calculates the inner product
        between the target state vector and the current state vector of the quantum
        register.

        Params:
            target (int): The target state to measure the probability for.
        """
        target_state = makeStateVector(int(target), self.register_size)

        print("I think I've found it!")
        print(
            "P("
            + str(target)
            + ") = "
            + str((self.register.measure(target_state)) ** 2)
        )
        return
