# Author: Richard Zhan (class of 2020), Jan 2019
# Modified by N.Kim on Jan 2020

# This is a driver (client program) for testing purpose. Do not submit this.

import sys
import os
import time
import tkinter as tk

# Change the following line
from othello import RandomBot, Best_AI_bot, Minimax_AI_bot, Worst_AI_bot


# constants
delay_time = 0
turn_off_printing = False
tile_size = 50
padding = 5
x_max = 8
y_max = 8
board_x = x_max*tile_size+(x_max+1)*padding-2
board_y = y_max*tile_size+(y_max+1)*padding-2
white = "#ffffff"
black = "#000000"
grey = "#505050"
green = "#00ff00"
yellow = "#ffff00"
brown = "#654321"
blue = "#0000ff"
cyan = "#00ffff"
asterisk = " "+u'\u2217'
directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
opposite_color = {black: white, white: black}

# variables
player_types = {0: "Player", 1: "Random", 2: "Minimax AI", 3: "Worst AI", 4: "Best AI"}
players = {black: None, white: None, None: None}
player_max_times = {black: 0, white: 0}
player_total_times = {black: 0, white: 0}
p1_name = ""
p2_name = ""
root = None
canvas = None
turn = white
board = []
score1_str = None
score2_str = None
score1 = 2
score2 = 2
possible_moves = {}
# commands


def whose_turn(my_board, prev_turn):
    global possible_moves
    cur_turn = opposite_color[prev_turn]
    possible_moves = find_moves(my_board, cur_turn)
    if len(possible_moves) > 0:
        return cur_turn
    possible_moves = find_moves(my_board, prev_turn)
    if len(possible_moves) > 0:
        return prev_turn
    return None


def find_flipped(my_board, x, y, my_color):
    if my_board[x][y] != ".":
        return []
    if my_color == black:
        my_color = "@"
    else:
        my_color = "O"
    flipped_stones = []
    for incr in directions:
        temp_flip = []
        x_pos = x + incr[0]
        y_pos = y + incr[1]
        while 0 <= x_pos < x_max and 0 <= y_pos < y_max:
            if my_board[x_pos][y_pos] == ".":
                break
            if my_board[x_pos][y_pos] == my_color:
                flipped_stones += temp_flip
                break
            temp_flip.append([x_pos, y_pos])
            x_pos += incr[0]
            y_pos += incr[1]
    return flipped_stones


def find_moves(my_board, my_color):
    moves_found = {}
    for i in range(len(my_board)):
        for j in range(len(my_board[i])):
            flipped_stones = find_flipped(my_board, i, j, my_color)
            if len(flipped_stones) > 0:
                moves_found.update({i*y_max+j: flipped_stones})
    return moves_found


def print_board(my_board):
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


def draw_rect(x_pos, y_pos, possible=False):
    coord = [x_pos*(padding+tile_size)+padding+1, y_pos*(padding+tile_size)+padding+1,
             (x_pos+1)*(padding+tile_size), (y_pos+1)*(padding+tile_size)]
    if possible:
        canvas.create_rectangle(coord, fill=cyan, activefill=yellow)
    else:
        canvas.create_rectangle(coord, fill=green)


def draw_circle(x_pos, y_pos, fill_color):
    coord = [x_pos*(padding+tile_size)+2*padding+1, y_pos*(padding+tile_size)+2*padding+1,
             (x_pos+1)*(padding+tile_size)-padding, (y_pos+1)*(padding+tile_size)-padding]
    canvas.create_oval(coord, fill=fill_color)


def make_move(x, y):
    if x*y_max+y not in possible_moves.keys():
        return False
    next_turn(x, y)
    return True


def click(event=None):
    x = int((event.x-padding)/(padding+tile_size))
    y = int((event.y-padding)/(padding+tile_size))
    if x*y_max+y not in possible_moves.keys():
        return
    next_turn(x, y)


def next_turn(x_pos, y_pos):
    global turn, possible_moves, score1, score2
    for pos in possible_moves:
        draw_rect(int(pos/y_max), pos % y_max)
    score1 = 0
    score2 = 0
    if turn == black:
        color_symbol = "@"
    else:
        color_symbol = "O"
    board[x_pos][y_pos] = color_symbol
    draw_circle(x_pos, y_pos, turn)
    for pos in possible_moves[x_pos*y_max+y_pos]:
        board[pos[0]][pos[1]] = color_symbol
        draw_circle(pos[0], pos[1], turn)
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == "@":
                score1 += 1
            if board[i][j] == "O":
                score2 += 1
    score1_str.set(p1_name+": "+str(score1))
    score2_str.set(p2_name+": "+str(score2))
    turn = whose_turn(board, turn)
    if turn is None:
        print_board(board)
        print("Black ("+p1_name+") Max Time", player_max_times[black])
        print("White ("+p2_name+") Max Time", player_max_times[white])
        print("Black ("+p1_name+") Total Time", round(player_total_times[black], 3))
        print("White ("+p2_name+") Total Time", round(player_total_times[white], 3))
        if score1 == score2:
            score1_str.set(p1_name+": "+str(score1)+" [Tie!]")
            score2_str.set(p2_name+": "+str(score2)+" [Tie!]")
        if score1 > score2:
            score1_str.set(p1_name+": "+str(score1)+" [Winner!]")
        if score1 < score2:
            score2_str.set(p2_name+": "+str(score2)+" [Winner!]")
        return
    if turn == black:
        score1_str.set(p1_name+": "+str(score1)+asterisk)
    if turn == white:
        score2_str.set(p2_name+": "+str(score2)+asterisk)
    for pos in possible_moves.keys():
        draw_rect(int(pos/y_max), pos % y_max, True)
    print_board(board)
    if players[turn] != "Player":
        root.update()
        time.sleep(delay_time)
        start = time.time()
        move, idc = players[turn].best_strategy(board, turn)
        time_used = round(time.time()-start, 3)
        # print("Time Used:", time_used, end=2*"\n")
        player_max_times[turn] = max(player_max_times[turn], time_used)
        player_total_times[turn] = player_total_times[turn]+time_used
        next_turn(move[0], move[1])


def init(choice_menu, e1, e2, v1, v2):
    global turn_off_printing, turn, root, canvas, score1_str, score2_str, p1_name, p2_name, players, player_types
    if turn_off_printing:
        sys.stdout = open(os.devnull, 'w')
    p1_name = e1.get()
    p2_name = e2.get()
    players[black] = player_types[v1.get()]
    players[white] = player_types[v2.get()]


    p1_name = players[black]
    p2_name = players[white]
    if players[black] == "Random":
        players[black] = RandomBot()
    elif players[black] == "Minimax AI":
        players[black] = Minimax_AI_bot()
    elif players[black] == "Worst AI":
        players[black] = Worst_AI_bot()
    elif players[black] == "Best AI":
        players[black] = Best_AI_bot()
    if players[white] == "Random":
        players[white] = RandomBot()
    elif players[white] == "Minimax AI":
        players[white] = Minimax_AI_bot()
    elif players[white] == "Worst AI":
        players[white] = Worst_AI_bot()
    elif players[white] == "Best AI":
        players[white] = Best_AI_bot()


    choice_menu.destroy()
    root = tk.Tk()
    root.title("Othello Game")
    root.resizable(width=False, height=False)
    canvas = tk.Canvas(root, width=board_x, height=board_y, bg=brown)
    score1_str = tk.StringVar()
    score2_str = tk.StringVar()
    canvas.bind("<Button-1>", click)
    canvas.grid(row=0, column=0, columnspan=2)
    score1_str.set(p1_name+": "+str(score1)+asterisk)
    score2_str.set(p2_name+": "+str(score2))
    tk.Label(textvariable=score1_str, font=("Arial", 20), bg=brown, fg=black).grid(
        row=1, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
    tk.Label(textvariable=score2_str, font=("Arial", 20), bg=brown, fg=white).grid(
        row=1, column=1, sticky=tk.W+tk.E+tk.N+tk.S)
    for i in range(x_max):
        board.append([])
        for j in range(y_max):
            draw_rect(i, j)
            board[i].append(".")
    draw_circle(x_max/2-1, y_max/2-1, white)
    draw_circle(x_max/2, y_max/2, white)
    draw_circle(x_max/2-1, y_max/2, black)
    draw_circle(x_max/2, y_max/2-1, black)
    board[int(x_max/2-1)][int(y_max/2-1)] = "O"
    board[int(x_max/2)][int(y_max/2)] = "O"
    board[int(x_max/2-1)][int(y_max/2)] = "@"
    board[int(x_max/2)][int(y_max/2-1)] = "@"
    turn = whose_turn(board, turn)
    for pos in possible_moves.keys():
        draw_rect(int(pos/y_max), pos % y_max, True)
    print_board(board)
    if players[turn] != "Player":
        root.update()
        time.sleep(delay_time)
        move, idc = players[turn].best_strategy(board, turn)
        next_turn(move[0], move[1])
    root.mainloop()

def menu():
    global p1_name, p2_name, radio_on, radio_off
    choice_menu = tk.Tk()
    choice_menu.title("Menu")
    choice_menu.resizable(width=False, height=False)
    tk.Label(text="Black", font=("Arial", 30), bg=black, fg=grey).grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
    tk.Label(text="White", font=("Arial", 30), bg=white, fg=black).grid(row=0, column=1, sticky=tk.W+tk.E+tk.N+tk.S)
    v1 = tk.IntVar()
    v2 = tk.IntVar()
    v1.set(0)
    v2.set(0)
    tk.Radiobutton(text="Player", compound=tk.LEFT, font=("Arial", 20), bg=black, fg=grey, anchor=tk.W, variable=v1, value=0).grid(row=1, column=0, sticky=tk.W + tk.E + tk.N + tk.S)
    tk.Radiobutton(text="Player", font=("Arial", 20), bg=white, fg=black, anchor=tk.W, variable=v2, value=0).grid(row=1, column=1, sticky=tk.W + tk.E + tk.N + tk.S)
    tk.Radiobutton(text="Random", font=("Arial", 20), bg=black, fg=grey, anchor=tk.W, variable=v1, value=1).grid(row=2, column=0, sticky=tk.W + tk.E + tk.N + tk.S)
    tk.Radiobutton(text="Random", font=("Arial", 20), bg=white, fg=black, anchor=tk.W, variable=v2, value=1).grid(row=2, column=1, sticky=tk.W + tk.E + tk.N + tk.S)
    tk.Radiobutton(text="Minimax AI", font=("Arial", 20), bg=black, fg=grey, anchor=tk.W, variable=v1, value=2).grid(row=3, column=0, sticky=tk.W + tk.E + tk.N + tk.S)
    tk.Radiobutton(text="Minimax AI", font=("Arial", 20), bg=white, fg=black, anchor=tk.W, variable=v2, value=2).grid(row=3, column=1, sticky=tk.W + tk.E + tk.N + tk.S)
    tk.Radiobutton(text="Worst AI", font=("Arial", 20), bg=black, fg=grey, anchor=tk.W, variable=v1, value=3).grid(row=4, column=0, sticky=tk.W + tk.E + tk.N + tk.S)
    tk.Radiobutton(text="Worst AI", font=("Arial", 20), bg=white, fg=black, anchor=tk.W, variable=v2, value=3).grid(row=4, column=1, sticky=tk.W + tk.E + tk.N + tk.S)
    tk.Radiobutton(text="Best AI", font=("Arial", 20), bg=black, fg=grey, anchor=tk.W, variable=v1, value=4).grid(row=5, column=0, sticky=tk.W + tk.E + tk.N + tk.S)
    tk.Radiobutton(text="Best AI", font=("Arial", 20), bg=white, fg=black, anchor=tk.W, variable=v2, value=4).grid(row=5, column=1, sticky=tk.W + tk.E + tk.N + tk.S)
    e1 = tk.Entry(font=("Arial", 15), bg=black, fg=grey, width=12)
    e2 = tk.Entry(font=("Arial", 15), bg=white, fg=black, width=12)
    e1.insert(0, "Player 1 Name")
    e2.insert(0, "Player 2 Name")
    e1.grid(row=99, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
    e2.grid(row=99, column=1, sticky=tk.W + tk.E + tk.N + tk.S)
    tk.Button(text="Begin", font=("Arial", 15), bg=white, fg=black, command=lambda: init(choice_menu, e1, e2, v1, v2)).grid(row=100, column=0, columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S)
    choice_menu.mainloop()


menu()