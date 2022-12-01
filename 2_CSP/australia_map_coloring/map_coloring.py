from tkinter import *
from graphics import *
import random


def check_complete(assignment, vars, adjs):
    for var in vars:
        if var not in assignment:
            return False
        if var in adjs:
            for adj in adjs[var]:
                if adj not in assignment or assignment[var] == assignment[adj]:
                    return False
    return True


def select_unassigned_var(assignment, vars, adjs):
    # Select an unassigned variable - forward checking, MRV, or LCV
    if len(assignment) != 0:
        for assigned in assignment:
            option_map = {}
            # print(assigned)
            if assigned in adjs:
                for adj in adjs[assigned]:
                    if adj not in assignment:
                        option_map[sum(isValid(i, adj, assignment, adjs) for i in vars[adj])] = adj
                if option_map:
                    # print(option_map)
                    return option_map[min(option_map)]
    return random.choice(list(vars.keys()))


def isValid(value, var, assignment, adjs):
    # value is consistent with assignment
    # check adjacents to check 'var' is working or not.
    if var in adjs:
        for adj in adjs[var]:
            if adj in assignment and assignment[adj] == value:
                return False
    return True


def backtracking_search(variables, adjs, shapes, frame):
    return recursive_backtracking({}, variables, adjs, shapes, frame)


def recursive_backtracking(assignment, variables, adjs, shapes, frame):
    if check_complete(assignment, variables, adjs):
        return assignment
    var = select_unassigned_var(assignment, variables, adjs)
    print(var)
    for value in variables[var]:
        if isValid(value, var, assignment, adjs):
            assignment[var] = value
            draw_shape(shapes[var], frame, value)
            result = recursive_backtracking(assignment, variables, adjs, shapes, frame)
            if result != None:
                return result
            # del assignment[var]
    return None


# return shapes as {region:[points], ...} form
def read_shape(filename):
    infile = open(filename)
    region, points, shapes = "", [], {}
    for line in infile.readlines():
        line = line.strip()
        if line.isalpha():
            if region != "": shapes[region] = points
            region, points = line, []
        else:
            x, y = line.split(" ")
            points.append(Point(int(x), 300 - int(y)))
    shapes[region] = points
    return shapes


# fill the shape
def draw_shape(points, frame, color):
    shape = Polygon(points)
    shape.setFill(color)
    shape.setOutline("black")
    shape.draw(frame)
    space = [x for x in range(9999999)]  # give some pause


def main():
    regions, variables, adjacents = [], {}, {}
    # Read mcNodes.txt and store all regions in regions list
    with open("mcNodes.txt") as f:
        for line in f.readlines():
            regions.append(line.strip())

    # Fill variables by using regions list -- no additional code for this part
    for r in regions: variables[r] = {'red', 'green', 'blue'}

    # Read mcEdges.txt and fill the adjacents. Edges are bi-directional.
    with open("mcEdges.txt") as f:
        for line in f.readlines():
            r1, r2 = line.strip().split(" ")
            if r1 not in adjacents: adjacents[r1] = []
            if r2 not in adjacents: adjacents[r2] = []
            adjacents[r1].append(r2)
            adjacents[r2].append(r1)

    # Set graphics -- no additional code for this part
    frame = GraphWin('Map', 300, 300)
    frame.setCoords(0, 0, 299, 299)
    shapes = read_shape("mcPoints.txt")
    for s, points in shapes.items():
        draw_shape(points, frame, 'white')

    # solve the map coloring problem by using backtracking_search -- no additional code for this part
    solution = backtracking_search(variables, adjacents, shapes, frame)
    print(solution)

    mainloop()


if __name__ == '__main__':
    main()
