from random import gauss
import math

switch_num = 0
avg_reward = {}  # average reward for each arm as index: (num of pulls, sum of rewards)
initial_value = 0  # initial value for each arm
epsilon = 0  # epsilon for epsilon-greedy
c = 0  # constant for upper confidence bound


def bandit(testNum, armIdx, pullVal):
    '''testNum is the current test number, armIdx is the last arm pulled, pullVal is the reward from the last pull'''
    global switch_num, avg_reward, initial_value, epsilon, c
    if testNum == 0:
        # initialize
        switch_num = 1
        initial_value = 10
        avg_reward = {i: (0, initial_value) for i in range(10)}
        c = 0.78
        return 0
    # update average reward
    avg_reward[armIdx] = (avg_reward[armIdx][0] + 1, avg_reward[armIdx][1] + pullVal)
    if testNum < 10:
        return testNum
    # upper confidence bound
    return max(avg_reward, key=lambda x: avg_reward[x][1] / avg_reward[x][0] + c * math.sqrt(
        math.log(testNum) / avg_reward[x][0]))

# Karthik Thyagarajan, 5, 2024

sum_reward = 0
sum_pct = 0
numRuns = 1000
for i in range(numRuns):
    ten_arm_means = [gauss(0, 1) for i in range(10)]
    reward = 0
    prev_armIdx = 0
    prev_pullVall = 0

    for testNum in range(1000):
        armIdx = bandit(testNum, prev_armIdx, prev_pullVall)
        pullVal = gauss(ten_arm_means[armIdx], 1)
        reward += pullVal
        prev_pullVall = pullVal
        prev_armIdx = armIdx

    sum_reward += reward
    sum_pct += reward / (max(ten_arm_means) * 1000)

    if i % 100 == 0 and i > 0: print(f'{sum_pct / i * 100}%;  rwd avg: {sum_reward / i}')





print()
print(f'Final: {sum_pct / numRuns * 100}%;  rwd avg: {sum_reward / numRuns}')