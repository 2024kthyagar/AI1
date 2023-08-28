import sys; args = sys.argv[1:]
import math
import random
import re


# This second back propagation lab takes a single argument, an inequality related to a circle, in the form of
# "x*x+y*y<1.1" where the less than may be any one of <, <=, >, or >= and the 1.1 may be any real in [.8,1.2].  The
# submitted script is to construct a neural network according to the same standards as in the first back propagation
# lab, and to output that NN.
#
# The NN that the submitted script is to determine takes either two arguments, x and y, or three, if a bias is to be
# included.  There is one single output which is whether (x,y) satisfies the inequality that the script is given.  x
# and y are guaranteed to be in [-1.5, 1.5].

def evaluate(op, num, x, y):
    if op == '<':
        return x*x + y*y < num
    elif op == '<=':
        return x*x + y*y <= num
    elif op == '>':
        return x*x + y*y > num
    elif op == '>=':
        return x*x + y*y >= num

def initialize_weights(num_nodes):
    # Random initialization
    weights = []
    for i in range(len(num_nodes) - 2):
        weights.append([random.uniform(-1.5, 1.5) for j in range(num_nodes[i] * num_nodes[i + 1])])
    weights.append([random.uniform(-1.5, 1.5) for j in range(num_nodes[-1])])
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
    dE = [[i - j] for [i], [j] in zip(target, outputs[-1])]
    E_matrices = [dE]
    # Last layer is special case
    E_matrices.append(broadcast_mult([[dlogistic(j)] for [j] in outputs[-2]], broadcast_mult(weights_matrices[-1], dE)))
    for i in range(len(weights_matrices) - 2, 0, -1):
        # E of layer = E of next layer * weights of next layer * derivative of logistic function of outputs of layer
        E_matrices.append(
            broadcast_mult([[dlogistic(j)] for [j] in outputs[i]], dot(transpose(weights_matrices[i]), E_matrices[-1])))
    E_matrices.reverse()
    # print("E_MATRICES", E_matrices)
    # print(E_matrices, outputs)
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
    for i in range(len(grad_matrices)):
        for j in range(len(grad_matrices[i])):
            for k in range(len(grad_matrices[i][j])):
                weights_matrices[i][j][k] += learning_rate * grad_matrices[i][j][k]
    return weights_matrices


def update_weights_adam(weights_matrices, grad_matrices, learning_rate, v, s, epoch_num):
    # Update weights
    # print(weights_matrices)
    # print(grad_matrices)

    # Adam Optimizer
    beta1 = 0.9
    beta2 = 0.999
    epsilon = 1e-8

    for i in range(len(grad_matrices)):
        for j in range(len(grad_matrices[i])):
            for k in range(len(grad_matrices[i][j])):
                v_new = (beta1 * v[i][j][k] + (1 - beta1) * grad_matrices[i][j][k])
                s_new = (beta2 * s[i][j][k] + (1 - beta2) * grad_matrices[i][j][k] * grad_matrices[i][j][k])
                v_hat = v_new / (1 - beta1 ** epoch_num)
                s_hat = s_new / (1 - beta2 ** epoch_num)
                weights_matrices[i][j][k] -= learning_rate * v_hat / (math.sqrt(s_hat) + epsilon)
                v[i][j][k] = v_new
                s[i][j][k] = s_new

    return weights_matrices, v, s


def forward_backward(weights_matrices, input_data, target, v, s, learning_rate, epoch_num):
    outputs = forward_pass(weights_matrices, input_data)
    grad_matrices = backpropagate(weights_matrices, outputs, target)
    # print(error(outputs, target))
    # weights_matrices, v, s = update_weights_adam(weights_matrices, grad_matrices, learning_rate, v, s, epoch_num)
    weights_matrices = update_weights(weights_matrices, grad_matrices, learning_rate)
    return weights_matrices, error(outputs, target), v, s


def train(num_nodes, training_data_inputs, training_data_targets, learning_rate, epochs):
    # Initialize weights
    weights = initialize_weights(num_nodes)
    weights_matrices = create_weights_matrices(weights, num_nodes)
    # Initialize Adam Optimizer
    v = [[[0 for k in range(len(weights_matrices[i][j]))] for j in range(len(weights_matrices[i]))] for i in
         range(len(weights_matrices))]
    s = [[[0 for k in range(len(weights_matrices[i][j]))] for j in range(len(weights_matrices[i]))] for i in
         range(len(weights_matrices))]
    # Train
    for i in range(epochs):
        new_learning_rate = learning_rate / (1 + 0.008 * i)
        average_error = 0
        for j in range(len(training_data_inputs)):
            weights_matrices, err, v, s = forward_backward(weights_matrices, training_data_inputs[j],
                                                     training_data_targets[j], v, s, learning_rate, i + 1)
            average_error += err
        print("Epoch", i, "Error:", average_error / len(training_data_inputs), "Learning Rate:", new_learning_rate)
    return weights_matrices




instr = args[0]
# Match operator
op = re.search(r'[<>]=?', instr).group(0)
# Match number
num = float(re.search(r'[0-9.]+', instr).group(0))
# Generate training data

# Random Generation
# training_data_inputs = [[[random.uniform(-1.5, 1.5)], [random.uniform(-1.5, 1.5)], [1]] for i in range(3000)]

# Grid Generation
# Uniform square grid from -1.5 to 1.5, 3025 points total, therefore 55 points per side
training_data_inputs = [[[3*i/55 - 1.5], [3*j/55 - 1.5], [1]] for i in range(55) for j in range(55)]
random.shuffle(training_data_inputs)
training_data_targets = [[[1 if evaluate(op, num, x, y) else 0]] for [[x],[y], _] in training_data_inputs]
num_nodes = [3, 17, 4, 1, 1]

# Train
weights_matrices = train(num_nodes, training_data_inputs, training_data_targets, 0.3, 50)

# Display results
# Print Layer Counts
print("Layer counts " + ' '.join([str(i) for i in num_nodes]))

# Print Weights
for i in range(len(weights_matrices)):
    weightstr = ''
    for j in range(len(weights_matrices[i])):
        weightstr += ' '.join([str(k) for k in weights_matrices[i][j]]) + ' '
    print(weightstr[:-1])

# Test goof count
# goof_count = 0
# for i in range(100000):
#     x = random.uniform(-1.5, 1.5)
#     y = random.uniform(-1.5, 1.5)
#     # print(x, y, evaluate(op, num, x, y), forward_pass(weights_matrices, [[x], [y]])[-1][0][0])
#     if int(evaluate(op, num, x, y)) != (forward_pass(weights_matrices, [[x], [y]])[-1][0][0] > 0.5):
#         # print(x, y, evaluate(op, num, x, y), forward_pass(weights_matrices, [[x], [y]])[-1][0][0])
#         goof_count += 1
# print("Goof count:", goof_count)


# Karthik Thyagarajan 5 2024






