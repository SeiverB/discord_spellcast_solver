rows = 5
cols = 5
numLetters = rows * cols
board = []
heuristicBoard = [0] * (rows * cols)
alphabet = "abcdefghijklmnopqrstuvwxyz"
neighbourOffsets = {
    "top" : -cols - 1,
    "bottom" : cols + 1,
    "left" : -1,
    "right" : 1,
    "ne" : -cols,
    "nw" : -cols - 2,
    "sw" : cols,
    "se" : cols + 2
    }

alphabetScores = {
    "a" : 1,
    "b" : 4,
    "c" : 5,
    "d" : 3,
    "e" : 1,
    "f" : 5,
    "g" : 3,
    "h" : 4,
    "i" : 1,
    "j" : 7,
    "k" : 6,
    "l" : 3,
    "m" : 4,
    "n" : 2,
    "o" : 1,
    "p" : 4,
    "q" : 8,
    "r" : 2,
    "s" : 2,
    "t" : 2,
    "u" : 4,
    "v" : 5,
    "w" : 5,
    "x" : 7,
    "y" : 4,
    "z" : 8
}
for letter in alphabet:
    alphabetScores[letter + "1"] = alphabetScores[letter] * 2
    alphabetScores[letter + "2"] = alphabetScores[letter]


# nested list, where each nested list corresponds to words starting with each letter in alphabet
wordList = {}
for letter in alphabet:
    wordList[letter] = []

print("Opening wordlist...")
f = open("dictionary.txt", "r")
print("Reading words...")
while True:
    line = f.readline().strip()
    if ("" == line):
        break;

    firstchar = line[0]
    wordList[firstchar].append(line)
print("Done!")

def enterLetters():
    print("enter letters in from left to right, top-down.")
    a = input("Enter in all letters, then press enter: ")
    #a = "frperylouhuskrardofrcitit"
    #assert len(a) == numLetters, "Number of letters must equal " + str(numLetters)

    # Create letters board with padding
    # Add top padding
    for i in range(cols + 1):
        board.append(0)
    for i in range(cols):
        for j in range(rows):
            x = a[i*cols + j]
            if(x.isdigit()):
                y = i*cols + j
                board.append(a[y + 1] + x)
                a = a[:(y)] + a[(y+1):]
            else:
                board.append(a[i*cols + j])
        # end-of-row padding
        board.append(0)

    print(board)

# returns letter's position in alphabet
def getLetterNumber(letter):
    return ord(letter) - 97

def getWordScore(candidate_tuple):
    print(candidate_tuple)
    res = candidate_tuple[1]
    word = candidate_tuple[0]
    if len(word) >= 6:
        res += 10
    if candidate_tuple[2]:
        res *= 2

    return res

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
            if(l == 1):
                continue
            elif(word[1] in neighbourLetters):
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

# Recursively search for longest word for given offset
# offset is the position we are at
# longest is longest word (or subset of word) found so far
# head is offset within list of words starting with first letter of longest
# seen is list of offsets we have seen (doodoo poo poo)
def getLongestWord(offset, head, longest, score, doubleFlag, seen, depth):
    depth+=1

    # best is thus also offset to end of longest word found thus far

    neighbours = getNeighbours(offset)
    # Add current offset to seen list
    seen.append(offset)

    # remove any neighbours we have seen already
    # not particularly efficient... oh well!
    x = 0
    y = len(neighbours)
    while x < y:
        if neighbours[x] in seen:
            neighbours.pop(x)
            y -= 1
        else:
            x += 1
    curTile = board[offset]

    score += alphabetScores[curTile[0]]
    if len(curTile) > 1:
        if curTile[1] == "1":
            score += alphabetScores[curTile[0]]
        else:
            doubleFlag = True

    if len(neighbours) == 0:
        #print("No neighbours!")
        return None, head, None, None

    candidates = []

    for n in neighbours:

        nextTile = board[n]
        neighbourLetter = nextTile[0]

        new_head = head
        max_len = len(wordList[longest[0]])

        # iterate thru words until next neighbour letter found.
        # could probably speed this up, especially by doing some indexing or binary search
        while (new_head < max_len):
            x = wordList[longest[0]][new_head]
            #print("X:", x, "depth:", depth, "longest:", longest, "head:", new_head, "neighbourLetter:", neighbourLetter)

            if(len(x) > depth):
                nextLetter = x[depth]
            elif(new_head == 0):
                new_head += 1
                continue
            else:
                break

            # If we are onto the next letter, we know we won't find a word with neighbourLetter
            if(longest != x[:depth]):
                break

            # Haven't found nextLetter yet...
            if(nextLetter != neighbourLetter):
                new_head += 1
            # if found next neighbour letter, then recurse.
            else:
                #print("RECURSE INPUT", "X:", x, "best:", depth, "longest:", longest + neighbourLetter, "head:", new_head)
                # if it is actual, full word in and of itself:
                if(str(longest + neighbourLetter) == str(x)):
                    #print("Found word!", (longest + neighbourLetter), x)

                    candidates.append([longest + neighbourLetter, score, doubleFlag])
                    head += 1
                else:

                    new_candidate, new_head, new_score, new_doubleFlag = getLongestWord(n, new_head + 1, longest + neighbourLetter, score, doubleFlag, seen.copy(), depth)
                    if new_candidate != None:
                        candidates.append([new_candidate, new_score, new_doubleFlag])

                new_head += 1

    if len(candidates) == 0:
        return None, new_head, None, None


    max_score = -1

    for ele in candidates:
        if getWordScore(ele) > max_score:
            max_score = getWordScore(ele)
            res = ele

    return res[0], new_head, res[1], res[2]

enterLetters()
#firstHeuristic()
print(getNeighbours(13))
for x in range(rows * cols):
    off = posToBoardOffset(x)
    res = getLongestWord(off, 0, board[off][0], 0, False, [], 0)
    if(res[0] != None):
        print(res[0], res[1], getWordScore(res))


#print(getLongestWord(6, 0, board[6], [], 0))

#frperylouhuskrardofrcitit
#aczzzabzzzzdzzzzzzzzzzzzz
# didnt find money? :
#rrnooqevnoagijuieugyumone

#imlnanvnteugpfcijkhedeeib
#ox2viodtgfhryrhd1gizgeutare

#aczzz
#abzzz
#zdzzz
#zzzzz
#zzzzz

#trper
#ylouh
#uskra
#rdofr
#citit