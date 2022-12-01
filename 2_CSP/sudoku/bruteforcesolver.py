def check_complete(assignment, csp_table):
    return "." not in assignment


def select_unassigned_var(assignment, variables, csp_table):
    for i in range(len(assignment)):
        if assignment[i] == ".":
            return i


def isValid(value, var_index, assignment, variables, csp_table):
    for lst in csp_table:
        if var_index in lst:
            for i in lst:
                if assignment[i] == value:
                    return False
    return True


def ordered_domain(var_index, assignment, variables, csp_table):
    return []


def update_variables(value, var_index, assignment, variables, csp_table):
    return {}


def backtracking_search(puzzle, variables, csp_table):
    return recursive_backtracking(puzzle, variables, csp_table)


def recursive_backtracking(assignment, variables, csp_table):
    if check_complete(assignment, csp_table):
        return assignment
    square = select_unassigned_var(assignment, variables, csp_table)
    for val in variables[square]:
        if isValid(val, square, assignment, variables, csp_table):
            assignment = assignment[:square] + val + assignment[square + 1:]
            result = recursive_backtracking(assignment, variables, csp_table)
            if result != None:
                return result
            assignment = assignment[:square] + "." + assignment[square + 1:]
    return None


def display(solution):
    result = ""
    for i in range(9):
        for j in range(9):
            result += solution[i * 9 + j] + " "
        result += "\n"
    return result


def sudoku_csp():
    lst = []
    for i in range(9):
        lst.append([i * 9 + j for j in range(9)])
    for i in range(9):
        lst.append([i + j * 9 for j in range(9)])
    for i in range(3):
        for j in range(3):
            lst.append([i * 27 + j * 3 + k * 9 + l for k in range(3) for l in range(3)])
    return lst


def initial_variables(puzzle, csp_table):
    variables = {}
    for i in range(81):
        if puzzle[i] == ".":
            variables[i] = set("123456789")
        else:
            variables[i] = set(puzzle[i])
    return variables


def main():
    puzzle = input("Type a 81-char string:")
    while len(puzzle) != 81:
        print("Invalid puzzle")
        puzzle = input("Type a 81-char string: ")
    csp_table = sudoku_csp()
    variables = initial_variables(puzzle, csp_table)
    print("Initial:\n" + display(puzzle))
    solution = backtracking_search(puzzle, variables, csp_table)
    if solution != None:
        print("solution\n" + display(solution))
    else:
        print("No solution found.\n")


if __name__ == '__main__': main()