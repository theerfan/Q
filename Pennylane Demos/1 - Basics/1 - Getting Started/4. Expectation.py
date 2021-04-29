import pennylane as qml
from pennylane import numpy as np

dev = qml.device("default.qubit", wires=2)

@qml.qnode(dev)
def circuit():
    qml.Hadamard(wires=0)
    qml.Hadamard(wires=1)
    return qml.expval(qml.PauliY(0)), qml.expval(qml.PauliY(1))

for _ in range(10):
    print(circuit())

