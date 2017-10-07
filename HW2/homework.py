import copy
import numpy

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
		remove_list = []

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


def runDfs(matrix, i, j, new_depth):

	stack = Stack()
	stack.add((i, j))

	score = 1

	value = matrix[i][j]
	matrix[i][j] = '*'
	remove_list = []
	while not stack.isEmpty():
		x, y = stack.get()
		new_x, new_y = x, y+1
		if new_y < N and matrix[new_x][new_y] == value:
			stack.add((new_x, new_y))
			matrix[new_x][new_y] = '*'
			remove_list.append((new_x, new_y))
			score += 1

		new_x, new_y = x-1, y
		if new_x >= 0 and matrix[new_x][new_y] == value:
			stack.add((new_x, new_y))
			matrix[new_x][new_y] = '*'
			remove_list.append((new_x, new_y))
			score += 1

		new_x, new_y = x+1, y
		if new_x < N and matrix[new_x][new_y] == value:
			stack.add((new_x, new_y))
			matrix[new_x][new_y] = '*'
			remove_list.append((new_x, new_y))
			score += 1

		new_x, new_y = x, y-1
		if new_y >= 0 and matrix[new_x][new_y] == value:
			stack.add((new_x, new_y))
			matrix[new_x][new_y] = '*'
			remove_list.append((new_x, new_y))
			score += 1


	state = State()
	state.move = (i, j)
	state.value = score ** 2
	state.matrix = gravity(matrix)
	state.depth = new_depth
	state.remove_list = remove_list

	return state


def actions(state):

	actions_list = []
	matrix = state.matrix
	done_list = []
	for i in range(N):
		for j in range(N):
			if matrix[i][j] != '*' and ((i, j) not in done_list):
				new_matrix = getNewMatrix(matrix)
				new_state = runDfs(new_matrix, i, j, state.depth + 1)
				actions_list.append(new_state)
				done_list = done_list + new_state.remove_list

	return actions_list


def utility(state, num_remaining):
	value = state.value
	num_remaining = num_remaining ** 2

	if num_remaining == 0:
		state.value = float(value)
	else:
		state.value = float(value)/num_remaining

	return state

def alphaBetaSearch(state):
	v = maxValue(state, -99999999, 999999999)
	return v

def maxValue(state, alpha, beta):

	b, num = terminalTest(state)
	if b:
		return utility(state, num)

	v = -99999999
	move = None
	temp_mat = None
	for a_state in actions(state):
		minValueState = minValue(a_state, alpha, beta)
		
		if v < minValueState.value:
			v = minValueState.value
			move = minValueState.move
			temp_mat = minValueState.matrix

		if v >= beta:
			state.value = v
			state.move = move
			state.matrix = temp_mat
			return state
		alpha = max(alpha, v)
	state.value = v
	state.move = move
	state.matrix = temp_mat
	return state

def minValue(state, alpha, beta):

	b, num = terminalTest(state)
	if b:
		return utility(state, num)

	v = 99999999
	move = None
	temp_mat = None
	for a_state in actions(state):
		maxValueState = maxValue(a_state, alpha, beta)

		if v > maxValueState.value:
			v = maxValueState.value
			move = maxValueState.move
			temp_mat = maxValueState.matrix

		if v <= alpha:
			state.value = v
			state.move = move
			state.matrix = temp_mat
			return state
		beta = min(beta, v)
	state.value = v
	state.move = move
	state.matrix = temp_mat
	return state


if __name__ == "__main__":

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

		state = State()
		state.value = 0
		state.matrix = matrix
		state.depth = 0
		state.move = None

		absearch = alphaBetaSearch(state)
		print absearch.move
		print absearch.matrix
		print absearch.value

		# fp = open("output.txt", "w")
		# fp.write(move + "\n")

		# for i in N:
		# 	fp.write("".join(matrix[i]))
