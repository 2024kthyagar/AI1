import time


def generate_adjacents(current, word_set):
    adj_set = set()
    letters = "qwertyuiopasdfghjklzxcvbnm"
    for i in range(len(current)):
        for ladybug in letters:
            replacement = current[:i] + ladybug + current[i + 1:]
            if replacement in word_set and replacement != current:
                # print(replacement)
                adj_set.add(replacement)
    # print(adj_set)
    return adj_set


def check_adj(words_set):
    # This check method is written for words_6_longer.txt
    adj = generate_adjacents('listen', words_set)
    target = {'listee', 'listel', 'litten', 'lister', 'listed'}
    return (adj == target)


def bi_bfs(start, goal, words_set):
    '''The idea of bi-directional search is to run two simultaneous searches--
    one forward from the initial state and the other backward from the goal--
    hoping that the two searches meet in the middle.
    '''
    if start == goal: return []
    start_explored = {start: None}
    goal_explored = {goal: None}
    start_queue = [start]
    goal_queue = [goal]
    while start_queue and goal_queue:
        start_node = start_queue.pop(0)
        goal_node = goal_queue.pop(0)
        if start_node in goal_queue:
            return make_path(start_node, start_explored)[:-1] + make_path(start_node, goal_explored)[::-1]
        if goal_node in start_queue:
            return make_path(goal_node, start_explored)[:-1] + make_path(goal_node, goal_explored)[::-1]
        for child in generate_adjacents(start_node, words_set):
            if child not in start_explored:
                start_queue.append(child)
                start_explored[child] = start_node
        for child in generate_adjacents(goal_node, words_set):
            if child not in goal_explored:
                goal_queue.append(child)
                goal_explored[child] = goal_node

    return None

# ['gammer', 'gimmer', 'rimmer', 'rimier', 'ribier', 'rubier', 'rubies', 'rubins', 'robins', 'robing', 'roking', 'toking', 'tsking', 'asking', 'arking', 'irking', 'inking', 'unking', 'unkind', 'unbind', 'unbend', 'unbent', 'unbelt', 'unbolt', 'unboot', 'unroot', 'enroot']
# The number steps: 27
# ['gammer', 'rammer', 'ramper', 'rapper', 'rapier', 'ropier', 'rosier', 'rosies', 'rosins', 'rosing', 'rising', 'riming', 'aiming', 'arming', 'arking', 'irking', 'inking', 'unking', 'unkind', 'unkend', 'unkent', 'unbent', 'unbelt', 'unbolt', 'unboot', 'unroot', 'enroot']
# The number of steps:  27
# ['gammer', 'hammer', 'hamper', 'camper', 'capper', 'copper', 'copier', 'copies', 'conies', 'conins', 'coning', 'toning', 'toking', 'tsking', 'asking', 'arking', 'irking', 'inking', 'unking', 'unkind', 'unkend', 'unbend', 'unbent', 'unbelt', 'unbolt', 'unboot', 'unroot', 'enroot']
# The number of steps:  28

def make_path(goal, explored):
    path = []
    while goal is not None:
        path.append(goal)
        goal = explored[goal]
    path.reverse()
    return path


def main():
    filename = input("Type the word file: ")
    words_set = set()
    file = open(filename, "r")
    for word in file.readlines():
        words_set.add(word.rstrip('\n'))
    print("Check generate_adjacents():", check_adj(words_set))
    initial = input("Type the starting word: ")
    goal = input("Type the goal word: ")
    cur_time = time.time()
    path = (bi_bfs(initial, goal, words_set))
    if path != None:
        print(path)
        print("The number of steps: ", len(path))
        print("Duration: ", time.time() - cur_time)
    else:
        print("There's no path")


if __name__ == '__main__':
    main()
