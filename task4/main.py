import networkx as nx
from matplotlib import pyplot as plt
import cirq
import numpy as np
import math
import random
from scipy.optimize import minimize


class Edge:
    def __init__(self, start_node, end_node, weight=1):
        self.start_node = start_node
        self.end_node = end_node
        self.weight = weight


def draw_graph(graph, title=None):
    # Create positions of all nodes and save them
    pos = nx.spring_layout(graph)

    # Draw the graph according to node positions
    nx.draw_networkx(graph, pos)

    # Create edge labels
    labels = nx.get_edge_attributes(graph, "weight")

    # Draw edge labels according to node positions
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)

    if title:
        fig = plt.gcf()
        fig.canvas.set_window_title(title)

    plt.show()
    plt.clf()


set_edges = [
    Edge(0, 1, weight=2),
    Edge(0, 2, weight=3),
    Edge(0, 5, weight=3),
    Edge(0, 4, weight=1),
    Edge(1, 2, weight=1),
    Edge(1, 3, weight=2),
    Edge(2, 3, weight=2),
    Edge(2, 5, weight=3),
    Edge(3, 4, weight=1),
    Edge(3, 5, weight=4),
    Edge(4, 5, weight=2),
]

G = nx.Graph()

for z in set_edges:
    G.add_edge(z.start_node, z.end_node, weight=z.weight)

draw_graph(G, "Initial Graph")

# Defines the list of qubits
num = 6
depth = 4
rep = 1000
qubits = [cirq.GridQubit(0, i) for i in range(0, num)]


# Defines the initialization
def initialization(qubits):
    for i in qubits:
        yield cirq.H.on(i)


# (Z⊗Z)^t = [1 . . .]
#            [. w . .]
#            [. . w .]
#            [. . . 1]
# where w = e^{iπt} and '.' = '0'
def cost_unitary(qubits, gamma):
    for i in set_edges:
        yield cirq.ZZPowGate(exponent=-1 * gamma / math.pi).on(
            qubits[i.start_node], qubits[i.end_node]
        )


# Defines the mixer unitary
def mixer_unitary(qubits, alpha):
    for i in range(0, len(qubits)):
        yield cirq.XPowGate(exponent=-1 * alpha / math.pi).on(qubits[i])


# Executes the circuit
def create_circuit(params):

    gamma = [params[0], params[2], params[4], params[6]]
    alpha = [params[1], params[3], params[5], params[7]]

    circuit = cirq.Circuit()
    circuit.append(initialization(qubits))

    # This is due to trotterization:
    # e^(A+B)=lim_n→∞(e^(A/n).e^(B/n))^n
    for i in range(0, depth):
        circuit.append(cost_unitary(qubits, gamma[i]))
        circuit.append(mixer_unitary(qubits, alpha[i]))
    circuit.append(cirq.measure(*qubits, key="x"))
    # print(circuit)

    simulator = cirq.Simulator()
    results = simulator.run(circuit, repetitions=rep)
    results = str(results)[2:].split(", ")
    new_res = []
    for i in range(0, rep):
        hold = []
        for j in range(0, num):
            hold.append(int(results[j][i]))
        new_res.append(hold)

    return new_res


# Defines the cost function
def cost_function(params):

    av = create_circuit(params)
    total_cost = 0
    for i in range(0, len(av)):
        for j in set_edges:
            total_cost += (
                0.5
                * j.weight
                * (((1 - 2 * av[i][j.start_node]) * (1 - 2 * av[i][j.end_node])) - 1)
            )
    total_cost = float(total_cost) / rep

    # print("Cost: " + str(total_cost))

    return total_cost


# Defines the optimization method
init = [float(random.randint(-314, 314)) / float(100) for i in range(0, 8)]
out = minimize(cost_function, x0=init, method="COBYLA", options={"maxiter": 100})
# print(out)

optimal_params = out["x"]
f = create_circuit(optimal_params)

# Creates visualization of the optimal state

nums = []
freq = []

for i in range(0, len(f)):
    number = 0
    for j in range(0, len(f[i])):
        number += 2 ** (len(f[i]) - j - 1) * f[i][j]
    if number in nums:
        freq[nums.index(number)] = freq[nums.index(number)] + 1
    else:
        nums.append(number)
        freq.append(1)

freq = [s / sum(freq) for s in freq]

# print(nums)
# print(freq)

x = range(0, 2 ** num)
y = []
for i in range(0, len(x)):
    if i in nums:
        y.append(freq[nums.index(i)])
    else:
        y.append(0)

plt.bar(x, y)
fig = plt.gcf()
fig.canvas.set_window_title("Bar chart of probabilities of answers.")
plt.show()

## More visualizations
def draw_cut_edges(S, T, cut_size):
    Cut = nx.Graph()
    for z in set_edges:
        if (z.start_node in S and z.end_node in T) or (
            z.start_node in T and z.end_node in S
        ):
            Cut.add_edge(z.start_node, z.end_node, weight=z.weight)
    draw_graph(Cut, "Cut edges for cut size: %s" % cut_size)


# Visualize the result of the next graph cut in y with the highest probability of sucess.
def print_next_results(y):
    max1 = max(y)
    x_max1 = y.index(max1)
    x_max1_bin = "{0:b}".format(x_max1).zfill(num)
    y.remove(max1)
    S = set()
    for i in range(len(x_max1_bin)):
        if x_max1_bin[i] == "1":
            S.add(i)

    T = set(G.nodes) - S
    cut_size = nx.cut_size(G, S, T, weight="weight")
    print("Subgraph string: %s" % x_max1_bin)
    print("Cut size: %s" % cut_size)
    draw_cut_edges(S, T, cut_size)


# Visualize the two cuts with the highest probabilities.
print_next_results(y)
print_next_results(y)