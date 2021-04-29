import pennylane as qml
from pennylane import numpy as np

dev_gaussian = qml.device("default.gaussian", wires=1)

@qml.qnode(dev_gaussian)
def mean_photon_gaussian(mag_alpha, phase_alpha, phi):
    qml.Displacement(mag_alpha, phase_alpha, wires=0)
    qml.Rotation(phi, wires=0)
    return qml.expval(qml.NumberOperator(0))

def cost(params):
    return (mean_photon_gaussian(params[0], params[1], params[2]) - 1.0) ** 2

init_params = [0.015, 0.02, 0.005]
print(cost(init_params))

# initialise the optimizer
opt = qml.GradientDescentOptimizer(stepsize=0.1)

# set the number of steps
steps = 20
# set the initial parameter values
params = init_params

for i in range(steps):
    # update the circuit parameters
    params = opt.step(cost, params)

    print("Cost after step {:5d}: {:8f}".format(i + 1, cost(params)))

print("Optimized mag_alpha:{:8f}".format(params[0]))
print("Optimized phase_alpha:{:8f}".format(params[1]))
print("Optimized phi:{:8f}".format(params[2]))