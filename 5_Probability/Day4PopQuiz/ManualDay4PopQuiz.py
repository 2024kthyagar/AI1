import numpy as np
from bayesian_network import BayesianNetwork, Node

Burglary = Node('Burglary')
Burglary.cpt = np.array([0.001, 0.999])  # 0=yes, 1=no

Earthquake = Node('Earthquake')
Earthquake.cpt = np.array([0.002, 0.998])  # 0=yes, 1=no

Alarm = Node('Alarm')
Alarm.add_cpt(np.array([  # B=true
    [
        [0.95, 0.05],  # E=true
        [0.94, 0.06]  # E=false
    ],
    [  # B=false
        [0.29, 0.71],  # E=true
        [0.001, 0.999]  # E=false
    ]
]))
Alarm.add_parents(Burglary, Earthquake)  # must be in the same order as the cpt

JohnCalls = Node('JohnCalls')
JohnCalls.add_cpt(np.array([
    [0.90, 0.10],  # A=true
    [0.05, 0.95]  # A=false
]))
JohnCalls.add_parents(Alarm)

MaryCalls = Node('MaryCalls')
MaryCalls.cpt = np.array([
    [0.70, 0.30],  # A=true
    [0.01, 0.99]  # A=false
])
MaryCalls.add_parents(Alarm)

model = BayesianNetwork()
model.add_nodes(Burglary, Earthquake, Alarm, JohnCalls, MaryCalls)

model.bake()

print("---------- Day 4 Pop Quiz ----------")
print("P(~B) =", model.predict_proba(Burglary, 1))  # 1=no
print("P(~A,|B, ~E) =", model.predict_proba(Alarm, 1, (Burglary, 0), (Earthquake, 1)))
print("P(B|J,M) =", model.predict_proba(Burglary, 0, (JohnCalls, 0), (MaryCalls, 0)))
