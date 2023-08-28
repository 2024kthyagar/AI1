import sys; args = sys.argv[1:]
import math
import random


# random.seed(10)

def initialize_weights(num_nodes):
    # Random initialization
    weights = []
    for i in range(len(num_nodes) - 2):
        weights.append([random.uniform(-2, 2) for j in range(num_nodes[i] * num_nodes[i + 1])])
    weights.append([random.uniform(-2, 2) for j in range(num_nodes[-1])])
    return weights


def create_weights_matrices(weights, num_nodes):
    # Turn weights into a list of matrices
    weights_matrices = []
    for i in range(len(weights)):
        if i == len(weights) - 1:
            weights_matrices.append([[num] for num in weights[i]])
        else:
            weights_matrices.append([])
            for j in range(num_nodes[i + 1]):
                weights_matrices[i].append(weights[i][j * num_nodes[i]:(j + 1) * num_nodes[i]])
    return weights_matrices


def dot(a, b):  # matrices a and b are 2D lists
    return [[sum(i * j for i, j in zip(r, c)) for c in zip(*b)] for r in a]


def logistic(x):
    return 1 / (1 + math.exp(-x))


def dlogistic(x):
    return x * (1 - x)


def forward_pass(weights_matrices, input_data):
    # Feed Forward Loop
    outputs = [input_data]
    for i in range(len(weights_matrices)):
        if i != len(weights_matrices) - 1:
            outputs.append(dot(weights_matrices[i], outputs[i]))
            outputs[i + 1] = [[logistic(j)] for [j] in outputs[i + 1]]
        else:
            outputs.append([[i * j] for [i], [j] in zip(outputs[i], weights_matrices[i])])
    return outputs


def error(outputs, target):
    return sum([(i - j) ** 2 for [i], [j] in zip(outputs[-1], target)]) / 2


def broadcast_mult(a, b):
    # a and b are two 2D lists with the same number of rows, columns of a is 1
    return [[i * k] for [i], j in zip(a, b) for k in j]


def transpose(a):
    # Row to column or column to row
    return [[row[i] for row in a] for i in range(len(a[0]))]


def backpropagate(weights_matrices, outputs, target):
    # Backpropagation
    dE = [[i - j] for [i], [j] in zip(outputs[-1], target)]
    E_matrices = [dE]
    # Last layer is special case
    E_matrices.append(broadcast_mult([[dlogistic(j)] for [j] in outputs[-2]], broadcast_mult(weights_matrices[-1], dE)))
    for i in range(len(weights_matrices) - 2, 0, -1):
        # E of layer = E of next layer * weights of next layer * derivative of logistic function of outputs of layer
        E_matrices.append(
            broadcast_mult([[dlogistic(j)] for [j] in outputs[i]], dot(transpose(weights_matrices[i]), E_matrices[-1])))
    E_matrices.reverse()
    grad_matrices = []
    for i in range(len(weights_matrices)-1):
        # gradient of weights of layer = E of layer * outputs of previous layer
        # needs to be same dims as weight matrix
        grad_matrices.append(dot(E_matrices[i], transpose(outputs[i])))
    # Last layer is special case
    grad_matrices.append(broadcast_mult(E_matrices[-1], outputs[-2]))
    return grad_matrices


def update_weights(weights_matrices, grad_matrices, learning_rate):
    # Update weights
    # print(weights_matrices)
    # print(grad_matrices)
    for i in range(len(weights_matrices)):
        for j in range(len(weights_matrices[i])):
            for k in range(len(weights_matrices[i][j])):
                weights_matrices[i][j][k] -= learning_rate * grad_matrices[i][j][k]
    return weights_matrices


def forward_backward(weights_matrices, input_data, target, learning_rate):
    outputs = forward_pass(weights_matrices, input_data)
    grad_matrices = backpropagate(weights_matrices, outputs, target)
    # print(error(outputs, target))
    weights_matrices = update_weights(weights_matrices, grad_matrices, learning_rate)
    return weights_matrices, error(outputs, target)

def train(inputs, targets):
    converged = False
    learning_rate = 0.2
    while not converged:
        weights = initialize_weights(num_nodes)
        weights_matrices = create_weights_matrices(weights, num_nodes)
        error = 0
        for i in range(70000):
            if i == 40000 and error > 0.01:
                break
            if i == 60000 and error > 0.005:
                break
            elif i == 69999:
                converged = True
            weights_matrices, new_error = forward_backward(weights_matrices, inputs[i % len(inputs)], targets[i % len(inputs)], learning_rate)
            # Print Layer Counts
            # print("Layer counts " + ' '.join([str(i) for i in num_nodes]))
            #
            # # Print Weights
            # for i in range(len(weights_matrices)):
            #     weightstr = ''
            #     for j in range(len(weights_matrices[i])):
            #         weightstr += ' '.join([str(k) for k in weights_matrices[i][j]]) + ' '
            #     print(weightstr[:-1])
            print(new_error)
            error = new_error
    return weights_matrices

def test(weights_matrices, input_data):
    outputs = forward_pass(weights_matrices, input_data)
    return outputs[-1]

# Inputs are 1 0 1 => 1
#          0 1 1 => 0
#          1 1 1 => 1
#          0 0 1 => 0



with open(args[0]) as infile:
    input_output = infile.read().splitlines()
inputs = []
targets = []
for line in input_output:
    instr = line[:line.find('=>')]
    outstr = line[line.find('=>') + 2:]
    input_data = [[int(i)] for i in instr.split()]
    input_data.append([1])
    target = [[int(i)] for i in outstr.split()]
    inputs.append(input_data)
    targets.append(target)
num_nodes = [len(inputs[0]), 2, len(targets[0]), len(targets[0])]

weights_matrices = train(inputs, targets)


# Print Layer Counts
print("Layer counts " + ' '.join([str(i) for i in num_nodes]))

# Print Weights
for i in range(len(weights_matrices)):
    weightstr = ''
    for j in range(len(weights_matrices[i])):
        weightstr += ' '.join([str(k) for k in weights_matrices[i][j]]) + ' '
    print(weightstr[:-1])

# for input in inputs:
#     print(test(weights_matrices, input))
# Karthik Thyagarajan 5 2024
