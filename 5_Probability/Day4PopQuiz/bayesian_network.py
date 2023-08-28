import numpy as np


class BayesianNetwork:
    def __init__(self):
        self.nodes = []  # list of nodes
        self.joint_dist = np.array([])  # joint distribution of all nodes

    def add_nodes(self, *nodes):
        for node in nodes:
            self.nodes.append(node)  # add node to list
            node.node_index = len(self.nodes) - 1  # set node index in order of adding

    def bake(self):
        self.full_joint_dist()

    def full_joint_dist(self):
        self.joint_dist = np.zeros(([node.num_states for node in self.nodes]))  # initialize joint distribution with 0s
        for i, val in np.ndenumerate(self.joint_dist):  # iterate over all possible combinations of node values
            self.joint_dist[i] = self.compute_joint_dist(i)  # compute joint probability for given index
        # print(self.joint_dist)

    def compute_joint_dist(self, index):
        joint_prob = 1  # initialize joint probability
        for node in self.nodes:
            # get parent states based off of index
            parent_values = [index[parent.node_index] for parent in node.parents]
            cpt_index = np.append(parent_values, index[node.node_index])  # append node state to parent states
            cpt_index = tuple(cpt_index.astype(int))  # P(child|all parents based on value)
            joint_prob *= node.cpt[cpt_index]  # multiply joint probability by probability of node given parents
        return joint_prob

    def predict_proba(self, node, value, *givens):
        node_index = node.node_index  # get node index
        indices = [slice(None)] * self.joint_dist.ndim  # initialize slice for all indices
        for given in givens:
            indices[given[0].node_index] = given[1]  # set slice for given values
        smaller_joint_dist = self.joint_dist[tuple(indices)]  # get joint distribution for given values
        indices[node_index] = value  # set slice for node value
        marginal_dist = self.joint_dist[tuple(indices)] # get marginal distribution for node value
        normalizer = np.sum(smaller_joint_dist)  # get normalizer, sum of all values in given joint distribution
        marginal_prob = marginal_dist.sum()  # get marginal probability, sum of all values in marginal distribution
        return marginal_prob / normalizer  # return normalized marginal probability


class Node:
    def __init__(self, name):
        self.name = name
        self.parents = []
        self.cpt = np.array([])
        self.num_states = 2
        self.node_index = 0

    def __repr__(self):
        return self.name

    def add_parents(self, *parents):
        for parent in parents:
            self.parents.append(parent)

    def add_cpt(self, cpt):
        self.cpt = cpt
        self.num_states = cpt.shape[-1]
