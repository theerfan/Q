#! /usr/bin/python3

import sys
import pennylane as qml
import numpy as np
import warnings

warnings.filterwarnings("ignore")


def find_excited_states(H):
    """
    Fill in the missing parts between the # QHACK # markers below. Implement
    a variational method that can find the three lowest energies of the provided
    Hamiltonian.

    Args:
        H (qml.Hamiltonian): The input Hamiltonian

    Returns:
        The lowest three eigenenergies of the Hamiltonian as a comma-separated string,
        sorted from smallest to largest.
    """

    energies = np.zeros(3)

    # QHACK #
    class MinEnergies():
        def __init__(self):
            self.lowest = float("inf")
            self.middle = float("inf")
            self.highest = float("inf")
        
        def add(self, e):
            if e < self.lowest:
                if np.abs(e - self.lowest) > 0.1:
                    self.highest = self.middle
                    self.middle = self.lowest 
                self.lowest = e
            elif e < self.middle:
                if np.abs(e - self.lowest) > 0.1:
                    self.highest = self.middle
                    self.middle = e
            elif e < self.highest:
                self.highest = e
            else:
                pass

    n_qubits = len(H.wires)
    min_es = MinEnergies()
    dev = qml.device('default.qubit', wires=n_qubits)
    cost_fn =  qml.ExpvalCost(qml.templates.layers.StronglyEntanglingLayers, H, dev)
    opt = qml.GradientDescentOptimizer(stepsize=0.3)

    for _ in range(3):
        params = np.random.normal(size=(n_qubits, 3, 3))
        max_iterations = 50
        for n in range(max_iterations):
            params = opt.step(cost_fn, params)
            energy = cost_fn(params)
            min_es.add(energy)
            # if n % 20 == 0:
                # print('Iteration = {:},  Energy = {:.8f} Ha'.format(n, energy))
    
    energies[0] = min_es.lowest
    energies[1] = min_es.middle
    energies[2] = min_es.highest

    # QHACK #

    return ",".join([str(E) for E in energies])


def pauli_token_to_operator(token):
    """
    DO NOT MODIFY anything in this function! It is used to judge your solution.

    Helper function to turn strings into qml operators.

    Args:
        token (str): A Pauli operator input in string form.

    Returns:
        A qml.Operator instance of the Pauli.
    """
    qubit_terms = []

    for term in token:
        # Special case of identity
        if term == "I":
            qubit_terms.append(qml.Identity(0))
        else:
            pauli, qubit_idx = term[0], term[1:]
            if pauli == "X":
                qubit_terms.append(qml.PauliX(int(qubit_idx)))
            elif pauli == "Y":
                qubit_terms.append(qml.PauliY(int(qubit_idx)))
            elif pauli == "Z":
                qubit_terms.append(qml.PauliZ(int(qubit_idx)))
            else:
                print("Invalid input.")

    full_term = qubit_terms[0]
    for term in qubit_terms[1:]:
        full_term = full_term @ term

    return full_term


def parse_hamiltonian_input(input_data):
    """
    DO NOT MODIFY anything in this function! It is used to judge your solution.

    Turns the contents of the input file into a Hamiltonian.

    Args:
        filename(str): Name of the input file that contains the Hamiltonian.

    Returns:
        qml.Hamiltonian object of the Hamiltonian specified in the file.
    """
    # Get the input
    coeffs = []
    pauli_terms = []

    # Go through line by line and build up the Hamiltonian
    for line in input_data.split("S"):
        line = line.strip()
        tokens = line.split(" ")

        # Parse coefficients
        sign, value = tokens[0], tokens[1]

        coeff = float(value)
        if sign == "-":
            coeff *= -1
        coeffs.append(coeff)

        # Parse Pauli component
        pauli = tokens[2:]
        pauli_terms.append(pauli_token_to_operator(pauli))

    return qml.Hamiltonian(coeffs, pauli_terms)


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block

    # Turn input to Hamiltonian
    H = parse_hamiltonian_input(sys.stdin.read())

    # Send Hamiltonian through VQE routine and output the solution
    lowest_three_energies = find_excited_states(H)
    print(lowest_three_energies)
