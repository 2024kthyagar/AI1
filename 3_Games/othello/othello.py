import random
import time


class RandomBot:
    def __init__(self):
        self.white = "O"
        self.black = "@"
        self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.opposite_color = {self.black: self.white, self.white: self.black}
        self.x_max = 8
        self.y_max = 8

    def best_strategy(self, board, color):
        # returns best move
        self.x_max = len(board)
        self.y_max = len(board[0])
        if color == "#000000":
            color = "@"
        else:
            color = "O"

        ''' Your code goes here '''
        best_move = random.choice(list(self.find_moves(board, color).keys()))
        return best_move, 0

    def stones_left(self, board):
        return sum(row.count(".") for row in board)

    def find_moves(self, board, color):
        moves_found = {}
        for i in range(len(board)):
            for j in range(len(board[i])):
                flipped_stones = self.find_flipped(board, i, j, color)
                if len(flipped_stones) > 0:
                    moves_found.update({(i, j): flipped_stones})
        return moves_found

    def find_flipped(self, board, x, y, color):
        if board[x][y] != ".":
            return []
        if color == self.black:
            color = "@"
        else:
            color = "O"
        flipped_stones = []
        for incr in self.directions:
            temp_flip = []
            x_pos = x + incr[0]
            y_pos = y + incr[1]
            while 0 <= x_pos < self.x_max and 0 <= y_pos < self.y_max:
                if board[x_pos][y_pos] == ".":
                    break
                if board[x_pos][y_pos] == color:
                    flipped_stones += temp_flip
                    break
                temp_flip.append((x_pos, y_pos))
                x_pos += incr[0]
                y_pos += incr[1]
        return flipped_stones


class Minimax_AI_bot:
    def __init__(self):
        self.white = "O"
        self.black = "@"
        self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.opposite_color = {self.black: self.white, self.white: self.black}
        self.x_max = None
        self.y_max = None

    def best_strategy(self, board, color):
        # returns best move
        self.x_max = len(board)
        self.y_max = len(board[0])
        if color == "#000000":
            color = "@"
        else:
            color = "O"
        return self.minimax(board, color, 3)

    def minimax(self, board, color, search_depth):
        best_value = -999999
        best_move = (-1, -1)
        for move, flipped in self.find_moves(board, color).items():
            new_board = self.make_move(board, color, move, flipped)
            value = self.minimize(new_board, self.opposite_color[color], search_depth - 1)
            if value > best_value:
                best_value = value
                best_move = move
        return best_move, best_value

    def maximize(self, board, color, search_depth):
        moves = self.find_moves(board, color)
        if search_depth == 0 or len(moves) == 0:
            return self.evaluate(board, color, self.find_moves(board, color))
        best_value = -999999
        for move, flipped in moves.items():
            new_board = self.make_move(board, color, move, flipped)
            value = self.minimize(new_board, self.opposite_color[color], search_depth - 1)
            if value > best_value:
                best_value = value
        return best_value

    def minimize(self, board, color, search_depth):
        moves = self.find_moves(board, color)
        if search_depth == 0 or len(moves) == 0:
            return self.evaluate(board, self.opposite_color[color], self.find_moves(board, self.opposite_color[color]))
        best_value = 999999
        for move, flipped in moves.items():
            new_board = self.make_move(board, color, move, flipped)
            value = self.maximize(new_board, self.opposite_color[color], search_depth - 1)
            if value < best_value:
                best_value = value
        return best_value

    def make_key(self, board, color):
        # hashes the board
        return 1

    def stones_left(self, board):
        return sum(row.count(".") for row in board)

    def make_move(self, board, color, move, flipped):
        new_board = [row[:] for row in board]
        new_board[move[0]][move[1]] = color
        for stone in flipped:
            new_board[stone[0]][stone[1]] = color
        return new_board

    def evaluate(self, board, color, possible_moves):
        # returns the utility value
        if self.stones_left(board) == 0:
            return (self.score(board, color) - self.score(board, self.opposite_color[color])) * 1000
        corners = [board[0][0], board[0][self.y_max - 1], board[self.x_max - 1][0],
                   board[self.x_max - 1][self.y_max - 1]]
        filled_corners = (corners.count(color) - (2 * corners.count(self.opposite_color[color]))) * 25
        return len(possible_moves) - (2 * len(self.find_moves(board, self.opposite_color[color]))) + filled_corners

    def score(self, board, color):
        return sum(row.count(color) for row in board)

    def find_moves(self, board, color):
        moves_found = {}
        for i in range(len(board)):
            for j in range(len(board[i])):
                flipped_stones = self.find_flipped(board, i, j, color)
                if len(flipped_stones) > 0:
                    moves_found.update({(i, j): flipped_stones})
        return moves_found

    def find_flipped(self, board, x, y, color):
        if board[x][y] != ".":
            return []
        if color == self.black:
            color = "@"
        else:
            color = "O"
        flipped_stones = []
        for incr in self.directions:
            temp_flip = []
            x_pos = x + incr[0]
            y_pos = y + incr[1]
            while 0 <= x_pos < self.x_max and 0 <= y_pos < self.y_max:
                if board[x_pos][y_pos] == ".":
                    break
                if board[x_pos][y_pos] == color:
                    flipped_stones += temp_flip
                    break
                temp_flip.append((x_pos, y_pos))
                x_pos += incr[0]
                y_pos += incr[1]
        return flipped_stones


class Best_AI_bot:

    def __init__(self):
        self.white = "O"
        self.black = "@"
        self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.stability_directions = [[-1, -1], [-1, 0], [-1, 1], [0, 1]]
        self.opposite_color = {self.black: self.white, self.white: self.black}
        self.x_max = 8
        self.y_max = 8
        self.history_table = {}
        self.zTable = [[[random.randint(1, 2 ** 32 - 1) for i in range(2)] for j in range(self.y_max)] for k in
                       range(self.x_max)]
        self.transposition_table = {}
        self.spiral = [0, 1, 2, 3, 4, 5, 6, 7, 15, 23, 31, 39, 47, 55, 63, 62, 61, 60, 59, 58, 57, 56, 48, 40, 32, 24,
                       16, 8,
                       9, 10, 11, 12, 13, 14, 22, 30, 38, 46, 54, 53, 52, 51, 50, 49, 41, 33, 25, 17, 18, 19, 20, 21,
                       29, 37,
                       45, 44, 43, 42, 34, 26, 27, 28, 36, 35]

        self.min_mobility = 0
        self.max_mobility = 0
        self.min_corners = 0
        self.max_corners = 0
        self.min_stability = 0
        self.max_stability = 0

        self.corners_weight = 0
        self.mobility_weight = 0
        self.stability_weight = 0
        self.coin_weight = 0

        self.conv_weights = [5, 6, 5, 5, 2, 3, 3, 5, 4, 3, 3, 3, 1]
        self.conv_functions = [self.conv1, self.conv2, self.conv3, self.conv4, self.conv5, self.conv6, self.conv7,
                               self.conv8, self.conv9, self.conv10, self.conv11, self.conv12, self.conv13]

    def best_strategy(self, board, color):
        # returns best move
        if color == "#000000":
            color = "@"
        else:
            color = "O"
        start_time = time.time()
        best_move, best_val = None, 0
        time_for_move = 2.5  # seconds
        if self.stones_left(board) <= 10:
            print(f'Endgame: depth = {self.stones_left(board)}')
            search_depth = self.stones_left(board)
        else:
            search_depth = 10

        for depth in range(1, search_depth + 1):
            temp_best_move, temp_best_val = self.negascout(board, color, depth, -999999999999, 999999999999, start_time,
                                                           time_for_move)
            if time.time() - start_time > time_for_move:
                break
            else:
                best_move, best_val = temp_best_move, temp_best_val
            print("Depth: " + str(depth) + " Best move: " + str(best_move) + " Best value: " + str(best_val))
            print("Time: " + str(time.time() - start_time))
        print(
            f'Minimum mobility: {self.min_mobility}, Maximum mobility: {self.max_mobility}, Minimum corners: {self.min_corners}, Maximum corners: {self.max_corners}, Minimum stability: {self.min_stability}, Maximum stability: {self.max_stability}')

        return best_move, best_val

    def minimax(self, board, color, search_depth):
        # returns best "value"
        return 1

    def negamax(self, board, color, search_depth):
        # returns best "value"
        return 1

    def alphabeta(self, board, color, search_depth):
        for b in self.history_table.keys():
            self.history_table[b] /= 2
        return self.nega_alphabeta(board, color, search_depth, -9999999999999, 9999999999999)

    def nega_alphabeta(self, board, color, search_depth, alpha, beta):
        if search_depth == 0 or self.stones_left(board) == 0:
            return None, self.evaluate(board, color, self.find_moves(board, color))
        best_value = -999999999999
        best_move = None
        best_board_key = None

        moves = self.find_moves(board, color)
        new_boards = {self.make_key(b := self.make_move(board, color, move, flipped)): (move, b) for
                      move, flipped in
                      moves.items()}

        new_boards = {k: v for k, v in sorted(new_boards.items(), key=lambda x: self.history_table[
            x[0]] if x[0] in self.history_table else -999999999999, reverse=True)}
        for new_board_key, (move, new_board) in new_boards.items():
            if new_board_key in self.transposition_table and self.transposition_table[new_board_key][1] >= search_depth:
                value = self.transposition_table[new_board_key][0]
            else:
                value = -1 * (
                    self.nega_alphabeta(new_board, self.opposite_color[color], search_depth - 1, -beta, -alpha)[1])
                self.transposition_table[new_board_key] = (value, search_depth)
            if value > best_value:
                best_value = value
                best_move = move
                best_board_key = new_board_key
            alpha = max(alpha, best_value)
            if alpha >= beta:
                self.history_table[best_board_key] = self.history_table[
                                                         best_board_key] + 2 ** search_depth if best_board_key in self.history_table else 2 ** search_depth
                return best_move, best_value
        if best_move is None:
            if len(moves) > 0:
                return random.choice(list(moves.keys())), 0
            else:
                return None, 0
        self.history_table[best_board_key] = self.history_table[
                                                 best_board_key] + 2 ** search_depth if best_board_key in self.history_table else 2 ** search_depth
        return best_move, best_value

    def negascout(self, board, color, search_depth, alpha, beta, start_time, time_for_move):
        for b in self.history_table.keys():
            self.history_table[b] /= 2
        return self.negascout_recursive(board, color, search_depth, alpha, beta, start_time,
                                        time_for_move)

    def negascout_recursive(self, board, color, search_depth, alpha, beta, start_time, time_for_move):
        moves = self.find_moves(board, color)
        if search_depth == 0 or self.stones_left(board) == 0 or len(
                moves) == 0 or time.time() - start_time > time_for_move:
            evaluation = self.evaluate(board, color)
            if evaluation <= alpha:
                self.transposition_table[self.make_key(board)] = (search_depth, None, eval, 1)  # lower bound
            elif evaluation >= beta:
                self.transposition_table[self.make_key(board)] = (search_depth, None, eval, 2)  # upper bound
            else:
                self.transposition_table[self.make_key(board)] = (search_depth, None, eval, 0)  # exact value
            return None, evaluation
        best_value = -999999999999
        best_move = None
        best_board_key = None

        tt_key = self.make_key(board)
        if tt_key in self.transposition_table:
            tt_entry = self.transposition_table[tt_key]  # (depth, move, value, flag)
            if tt_entry[0] >= search_depth:
                if tt_entry[2] == 0:  # exact value
                    return tt_entry[1], tt_entry[0]
                elif tt_entry[2] == 1:  # lower bound
                    alpha = max(alpha, tt_entry[3])
                elif tt_entry[2] == 2:  # upper bound
                    beta = min(beta, tt_entry[3])
                if alpha >= beta:  # cutoff
                    return tt_entry[1], tt_entry[0]

        n = beta

        new_boards = {self.make_key(b := self.make_move(board, color, move, flipped)): (move, b) for
                      move, flipped in
                      moves.items()}
        new_boards = {k: v for k, v in sorted(new_boards.items(), key=lambda x: self.history_table[
            x[0]] if x[0] in self.history_table else -999999999999, reverse=True)}
        for new_board_key, (move, new_board) in new_boards.items():
            value = -1 * (
                self.negascout_recursive(new_board, self.opposite_color[color], search_depth - 1, -beta, -alpha,
                                         start_time, time_for_move)[1])

            if value > best_value:
                if n == beta or search_depth <= 2:
                    best_value = value
                else:
                    best_value = -1 * (
                        self.negascout_recursive(new_board, self.opposite_color[color], search_depth - 1, -beta,
                                                 -value, start_time, time_for_move)[1])
                best_move = move
                best_board_key = new_board_key

            alpha = max(alpha, best_value)
            if alpha >= beta:
                self.history_table[best_board_key] = self.history_table[
                                                         best_board_key] + 2 ** search_depth if best_board_key in self.history_table else 2 ** search_depth
                return best_move, best_value
            n = alpha + 1

        if best_move is None:
            if len(moves) > 0:
                return random.choice(list(moves.keys())), 0
            else:
                return None, 0

        self.history_table[best_board_key] = self.history_table[
                                                 best_board_key] + 2 ** search_depth if best_board_key in self.history_table else 2 ** search_depth
        if best_value <= alpha:
            self.transposition_table[tt_key] = (search_depth, best_move, best_value, 1)  # lower bound
        elif best_value >= beta:
            self.transposition_table[tt_key] = (search_depth, best_move, best_value, 2)  # upper bound
        else:
            self.transposition_table[tt_key] = (search_depth, best_move, best_value, 0)  # exact value
        return best_move, best_value

    def make_key(self, board):
        # hashes the board
        hash = 0
        for i in range(self.x_max):
            for j in range(self.y_max):
                if p := board[i][j] != '.':
                    piece = 0 if p == self.white else 1
                    hash ^= self.zTable[i][j][piece]
        return hash

    def stones_left(self, board):
        return sum(row.count(".") for row in board)

    def make_move(self, board, color, move, flipped):
        new_board = [row[:] for row in board]
        new_board[move[0]][move[1]] = color
        for stone in flipped:
            new_board[stone[0]][stone[1]] = color
        return new_board

    def update_weights(self, mobility_weight, stability_weight, corners_weight, coin_weight):
        self.mobility_weight = mobility_weight
        self.stability_weight = stability_weight
        self.corners_weight = corners_weight
        self.coin_weight = coin_weight


    def potential_mobility(self, board, color):
        coins_to_check = 4
        potential = 0
        for row in range(self.x_max):
            if coins_to_check == 0:
                break
            for col in range(self.y_max):
                if coins_to_check == 0:
                    break
                if board[row][col] == self.opposite_color[color]:
                    border = []
                    coins_to_check -= 1
                    for v in range(row - 1, row + 1):
                        for h in range(col - 1, col + 1):
                            border.append((v, h))
                    potential += sum(board[i[0]][i[1]] == '.' for i in border)
        return potential

    def next_to_danger_squares(self, board, color):
        score = 0
        next_to_danger_squares = [2, 10, 18, 17, 16, 40, 41, 42, 50, 58, 61, 53, 45, 46, 47, 23, 22, 21, 13, 5]
        for i in next_to_danger_squares:
            if board[i // 8][i % 8] == color:
                score += 1

    def corner_heuristic(self, board, color, possible_moves, corners):
        captured = sum(board[i[0]][i[1]] == color for i in corners)
        potential_corners = len([val for val in corners if val in possible_moves])
        unlikely_corners = 4 - captured - potential_corners
        return 5 * captured + 0.5 * potential_corners - 2 * unlikely_corners

    def stability_heuristic(self, board, color, opposite_moves):
        unstable_coins = []
        for move in opposite_moves:
            for flipped_coin in self.find_flipped(board, move[0], move[1], color):
                if flipped_coin not in unstable_coins:
                    unstable_coins.append(flipped_coin[0] * 8 + flipped_coin[1])

        stable_coins = []
        stables = [0, 1, 6, 7, 8, 15, 48, 55, 56, 57, 62, 63]
        for stable in stables:
            if board[stable // 8][stable % 8] == color:
                stable_coins.append(stable)

        if len(stable_coins) > 0:
            all_stable = True
            for i in self.spiral:
                if (i-8) % 9 == 0 and not all_stable:
                    break
                if i not in unstable_coins:
                    if board[i // 8][i % 8] == color:
                        stable = self.is_stable(board, i, color, stable_coins)
                        if stable:
                            stable_coins.append(i)
                        else:
                            all_stable = False
        stable_num = len(stable_coins)
        unstable_num = len(unstable_coins)
        semi_stable_num = self.score(board, color) - stable_num - unstable_num
        return (stable_num * 10 + semi_stable_num * 3 - unstable_num * 4) / 9

    def is_stable(self, board, i, color, stable_coins):
        stable = True
        for direction in self.stability_directions:
            if not stable:
                break
            if 0 < i // 8 + direction[0] < self.x_max and 0 < i % 8 + direction[1] < self.y_max:
                if board[i // 8 + direction[0]][i % 8 + direction[1]] == color and i + 8 * \
                        direction[0] + direction[1] in stable_coins:
                    continue
            if 0 < i // 8 - direction[0] < self.x_max and 0 < i % 8 - direction[1] < self.y_max:
                if board[i // 8 - direction[0]][i % 8 - direction[1]] == color and i - 8 * \
                        direction[0] - direction[1] in stable_coins:
                    continue
            for distance in range(self.x_max):
                x = i // 8 + distance * direction[0]
                y = i % 8 + distance * direction[1]
                if 0 <= x < self.x_max and 0 <= y < self.y_max:
                    if board[x][y] == '.':
                        stable = False
                        break
                else:
                    break
                x = i // 8 - distance * direction[0]
                y = i % 8 - distance * direction[1]
                if 0 <= x < self.x_max and 0 <= y < self.y_max:
                    if board[x][y] == '.':
                        stable = False
                        break
                else:
                    break
        return stable

    def evaluate(self, board, color):
        # returns the utility value
        possible_moves = self.find_moves(board, color)
        opponent_moves = self.find_moves(board, self.opposite_color[color])
        stones = self.stones_left(board)
        if stones == 0 or (len(possible_moves) == 0 and len(opponent_moves) == 0):
            s = self.score(board, color)
            o = self.score(board, self.opposite_color[color])
            return 1000 * (s - o)

        if a := (len(possible_moves) + len(opponent_moves)) != 0:
            actual_mobility = (len(possible_moves) - len(opponent_moves)) / a
        else:
            actual_mobility = 0
        #
        # potential = self.potential_mobility(board, color)
        # opponent_potential = self.potential_mobility(board, self.opposite_color[color])
        # if p := (potential + opponent_potential) != 0:
        #     potential_mobility = (potential - opponent_potential) / p
        # else:
        #     potential_mobility = 0

        # mobility_val = (4*actual_mobility + potential_mobility)/2.5
        mobility_val = actual_mobility*2

        # mobility_val = (mobility_val+5000)/10000
        corners = [(0, 0), (0, self.y_max - 1), (self.x_max - 1, 0),
                   (self.x_max - 1, self.y_max - 1)]
        my_corners = self.corner_heuristic(board, color, possible_moves, corners)
        opponent_corners = self.corner_heuristic(board, self.opposite_color[color], opponent_moves, corners)
        if c := (my_corners + opponent_corners) != 0:
            corner_val = (my_corners - opponent_corners) / c
        else:
            corner_val = 0

        # corner_val = (corner_val + 2500) / 5000

        stability = self.stability_heuristic(board, color, opponent_moves)
        opponent_stability = self.stability_heuristic(board, self.opposite_color[color], possible_moves)
        if s := (stability + opponent_stability) != 0:
            stability_val = (stability - opponent_stability) / s
        else:
            stability_val = 0

        # stability_val = (stability_val + 50000) / 100000

        coins = self.score(board, color)
        opponent_coins = self.score(board, self.opposite_color[color])
        coin_val = (coins - opponent_coins) / (coins + opponent_coins)

        self.min_mobility = min(self.min_mobility, mobility_val)
        self.max_mobility = max(self.max_mobility, mobility_val)
        self.min_corners = min(self.min_corners, corner_val)
        self.max_corners = max(self.max_corners, corner_val)
        self.min_stability = min(self.min_stability, stability_val)
        self.max_stability = max(self.max_stability, stability_val)

        if stones > 50:
            self.update_weights(3, 1, 6, 0)
        elif stones > 40:
            self.update_weights(6, 3, 9, 0)
        elif stones > 30:
            self.update_weights(7, 5, 10, 0)
        elif stones > 20:
            self.update_weights(8, 6, 12, 1)
        elif stones > 10:
            self.update_weights(6, 6, 12, 2)
        else:
            self.update_weights(1, 1, 7, 15)

        return self.corners_weight * corner_val + self.mobility_weight * mobility_val + self.stability_weight * stability_val + self.coin_weight * coin_val

    def score(self, board, color):
        return sum(row.count(color) for row in board)

    def find_moves(self, board, color):
        moves_found = {}
        for i in range(len(board)):
            for j in range(len(board[i])):
                flipped_stones = self.find_flipped(board, i, j, color)
                if len(flipped_stones) > 0:
                    moves_found.update({(i, j): flipped_stones})
        return moves_found

    def find_flipped(self, board, x, y, color):
        if board[x][y] != ".":
            return []
        if color == self.black:
            color = "@"
        else:
            color = "O"
        flipped_stones = []
        for incr in self.directions:
            temp_flip = []
            x_pos = x + incr[0]
            y_pos = y + incr[1]
            while 0 <= x_pos < self.x_max and 0 <= y_pos < self.y_max:
                if board[x_pos][y_pos] == ".":
                    break
                if board[x_pos][y_pos] == color:
                    flipped_stones += temp_flip
                    break
                temp_flip.append((x_pos, y_pos))
                x_pos += incr[0]
                y_pos += incr[1]
        return flipped_stones

    def conv1(self, board, color):
        square1 = [0, 1, 2, 8, 9, 10, 16, 17, 18]
        square2 = [x + 5 for x in square1]
        square3 = [x + 40 for x in square1]
        square4 = [x + 45 for x in square1]
        squares = square1 + square2 + square3 + square4
        score = 0
        for square in squares:
            if board[square // 8][square % 8] == color:
                score += 1
            elif board[square // 8][square % 8] == self.opposite_color[color]:
                score -= 1
        return score

    def conv2(self, board, color):
        square1 = [0, 1, 2, 3, 4, 5, 8, 9, 16, 24, 32]
        square2 = [3, 4, 5, 6, 7, 14, 15, 23, 31, 39, 47]
        square3 = [24, 32, 40, 48, 49, 56, 57, 58, 59, 60]
        square4 = [31, 39, 47, 54, 55, 59, 60, 61, 62, 63]
        squares = square1 + square2 + square3 + square4
        score = 0
        for square in squares:
            if board[square // 8][square % 8] == color:
                score += 1
            elif board[square // 8][square % 8] == self.opposite_color[color]:
                score -= 1
        return score

    def conv3(self, board, color):
        square1 = list(range(8)) + [9, 14]
        square2 = list(range(0, 57, 8)) + [9, 49]
        square3 = list(range(7, 64, 8)) + [14, 54]
        square4 = list(range(56, 64)) + [49, 54]
        squares = square1 + square2 + square3 + square4
        score = 0
        for square in squares:
            if board[square // 8][square % 8] == color:
                score += 1
            elif board[square // 8][square % 8] == self.opposite_color[color]:
                score -= 1
        return score

    def conv4(self, board, color):
        square1 = list(range(2, 6)) + list(range(10, 14)) + [0, 7]
        square2 = list(range(16, 41, 8)) + list(range(17, 41, 8)) + [0, 56]
        square3 = list(range(23, 47, 8)) + list(range(22, 46, 8)) + [7, 63]
        square4 = list(range(50, 54)) + list(range(58, 62)) + [56, 63]
        squares = square1 + square2 + square3 + square4
        score = 0
        for square in squares:
            if board[square // 8][square % 8] == color:
                score += 1
            elif board[square // 8][square % 8] == self.opposite_color[color]:
                score -= 1
        return score

    def conv5(self, board, color):
        square1 = list(range(8, 16))
        square2 = list(range(1, 58, 8))
        square3 = list(range(6, 63, 8))
        square4 = list(range(48, 56))
        squares = square1 + square2 + square3 + square4
        score = 0
        for square in squares:
            if board[square // 8][square % 8] == color:
                score += 1
            elif board[square // 8][square % 8] == self.opposite_color[color]:
                score -= 1
        return score

    def conv6(self, board, color):
        square1 = list(range(16, 24))
        square2 = list(range(40, 48))
        square3 = list(range(2, 59, 8))
        square4 = list(range(5, 62, 8))
        squares = square1 + square2 + square3 + square4
        score = 0
        for square in squares:
            if board[square // 8][square % 8] == color:
                score += 1
            elif board[square // 8][square % 8] == self.opposite_color[color]:
                score -= 1
        return score

    def conv7(self, board, color):
        square1 = list(range(24, 32))
        square2 = list(range(32, 40))
        square3 = list(range(3, 60, 8))
        square4 = list(range(4, 61, 8))
        squares = square1 + square2 + square3 + square4
        score = 0
        for square in squares:
            if board[square // 8][square % 8] == color:
                score += 1
            elif board[square // 8][square % 8] == self.opposite_color[color]:
                score -= 1
        return score

    def conv8(self, board, color):
        square1 = list(range(0, 64, 9))
        square2 = list(range(7, 57, 7))
        squares = square1 + square2
        score = 0
        for square in squares:
            if board[square // 8][square % 8] == color:
                score += 1
            elif board[square // 8][square % 8] == self.opposite_color[color]:
                score -= 1
        return score

    def conv9(self, board, color):
        square1 = list(range(1, 56, 9))
        square2 = list(range(6, 49, 7))
        square3 = list(range(8, 63, 9))
        square4 = list(range(15, 58, 7))
        squares = square1 + square2 + square3 + square4
        score = 0
        for square in squares:
            if board[square // 8][square % 8] == color:
                score += 1
            elif board[square // 8][square % 8] == self.opposite_color[color]:
                score -= 1
        return score

    def conv10(self, board, color):
        square1 = list(range(2, 48, 9))
        square2 = list(range(5, 41, 7))
        square3 = list(range(16, 62, 9))
        square4 = list(range(23, 59, 7))
        squares = square1 + square2 + square3 + square4
        score = 0
        for square in squares:
            if board[square // 8][square % 8] == color:
                score += 1
            elif board[square // 8][square % 8] == self.opposite_color[color]:
                score -= 1
        return score

    def conv11(self, board, color):
        square1 = list(range(3, 40, 9))
        square2 = list(range(4, 33, 7))
        square3 = list(range(24, 61, 9))
        square4 = list(range(31, 60, 7))
        squares = square1 + square2 + square3 + square4
        score = 0
        for square in squares:
            if board[square // 8][square % 8] == color:
                score += 1
            elif board[square // 8][square % 8] == self.opposite_color[color]:
                score -= 1
        return score

    def conv12(self, board, color):
        square1 = list(range(3, 25, 7))
        square2 = list(range(4, 32, 9))
        square3 = list(range(32, 60, 9))
        square4 = list(range(39, 61, 7))
        squares = square1 + square2 + square3 + square4
        score = 0
        for square in squares:
            if board[square // 8][square % 8] == color:
                score += 1
            elif board[square // 8][square % 8] == self.opposite_color[color]:
                score -= 1
        return score

    def conv13(self, board, color):
        squares = list(range(0, 64))
        score = 0
        for square in squares:
            if board[square // 8][square % 8] == color:
                score += 1
            elif board[square // 8][square % 8] == self.opposite_color[color]:
                score -= 1
        return score

    def conv_eval(self, board, color):
        score = 0
        for i in range(13):
            score += self.conv_weights[i] * self.conv_functions[i](board, color)
        return score


class Worst_AI_bot:

    def __init__(self):
        self.white = "O"
        self.black = "@"
        self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.opposite_color = {self.black: self.white, self.white: self.black}
        self.x_max = 8
        self.y_max = 8
        self.history_table = {}
        self.zTable = [[[random.randint(1, 2 ** 32 - 1) for i in range(2)] for j in range(self.y_max)] for k in
                       range(self.x_max)]

    def best_strategy(self, board, color):
        # returns best move
        if color == "#000000":
            color = "@"
        else:
            color = "O"
        start_time = time.time()
        best_move, best_val = None, 0
        time_for_move = 1  # seconds
        for depth in range(6):
            best_move, best_val = self.negascout(board, color, depth, start_time, time_for_move)
        return best_move, best_val

    def minimax(self, board, color, search_depth):
        # returns best "value"
        return 1

    def negamax(self, board, color, search_depth):
        # returns best "value"
        return 1

    def alphabeta(self, board, color, search_depth):
        for b in self.history_table.keys():
            self.history_table[b] /= 2
        return self.nega_alphabeta(board, color, search_depth, -9999999999999, 9999999999999)

    def nega_alphabeta(self, board, color, search_depth, alpha, beta):
        if search_depth == 0 or self.stones_left(board) == 0:
            return None, self.evaluate(board, color, self.find_moves(board, color))
        best_value = -999999999999
        best_move = None
        best_board_key = None

        moves = self.find_moves(board, color)
        new_boards = {self.make_key(b := self.make_move(board, color, move, flipped)): (move, b) for
                      move, flipped in
                      moves.items()}
        new_boards = {k: v for k, v in sorted(new_boards.items(), key=lambda x: self.history_table[
            x[0]] if x[0] in self.history_table else -999999999999, reverse=True)}
        for new_board_key, (move, new_board) in new_boards.items():
            value = -1 * (
                self.nega_alphabeta(new_board, self.opposite_color[color], search_depth - 1, -beta, -alpha)[1])
            if value > best_value:
                best_value = value
                best_move = move
                best_board_key = new_board_key
            alpha = max(alpha, best_value)
            if alpha >= beta:
                self.history_table[best_board_key] = self.history_table[
                                                         best_board_key] + 2 ** search_depth if best_board_key in self.history_table else 2 ** search_depth
                return best_move, best_value
        if best_move is None:
            if len(moves) > 0:
                return random.choice(list(moves.keys())), 0
            else:
                return None, 0
        self.history_table[best_board_key] = self.history_table[
                                                 best_board_key] + 2 ** search_depth if best_board_key in self.history_table else 2 ** search_depth
        return best_move, best_value

    def negascout(self, board, color, search_depth, start_time, time_for_move):
        for b in self.history_table.keys():
            self.history_table[b] /= 2
        return self.negascout_recursive(board, color, search_depth, -9999999999999, 9999999999999, start_time,
                                        time_for_move)

    def negascout_recursive(self, board, color, search_depth, alpha, beta, start_time, time_for_move):
        if search_depth == 0 or self.stones_left(board) == 0:
            return None, self.evaluate(board, self.opposite_color[color],
                                       self.find_moves(board, self.opposite_color[color]))
        best_value = -999999999999
        best_move = None
        best_board_key = None

        n = beta

        moves = self.find_moves(board, color)
        new_boards = {self.make_key(b := self.make_move(board, color, move, flipped)): (move, b) for
                      move, flipped in
                      moves.items()}
        new_boards = {k: v for k, v in sorted(new_boards.items(), key=lambda x: self.history_table[
            x[0]] if x[0] in self.history_table else -999999999999, reverse=True)}
        for new_board_key, (move, new_board) in new_boards.items():
            value = -1 * (
                self.negascout_recursive(new_board, self.opposite_color[color], search_depth - 1, -beta, -alpha,
                                         start_time, time_for_move)[1])

            if value > best_value:
                if n == beta or search_depth <= 2:
                    best_value = value
                else:
                    best_value = -1 * (
                        self.negascout_recursive(new_board, self.opposite_color[color], search_depth - 1, -beta,
                                                 -value, start_time, time_for_move)[1])
                best_move = move
                best_board_key = new_board_key

            alpha = max(alpha, best_value)
            if alpha >= beta or time.time() - start_time > time_for_move:
                self.history_table[best_board_key] = self.history_table[
                                                         best_board_key] + 2 ** search_depth if best_board_key in self.history_table else 2 ** search_depth
                return best_move, best_value
            n = alpha + 1

        if best_move is None:
            if len(moves) > 0:
                return random.choice(list(moves.keys())), 0
            else:
                return None, 0
        self.history_table[best_board_key] = self.history_table[
                                                 best_board_key] + 2 ** search_depth if best_board_key in self.history_table else 2 ** search_depth
        return best_move, best_value

    def make_key(self, board):
        # hashes the board
        hash = 0
        for i in range(self.x_max):
            for j in range(self.y_max):
                if p := board[i][j] != '.':
                    piece = 0 if p == self.white else 1
                    hash ^= self.zTable[i][j][piece]
        return hash

    def stones_left(self, board):
        return sum(row.count(".") for row in board)

    def make_move(self, board, color, move, flipped):
        new_board = [row[:] for row in board]
        new_board[move[0]][move[1]] = color
        for stone in flipped:
            new_board[stone[0]][stone[1]] = color
        return new_board

    def potential_mobility(self, board, color):
        coins_to_check = 3
        potential = 0
        for row in range(self.x_max):
            if coins_to_check == 0:
                break
            for col in range(self.y_max):
                if coins_to_check == 0:
                    break
                if board[row][col] == self.opposite_color[color]:
                    border = []
                    coins_to_check -= 1
                    for v in range(row - 1, row + 1):
                        for h in range(col - 1, col + 1):
                            border.append((v, h))
                    potential += sum(board[i[0]][i[1]] == '.' for i in border)
        return potential

    def corner_heuristic(self, board, color, possible_moves):
        corners = [(0, 0), (0, self.y_max - 1), (self.x_max - 1, 0),
                   (self.x_max - 1, self.y_max - 1)]
        captured = sum(board[i[0]][i[1]] == color for i in corners) * 10
        potential_corners = len([val for val in corners if val in possible_moves]) * 5
        return captured + potential_corners

    def stability_heuristic(self, board, color):
        stable_coins = 0
        for i in range(self.x_max):
            for j in range(self.y_max):
                if board[i][j] == color:
                    stable = True
                    for direction in self.directions:
                        if not stable:
                            break
                        for distance in range(self.x_max):
                            x = i + distance * direction[0]
                            y = j + distance * direction[1]
                            if 0 <= x < self.x_max and 0 <= y < self.y_max:
                                if board[x][y] == self.opposite_color[color]:
                                    break
                                elif board[x][y] == '.':
                                    stable = False
                                    break
                    if stable:
                        stable_coins += 1
        return stable_coins

    def evaluate(self, board, color, possible_moves):
        # returns the utility value
        if self.stones_left(board) == 0:
            s = self.score(board, color)
            o = self.score(board, self.opposite_color[color])
            return 100 * (s - o) / (s + o)

        opponent_moves = self.find_moves(board, self.opposite_color[color])
        if a := (len(possible_moves) + len(opponent_moves)) != 0:
            actual_mobility = 100 * (len(possible_moves) - len(opponent_moves)) / a
        else:
            actual_mobility = 0

        potential = self.potential_mobility(board, color)
        opponent_potential = self.potential_mobility(board, self.opposite_color[color])
        if p := (potential + opponent_potential) != 0:
            potential_mobility = 100 * (potential - opponent_potential) / p
        else:
            potential_mobility = 0

        mobility_val = actual_mobility + potential_mobility

        corners = self.corner_heuristic(board, color, possible_moves)
        opponent_corners = self.corner_heuristic(board, self.opposite_color[color], opponent_moves)
        if c := (corners + opponent_corners) != 0:
            corner_val = 100 * (corners - opponent_corners) / c
        else:
            corner_val = 0

        stability = self.stability_heuristic(board, color)
        opponent_stability = self.stability_heuristic(board, self.opposite_color[color])
        if s := (stability + opponent_stability) != 0:
            stability_val = 100 * (stability - opponent_stability) / s
        else:
            stability_val = 0

        return 30 * corner_val + 15 * mobility_val + 25 * stability_val

    def score(self, board, color):
        return sum(row.count(color) for row in board)

    def find_moves(self, board, color):
        moves_found = {}
        for i in range(len(board)):
            for j in range(len(board[i])):
                flipped_stones = self.find_flipped(board, i, j, color)
                if len(flipped_stones) > 0:
                    moves_found.update({(i, j): flipped_stones})
        return moves_found

    def find_flipped(self, board, x, y, color):
        if board[x][y] != ".":
            return []
        if color == self.black:
            color = "@"
        else:
            color = "O"
        flipped_stones = []
        for incr in self.directions:
            temp_flip = []
            x_pos = x + incr[0]
            y_pos = y + incr[1]
            while 0 <= x_pos < self.x_max and 0 <= y_pos < self.y_max:
                if board[x_pos][y_pos] == ".":
                    break
                if board[x_pos][y_pos] == color:
                    flipped_stones += temp_flip
                    break
                temp_flip.append((x_pos, y_pos))
                x_pos += incr[0]
                y_pos += incr[1]
        return flipped_stones
