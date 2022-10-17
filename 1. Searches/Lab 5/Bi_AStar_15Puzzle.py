# Name: Karthik Thyagarajan   Date:
import random, time, math


class HeapPriorityQueue():
    def __init__(self):
        self.queue = ['dummy']
        self.current = 1

    def next(self):
        if self.current >= len(self.queue):
            raise StopIteration

        out = self.queue[self.current]
        self.current += 1

        return out

    def __iter__(self):
        return self

    __next__ = next

    def isEmpty(self):
        return len(self.queue) == 1

    def swap(self, a, b):
        self.queue[a], self.queue[b] = self.queue[b], self.queue[a]

    def remove(self, index):
        val = self.queue[index]
        del self.queue[index]
        self.reheap()
        return val

    def pop(self):
        self.swap(1, -1)
        val = self.queue.pop()
        self.heapDown(1, len(self.queue) - 1)
        return val

    def push(self, value):
        self.queue.append(value)
        self.heapUp(len(self.queue) - 1)

    def peek(self):
        return self.queue[1]

    def reheap(self):
        for k in range(len(self.queue) // 2, 0, -1):
            self.heapDown(k, len(self.queue) - 1)

    def heapDown(self, k, size):
        left, right = 2 * k, 2 * k + 1

        if left == size and self.queue[k] > self.queue[size]:
            self.swap(k, size)

        elif right <= size:
            min_child = left if self.queue[left] <= self.queue[right] else right

            if self.queue[k] > self.queue[min_child]:
                self.swap(k, min_child)
                self.heapDown(min_child, size)

    def heapUp(self, k):
        parent = k // 2 if k > 1 else k
        if self.queue[k] < self.queue[parent]:
            self.swap(k, parent)
            self.heapUp(parent)

    def isEmpty(self):
        return len(self.queue) <= 1


def inversion_count(new_state, width=4, N=4):
    # Count inversions
    count = 0
    state = new_state[:(x := new_state.find('_'))] + new_state[x + 1:]
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            if state[i] > state[j]:
                count += 1
    # if N is odd
    if N % 2 == 1:
        return count % 2 == 0  # true if inversions is even
    # if N is even
    else:
        # if even row
        if ((len(new_state) - 1 - new_state.find('_')) // width) % 2 == 0:
            # checking odd row (index of row starting from 0, so )
            return count % 2 == 1
        else:
            return count % 2 == 0


def check_inversion():
    t1 = inversion_count("_42135678", 3, 3)  # N=3
    f1 = inversion_count("21345678_", 3, 3)
    t2 = inversion_count("4123C98BDA765_EF", 4)  # N is default, N=4
    f2 = inversion_count("4123C98BDA765_FE", 4)
    return t1 and t2 and not (f1 or f2)


def getInitialState(sample, size):
    sample_list = list(sample)
    random.shuffle(sample_list)
    new_state = ''.join(sample_list)
    while not inversion_count(new_state, size, size):
        random.shuffle(sample_list)
        new_state = ''.join(sample_list)
    return new_state


def swap(n, i, j):
    lst = list(n)
    lst[i], lst[j] = lst[j], lst[i]
    return "".join(lst)


'''Generate a list which hold all children of the current state
   and return the list'''


def generate_children(state, size=4):
    blank = state.find('_')
    up = swap(state, blank, blank - size) if blank >= size else None
    down = swap(state, blank, blank + size) if blank < len(state) - size else None
    left = swap(state, blank, blank - 1) if blank % size > 0 else None
    right = swap(state, blank, blank + 1) if blank % size < size - 1 else None
    return [v for v in [up, left, down, right] if v is not None]


def display_path(path_list, size):
    for n in range(size):
        for path in path_list:
            print(path[n * size:(n + 1) * size], end=" " * size)
        print()
    print("\nThe shortest path length is :", len(path_list))
    return ""


''' You can make multiple heuristic functions '''


def dist_heuristic(state, goal="_123456789ABCDEF", size=4):
    total_dist = 0
    for i in range(len(goal)):
        goal_index = goal.find(state[i])
        total_dist += abs(i % size - goal_index % size) + abs(i // size - goal_index // size)
    return total_dist


def check_heuristic():
    a = dist_heuristic("152349678_ABCDEF", "_123456789ABCDEF", 4)
    b = dist_heuristic("8936C_24A71FDB5E", "_123456789ABCDEF", 4)
    return a < b


def solve(start, goal="_123456789ABCDEF", heuristic=dist_heuristic, size=4):
    # 2_63514B897ACDEF
    # inf = 10**300 # like infinity
    # distance = inf
    # shortest_path = []

    start_frontier = HeapPriorityQueue()
    goal_frontier = HeapPriorityQueue()
    start_explored = {start: 1}
    goal_explored = {goal: 1}

    if start == goal: return [start]

    start_frontier.push((heuristic(start,goal)+1, start, [start]))
    goal_frontier.push((heuristic(goal, start) + 1, goal, [goal]))

    # frontier.push((1+ heuristic(start,goal) + 1, start, [start], goal, [goal]))  # total cost, start state, start path, goal state, goal path
    while not start_frontier.isEmpty() and not goal_frontier.isEmpty():

        # node_pair = frontier.pop()
        # start_state = node_pair[1]
        # start_path = node_pair[2]
        # goal_state = node_pair[3]
        # goal_path = node_pair[4]

        start_node = start_frontier.pop()
        goal_node = goal_frontier.pop()
        start_path = start_node[2]
        goal_path = goal_node[2]

        # if start_state == goal_state:
        #     return start_path + goal_path[::-1]
        #
        # for start_child in generate_children(start_state):
        #     for goal_child in generate_children(goal_state):
        #         h = heuristic(start_child, goal_child)
        #         start_g = len(start_path) + 1
        #         goal_g = len(goal_path) + 1
        #         total_cost = h + start_g + goal_g
        #         if (start_child not in start_explored or start_g <= start_explored[start_child]) and (goal_child not in goal_explored or goal_g <= goal_explored[goal_child]):
        #             # check if the current path cost to get to that node is better
        #             frontier.push((total_cost, start_child, start_path + [start_child], goal_child, goal_path+[goal_child]))
        #             start_explored[start_child] = start_g
        #             goal_explored[goal_child] = goal_g


        if start_node[1] in goal_explored:
            for i in goal_frontier:
                if i[1] == start_node[1]:
                    return start_node[2][:-1] + i[2][::-1]


        if goal_node[1] in start_explored:
            for i in start_frontier:
                if i[1] == goal_node[1]:
                    return i[2][:-1] + goal_node[2][::-1]

        for child in generate_children(start_node[1]):
            h = heuristic(child, goal)
            g = len(start_path) + 1
            total_cost = h + g
            if child not in start_explored or g < start_explored[child]:
                # check if the current path cost to get to that node is better
                start_frontier.push((total_cost, child, start_path + [child]))
                start_explored[child] = g

        for child in generate_children(goal_node[1]):
            h = heuristic(child, start)
            g = len(goal_path) + 1
            total_cost = h + g
            if child not in goal_explored or g < goal_explored[child]:
                # check if the current path cost to get to that node is better
                goal_frontier.push((total_cost, child, goal_path + [child]))
                goal_explored[child] = g

        # start_set.add(start_node[1])

        # if start_node[1] in goal_explored:
        #     total_set = start_set | goal_set
        #     for state in total_set:
        #         start_g = start_explored[state] if state in start_explored else inf
        #         goal_g = goal_explored[state] if state in goal_explored else inf
        #         for i in goal_frontier:
        #             if i[1] == state:
        #                 back_path = i[2]
        #                 break
        #         if start_g + goal_g < distance:
        #             distance = start_explored[state] + goal_explored[state]
        #             shortest_path = start_path + back_path[::-1]
        #     return shortest_path

        # goal_set.add(goal_node[1])

        # if goal_node[1] in start_explored:
        #     total_set = start_set | goal_set
        #     for state in total_set:
        #         start_g = start_explored[state] if state in start_explored else inf
        #         goal_g = goal_explored[state] if state in goal_explored else inf
        #         for i in start_frontier:
        #             print(i[1], state)
        #             if i[1] == state:
        #                 front_path = i[2]
        #                 break
        #         if start_g + goal_g < distance:
        #             distance = start_explored[state] + goal_explored[state]
        #             shortest_path = goal_path + front_path[::-1]
        #     return shortest_path

    return None


def main():
    # A star
    print("Inversion works?:", check_inversion())
    print("Heuristic works?:", check_heuristic())
    # initial_state = getInitialState("_123456789ABCDEF", 4)
    initial_state = input("Type initial state: ")
    if inversion_count(initial_state):
        cur_time = time.time()
        path = (solve(initial_state))
        if path is not None:
            display_path(path, 4)
        else:
            print("No Path Found.")
        print("Duration: ", (time.time() - cur_time))
    else:
        print("{} did not pass inversion test.".format(initial_state))


if __name__ == '__main__':
    main()
