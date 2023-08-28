import random
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
        initial_value = 3
        avg_reward = {i: (0, initial_value) for i in range(10)}
        epsilon = 0.1
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
