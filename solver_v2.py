import copy

rows = 5
cols = 5
numLetters = rows * cols
board = []
heuristicBoard = [0] * (rows * cols)
alphabet = "abcdefghijklmnopqrstuvwxyz"
neighbourOffsets = {
    "top": -cols - 1,
    "bottom": cols + 1,
    "left": -1,
    "right": 1,
    "ne": -cols,
    "nw": -cols - 2,
    "sw": cols,
    "se": cols + 2
}

alphabetScores = {
    "a": 1,
    "b": 4,
    "c": 5,
    "d": 3,
    "e": 1,
    "f": 5,
    "g": 3,
    "h": 4,
    "i": 1,
    "j": 7,
    "k": 6,
    "l": 3,
    "m": 4,
    "n": 2,
    "o": 1,
    "p": 4,
    "q": 8,
    "r": 2,
    "s": 2,
    "t": 2,
    "u": 4,
    "v": 5,
    "w": 5,
    "x": 7,
    "y": 4,
    "z": 8
}

# offsets for the start of each word
wordList = {}
for letter in alphabet:
    wordList[letter] = []

print("Opening wordlist...")
f = open("dictionary.txt", "r")
print("Reading words...")
while True:
    line = f.readline().strip()
    if "" == line:
        break

    firstchar = line[0]
    wordList[firstchar].append(line)
print("Done!")


def enterLetters():
    print("enter letters in from left to right, top-down.")
    print("For TL, place a number 1 before the character. For 2x word, add a 2 before the character.")
    board_letters = input("Enter in all letters, then press enter: ")

    # assert len(a) == numLetters, "Number of letters must equal " + str(numLetters)

    # Create letters board with padding
    # Add top padding
    for i in range(cols + 1):
        board.append(0)
    for i in range(cols):
        for j in range(rows):
            x = board_letters[i * cols + j]
            if x.isdigit():
                assert (x == "1") or (x == "2") or (x == "3"), "invalid number found in board description: {}".format(x)
                y = i * cols + j
                new_letter = Letter(board_letters[y + 1], int(x))
                board.append(new_letter)
                # board.append(board_letters[y + 1] + x)
                board_letters = board_letters[:(y)] + board_letters[(y + 1):]
            else:
                board.append(Letter(board_letters[i * cols + j], 0))
                # board.append(board_letters[i*cols + j])
        # end-of-row padding
        board.append(0)

    print(board)


class Letter:
    Scores = {
        "a": 1,
        "b": 4,
        "c": 5,
        "d": 3,
        "e": 1,
        "f": 5,
        "g": 3,
        "h": 4,
        "i": 1,
        "j": 7,
        "k": 6,
        "l": 3,
        "m": 4,
        "n": 2,
        "o": 1,
        "p": 4,
        "q": 8,
        "r": 2,
        "s": 2,
        "t": 2,
        "u": 4,
        "v": 5,
        "w": 5,
        "x": 7,
        "y": 4,
        "z": 8
    }

    def __init__(self, character, flags):

        assert (character.isalpha())
        assert (len(character) == 1)
        assert (flags == 0) or (flags == 1) or (flags == 2) or (flags == 3)

        self.character = character
        self.flags = flags

    def get_score(self):
        if self.flags == 1:
            return 2 * Letter.Scores[self.character]
        elif self.flags == 3:
            return 3 * Letter.Scores[self.character]

        return Letter.Scores[self.character]

    def has_double_flag(self):
        return self.flags == 2

    def __eq__(self, other):
        if other == 0:
            return False
        return self.character == other.character

    def __lt__(self, other):
        if other == 0:
            return False
        return self.character < other.character

    def __le__(self, other):
        if other == 0:
            return False
        return self.__eq__(other) or (self.character < other.character)

    def __gt__(self, other):
        if other == 0:
            return False
        return self.character > other.character

    def __ge__(self, other):
        if other == 0:
            return False
        return self.__eq__(other) or (self.character < other.character)


class Word:

    def __init__(self):
        self.score = 0
        self.letters = []
        self.double_flag = False
        self.repr = ""
        self.isValid = False

    def add_letter(self, new_letter):

        assert isinstance(new_letter, Letter), "new_letter is not 'Letter' class!"

        if new_letter.has_double_flag():
            assert self.double_flag == False, "tried adding letter: {}, but word: {} already has double flag set".format(
                new_letter.character, Word)
            self.double_flag = True
        self.isValid = False
        self.repr = self.repr + new_letter.character
        self.score += new_letter.get_score()
        self.letters.append(new_letter)

    def pop_letter(self):

        removed_letter = self.letters.pop()

        if removed_letter.has_double_flag():
            assert self.double_flag == True, "While removing letter: {}, double flag found, but word: {} does not have double flag set!".format(
                removed_letter.character, Word)
            self.double_flag = False

        self.repr = self.repr[:-1]
        self.score -= removed_letter.get_score()

        return removed_letter

    def __len__(self):
        return len(self.repr)

    def __repr__(self):
        return self.repr

    def __str__(self):
        return self.repr

    def get_score(self):
        ret_score = self.score
        if self.double_flag:
            ret_score = 2 * self.score
        if len(self.letters) >= 6:
            ret_score += 10
        return ret_score


# Translate from human-intuitive board position
# To offset used in board representation
def posToBoardOffset(position):
    a = (position + cols + 1) + (position // cols)
    assert a >= 0 or a < len(board), "Position requested is out of range! " + str(a)
    return a


# For given first letter, and adjacent letters, find number of words.
# cull letters if none possible
def firstHeuristic():
    for pos in range(rows * cols):
        neighbours = []
        offset = posToBoardOffset(pos)
        neighbours = getNeighbours(offset)
        assert len(neighbours) >= 3, "Something messed up, each position should have AT LEAST 3 neighbours..."

        neighbourLetters = ""
        for n in neighbours:
            neighbourLetters += board[n][0]

        letter = board[offset][0]

        for word in wordList[letter]:
            l = len(word)
            # Single letter word, so no neighbours
            if (l == 1):
                continue
            elif (word[1] in neighbourLetters):
                heuristicBoard[pos] += l


# For a given BOARD OFFSET, get neighbours board offsets
def getNeighbours(offset):
    neighbours = []
    for x in neighbourOffsets.values():
        test = offset + x
        if (test < 0) or (test >= len(board)):
            continue
        elif board[test] == 0:
            continue
        neighbours.append(test)
    return neighbours

#     # remove any neighbours we have seen already
#     # not particularly efficient... oh well!
def removeSeen(neighbours, seen):
    result = []
    for x in range(len(neighbours)):
        if neighbours[x] not in seen:
            result.append(neighbours[x])
    return result

# Returns a string containing all the letters that
def offsetsToLetters(offsets):
    letters = []
    for offset in offsets:
        letters.append(board[offset])

def getBestWord(words):
    best_score = 0
    best_word = None
    for word in words:
        score = word.get_score()
        if score > best_score:
            best_score = score
            best_word = word
    return best_word


def getLongestWord(position, seen, offset, current_word):

    best_words = [current_word]
    neighbours = getNeighbours(position)
    neighbours = removeSeen(neighbours, seen)
    l_wordList = wordList[current_word.letters[0].character]
    #length of current word, or index for next letter
    depth = len(current_word)

    if len(neighbours) == 0:
        return None, offset

    for neighbour in neighbours:
        new_offset = offset
        # find first matching word for each neighbour letter
        neighbourChar = board[neighbour].character

        # go down list until reach word with neighbour at next index
        while new_offset < len(l_wordList):
            word_candidate = l_wordList[new_offset]
            word_result = Word()

            # If the word we are looking at is alphabetically past our current word at the current depth, stop checking for more words for this neighbour
            if word_candidate[:depth] > str(current_word)[:depth]:
                break

            # If we find a matching letter, recurse.
            elif word_candidate[depth] == neighbourChar:
                new_word = copy.deepcopy(current_word)
                new_word.add_letter(board[neighbour])

                # In the case of the new word length being equal to the current depth + 1, increase offset:
                # And mark as a valid word
                if len(word_candidate) == depth + 1:
                    new_word.isValid = True
                    best_words.append(new_word)
                    word_result, new_offset = getLongestWord(neighbour, seen + [neighbour], new_offset + 1, new_word)
                # Else, if the new word is larger than the depth + 1, don't increase offset (explore this word)
                else:
                    word_result, new_offset = getLongestWord(neighbour, seen + [neighbour], new_offset, new_word)

                if (word_result is not None) and word_result.isValid:
                    best_words.append(word_result)

            new_offset += 1

    return getBestWord(best_words), new_offset

enterLetters()
# firstHeuristic()
print(getNeighbours(13))
fResult = []
for x in range(rows * cols):
    position = posToBoardOffset(x)
    new_word = Word()
    new_word.add_letter(board[position])
    res = getLongestWord(position, [position], 1, new_word)
    fResult.append(res[0])
    print(res[0], res[0].get_score())
best = getBestWord(fResult)
print("---------------------")
print("best:", best, best.get_score())

# print(getLongestWord(6, 0, board[6], [], 0))

# frperylouhuskrardofrcitit
# aczzzabzzzzdzzzzzzzzzzzzz
# didnt find money? :
# rrnooqevnoagijuieugyumone

# imlnanvnteugpfcijkhedeeib
# ox2viodtgfhryrhd1gizgeutare

# 1gawgplmatvviuejnarudyedot

# aczzz
# abzzz
# zdzzz
# zzzzz
# zzzzz

# trper
# ylouh
# uskra
# rdofr
# citit
