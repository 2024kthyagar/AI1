import random, pickle, math, time
from math import pi, acos, sin, cos
from tkinter import *


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


def calc_edge_cost(y1, x1, y2, x2):
    #
    # y1 = lat1, x1 = long1
    # y2 = lat2, x2 = long2
    # all assumed to be in decimal degrees

    # if (and only if) the input is strings
    # use the following conversions

    y1 = float(y1)
    x1 = float(x1)
    y2 = float(y2)
    x2 = float(x2)
    #
    R = 3958.76  # miles = 6371 km
    #
    y1 *= pi / 180.0
    x1 *= pi / 180.0
    y2 *= pi / 180.0
    x2 *= pi / 180.0
    #
    # approximate great circle distance with law of cosines
    #
    return acos(sin(y1) * sin(y2) + cos(y1) * cos(y2) * cos(x2 - x1)) * R
    #


# NodeLocations, NodeToCity, CityToNode, Neighbors, EdgeCost
# Node: (lat, long) or (y, x), node: city, city: node, node: neighbors, (n1, n2): cost
def make_graph(nodes="rrNodes.txt", node_city="rrNodeCity.txt", edges="rrEdges.txt"):
    nodeLoc, nodeToCity, cityToNode, neighbors, edgeCost = {}, {}, {}, {}, {}
    map = {}  # have screen coordinate for each node location

    # Your code goes here
    with open(nodes) as node_loc_file:
        for line in node_loc_file.readlines():
            vals = line.rstrip().split()
            nodeLoc[vals[0]] = (vals[1], vals[2])

    # Un-comment after you fill the nodeLoc dictionary.
    for node in nodeLoc:  # checks each
        lat = float(nodeLoc[node][0])  # gets latitude
        long = float(nodeLoc[node][1])  # gets long
        modlat = (lat - 10) / 60  # scales to 0-1
        modlong = (long + 130) / 70  # scales to 0-1
        map[node] = [modlat * 800, modlong * 1200]  # scales to fit 800 1200

    with open(node_city) as node_city_file:
        for line in node_city_file.readlines():
            vals = line.rstrip().split(" ", 1)
            nodeToCity[vals[0]] = vals[1]
            cityToNode[vals[1]] = vals[0]
    with open(edges) as edges_file:
        for line in edges_file.readlines():
            vals = line.rstrip().split()
            if vals[0] not in neighbors:
                neighbors[vals[0]] = set()
            neighbors[vals[0]].add(vals[1])
            if vals[1] not in neighbors:
                neighbors[vals[1]] = set()
            neighbors[vals[1]].add(vals[0])
            lat1 = nodeLoc[vals[0]][0]
            long1 = nodeLoc[vals[0]][1]
            lat2 = nodeLoc[vals[1]][0]
            long2 = nodeLoc[vals[1]][1]
            cost = calc_edge_cost(lat1, long1, lat2, long2)
            edgeCost[(vals[0], vals[1])] = cost
            edgeCost[(vals[1], vals[0])] = cost

    return [nodeLoc, nodeToCity, cityToNode, neighbors, edgeCost, map]


# Retuen the direct distance from node1 to node2
# Use calc_edge_cost function.
def dist_heuristic(n1, n2, graph):
    # Your code goes here
    nodeLoc = graph[0]
    lat1 = nodeLoc[n1][0]
    long1 = nodeLoc[n1][1]
    lat2 = nodeLoc[n2][0]
    long2 = nodeLoc[n2][1]
    return calc_edge_cost(lat1, long1, lat2, long2)


# Create a city path.
# Visit each node in the path. If the node has the city name, add the city name to the path.
# Example: ['Charlotte', 'Hermosillo', 'Mexicali', 'Los Angeles']
def display_path(path, graph):
    # Your code goes here
    city_path = []
    nodeToCity = graph[1]
    for node in path:
        if node in nodeToCity:
            city_path.append(nodeToCity[node])
    print(city_path)


# Using the explored, make a path by climbing up to "s"
# This method may be used in your BFS and Bi-BFS algorithms.
def generate_path(state, explored, graph):
    path = [state]
    cost = 0
    edgeCost = graph[4]
    # Your code goes here
    while explored[state] != 's':
        path.append(explored[state])
        cost += edgeCost[(state, explored[state])]
        state = explored[state]
    return path[::-1], cost


def drawLine(canvas, y1, x1, y2, x2, col):
    x1, y1, x2, y2 = float(x1), float(y1), float(x2), float(y2)
    canvas.create_line(x1, 800 - y1, x2, 800 - y2, fill=col)


# Draw the final shortest path.
# Use drawLine function.
def draw_final_path(ROOT, canvas, path, graph, col='red'):
    # Your code goes here
    map = graph[5]
    for node, next in zip(path, path[1:]):
        lat1 = map[node][0]
        long1 = map[node][1]
        lat2 = map[next][0]
        long2 = map[next][1]
        drawLine(canvas, lat1, long1, lat2, long2, col)
        ROOT.update()


def draw_all_edges(ROOT, canvas, graph):
    ROOT.geometry("1200x800")  # sets geometry
    canvas.pack(fill=BOTH, expand=1)  # sets fill expand
    for n1, n2 in graph[4]:  # graph[4] keys are edge set
        drawLine(canvas, *graph[5][n1], *graph[5][n2], 'white')  # graph[5] is map dict
    ROOT.update()


def bfs(start, goal, graph, col):
    ROOT = Tk()  # creates new tkinter
    ROOT.title("BFS")
    canvas = Canvas(ROOT, background='black')  # sets background
    draw_all_edges(ROOT, canvas, graph)

    counter = 0
    frontier, explored = [], {start: "s"}
    frontier.append(start)
    while frontier:
        s = frontier.pop(0)
        if s == goal:
            path, cost = generate_path(s, explored, graph)
            draw_final_path(ROOT, canvas, path, graph)
            return path, cost
        for a in graph[3][s]:  # graph[3] is neighbors
            if a not in explored:
                explored[a] = s
                frontier.append(a)
                drawLine(canvas, *graph[5][s], *graph[5][a], col)
        counter += 1
        if counter % 1000 == 0: ROOT.update()
    return None


def bi_bfs(start, goal, graph, col):
    ROOT = Tk()  # creates new tkinter
    ROOT.title("Bi-BFS")
    canvas = Canvas(ROOT, background='black')  # sets background
    draw_all_edges(ROOT, canvas, graph)

    counter = 0
    start_explored = {start: 's'}
    goal_explored = {goal: 's'}
    start_queue = [start]
    goal_queue = [goal]
    while start_queue and goal_queue:
        start_node = start_queue.pop(0)
        goal_node = goal_queue.pop(0)
        if start_node in goal_queue:
            path1, cost1 = generate_path(start_node, start_explored, graph)
            path1 = path1[:-1]
            path2, cost2 = generate_path(start_node, goal_explored, graph)
            path2 = path2[::-1]
            draw_final_path(ROOT, canvas, path1 + path2, graph)
            return path1 + path2, cost1 + cost2
        if goal_node in start_queue:
            path1, cost1 = generate_path(goal_node, start_explored, graph)
            path1 = path1[:-1]
            path2, cost2 = generate_path(goal_node, goal_explored, graph)
            path2 = path2[::-1]
            draw_final_path(ROOT, canvas, path1 + path2, graph)
            return path1 + path2, cost1 + cost2
        for child in graph[3][start_node]:
            if child not in start_explored:
                start_queue.append(child)
                start_explored[child] = start_node
                drawLine(canvas, *graph[5][start_node], *graph[5][child], col)
        for child in graph[3][goal_node]:
            if child not in goal_explored:
                goal_queue.append(child)
                goal_explored[child] = goal_node
                drawLine(canvas, *graph[5][goal_node], *graph[5][child], col)
        counter += 1
        if counter % 1000 == 0: ROOT.update()
    return None


def a_star(start, goal, graph, col, heuristic=dist_heuristic):
    ROOT = Tk()  # creates new tkinter
    ROOT.title("A Star")
    canvas = Canvas(ROOT, background='black')  # sets background
    draw_all_edges(ROOT, canvas, graph)

    frontier = HeapPriorityQueue()
    explored = {start: 0}
    frontier.push((heuristic(start, goal, graph), start, [start]))  # total cost, pathcost, state, path
    edgeCost = graph[4]
    counter = 0
    while not frontier.isEmpty():
        node = frontier.pop()
        path = node[2]
        if node[1] == goal:
            draw_final_path(ROOT, canvas, path, graph)
            return path, explored[node[1]]
        for child in graph[3][node[1]]:
            h = heuristic(child, goal, graph)
            g = explored[node[1]] + edgeCost[(node[1], child)]
            total_cost = h + g
            if child not in explored or g < explored[child]:
                # check if the current path cost to get to that node is better
                frontier.push((total_cost, child, path + [child]))
                explored[child] = g
                drawLine(canvas, *graph[5][node[1]], *graph[5][child], col)
        counter += 1
        if counter % 1000 == 0: ROOT.update()
    return None


def bi_a_star(start, goal, graph, col, ROOT, canvas, heuristic=dist_heuristic):
    start_frontier = HeapPriorityQueue()
    goal_frontier = HeapPriorityQueue()
    start_explored = {start: (0, [start])}
    goal_explored = {goal: (0, [goal])}

    if start == goal: return [start]

    start_frontier.push((heuristic(start, goal, graph), start))
    goal_frontier.push((heuristic(goal, start, graph), goal))
    edgeCost = graph[4]
    counter = 0
    while not start_frontier.isEmpty() and not goal_frontier.isEmpty():
        start_node = start_frontier.pop()
        goal_node = goal_frontier.pop()

        start_path = start_explored[start_node[1]][1]
        goal_path = goal_explored[goal_node[1]][1]

        if start_node[1] in goal_explored:
            path = start_path[:-1] + goal_explored[start_node[1]][1][::-1]
            # print(path)
            return path, start_explored[start_node[1]][0] + goal_explored[start_node[1]][0]

        if goal_node[1] in start_explored:
            path = start_explored[goal_node[1]][1][:-1] + goal_path[::-1]
            # print(path)
            return path, start_explored[goal_node[1]][0] + goal_explored[goal_node[1]][0]

        for child in graph[3][start_node[1]]:
            h = heuristic(child, goal, graph)
            g = start_explored[start_node[1]][0] + edgeCost[(start_node[1], child)]
            total_cost = h + g
            if child not in start_explored or g < start_explored[child][0]:
                # check if the current path cost to get to that node is better
                start_frontier.push((total_cost, child))
                start_explored[child] = (g, start_path + [child])
                drawLine(canvas, *graph[5][start_node[1]], *graph[5][child], col)

        for child in graph[3][goal_node[1]]:
            h = heuristic(child, start, graph)
            g = goal_explored[goal_node[1]][0] + edgeCost[(goal_node[1], child)]
            total_cost = h + g
            if child not in goal_explored or g < goal_explored[child][0]:
                # check if the current path cost to get to that node is better
                goal_frontier.push((total_cost, child))
                goal_explored[child] = (g, goal_path + [child])
                drawLine(canvas, *graph[5][goal_node[1]], *graph[5][child], col)

        counter += 1
        if counter % 1000 == 0: ROOT.update()
    return None


def tri_directional(city1, city2, city3, graph, col, ROOT, canvas, heuristic=dist_heuristic):
    path12, cost12 = bi_a_star(city1, city2, graph, col, ROOT, canvas)
    path23, cost23 = bi_a_star(city2, city3, graph, col, ROOT, canvas)
    path31, cost31 = bi_a_star(city3, city1, graph, col, ROOT, canvas)
    cost, path = min([(cost12 + cost23, path12[:-1] + path23), (cost23 + cost31, path23[:-1] + path31),
                      (cost31 + cost12, path31[:-1] + path12)])
    draw_final_path(ROOT, canvas, path, graph)
    return path, cost


def main():
    start, goal = input("Start city: "), input("Goal city: ")
    # third = input("Third city for tri-directional: ")
    graph = make_graph("rrNodes.txt", "rrNodeCity.txt", "rrEdges.txt")  # Task 1

    # cur_time = time.time()
    # path, cost = bfs(graph[2][start], graph[2][goal], graph, 'yellow')  # graph[2] is city to node
    # if path != None:
    #     print(f"Path Length: {len(path)}")
    #     print(path)
    #     display_path(path, graph)
    # else:
    #     print("No Path Found.")
    # print('BFS Path Cost:', cost)
    # print('BFS duration:', (time.time() - cur_time))
    # print()
    #
    # cur_time = time.time()
    # p, cost = bi_bfs(graph[2][start], graph[2][goal], graph, 'green')
    # if path != None:
    #     print(f"Path Length: {len(path)}")
    #     print(path)
    #     display_path(path, graph)
    # else: print ("No Path Found.")
    # print ('Bi-BFS Path Cost:', cost)
    # print ('Bi-BFS duration:', (time.time() - cur_time))
    # print ()
    #
    # print(f"BFS Path is the same as Bi-BFS Path: {path==p}")
    #
    cur_time = time.time()
    path, cost = a_star(graph[2][start], graph[2][goal], graph, 'blue')
    if path != None:
        print(f"Path Length: {len(path)}")
        print(path)
        display_path(path, graph)
    else: print ("No Path Found.")
    print ('A star Path Cost:', cost)
    print ('A star duration:', (time.time() - cur_time))
    print ()

    ROOT = Tk()  # creates new tkinter
    ROOT.title("Bidirectional A Star")
    canvas = Canvas(ROOT, background='black')  # sets background
    draw_all_edges(ROOT, canvas, graph)
    cur_time = time.time()
    path, cost = bi_a_star(graph[2][start], graph[2][goal], graph, 'orange', ROOT, canvas)
    if path != None:
        print(f"Path Length: {len(path)}")
        print(path)
        draw_final_path(ROOT, canvas, path, graph)
        display_path(path, graph)
    else:
        print("No Path Found.")
    print('Bi-A star Path Cost:', cost)
    print("Bi-A star duration: ", (time.time() - cur_time))
    print()

    third = input("Third City: ")
    print("Tri-Search of ({}, {}, {})".format(start, goal, third))
    ROOT = Tk()  # creates new tkinter
    ROOT.title("Tridirectional A Star")
    canvas = Canvas(ROOT, background='black')  # sets background
    draw_all_edges(ROOT, canvas, graph)
    cur_time = time.time()
    path, cost = tri_directional(graph[2][start], graph[2][goal], graph[2][third], graph, 'pink', ROOT, canvas)
    if path != None:
        print(f"Path Length: {len(path)}")
        print(path)
        display_path(path, graph)
    else:
        print("No Path Found.")
    print('Tri-A star Path Cost:', cost)
    print("Tri-directional search duration:", (time.time() - cur_time))

    mainloop()  # Let TK windows stay still


if __name__ == '__main__':
    main()
