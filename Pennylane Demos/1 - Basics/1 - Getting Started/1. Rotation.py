import pennylane as qml
from pennylane import numpy as np

dev1 = qml.device("default.qubit", wires=1)

@qml.qnode(dev1)
def circuit(params: list):
    qml.RX(params[0], wires=0)
    qml.RY(params[1], wires=0)
    return qml.expval(qml.PauliZ(0))

def_params = [0.69, 0.85]

print(circuit(def_params))

d_circuit = qml.grad(circuit, argnum=0)

print(d_circuit(def_params))

def cost(x):
    return circuit(x)

init_params = np.array(def_params)
print(cost(init_params))

# Optimize for |1>

opt = qml.GradientDescentOptimizer(stepsize=0.4)

steps = 100

params = init_params

for i in range(steps):
    params = opt.step(cost, params)

    if (i+1) % 5 == 0:
        print("Cost after step {:5d}: {: .7f}".format(i + 1, cost(params)))

print("Optimized rotation angles: {}".format(params))