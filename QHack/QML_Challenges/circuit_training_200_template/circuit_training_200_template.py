#! /usr/bin/python3
import json
import sys
import networkx as nx
import numpy as np
import pennylane as qml
# from matplotlib import pyplot as plt


# DO NOT MODIFY any of these parameters
NODES = 6
N_LAYERS = 10


def find_max_independent_set(graph, params):
    """Find the maximum independent set of an input graph given some optimized QAOA parameters.

    The code you write for this challenge should be completely contained within this function
    between the # QHACK # comment markers. You should create a device, set up the QAOA ansatz circuit
    and measure the probabilities of that circuit using the given optimized parameters. Your next
    step will be to analyze the probabilities and determine the maximum independent set of the
    graph. Return the maximum independent set as an ordered list of nodes.

    Args:
        graph (nx.Graph): A NetworkX graph
        params (np.ndarray): Optimized QAOA parameters of shape (2, 10)

    Returns:
        list[int]: the maximum independent set, specified as a list of nodes in ascending order
    """

    max_ind_set = []

    # QHACK #
    qaoa = qml.qaoa
    cost_h, mixer_h = qaoa.max_independent_set(graph, constrained=True)

    def qaoa_layer(gamma, alpha):
        qaoa.cost_layer(gamma, cost_h)
        qaoa.mixer_layer(alpha, mixer_h)

    wires = range(NODES)

    def circuit(params, **kwargs):
        qml.layer(qaoa_layer, N_LAYERS, params[0], params[1])
    
    dev = qml.device("default.qubit", wires=wires)
    # dev = qml.device("qulacs.simulator", wires=wires)
    cost_function = qml.ExpvalCost(circuit, cost_h, dev)

    optimizer = qml.GradientDescentOptimizer()
    steps = 3
    # params = [[0.5 for _ in range(N_LAYERS)] for _ in range(2)]

    for _ in range(steps):
        params = optimizer.step(cost_function, params)
    
    @qml.qnode(dev)
    def probability_circuit(gamma, alpha):
        circuit([gamma, alpha])
        return qml.probs(wires=wires)

    probs = probability_circuit(params[0], params[1])
    probs_list = []
    for p in probs:
        probs_list.append(float(p))
    # print(probs_list)
    # probs[0] = 0.0

    # print(probs)
    # plt.style.use("seaborn")   
    # fig = plt.figure()
    # ax1 = fig.add_subplot(111)
    # ax1.set_xticks(np.arange(len(probs)))
    # ax1.bar(range(2 ** len(wires)), probs)
    # plt.show()

    max_prob = max(probs_list)
    max_index = probs_list.index(max_prob)
    bit_str = "{0:b}".format(max_index).zfill(NODES)
    # print(bit_str)

    for idx, val in enumerate(bit_str):
        if val == "1":
            max_ind_set.append(idx)
    # QHACK #

    return max_ind_set


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block

    # Load and process input
    graph_string = sys.stdin.read()
    graph_data = json.loads(graph_string)

    params = np.array(graph_data.pop("params"))
    graph = nx.json_graph.adjacency_graph(graph_data)

    max_independent_set = find_max_independent_set(graph, params)

    print(max_independent_set)
