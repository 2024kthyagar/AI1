from pomegranate import *

G = DiscreteDistribution({'Y': 0.9, 'N': 0.1})

O1 = ConditionalProbabilityTable([
    ['Y', 'Y', 0.5],
    ['Y', 'N', 0.5],
    ['N', 'Y', 0.05],
    ['N', 'N', 0.95]], [G])

O2 = ConditionalProbabilityTable([
    ['Y', 'Y', 0.75],
    ['Y', 'N', 0.25],
    ['N', 'Y', 0.25],
    ['N', 'N', 0.75]], [G])

s_G = Node(G, name='G')
s_O1 = Node(O1, name='O1')
s_O2 = Node(O2, name='O2')

model = BayesianNetwork('Day 3 Notes')
model.add_states(s_G, s_O1, s_O2)

model.add_edge(s_G, s_O1)
model.add_edge(s_G, s_O2)

model.bake()

print("---------- Day 3 Pop Quiz ----------")
print("P(o2|g, ~o1) =", model.predict_proba({'G': 'Y', 'O1': 'N'})[2].parameters[0]['Y'])
print("P(g|o1, o2) =", model.predict_proba({'O1': 'Y', 'O2': 'Y'})[0].parameters[0]['Y'])
print("P(g|~o1, o2) =", model.predict_proba({'O1': 'N', 'O2': 'Y'})[0].parameters[0]['Y'])
print("P(g|~o1, ~o2) =", model.predict_proba({'O1': 'N', 'O2': 'N'})[0].parameters[0]['Y'])
print("P(o2|o1) =", model.predict_proba({'O1': 'Y'})[2].parameters[0]['Y'])
print()

S = DiscreteDistribution({'Y': 0.7, 'N': 0.3})
R = DiscreteDistribution({'Y': 0.01, 'N': 0.99})
H = ConditionalProbabilityTable([
    ['Y', 'Y', 'Y', 1],
    ['Y', 'Y', 'N', 0],
    ['N', 'Y', 'Y', 0.9],
    ['N', 'Y', 'N', 0.1],
    ['Y', 'N', 'Y', 0.7],
    ['Y', 'N', 'N', 0.3],
    ['N', 'N', 'Y', 0.1],
    ['N', 'N', 'N', 0.9]], [S, R])

s_S = Node(S, name='S')
s_R = Node(R, name='R')
s_H = Node(H, name='H')

model = BayesianNetwork('Day 2 Notes Example 3')

model.add_states(s_S, s_R, s_H)

model.add_edge(s_S, s_H)
model.add_edge(s_R, s_H)

model.bake()

print("---------- Day 2 Notes Example 3 ----------")
print("P(r|s) =", model.predict_proba({'S': 'Y'})[1].parameters[0]['Y'])
print("P(r|h, s) =", model.predict_proba({'H': 'Y', 'S': 'Y'})[1].parameters[0]['Y'])
print("P(r|h) =", model.predict_proba({'H': 'Y'})[1].parameters[0]['Y'])
print("P(r|h, ~s) =", model.predict_proba({'H': 'Y', 'S': 'N'})[1].parameters[0]['Y'])