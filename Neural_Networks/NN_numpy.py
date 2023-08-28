import sys; args = sys.argv[1:]
import math
import numpy as np
import re
import matplotlib.pyplot as plt
import pandas as pd

def initialize_weights(num_nodes):
    # Random initialization
    weights = []
    for i in range(len(num_nodes) - 2):
        weights.append(np.random.uniform(-0.1, 0.1, (num_nodes[i + 1], num_nodes[i])))
    weights.append(np.random.uniform(-0.1, 0.1, (num_nodes[-1], 1)))
    return weights


def logistic(x):
    return 1 / (1 + np.exp(-x))


def dlogistic(x):
    return x * (1 - x)

def relu(x):
    return np.maximum(x, 0)

def drelu(x):
    return np.where(x > 0, 1, 0)

def forward_pass(weights_matrices, input_data):
    # Feed Forward Loop
    outputs = [input_data]
    for i in range(len(weights_matrices)):
        if i < len(weights_matrices) - 2:
            # Need to do weight dot output for each output, dims should end up as (m, num_nodes[i+1], 1)
            outputs.append(np.matmul(weights_matrices[i], outputs[i]))
            outputs[i + 1] = relu(outputs[i + 1])
        elif i == len(weights_matrices) - 2:
            outputs.append(np.matmul(weights_matrices[i], outputs[i]))
            outputs[i + 1] = logistic(outputs[i + 1])
        else:
            outputs.append(outputs[i] * weights_matrices[i])
    return outputs

def forward_pass_dropout(weights_matrices, input_data, keep_prob):
    outputs = [input_data]
    dropouts = []
    for i in range(len(weights_matrices)):
        if i < len(weights_matrices) - 2:
            outputs.append(np.matmul(weights_matrices[i], outputs[i]))
            outputs[i + 1] = relu(outputs[i + 1])
            dropouts.append(np.random.rand(*outputs[i + 1].shape) < keep_prob)
            outputs[i + 1] *= dropouts[i] / keep_prob
        elif i == len(weights_matrices) - 2:
            outputs.append(np.matmul(weights_matrices[i], outputs[i]))
            outputs[i + 1] = logistic(outputs[i + 1])
        else:
            outputs.append(outputs[i] * weights_matrices[i])
    return outputs, dropouts

def error(outputs, target):
    # MSE
    return np.sum((outputs[-1] - target) ** 2) / 2



def backpropagate(weights_matrices, outputs, target):
    # Backpropagation Loop
    dE = target - outputs[-1]
    E_matrices = [dE]
    # Last layer is a special case
    E_matrices.append(dlogistic(outputs[-2]) * dE * weights_matrices[-1])
    for i in range(len(weights_matrices) - 2, 0, -1):
        E_matrices.append(drelu(outputs[i]) * np.matmul(weights_matrices[i].T, E_matrices[-1]))
    E_matrices.reverse()
    gradients = []
    for i in range(len(weights_matrices) - 1):
        gradients.append(np.tensordot(E_matrices[i], outputs[i], axes=([0,2], [0,2])) / outputs[i].shape[0])
    gradients.append(np.sum(E_matrices[-1] * outputs[-2], axis=0)/outputs[-2].shape[0])
    return gradients


def backpropagate_dropout(weights_matrices, outputs, target, dropouts, keep_prob):
    # Backpropagation Loop
    dE = target - outputs[-1]
    E_matrices = [dE]
    # Last layer is a special case
    E_matrices.append(dlogistic(outputs[-2]) * dE * weights_matrices[-1])
    for i in range(len(weights_matrices) - 2, 0, -1):
        E_matrices.append(drelu(outputs[i]) * np.matmul(weights_matrices[i].T, E_matrices[-1]) * dropouts[i - 1] / keep_prob)
    E_matrices.reverse()
    gradients = []
    for i in range(len(weights_matrices) - 1):
        gradients.append(np.tensordot(E_matrices[i], outputs[i], axes=([0,2], [0,2])) / outputs[i].shape[0])
    gradients.append(np.sum(E_matrices[-1] * outputs[-2], axis=0)/outputs[-2].shape[0])
    return gradients

def update_weights(weights_matrices, gradients, learning_rate):
    # Update weights
    for i in range(len(weights_matrices)):
        weights_matrices[i] = weights_matrices[i] + learning_rate * gradients[i]
    return weights_matrices

def forward_backward(weights_matrices, input_data, target, learning_rate):
    outputs = forward_pass(weights_matrices, input_data)
    gradients = backpropagate(weights_matrices, outputs, target)
    weights_matrices = update_weights(weights_matrices, gradients, learning_rate)
    return weights_matrices, error(outputs, target)

def train(num_nodes, input_data, target, learning_rate, epochs):
    # Initialize weights
    weights_matrices = initialize_weights(num_nodes)

    batch_size = 64
    for i in range(epochs):
        average_error = 0
        new_learning_rate = learning_rate / (1 + i * 0.0001)
        for j in range(0, len(input_data), batch_size):
            input_batch = input_data[j:j + batch_size]
            target_batch = target[j:j + batch_size]
            average_error = 0
            # for j in range(len(input_data)):
            weights_matrices, error = forward_backward(weights_matrices, input_batch, target_batch, new_learning_rate)
            average_error += error
        average_error /= len(input_data)
        print(f"Epoch: {i + 1} Error: {average_error} Learning Rate: {new_learning_rate}")
    return weights_matrices

def update_weights_adam(weights_matrices, gradients, learning_rate, v, s, beta1=0.9, beta2=0.999, epsilon=1e-8):
    # Update weights
    for i in range(len(weights_matrices)):
        v[i] = beta1 * v[i] + (1 - beta1) * gradients[i]
        s[i] = beta2 * s[i] + (1 - beta2) * gradients[i] ** 2
        v_hat = v[i] / (1 - beta1)
        s_hat = s[i] / (1 - beta2)
        weights_matrices[i] = weights_matrices[i] + learning_rate * v_hat / (np.sqrt(s_hat) + epsilon)
    return weights_matrices, v, s

def forward_backward_adam(weights_matrices, input_data, target, learning_rate, v, s, beta1=0.9, beta2=0.999, epsilon=1e-8):
    outputs = forward_pass(weights_matrices, input_data)
    gradients = backpropagate(weights_matrices, outputs, target)
    weights_matrices, v, s = update_weights_adam(weights_matrices, gradients, learning_rate, v, s, beta1, beta2, epsilon)
    return weights_matrices, v, s, error(outputs, target)

def train_adam(num_nodes, input_data, target, learning_rate, epochs):
    # Initialize weights
    weights_matrices = initialize_weights(num_nodes)

    # Adam Optimizer
    v = [np.zeros_like(weights_matrices[i]) for i in range(len(weights_matrices))]
    s = [np.zeros_like(weights_matrices[i]) for i in range(len(weights_matrices))]

    batch_size = 64
    for i in range(epochs):
        average_error = 0
        new_learning_rate = learning_rate / (1 + i * 0.0001)
        for j in range(0, len(input_data), batch_size):
            input_batch = input_data[j:j + batch_size]
            target_batch = target[j:j + batch_size]
            average_error = 0
            # for j in range(len(input_data)):
            weights_matrices, v, s, error = forward_backward_adam(weights_matrices, input_batch, target_batch, new_learning_rate, v, s)
            average_error += error
        average_error /= len(input_data)
        print(f"Epoch: {i + 1} Error: {average_error} Learning Rate: {new_learning_rate}")
    return weights_matrices

def forward_backward_dropout(weights_matrices, input_data, target, learning_rate, keep_prob=0.8):
    outputs, dropouts = forward_pass_dropout(weights_matrices, input_data, keep_prob)
    gradients = backpropagate_dropout(weights_matrices, outputs, target, dropouts, keep_prob)
    weights_matrices = update_weights(weights_matrices, gradients, learning_rate)
    return weights_matrices, error(outputs, target)

def train_dropout(num_nodes, input_data, target, learning_rate, epochs, keep_prob=0.8):
    # Initialize weights
    weights_matrices = initialize_weights(num_nodes)

    batch_size = 64
    for i in range(epochs):
        average_error = 0
        new_learning_rate = learning_rate / (1 + i * 0.02)
        for j in range(0, len(input_data), batch_size):
            input_batch = input_data[j:j + batch_size]
            target_batch = target[j:j + batch_size]
            average_error = 0
            # for j in range(len(input_data)):
            weights_matrices, error = forward_backward_dropout(weights_matrices, input_batch, target_batch, new_learning_rate, keep_prob)
            average_error += error
        average_error /= len(input_data)
        print(f"Epoch: {i + 1} Error: {average_error} Learning Rate: {new_learning_rate}")
    return weights_matrices

mnist_df = pd.read_csv(args[0])
training_data = mnist_df.to_numpy()
np.random.shuffle(training_data)
training_data_inputs_og = training_data[:, 1:]
training_data_targets = training_data[:, 0]
# Convert to one hot encoding
training_data_targets = np.eye(10)[training_data_targets]
# Add bias
training_data_inputs = np.hstack((training_data_inputs_og, np.ones((training_data_inputs_og.shape[0], 1))))
training_data_inputs = training_data_inputs.reshape((training_data_inputs.shape[0], 785, 1))

training_data_targets = training_data_targets.reshape((training_data_targets.shape[0], 10, 1))
print(training_data_inputs.shape, training_data_targets.shape)

num_nodes = [785, 300, 100, 10, 10]

weights_matrices = train_dropout(num_nodes, training_data_inputs, training_data_targets, 0.01, 20)


# Test on train data
final_outputs = forward_pass(weights_matrices, training_data_inputs)[-1]
final_outputs = np.argmax(final_outputs, axis=1)

print(f"Training Accuracy: {np.sum(final_outputs == training_data_targets.argmax(axis=1)) / len(training_data_targets)}")

# Test on test data
test_data = pd.read_csv(args[1]).to_numpy()
test_data_inputs_og = test_data[:, 1:]
test_data_targets = test_data[:, 0]
# Convert to one hot encoding
test_data_targets = np.eye(10)[test_data_targets]
# Add bias
test_data_inputs = np.hstack((test_data_inputs_og, np.ones((test_data_inputs_og.shape[0], 1))))
test_data_inputs = test_data_inputs.reshape((test_data_inputs.shape[0], 785, 1))

test_data_targets = test_data_targets.reshape((test_data_targets.shape[0], 10, 1))
print(test_data_inputs.shape, test_data_targets.shape)

final_outputs = forward_pass(weights_matrices, test_data_inputs)
final_outputs = np.array(final_outputs[-1])
final_outputs = final_outputs.argmax(axis=1)

print(f"Test Accuracy: {np.sum(final_outputs == test_data_targets.argmax(axis=1))/len(test_data_targets)}")

# Plot some random datapoints

for i in range(10):
    random_index = np.random.randint(0, len(test_data_inputs_og))
    random_image = test_data_inputs_og[random_index]
    random_image = random_image.reshape((28, 28))
    plt.imshow(random_image, cmap='gray')
    plt.title(f"Predicted: {final_outputs[random_index]} Actual: {test_data_targets[random_index].argmax()}")
    plt.show()