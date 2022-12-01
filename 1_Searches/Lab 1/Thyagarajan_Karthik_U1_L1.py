import random, time


def getInitialState():
    x = "_12345678"
    l = list(x)
    random.shuffle(l)
    y = ''.join(l)
    return y


'''precondition: i<j
   swap characters at position i and j and return the new state'''


def swap(state, i, j):
    """your code goes here"""
    lst = list(state)
    lst[i], lst[j] = lst[j], lst[i]
    return "".join(lst)


'''Generate a list which hold all children of the current state
   and return the list'''


def generate_children(state):
    s = state.index('_')
    up = swap(state, s, s - 3) if s > 2 else None
    down = swap(state, s, s + 3) if s < len(state) - 3 else None
    left = swap(state, s, s - 1) if s % 3 > 0 else None
    right = swap(state, s, s + 1) if s % 3 < 2 else None
    return [v for v in [up, left, down, right] if v is not None]


def display_path(n, explored):  # key: current, value: parent
    lst = []
    while explored[n] != "s":  # "s" is initial's parent
        lst.append(n)
        n = explored[n]
    print()
    lst = lst[::-1]
    for i in lst:
        print(i[0:3], end="   ")
    print()
    for j in lst:
        print(j[3:6], end="   ")
    print()
    for k in lst:
        print(k[6:9], end="   ")
    return len(lst)


'''Find the shortest path to the goal state "_12345678" and
   returns explored and an empty string or "No solution".
   You can make other helper methods, but you must use dictionary for explored.'''


def BFS(initial_state, goal="_12345678"):
    explored = {initial_state: "s"}
    queue = [initial_state]
    while queue:
        node = queue.pop(0)
        if node == goal:
            return explored, ""
        for child in generate_children(node):
            if child not in explored:
                queue.append(child)
                explored[child] = node
    return explored, "No solution"


'''Find the path to the goal state "_12345678" and
   returns explored and an empty string or "No solution".
   You can make other helper methods, but you must use dictionary for explored.'''


def DFS(initial_state, goal="_12345678"):
    explored = {initial_state: "s"}
    '''Your code goes here'''
    stack = [initial_state]
    while stack:
        node = stack.pop()
        if node == goal:
            return explored, ""
        for child in generate_children(node):
            if child not in explored:
                stack.append(child)
                explored[child] = node
    # goal test is passed? return explored, ""
    return explored, "No solution"


def permutations(lst):
    if not lst:
        return []
    if len(lst) == 1:
        return lst
    perms = []
    for i in range(len(lst)):
        remainder = lst[:i] + lst[i + 1:]
        # all permutations lst[i] as first character
        for p in permutations(remainder):
            perms.append(lst[i] + p)
    return perms


def count_inversions(state):
    count = 0
    state = state[:(x := state.index('_'))] + state[x + 1:]
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            if state[i] > state[j]:
                count += 1
    return count


def main():
    goal = '_12345678'
    goal_inversions = count_inversions(goal)
    with open("solvable_8_puzzle.txt", 'w') as outfile:
        for perm in permutations(list(goal)):
            if count_inversions(perm) % 2 == goal_inversions % 2:
                outfile.write(perm + '\n')

    # find_solvables()

    # initial = getInitialState()
    # goal = "_12345678"
    # initial = "1345267_8"
    # # initial = "_42135678"
    # # initial = "1_2345678"
    # # Fun of 8 puzzle
    # # initial = "1234567_8"
    # # initial = "14725836_"
    # # initial = "12345678_"
    # # initial = "84765231_"
    # start = time.time()
    # print("BFS start with:\n", initial[0:3], "\n", initial[3:6], "\n", initial[6:], "\n")
    # bfs_result = BFS(initial)
    # print("\n\nThe number of nodes explored:", len(bfs_result[0]))
    # if bfs_result[1] != "No solution":
    #     print("\nThe shortest path length is :", display_path(goal, bfs_result[0]))
    # else:
    #     print("NO SOLUTION")
    # print("BFS duration:", time.time() - start)
    # start = time.time()
    # print("\n\nDFS start with:\n", initial[0:3], "\n", initial[3:6], "\n", initial[6:], "\n")
    # dfs_result = DFS(initial)
    # print("\n\nThe number of nodes explored:", len(dfs_result[0]))
    # if dfs_result[1] != "No solution":
    #     print("\nThe path length is :", display_path(goal, dfs_result[0]))
    # else:
    #     print("NO SOLUTION")
    # print("DFS duration:", time.time() - start)


if __name__ == '__main__':
    main()

# Karthik Thyagarajan, 5, 2024
