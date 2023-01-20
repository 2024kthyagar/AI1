from othello import Best_AI_bot, Minimax_AI_bot

directions = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
x_max = 8
y_max = 8

best_weights_and_score = ((0,0,0), 15)
update_mobility_weight = 0
update_corner_weight = 0
update_stability_weight = 0



def play_game():
    global best_weights_and_score, update_mobility_weight, update_corner_weight, update_stability_weight

    # Initialize the board and current player.
    board = [['.' for i in range(8)] for j in range(8)]
    board[3][3] = board[4][4] = '@'
    board[3][4] = board[4][3] = 'O'
    p1 = Best_AI_bot()
    p2 = Minimax_AI_bot()
    p1.update_weights(update_mobility_weight, update_corner_weight, update_stability_weight)

    # Play the game.
    while stones_left(board) > 0 and (len(find_moves(board, '@')) > 0 or len(find_moves(board, 'O')) > 0):
        if len(find_moves(board, '@')) > 0:
            move, val = p1.best_strategy(board, '#000000')
            board = make_move(board, '@', move, find_flipped(board, move[0], move[1], '@'))
            print("Black's move: " + str(move))
            print_board(board)
        if len(find_moves(board, 'O')) > 0:
            move, val = p2.best_strategy(board, '#FFFFFF')
            board = make_move(board, 'O', move, find_flipped(board, move[0], move[1], 'O'))
            print("White's move: " + str(move))
            print_board(board)
    print("Game over!")
    print("Score: Black " + str(score(board, '@')) + " White " + str(score(board, 'O')))
    if score(board, '@') > best_weights_and_score[1]:
        best_weights_and_score = ((update_mobility_weight, update_corner_weight, update_stability_weight), score(board, '@'))
        print("New best score: " + str(best_weights_and_score))



def stones_left(board):
    return sum(row.count(".") for row in board)

def make_move(board, color, move, flipped):
    new_board = [row[:] for row in board]
    new_board[move[0]][move[1]] = color
    for stone in flipped:
        new_board[stone[0]][stone[1]] = color
    return new_board

def score(board, color):
    return sum(row.count(color) for row in board)

def find_moves(board, color):
    moves_found = {}
    for i in range(len(board)):
        for j in range(len(board[i])):
            flipped_stones = find_flipped(board, i, j, color)
            if len(flipped_stones) > 0:
                moves_found.update({(i, j): flipped_stones})
    return moves_found

def find_flipped(board, x, y, color):
    global directions, x_max, y_max
    if board[x][y] != ".":
        return []
    flipped_stones = []
    for incr in directions:
        temp_flip = []
        x_pos = x + incr[0]
        y_pos = y + incr[1]
        while 0 <= x_pos < x_max and 0 <= y_pos < y_max:
            if board[x_pos][y_pos] == ".":
                break
            if board[x_pos][y_pos] == color:
                flipped_stones += temp_flip
                break
            temp_flip.append((x_pos, y_pos))
            x_pos += incr[0]
            y_pos += incr[1]
    return flipped_stones

def print_board(my_board):
    global x_max, y_max
    # return  # comment to print board each time
    print("\t", end="")
    for i in range(x_max):
        print(chr(ord("a")+i), end=" ")
    print()
    for i in range(y_max):
        print(i+1, end="\t")
        for j in range(x_max):
            print(my_board[j][i], end=" ")
        print()
    print()

def main():
    global update_mobility_weight, update_corner_weight, update_stability_weight
    for update_mobility_weight in range(5, 10):
        for update_corner_weight in range(2, 10):
            for update_stability_weight in range(4, 10):
                play_game()
    print("Best weights and score: " + str(best_weights_and_score))

if __name__ == "__main__":
    main()