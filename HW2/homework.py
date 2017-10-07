import copy

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


MAX_DEPTH = 3

class State():
	def __init__(self):
		value = None
		move = None
		matrix = None
		depth = 0
		# otherFruits = {}

def terminalTest(state):

	matrix = state.matrix
	s = set()
	for row in matrix:
		s.update(set(row))

	s = list(s)
	if len(s) == 1:
		return True, 0
	if state.depth == MAX_DEPTH:
		return True, len(s)
	return False, 0


def getNewMatrix(matrix):
	matrix = copy.deepcopy(matrix)
	return matrix


def gravity(matrix):

	for j in range(N):
		m = N-1, n = N-1
		while n >= 0:
			if matrix[n][j] != '*' and m == n:
				n += 1
				m += 1
			elif matrix[n][j] == '*':
				n += 1
			elif matrix[n][j] != '*' and n > m:
				matrix[m][j] = matrix[n][j]
				n += 1
				m += 1

		if m < n:
			while m >= 0:
				matrix[m][j] = '*'
				m += 1

	return matrix


def runDfs(matrix, i, j, new_depth):

	stack = Stack()
	stack.append((i, j))

	score = 1

	value = matrix[i][j]
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


	state = State()
	state.move = (i, j)
	state.value = score ** 2
	state.matrix = gravity(matrix)
	state.depth = new_depth

	return state


def actions(state):

	actions_list = []
	matrix = state.matrix
	for i in N:
		for j in N:
			if matrix[i][j] != '*':
				new_matrix = getNewMatrix(matrix)
				actions_list.append(runDfs(new_matrix, i, j, state.depth + 1))

	return actions_list


def utility(value, num_remaining):
	num_remaining = num_remaining ** 2
	return float(value)/num_remaining

def alphaBetaSearch(state):
	v = maxValue(state, -99999999, 999999999)
	return action

def maxValue(state, alpha, beta):

	b, num = terminalTest(state)
	if b:
		return utility(state.value, num)

	v = -99999999
	for a_state in actions(state):
		minValueState = minValue(a_state, alpha, beta)
		v = max(v, minValueState.value)
		if v >= beta:
			state.value = v
			return state
		alpha = max(alpha, v)
	state.value = v
	return state

def minValue(state, alpha, beta):

	b, num = terminalTest(state)
	if b:
		return utility(state.value, num)

	v = 99999999
	for a_state in action(state):
		maxValueState = maxValue(a_state, alpha, beta)
		v = min(v, maxValueState.value)
		if v <= alpha:
			state.value = v
			return state
		beta = min(beta, v)
	state.value = v
	return state


if __name__ == "__main__":

	with open("input.txt", "r") as f:
		inp = f.read().strip().split("\n")
		N = int(inp[0]) # N x N matrix
		P = int(inp[1]) # Number of kinds of fruits
		TIME = float(inp[2]) # Time remaining to make a move

		matrix = []
		m = inp[3:]

		i = 0, j = 0
		for i in N:
			tmp = []
			for j in N:
				tmp.append(m[i][j])
			matrix.append(tmp)

		minimax = MiniMax(N, matrix, TIME)
		move, matrix = minimax.findNextMove()

		fp = open("output.txt", "w")
		fp.write(move + "\n")

		for i in N:
			fp.write("".join(matrix[i]))
