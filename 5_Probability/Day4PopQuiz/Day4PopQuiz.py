from pomegranate import *

Burglary = DiscreteDistribution({'Y': 0.001, 'N': 0.999})
Earthquake = DiscreteDistribution({'Y': 0.002, 'N': 0.998})
Alarm = ConditionalProbabilityTable([
    ['Y', 'Y', 'Y', 0.95],
    ['Y', 'Y', 'N', 0.05],
    ['Y', 'N', 'Y', 0.94],
    ['Y', 'N', 'N', 0.06],
    ['N', 'Y', 'Y', 0.29],
    ['N', 'Y', 'N', 0.71],
    ['N', 'N', 'Y', 0.001],
    ['N', 'N', 'N', 0.999]], [Burglary, Earthquake])

JohnCalls = ConditionalProbabilityTable([
    ['Y', 'Y', 0.90],
    ['Y', 'N', 0.10],
    ['N', 'Y', 0.05],
    ['N', 'N', 0.95]], [Alarm])

MaryCalls = ConditionalProbabilityTable([
    ['Y', 'Y', 0.70],
    ['Y', 'N', 0.30],
    ['N', 'Y', 0.01],
    ['N', 'N', 0.99]], [Alarm])

s_Burglary = State(Burglary, name='Burglary')
s_Earthquake = State(Earthquake, name='Earthquake')
s_Alarm = State(Alarm, name='Alarm')
s_JohnCalls = State(JohnCalls, name='JohnCalls')
s_MaryCalls = State(MaryCalls, name='MaryCalls')

model = BayesianNetwork('Day 4 Pop Quiz')

model.add_states(s_Burglary, s_Earthquake, s_Alarm, s_JohnCalls, s_MaryCalls)
model.add_edge(s_Burglary, s_Alarm)
model.add_edge(s_Earthquake, s_Alarm)
model.add_edge(s_Alarm, s_JohnCalls)
model.add_edge(s_Alarm, s_MaryCalls)

model.bake()

print("---------- Day 4 Pop Quiz ----------")
print("P(~B) =", 0.999)
print("P(~A,|B, ~E) =", model.predict_proba({'Burglary': 'Y', 'Earthquake': 'N'})[2].parameters[0]['N'])
print("P(B|J,M) =", model.predict_proba({'JohnCalls': 'Y', 'MaryCalls': 'Y'})[0].parameters[0]['Y'])
