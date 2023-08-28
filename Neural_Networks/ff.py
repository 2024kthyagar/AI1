import sys; args = sys.argv[1:]
import math

# Feed Forward Neural Network
weights = []
with open(args[0]) as infile:
    weightstr = infile.read().splitlines()
    for i in range(len(weightstr)):
        weights.append([float(j) for j in weightstr[i].split(' ')])
transfer = args[1]
input_data = args[2:]
input_data = [[float(i)] for i in input_data]
num_nodes = [len(input_data)]
for i in range(len(weights)-1):
    num_nodes.append(int(len(weights[i])/num_nodes[i]))
num_nodes.append(num_nodes[-1])



# Turn weights into a list of matrices
weights_matrices = []
for i in range(len(weights)):
    if i == len(weights)-1:
        weights_matrices.append([[num] for num in weights[i]])
    else:
        weights_matrices.append([])
        for j in range(num_nodes[i+1]):
            weights_matrices[i].append(weights[i][j*num_nodes[i]:(j+1)*num_nodes[i]])



def T1(x):
    return x

def T2(x):
    return x * (x > 0)

def T3(x):
    return 1 / (1 + math.exp(-x))

def T4(x):
    return -1 + (2 / (1 + math.exp(-x)))

def dot(a, b):  # matrices a and b are 2D lists
    return [[sum(i * j for i, j in zip(r, c)) for c in zip(*b)] for r in a]



# Feed Forward Loop
outputs = [input_data]
for i in range(len(weights_matrices)):
    if i != len(weights_matrices)-1:
        outputs.append(dot(weights_matrices[i], outputs[i]))
        if transfer == 'T1':
            outputs[i+1] = [[T1(j)] for [j] in outputs[i+1]]
        elif transfer == 'T2':
            outputs[i+1] = [[T2(j)] for [j] in outputs[i+1]]
        elif transfer == 'T3':
            outputs[i+1] = [[T3(j)] for [j] in outputs[i+1]]
        elif transfer == 'T4':
            outputs[i+1] = [[T4(j)] for [j] in outputs[i+1]]
    else:
        outputs.append([i*j] for [i], [j] in zip(outputs[i], weights_matrices[i]))

str = ""
for [num] in outputs[-1]:
    str += f"{num},"
print(str[:-1])


# Karthik Thyagarajan 5 2024