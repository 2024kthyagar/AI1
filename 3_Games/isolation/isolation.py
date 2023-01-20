import random


class RandomPlayer:
    def __init__(self):
        self.white = "#ffffff"  # "O"
        self.black = "#000000"  # "X"
        self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.opposite_color = {self.black: self.white, self.white: self.black}
        self.x_max = 5
        self.y_max = 5
        self.first_turn = True

    def best_strategy(self, board, color):
        moves = list(self.find_moves(board, color))
        return random.choice(moves), 0

    def find_moves(self, board, color):  # possible moves
        if self.first_turn:
            self.first_turn = False
            while board[x := random.randint(0, 4)][y := random.randint(0, 4)] != ".":
                continue
            return {(x, y)}
        moves = set()
        for i in range(self.x_max):
            for j in range(self.y_max):
                if board[i][j] == ("X" if color == self.black else "O"):
                    for direction in self.directions:
                        stop = False
                        for dist in range(1, 5):
                            if stop:
                                break
                            x = i + direction[0] * dist
                            y = j + direction[1] * dist
                            if 0 <= x < self.x_max and 0 <= y < self.y_max and board[x][y] == ".":
                                moves.add((x, y))
                            else:
                                stop = True
        return moves


class CustomPlayer:

    def __init__(self):
        self.white = "#ffffff"  # "O"
        self.black = "#000000"  # "X"
        self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.opposite_color = {self.black: self.white, self.white: self.black}
        self.x_max = 5
        self.y_max = 5
        self.first_turn = True
        self.opponent_first_turn = True

    def best_strategy(self, board, color):
        return self.minimax(board, color, 3)

    def minimax(self, board, color, search_depth):
        best_value = -999999
        best_move = (-1, -1)
        # print(board, m:=self.find_moves(board, color))
        for move in self.find_moves(board, color):
            new_board = self.make_move(board, color, move)
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
        for move in moves:
            new_board = self.make_move(board, color, move)
            value = self.minimize(new_board, self.opposite_color[color], search_depth - 1)
            if value > best_value:
                best_value = value
        return best_value

    def minimize(self, board, color, search_depth):
        moves = self.find_moves(board, color)
        if search_depth == 0 or len(moves) == 0:
            return self.evaluate(board, self.opposite_color[color], self.find_moves(board, self.opposite_color[color]))
        best_value = 999999
        for move in moves:
            new_board = self.make_move(board, color, move)
            value = self.maximize(new_board, self.opposite_color[color], search_depth - 1)
            if value < best_value:
                best_value = value
        return best_value

    def megamax(self, board, color, search_depth):
        # returns best "value"
        return 1

    def alphabeta(self, board, color, search_depth, alpha, beta):
        # returns best "value" while also pruning
        pass

    def make_move(self, board, color, move):
        new_board = [list(row) for row in board]
        new_board[move[0]][move[1]] = "X" if color == self.black else "O"
        return new_board

    def evaluate(self, board, color, possible_moves):
        return len(possible_moves) - len(self.find_moves(board, self.opposite_color[color]))

    def find_moves(self, board, color):  # possible moves
        moves = set()

        if self.first_turn:
            self.first_turn = False
            for x in range(self.x_max):
                for y in range(self.y_max):
                    if board[x][y] == ".":
                        moves.add((x, y))
            return moves

        if self.opponent_first_turn:
            self.opponent_first_turn = False
            for x in range(self.x_max):
                for y in range(self.y_max):
                    if board[x][y] == ".":
                        moves.add((x, y))
            return moves

        for i in range(self.x_max):
            for j in range(self.y_max):
                if board[i][j] == ("X" if color == self.black else "O"):
                    for direction in self.directions:
                        stop = False
                        for dist in range(1, 5):
                            if stop:
                                break
                            x = i + direction[0] * dist
                            y = j + direction[1] * dist
                            if 0 <= x < self.x_max and 0 <= y < self.y_max and board[x][y] == ".":
                                moves.add((x, y))
                            else:
                                stop = True
        return moves
