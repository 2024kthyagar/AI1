def successors(state, turn):
    return [state[:i] + turn + state[i + 1:] for i, val in enumerate(state) if val == "."]


def get_turn(state):
    return "O" if state.count("O") < state.count("X") else "X"


def conditions_table(n=3, n2=9):
    table = []
    for i in range(n):
        table.append([i * n + j for j in range(n)])
    for i in range(n):
        table.append([i + j * n for j in range(n)])
    table.append([i * n + i for i in range(n)])
    table.append([i * n + n - i - 1 for i in range(n)])
    return table


def display(state, n=3, n2=9):
    result = ""
    for i in range(n):
        for j in range(n):
            result += state[i * n + j] + " "
        result += "\n"
    return result


def terminal_test(state, tc):
    if state.find('.') < 0: return True  # check empty spot
    for li in tc:
        check_li = [state[x] for x in li]
        if len(set(check_li)) == 1 and check_li[0] != '.':
            return True
    return False

def switch_turn(turn):
    return 'O' if turn == 'X' else 'X'


def minimax(state, turn, tc):
    return max_value(state, turn, tc)[1]


def max_value(state, turn, tc):
    if terminal_test(state, tc):
        return utility(turn, tc, state), state
    v = -999999
    for s in successors(state, get_turn(state)):
        small = min_value(s, turn, tc)[0]
        if small > v:
            v = small
            state = s
    return v, state


def min_value(state, turn, tc):
    if terminal_test(state, tc):
        return utility(turn, tc, state), state
    v = 999999

    for s in successors(state, get_turn(state)):
        big = max_value(s, turn, tc)[0]
        if big < v:
            v = big
            state = s
    return v, state


def utility(turn, tc, state):
    x_turn = True if turn == 'X' else False
    for condition in tc:
        if all(state[i] == "X" for i in condition):
            return 1 if x_turn else -1
        if all(state[i] == "O" for i in condition):
            return -1 if x_turn else 1
    return 0


def human_play(s, n, turn):
    index_li = [x for x in range(len(s)) if s[x] == '.']
    for i in index_li:
        print('[%s] (%s, %s)' % (i, i // n, i % n))
    index = int(input("What's your input? (Type a number): "))
    while s[index] != '.':
        index = int(input("Invalid. What's your input? "))
    state = s[0:index] + turn + s[index + 1:]
    return state


def main():
    X = input("X is human or AI? (h: human, a: AI) ")
    O = input("O is human or AI? (h: human, a: AI) ")
    state = input("input state (ENTER if it's an empty state): ")
    if len(state) == 0: state = '.........'
    turn = get_turn(state)
    tc = conditions_table(3, 9)
    print("Game start!")
    print(display(state, 3, 9))
    while terminal_test(state, tc) == False:
        if turn == 'X':
            print("{}'s turn:".format(turn))
            if X == 'a':
                state = minimax(state, turn, tc)
            else:
                state = human_play(state, 3, turn)
            print(display(state, 3, 9))
            turn = 'O'
        else:
            print("{}'s turn:".format(turn))
            if O == 'a':
                state = minimax(state, turn, tc)
            else:
                state = human_play(state, 3, turn)
            print(display(state, 3, 9))
            turn = 'X'

    if utility(turn, tc, state) == 0:
        print("Game over! Tie!")
    else:
        turn = 'O' if turn == 'X' else 'X'
        print('Game over! ' + turn + ' win!')


if __name__ == '__main__':
    main()
