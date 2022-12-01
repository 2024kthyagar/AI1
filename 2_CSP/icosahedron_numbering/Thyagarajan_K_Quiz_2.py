
def check_complete(independent, puzzle, csp_table):
    for val in puzzle:
        if isValid(val, independent, csp_table) and val not in independent:
            return False
    return True


def select_unassigned_var(independent, puzzle, csp_table):
    for i in puzzle:
        if i not in independent:
            return i
    # option_map = {}
    # for i in puzzle:
    #     if i in independent:
    #         continue
    #     option_map[i] = sum(isValid(val, independent, csp_table) for val in csp_table[i])
    # if option_map:
    #     return min(option_map, key=option_map.get)


def domain_returner(independent, puzzle):
    domain = []
    for i in puzzle:
        if i not in independent:
            domain.append(i)
    return domain


def isValid(value, independent, csp_table):
    for val in independent:
        if val in csp_table[value]:
            return False
    return True


# ........................

def backtracking_search(puzzle, csp_table):
    return recursive_backtracking(set(), puzzle, csp_table)


def recursive_backtracking(independent, puzzle, csp_table):
    if check_complete(independent, puzzle, csp_table):
        return independent
    # triangle = select_unassigned_var(independent, puzzle, csp_table)
    for triangle in domain_returner(independent, puzzle):
        if isValid(triangle, independent, csp_table):
            independent.add(triangle)
            result = recursive_backtracking(independent, puzzle, csp_table)
            if result is not None:
                return result
            independent.remove(triangle)
    return None


def display(solution):
    result = ""
    for i in range(len(solution)):
        if i == 0: result += "  "
        if i == 5: result += "\n"
        if i == 12: result += "\n"
        if i == 19: result += "\n  "
        result += solution[i] + " "
    return result


def main():
    csp_table = {0: {1, 19, 10}, 1: {0, 2, 8}, 2: {1, 6, 3}, 3: {4, 19, 2}, 4: {3, 5, 17}, 5: {4, 6, 15}, 6: {2, 5, 7},
                 7: {6, 8, 14}, 8: {1, 7, 6}, 9: {8, 10, 13}, 10: {9, 11, 0}, 11: {12, 10, 18}, 12: {11, 13, 16},
                 13: {9, 12, 14}, 14: {7, 13, 15}, 15: {5, 14, 16}, 16: {12, 15, 17}, 17: {4, 16, 18}, 18: {11, 17, 19},
                 19: {0, 3, 18}}
    puzzle = [i for i in range(20)]
    solution = backtracking_search(puzzle, csp_table)
    if solution != None:
        print(solution)
    else:
        print("It's not solvable.")


if __name__ == '__main__':
    main()
