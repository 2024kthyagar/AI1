import random


def check_complete(assignment, csp_table):
    if assignment.find('.') != -1: return False
    for hexa in csp_table:
        if len(set([assignment[i] for i in hexa])) != 6: return False
    return True


def select_unassigned_var(assignment, csp_table):
    for i in range(len(assignment)):
        if assignment[i] == ".":
            continue
        option_map = {}
        for hexa in csp_table:
            if i in hexa:
                for val in hexa:
                    if assignment[val] == ".":
                        option_map[val] = sum(isValid(j, val, assignment, csp_table) for j in range(1, 7))
        if option_map:
            return min(option_map, key=option_map.get)
    return random.randint(0, 23)


def isValid(value, var_index, assignment, csp_table):
    for hexa in csp_table:
        if var_index in hexa:
            for val in hexa:
                if val != var_index and assignment[val] == str(value):
                    return False
    return True

# ........................

def backtracking_search(input, csp_table):
    return recursive_backtracking(input, csp_table)


def recursive_backtracking(assignment, csp_table):
    if check_complete(assignment, csp_table):
        return assignment
    triangle = select_unassigned_var(assignment, csp_table)
    for val in range(1, 7):
        if isValid(val, triangle, assignment, csp_table):
            assignment = assignment[:triangle] + str(val) + assignment[triangle + 1:]
            result = recursive_backtracking(assignment, csp_table)
            if result is not None:
                return result
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
    csp_table = [[0, 1, 2, 6, 7, 8], [2, 3, 4, 8, 9, 10], [5, 6, 7, 12, 13, 14], [7, 8, 9, 14, 15, 16],
                 [9, 10, 11, 16, 17, 18], [13, 14, 15, 19, 20, 21], [15, 16, 17, 21, 22, 23]]
    solution = backtracking_search(input("24-char(. and 1-6) input: "), csp_table)
    if solution != None:
        print(display(solution))
        print('\n' + solution)
        print(check_complete(solution, csp_table))
    else:
        print("It's not solvable.")


if __name__ == '__main__':
    main()
