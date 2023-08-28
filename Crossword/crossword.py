import sys; args = sys.argv[1:]
import re
import time

class CrosswordBoard:
    ''' A class representing a crossword board. Has dimensions, number of blocked cells, and a list of words to
    place.'''

    def __init__(self, width, height, num_blocked, required_words, wordlst):
        self.width = width
        self.height = height
        self.num_blocked = num_blocked
        self.required_words = required_words  # (index, direction), word
        self.BLOCKCHAR = "#"
        self.OPENCHAR = '-'
        self.PROTECTEDCHAR = '.'
        self.SEARCHEDCHAR = 'x'
        self.xword = self.create_board()
        self.worddict, self.wordset = self.create_worddict(wordlst)
        board = self.outer_block(self.xword)
        board = self.backtracking_search_words(board)
        board = self.remove_outer_block(board)
        self.xword = board


    def place_required_words(self, board):
        ''' Places required words on the board. '''
        for location, word in self.required_words.items():
            location = location.split(",")
            index = int(location[0])
            direction = location[1]
            iter_mult = 1 if direction == "H" else self.width
            for i, letter in enumerate(word):
                if letter == self.BLOCKCHAR and board[index + i * iter_mult] != self.BLOCKCHAR:
                    board = board[:index + i * iter_mult] + letter + board[index + i * iter_mult + 1:]
                    opposite = self.width * self.height - index - i * iter_mult - 1
                    board = board[:opposite] + letter + board[opposite + 1:]
                else:
                    board = board[:index + i * iter_mult] + letter + board[index + i * iter_mult + 1:]
        return board

    def create_worddict(self, wordlst):
        ''' Creates a dictionary of words using lengths and patterns '''
        worddict = {}
        wordset = set()
        for word in wordlst:
            for i, char in enumerate(word):
                if len(word) not in worddict.keys():
                    worddict[len(word)] = {}
                if str(i)+char not in worddict[len(word)].keys():
                    worddict[len(word)][str(i)+char] = {word}
                else:
                    worddict[len(word)][str(i)+char].add(word)
            wordset.add(word)
        return worddict, wordset


    def outer_block(self, board):
        ''' BLocks outer edges of the board.
        Must be called after place_required_words()'''
        xw = self.BLOCKCHAR * (self.width + 3)
        xw += (self.BLOCKCHAR * 2).join([board[i:i + self.width] for i in range(0, len(board), self.width)])
        xw += self.BLOCKCHAR * (self.width + 3)
        board = xw
        self.width += 2
        self.height += 2
        return board

    def remove_outer_block(self, board):
        ''' Removes outer block of the board.
        Must be called after outer_block()'''
        final_board = ""
        for row in range(1, self.height - 1):
            for col in range(1, self.width - 1):
                # ignore the outer block
                char = board[row * (self.width) + col]
                final_board += char
        self.width -= 2
        self.height -= 2
        return final_board


    def generate_protected_cells(self, board):
        ''' Generates a list of protected cells, i.e. cells that are guaranteed to be open.
        Words must be at least 3 letters long. Protected cells are indicated with a "."'''
        temp_protected = "~"
        for i in range(len(board)):
            if board[i] not in [self.BLOCKCHAR, self.OPENCHAR, self.PROTECTEDCHAR]:
                board = board[:i] + self.PROTECTEDCHAR + board[i + 1:]
                index = self.width * self.height - i - 1
                board = board[:index] + self.PROTECTEDCHAR + board[index + 1:]
        reblock2charopen = "(?<=[{}][{}][{}])[{}]".format(self.BLOCKCHAR, self.PROTECTEDCHAR, self.PROTECTEDCHAR, self.OPENCHAR)
        reopen2charblock = "[{}](?=[{}][{}][{}])".format(self.OPENCHAR, self.PROTECTEDCHAR, self.PROTECTEDCHAR, self.BLOCKCHAR)
        reblockchar2open = "(?<=[{}][{}])[{}][{}]?".format(self.BLOCKCHAR, self.PROTECTEDCHAR, self.OPENCHAR, self.OPENCHAR)
        re2opencharblock = "[{}][{}]?(?=[{}][{}])".format(self.OPENCHAR, self.OPENCHAR, self.PROTECTEDCHAR, self.BLOCKCHAR)
        transpose_height = len(board) // self.width
        for counter in range(2):
            board = re.sub(reblockchar2open, lambda x: temp_protected*len(x.group()), board)
            board = re.sub(re2opencharblock, lambda x: temp_protected*len(x.group()), board)
            board = re.sub(reblock2charopen, temp_protected, board)
            board = re.sub(reopen2charblock, temp_protected, board)
            board = self.transpose(board, len(board) // transpose_height)
            transpose_height = len(board) // transpose_height
        board = board.replace(temp_protected, self.PROTECTEDCHAR)
        return board

    def select_unnassigned_block(self, board, searched_indices):
        ''' Selects an unassigned block. Returns the index of the block.'''
        pos = [m.start() for m in re.finditer(self.OPENCHAR, board) if searched_indices[m.start()] != self.SEARCHEDCHAR]
        posvals = {}
        for i in pos:
            posvals[i] = self.get_num_open_neighbors(board, i)
        return min(posvals, key=posvals.get) if posvals else -1

    def get_num_open_neighbors(self, board, index):
        ''' Heuristic for selecting unassigned block. Uses number of spaces to the left,right,top,and bottom.'''
        left = "(?<=[{}])[{}{}]*$".format(self.BLOCKCHAR, self.OPENCHAR, self.PROTECTEDCHAR)
        right = "^[{}{}]*(?=[{}])".format(self.OPENCHAR, self.PROTECTEDCHAR, self.BLOCKCHAR)
        leftnum = len(re.search(left, board[:index]).group()) - 2
        rightnum = len(re.search(right, board[index + 1:]).group()) - 2
        board = self.transpose(board, self.width)
        topnum = len(re.search(left, board[:index]).group()) - 2
        bottomnum = len(re.search(right, board[index + 1:]).group()) - 2
        return leftnum * rightnum + topnum * bottomnum

    def backtracking_search_block(self, board, explored_boards):
        ''' Solves the crossword puzzle using backtracking search.'''
        if self.num_blocked == (self.width-2) * (self.height-2):
            return self.BLOCKCHAR * (self.width * self.height)
        searched_indices = "."*(self.width*self.height)
        return self.recursive_backtracking_block(board, searched_indices, explored_boards)

    def recursive_backtracking_block(self, board, searched_indices, explored_boards):
        ''' Recursive backtracking search. Requires symmetry if rotated 180 degrees'''
        blocks = board.count(self.BLOCKCHAR) - 2 * (self.width + self.height-2)
        if blocks == self.num_blocked:
            return board
        i = self.select_unnassigned_block(board, searched_indices)
        if i == -1:
            return None
        while searched_indices[i] == self.SEARCHEDCHAR:
            i = self.select_unnassigned_block(board, searched_indices)
            if i == -1 or i > self.width * self.height // 2 + 1:
                return None
        valid, temp_board = self.isValidBlock(board, i, explored_boards)
        if valid:
            result = self.recursive_backtracking_block(temp_board, searched_indices, explored_boards)
            if result is not None:
                return result
        searched_indices = searched_indices[:i] + self.SEARCHEDCHAR + searched_indices[i + 1:]
        result = self.recursive_backtracking_block(board, searched_indices, explored_boards)
        if result is not None:
            return result

    def isValidBlock(self, board, i, explored_boards):
        ''' If index has 1 or 2 spaces to another block, must check if all spaces can be filled by blocks.
        Returns True or False, followed by xword.'''
        board = board[:i] + self.BLOCKCHAR + board[i + 1:]
        index = self.width * self.height - i - 1
        board = board[:index] + self.BLOCKCHAR + board[index + 1:]
        # print(f"INDEX: {i}\n" + self.display_board(board))

        illegalRegex = "[{}](.?[{}]|[{}].?)[{}]".format(self.BLOCKCHAR, self.PROTECTEDCHAR, self.PROTECTEDCHAR,
                                                        self.BLOCKCHAR)
        if re.search(illegalRegex, board):
            return False, board
        if re.search(illegalRegex, self.transpose(board, self.width)):
            return False, board
        re1open = "[{}][{}][{}]".format(self.BLOCKCHAR, self.OPENCHAR, self.BLOCKCHAR)
        re2open = "[{}][{}][{}][{}]".format(self.BLOCKCHAR, self.OPENCHAR, self.OPENCHAR, self.BLOCKCHAR)
        transpose_height = len(board) // self.width
        for counter in range(2):
            while re.search(re1open, board) or re.search(re2open, board):
                board = re.sub(re1open, self.BLOCKCHAR * 3, board)
                board = re.sub(re2open, self.BLOCKCHAR * 4, board)
            board = self.transpose(board, len(board) // transpose_height)
            transpose_height = len(board) // transpose_height
        num_blocks = board.count(self.BLOCKCHAR) - 2 * (self.width + self.height-2)
        if num_blocks > self.num_blocked:
            return False, board
        if not self.check_connected(board):
            return False, board
        if board in explored_boards:
            return False, board
        return True, board

    def check_connected(self, board):
        '''Checks if the board is a single connected figure. (Blocks cannot seperate sections of the board)'''
        initial_index = board.find(self.OPENCHAR)
        domain = [initial_index]
        while domain:
            index = domain.pop()
            board = board[:index] + self.SEARCHEDCHAR + board[index + 1:]
            if index - self.width >= 0 and board[index - self.width] not in [self.SEARCHEDCHAR, self.BLOCKCHAR]:
                domain.append(index - self.width)
            if index + self.width < len(board) and board[index + self.width] not in [self.SEARCHEDCHAR, self.BLOCKCHAR]:
                domain.append(index + self.width)
            if index % self.width != 0 and board[index - 1] not in [self.SEARCHEDCHAR, self.BLOCKCHAR]:
                domain.append(index - 1)
            if index % self.width != self.width - 1 and board[index + 1] not in [self.SEARCHEDCHAR, self.BLOCKCHAR]:
                domain.append(index + 1)
        if board.count(self.SEARCHEDCHAR) == self.width * self.height - board.count(self.BLOCKCHAR):
            return True
        return False

    def clean_board(self, board):
        ''' Cleans the board of all characters used in the algorithm.'''
        board = board.replace(self.SEARCHEDCHAR, self.OPENCHAR)
        board = board.replace(self.PROTECTEDCHAR, self.OPENCHAR)
        board = self.place_required_words(board)
        return board

    def transpose(self, board, newWidth):
        ''' Transposes the board.'''
        return "".join([board[i::newWidth] for i in range(newWidth)])

    def display(self):
        return self.display_board(self.xword)

    def display_board(self, board):
        ''' Displays the board.'''
        finalstr = ""
        for row in range(self.height):
            for col in range(self.width):
                # ignore the outer block
                letter = board[row * (self.width) + col]
                finalstr += letter
            finalstr += "\n"
        return finalstr

    def display_with_outer_block(self, board):
        finalstr = ""
        height = self.height - 2
        width = self.width - 2
        for row in range(height):
            for col in range(width):
                # ignore the outer block
                letter = board[(row+1) * (self.width) + col+1]
                finalstr += letter
            finalstr += "\n"
        return finalstr

    def create_board(self, explored_boards=set()):
        ''' Creates a board with the required words placed.'''
        board = self.OPENCHAR * self.width * self.height
        board = self.place_required_words(board)
        board = self.outer_block(board)
        board = self.generate_protected_cells(board)
        board = self.backtracking_search_block(board, explored_boards)
        if board is None:
            return None
        board = self.remove_outer_block(board)
        board = self.clean_board(board)
        return board

    def find_words_on_board(self, board):
        ''' Finds the words on the board.'''
        words = set()
        relocationmatch = r"(?<={})[^{}]+(?={})".format(self.BLOCKCHAR, self.BLOCKCHAR, self.BLOCKCHAR)
        for match in re.finditer(relocationmatch, board):
            if match.group().count(self.OPENCHAR) == 0:
                words.add(match.group())
        for match in re.finditer(relocationmatch, self.transpose(board, self.width)):
            if match.group().count(self.OPENCHAR) == 0:
                words.add(match.group())
        return words

    def find_words_to_place(self, board):
        ''' Finds the locations of words to be placed. Stored as (index, direction): (length, known letters)'''
        relocationmatch = r"(?<={})[^{}]+(?={})".format(self.BLOCKCHAR, self.BLOCKCHAR, self.BLOCKCHAR)
        words_on_board = self.find_words_on_board(board)
        words_to_place = set()  # direction : (index, length, known letters)
        for match in re.finditer(relocationmatch, board):
            start = match.start()
            end = match.end()
            if match.group().count(self.OPENCHAR) == 0:
                continue
            known_sets = []
            length = end-start
            for i in range(start, end):
                if board[i] != self.OPENCHAR:
                    if str(i-start)+board[i] not in self.worddict[length]:
                        return None
                    known_sets.append(self.worddict[length][str(i-start)+board[i]])
            if not known_sets:
                known_sets = [self.worddict[length][thing] for thing in self.worddict[length].keys()]
                words_to_place.add(("H", start, length, frozenset(set.union(*known_sets)-words_on_board)))
            else:
                inset = ("H", start, length, frozenset(set.intersection(*known_sets)-words_on_board))
                words_to_place.add(inset)
                if len(inset[3]) == 0:
                    return None
        transpose_board = self.transpose(board, self.width)
        for match in re.finditer(relocationmatch, transpose_board):
            start = match.start()
            end = match.end()
            if match.group().count(self.OPENCHAR) == 0:
                continue
            known_sets = []
            length = end-start
            for i in range(start, end):
                if transpose_board[i] != self.OPENCHAR:
                    if str(i-start)+transpose_board[i] not in self.worddict[length]:
                        return None
                    known_sets.append(self.worddict[length][str(i-start)+transpose_board[i]])
            if not known_sets:
                known_sets = self.worddict[length].values()
                words_to_place.add(("V", start, length, frozenset(set.union(*known_sets) - words_on_board)))
            else:
                inset = ("V", start, length, frozenset(set.intersection(*known_sets) - words_on_board))
                words_to_place.add(inset)
                if len(inset[3]) == 0:
                    return None
        return words_to_place

    def word_heuristic(self, word_tuple):
        ''' Heuristic for the words to place. Goal is to minimize heuristic.'''
        direction, index, length, words = word_tuple
        return len(words) - length

    def backtracking_search_words(self, board):
        ''' Backtracking search to place the words.'''
        words_to_place = self.find_words_to_place(board)
        result = self.recursive_backtracking_search_words(board, words_to_place, set())
        explored_boards = {board}
        # print(board)
        while result is None:
            board = self.create_board(explored_boards)
            # print(board)
            result = self.recursive_backtracking_search_words(board, words_to_place, set())
            explored_boards.add(board)
        return result

    def recursive_backtracking_search_words(self, board, words_to_place, explored_boards):
        ''' Backtracking search to place the words.'''
        if board.find(self.OPENCHAR) == -1 and self.final_board_check(board):
            return board
        if not words_to_place:
            return None
        # print(self.display_board(board))
        print(self.display_with_outer_block(board))
        # print(words_to_place)
        direction, index, length, known_words = min(words_to_place, key=lambda x: self.word_heuristic(x))
        if direction == "V":
            board = self.transpose(board, self.width)
        for word in known_words:
            new_board = board[:index] + word + board[index + length:]
            if direction == "V":
                new_board = self.transpose(new_board, self.height)
            if new_board in explored_boards:
                continue
            new_words_to_place = self.find_words_to_place(new_board)
            explored_boards.add(new_board)
            result = self.recursive_backtracking_search_words(new_board, new_words_to_place, explored_boards)
            if result is not None:
                return result
        return None

    def final_board_check(self, board):
        relocationmatch = r"(?<={})[^{}]+(?={})".format(self.BLOCKCHAR, self.BLOCKCHAR, self.BLOCKCHAR)
        words = set()
        for match in re.finditer(relocationmatch, board):
            if match.group() not in self.wordset or match.group() in words:
                return False
            words.add(match.group())
            # print(words)
        transpose_board = self.transpose(board, self.width)
        for match in re.finditer(relocationmatch, transpose_board):
            if match.group() not in self.wordset or match.group() in words:
                return False
            words.add(match.group())
            # print(words)
        return True




width = 0
height = 0
num_blocked = 0
required_words = {}
wordlst = []
intTest = [r"^(\d+)x(\d+)$", r"^\d+$", r"^(H|V)(\d+)x(\d+)(.*)$"]
for num, arg in enumerate(args):
    if num == 0:
        file = open(args[0])
        wordlst = file.read().upper().splitlines()
    for i, test in enumerate(intTest):
        match = re.search(test, arg, re.I)
        if match:
            if i == 0:
                height = int(match.group(1))
                width = int(match.group(2))
            elif i == 1:
                num_blocked = int(match.group(0))
            elif i == 2:
                required_words[str(int(match.group(2)) * width + int(match.group(3))) + "," + match.group(1).upper()] \
                    = match.group(4).upper()
xword = CrosswordBoard(width, height, num_blocked, required_words, wordlst)
if xword.xword is None:
    print("No solution found.")
else:
    print(xword.display())


# Karthik Thyagarajan 5 2024