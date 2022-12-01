def select_var(grid):
    for i in range(len(grid)):
        if grid[i] == ".":
            return i


def check_complete(grid):
    for i in range(len(grid)):
        if grid[i] == ".":
            return False
    return True


def isValid(char, index, grid):
    # check row
    rowstart = index // 3 * 3
    for i in range(rowstart, rowstart + 3):
        if i != index and grid[i] == char:
            return False
    # check column
    colstart = index % 3
    for i in range(colstart, len(grid), 3):
        if i != index and grid[i] == char:
            return False
    return True


def solve(line):
    grid = "........."
    linelist = line.split(" ")
    for i in range(1, int(linelist[0]) * 2 + 1, 2):
        grid = grid[:int(linelist[i]) - 1] + linelist[i + 1] + grid[int(linelist[i]):]
    return backtracking(grid)


def backtracking(grid):
    if check_complete(grid):
        return grid
    index = select_var(grid)
    for char in ["A", "B", "C"]:
        if isValid(char, index, grid):
            grid = grid[:index] + char + grid[index + 1:]
            result = backtracking(grid)
            if result is not None:
                return result
            grid = grid[:index] + "." + grid[index + 1:]
    return None


print(solve(input("Enter input: ")))
