#! /usr/bin/python3
import pennylane as qml
from pennylane import numpy as np
import sys


def simple_circuits_50(angle):
    """The code you write for this challenge should be completely contained within this function
        between the # QHACK # comment markers.

    In this function:
        * Create the standard Bell State
        * Rotate the first qubit around the y-axis by angle
        * Measure the expectation value of the tensor observable `qml.PauliZ(0) @ qml.PauliZ(1)`

    Args:
        angle (float): how much to rotate a state around the y-axis

    Returns:
        float: the expectation value of the tensor observable
    """

    expectation_value = 0.0

    # QHACK #

    # Step 1 : initialize a device

    # Step 2 : Create a quantum circuit and qnode

    # Step 3 : Run the qnode
    # expectation_value = ?

    # QHACK #
    return expectation_value


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block

    # Load and process input
    angle_str = sys.stdin.read()
    angle = float(angle_str)

    ans = simple_circuits_50(angle)

    if isinstance(ans, np.tensor):
        ans = ans.item()

    if not isinstance(ans, float):
        raise TypeError(
            "the simple_circuits_50 function needs to return either a float or PennyLane tensor."
        )

    print(ans)
