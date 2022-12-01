import sys; args = sys.argv[1:]
puzzles = open(args[0]).read().splitlines()

import time


def check_complete(assignment, csp_table):
    return "." not in assignment
    # for i in range(len(assignment)):
    #     if assignment[i] == ".":
    #         return False
    #     for j in csp_table[i]:
    #         if assignment[i] == assignment[j]:
    #             return False
    # return True


def select_unassigned_var(assignment, variables, csp_table):  # Minimum Remaining Value
    # for i in range(len(assignment)):
    #     if assignment[i] == ".":
    #         return i
    # return None
    index, min_value = None, 10
    for i in range(81):
        if assignment[i] == ".":
            length = len(variables[i])
            if min_value > length:
                index = i
                min_value = length
    if index is not None:
        return index, ordered_domain(index, assignment, variables, csp_table)


def isValid(value, var_index, assignment, csp_table):
    for i in csp_table[var_index]:
        if assignment[i] == value:
            return False
    return True


def ordered_domain(var_index, assignment, variables, csp_table):
    order = sorted(variables[var_index], reverse=False, key=lambda x: assignment.count(x))
    # print(variables[var_index])
    # print(order)
    return order


def count_appearances(assignment, variables, csp_table):
    modified_overall = False
    for i in range(81):
        if assignment[i] == ".":
            for val in variables[i]:
                modified, assignment = count_appearance_row(i, val, assignment, variables)
                if modified:
                    update_variables(val, i, assignment, variables, csp_table)
                    modified_overall = True
                    break
                modified, assignment = count_appearance_col(i, val, assignment, variables)
                if modified:
                    update_variables(val, i, assignment, variables, csp_table)
                    modified_overall = True
                    break
                modified, assignment = count_appearance_block(i, val, assignment, variables)
                if modified:
                    update_variables(val, i, assignment, variables, csp_table)
                    modified_overall = True
                    break
    return modified_overall, assignment


def count_appearance_row(val_index, val, assignment, variables):
    modified = False
    count = 0
    for i in range(9):
        if count != 0:
            break
        constraint = val_index // 9 * 9 + i
        if assignment[constraint] == "." and val_index % 9 != i:
            for cons_val in variables[constraint]:
                if val == cons_val:
                    count += 1
                    break
    if count == 0:
        assignment = assignment[:val_index] + val + assignment[val_index + 1:]
        modified = True
    return modified, assignment


def count_appearance_col(val_index, val, assignment, variables):
    modified = False
    count = 0
    for i in range(9):
        if count != 0:
            break
        constraint = i * 9 + val_index % 9
        if assignment[constraint] == "." and val_index // 9 != i:
            for cons_val in variables[constraint]:
                if val == cons_val:
                    count += 1
                    break
    if count == 0:
        assignment = assignment[:val_index] + val + assignment[val_index + 1:]
        modified = True
    return modified, assignment


def count_appearance_block(val_index, val, assignment, variables):
    modified = False
    count = 0
    for i in range(3):
        if count != 0:
            break
        for j in range(3):
            if count != 0:
                break
            constraint = (val_index // 27 * 3 + i) * 9 + val_index % 9 // 3 * 3 + j
            if assignment[constraint] == "." and val_index != constraint:
                for cons_val in variables[constraint]:
                    if val == cons_val:
                        count += 1
                        break
    if count == 0:
        assignment = assignment[:val_index] + val + assignment[val_index + 1:]
        modified = True
    return modified, assignment


def update_variables(value, var_index, assignment, variables, csp_table):
    for i in csp_table[var_index]:
        if assignment[i] == "." and value in variables[i]:
            variables[i].remove(value)


def add_variables(value, var_index, assignment, variables, csp_table):
    for i in csp_table[var_index]:
        if assignment[i] == "." and value not in variables[i]:
            variables[i].add(value)


def backtracking_search(puzzle, variables, csp_table):
    return recursive_backtracking(puzzle, variables, csp_table)


def recursive_backtracking(assignment, variables, csp_table):
    # assignment = initial_assignment(assignment, variables, csp_table)
    # assignment = count_appearances(assignment, variables, csp_table)[1]
    if check_complete(assignment, csp_table):
        return assignment
    square, domain = select_unassigned_var(assignment, variables, csp_table)
    while len(domain) != 1:
        modified, assignment = count_appearances(assignment, variables, csp_table)
        if not modified:
            break
        if check_complete(assignment, csp_table):
            return assignment
        square, domain = select_unassigned_var(assignment, variables, csp_table)
    for val in domain:
        # if isValid(val, square, assignment, csp_table):
        assignment = assignment[:square] + val + assignment[square + 1:]
        tempvars = {k: v.copy() for k, v in variables.items()}
        update_variables(val, square, assignment, tempvars, csp_table)
        result = recursive_backtracking(assignment, tempvars, csp_table)
        if result is not None:
            return result
        assignment = assignment[:square] + "." + assignment[square + 1:]
            # add_variables(val, square, assignment, variables, csp_table)
    return None


def display(solution):
    result = "-------------------------"
    for i in range(81):
        if i % 27 == 0:
            result += "\n\n"
            result += solution[i]
        elif i % 9 == 0:
            result += "\n"
            result += solution[i]
        elif i % 3 == 0:
            result += "\t" + solution[i]
        else:
            result += " " + solution[i]
    return result + "\n-------------------------\n"


def sudoku_csp():
    csp_table = {}
    for i in range(81):
        csp_table[i] = set()
    for i in range(81):
        for j in range(81):
            if i != j:
                if i // 9 == j // 9 or i % 9 == j % 9 or (i // 27 == j // 27 and i % 9 // 3 == j % 9 // 3):
                    csp_table[i].add(j)
    return csp_table


def initial_variables(assignment, csp_table):
    nums = set(str(x + 1) for x in range(9))
    variables = {}
    for x in range(0, 81):
        if assignment[x] == '.':
            variables[x] = set(nums - set(assignment[a] for a in csp_table[x]))
        else:
            variables[x] = set(assignment[x])
    return variables


def initial_assignment(assignment, variables, csp_table):
    result = count_appearances(assignment, variables, csp_table)
    while result[0]:
        assignment = result[1]
        result = count_appearances(assignment, variables, csp_table)
    return assignment


def checksum(solution):
    return 324


def main():
    initial_time = time.time()
    csp_table = sudoku_csp()
    for line, puzzle in enumerate(puzzles):
        line, puzzle = line + 1, puzzle.rstrip()
        print("{}: {}".format(line, puzzle))
        variables = initial_variables(puzzle, csp_table)
        puzzle = initial_assignment(puzzle, variables, csp_table)
        solution = backtracking_search(puzzle, variables, csp_table)
        if solution is None: print("No solution found."); break
        print("{}{} {}".format(" " * (len(str(line)) + 2), solution, checksum(solution)))
    print(time.time() - initial_time)

    # puzzle = input("Type a 81-char string:")
    # while len(puzzle) != 81:
    #     print("Invalid puzzle")
    #     puzzle = input("Type a 81-char string: ")
    # csp_table = sudoku_csp()
    # variables = initial_variables(puzzle, csp_table)
    # print("Initial:\n" + display(puzzle))
    # solution = backtracking_search(puzzle, variables, csp_table)
    # if solution is not None:
    #     print("solution\n" + display(solution))
    # else:
    #     print("No solution found.\n")
    #
    # csp_table = sudoku_csp()
    # puzzle = "52...6.........7.13...........4..8..6......5...........418.........3..2...87....."
    # variables = initial_variables(puzzle, csp_table)
    # assignment = initial_assignment(puzzle, variables, csp_table)
    # solution = backtracking_search(assignment, variables, csp_table)
    # print("WOWOWOWOWOWO LOOK\n" + display(solution))

    # with open("puzzles.txt") as f:
    #     puzzles = f.readlines()
    # csp_table = sudoku_csp()
    # initial_time = time.time()
    # for num, p in enumerate(puzzles):
    #     # if num == 26:
    #     #     break
    #     puzzle = p.strip()
    #     variables = initial_variables(puzzle, csp_table)
    #     assignment = initial_assignment(puzzle, variables, csp_table)
    #     # print(f"Puzzle #{num+1}:\n" + display(puzzle))
    #     solution = backtracking_search(assignment, variables, csp_table)
    #     if solution is not None:
    #         print(f"Solution #{num+1} completed!\n" + display(solution))
    #     else:
    #         print("You suck.\n")
    # print(f"Time: {time.time() - initial_time}")


if __name__ == '__main__': main()

# Karthik Thyagarajan, Period 5, 2024