import code
import main1
import random
import numpy

player1_score = 0
player2_score = 0
movePossible = 0

matrix = []
with open("input.txt", "r") as f:
    inp = f.read().strip().split("\n")
    N = int(inp[0]) # N x N matrix
    P = int(inp[1]) # Number of kinds of fruits
    TIME = float(inp[2]) # Time remaining to make a move

    matrix = []
    m = inp[3:]

    i = 0
    j = 0
    for i in range(N):
        tmp = []
        for j in range(N):
            tmp.append(m[i][j])
        matrix.append(tmp)

class Stack():
    def __init__(self):
        self.stack = []

    def isEmpty(self):
        if len(self.stack) == 0:
            return True
        return False

    def get(self):
        if not self.isEmpty():
            first = self.stack.pop(0)
            return first
        return False

    def add(self, value):
        self.stack.insert(0, value)

def checkMove(matrix):
    global movePossible
    s = set()
    for row in matrix:
        s.update(set(row))
    s = list(s)
    if len(s) == 1 and s[0] == '*':
        movePossible = 1

def gravity(matrix):

    for j in range(N):
        m = N-1
        n = N-1
        while n >= 0:
            if matrix[n][j] != '*' and m == n:
                n -= 1
                m -= 1
            elif matrix[n][j] == '*':
                n -= 1
            elif matrix[n][j] != '*' and n < m:
                matrix[m][j] = matrix[n][j]
                n -= 1
                m -= 1

        if m > n:
            while m >= 0:
                matrix[m][j] = '*'
                m -= 1

    return matrix

def runDfs(matrix, i, j, p):

    stack = Stack()
    stack.add((i, j))

    score = 1

    value = matrix[i][j]

    if value == "*":
        print "Invalid move by " + p + ". Exiting!!"
        exit()

    matrix[i][j] = '*'
    while not stack.isEmpty():
        x, y = stack.get()
        new_x, new_y = x, y+1
        if new_y < N and matrix[new_x][new_y] == value:
            stack.add((new_x, new_y))
            matrix[new_x][new_y] = '*'
            score += 1

        new_x, new_y = x-1, y
        if new_x >= 0 and matrix[new_x][new_y] == value:
            stack.add((new_x, new_y))
            matrix[new_x][new_y] = '*'
            score += 1

        new_x, new_y = x+1, y
        if new_x < N and matrix[new_x][new_y] == value:
            stack.add((new_x, new_y))
            matrix[new_x][new_y] = '*'
            score += 1

        new_x, new_y = x, y-1
        if new_y >= 0 and matrix[new_x][new_y] == value:
            stack.add((new_x, new_y))
            matrix[new_x][new_y] = '*'
            score += 1

    score = score ** 2
    matrix = gravity(matrix)
    return score, matrix

def writeToFile():
    with open("input.txt", "w") as f:
        f.write(str(N) + "\n")
        f.write(str(P) + "\n")
        f.write(str(TIME) + "\n")

        for i in range(N):
            f.write("".join(matrix[i]) + "\n")

# MIN_SIZE = 26
# MAX_SIZE = 26
# N = random.randint(MIN_SIZE, MAX_SIZE)
#
# MIN_FRUIT_TYPE = 0
# MAX_FRUIT_TYPE = 9
#
# s = ""
# for i in range(N):
#     for j in range(N):
#         s += str(random.randint(MIN_FRUIT_TYPE, MAX_FRUIT_TYPE))
#     s += "\n"

# with open("input.txt", "w") as f:
#     f.write(str(N) + "\n")
#     f.write(str(MAX_FRUIT_TYPE) + "\n")
#     f.write("300.0\n")
#     f.write(s)


while True:

    print "Calling Player2 code......"
    x, y = main1.main()
    print x, y
    score, matrix = runDfs(matrix, x, y, "PLAYER2")
    writeToFile()
    player2_score += score
    print "player2's total score: " + str(player2_score)
    checkMove(matrix)
    print "Done\n"

    if movePossible == 1:
        break

    print "Calling Player1 code......."
    x, y = code.main()
    score, matrix = runDfs(matrix, x, y, "PLAYER1")
    writeToFile()
    player1_score += score
    print "player1 total score: " + str(player1_score)
    checkMove(matrix)
    print "Done\n"

    if movePossible == 1:
        break


if player1_score > player2_score:
    print "Player1 WINS!!"
    print "player1 total score: " + str(player1_score)
    print "player2's total score: " + str(player2_score)

elif player2_score > player1_score:
    print "Player2 WINS!!"
    print "player1 total score: " + str(player1_score)
    print "player2 total score: " + str(player2_score)

else:
    print "DRAW!"
    print "player1 total score: " + str(player1_score)
    print "player2 total score: " + str(player2_score)

    # fp = open("input_temp.txt", "r")
    # fp2 = open("input.txt", "w")
    # fp2.write(fp.read())
    # fp.close()
    # fp2.close()