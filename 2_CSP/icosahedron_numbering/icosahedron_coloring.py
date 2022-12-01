def check_complete(puzzle):
    return "." not in puzzle


def select_unassigned_var(puzzle, csp_table):
    for i in range(len(puzzle)):
        if puzzle[i] == ".":
            return i
    # option_map = {}
    # for i in range(len(puzzle)):
    #     if puzzle[i] != ".":
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


def isValid(value, var_index, puzzle, csp_table):
    for val in csp_table[var_index]:
        if puzzle[val] == value:
            return False
    return True


def backtracking_search(puzzle, csp_table):
    return recursive_backtracking(puzzle, csp_table)


def recursive_backtracking(puzzle, csp_table):
    if check_complete(puzzle):
        return puzzle
    triangle = select_unassigned_var(puzzle, csp_table)
    for val in "ABC":
        if isValid(val, triangle, puzzle, csp_table):
            puzzle = puzzle[:triangle] + val + puzzle[triangle + 1:]
            result = recursive_backtracking(puzzle, csp_table)
            if result is not None:
                return result
            puzzle = puzzle[:triangle] + "." + puzzle[triangle + 1:]
    return None


def display(solution, csp_table):
    result = ""
    for i in range(len(solution)):
        neighbors = ",".join(solution[j] for j in csp_table[i])
        result += f"Index {i} is {solution[i]} and it's neighbors are {neighbors}\n"
    return result


def main():
    csp_table = {0: {1, 19, 10}, 1: {0, 2, 8}, 2: {1, 6, 3}, 3: {4, 19, 2}, 4: {3, 5, 17}, 5: {4, 6, 15}, 6: {2, 5, 7},
                 7: {6, 8, 14}, 8: {1, 7, 6}, 9: {8, 10, 13}, 10: {9, 11, 0}, 11: {12, 10, 18}, 12: {11, 13, 16},
                 13: {9, 12, 14}, 14: {7, 13, 15}, 15: {5, 14, 16}, 16: {12, 15, 17}, 17: {4, 16, 18}, 18: {11, 17, 19},
                 19: {0, 3, 18}}
    puzzle = "." * 20
    solution = backtracking_search(puzzle, csp_table)
    if solution != None:
        print(display(solution, csp_table))
        print(solution)
    else:
        print("It's not solvable.")


if __name__ == '__main__':
    main()
