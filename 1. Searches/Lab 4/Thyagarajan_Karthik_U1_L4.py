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


def a_star(start, goal="_123456789ABCDEF", heuristic=dist_heuristic, size=4):
    # 2_63514B897ACDEF
    frontier = HeapPriorityQueue()
    explored = {start: 0}
    if start == goal: return [start]
    frontier.push((heuristic(start)+1, start, [start]))  # total cost, state, path
    while not frontier.isEmpty():
        node = frontier.pop()
        path = node[2]
        if node[1] == goal:
            return path
        for child in generate_children(node[1]):
            h = heuristic(child)  # O(n), makes it too slow
            g = len(path) + 1
            total_cost = h + g
            if child not in explored or g < explored[child]:
                # check if the current path cost to get to that node is better
                frontier.push((total_cost, child, path + [child]))
                explored[child] = g
    return None


def main():
    # A star
    print("Inversion works?:", check_inversion())
    print("Heuristic works?:", check_heuristic())
    # initial_state = getInitialState("_123456789ABCDEF", 4)
    initial_state = input("Type initial state: ")
    if inversion_count(initial_state):
        cur_time = time.time()
        path = (a_star(initial_state))
        if path is not None:
            display_path(path, 4)
        else:
            print("No Path Found.")
        print("Duration: ", (time.time() - cur_time))
    else:
        print("{} did not pass inversion test.".format(initial_state))


if __name__ == '__main__':
    main()
