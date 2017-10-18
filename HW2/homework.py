import copy
import time

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


MOVES = None
IS_MOVES_SET = False
TIME_PER_MOVE = None
TIME_EXCEEDED = False

class State():
	def __init__(self):
		self.value = None
		self.move = None
		self.score = 0
		self.matrix = None
		self.depth = 0
		self.remove_list = []

def terminalTest(state):

	global TIME_EXCEEDED
	matrix = state.matrix
	s = set()
	for row in matrix:
		s.update(set(row))

	s = list(s)
	if len(s) == 1 and s[0] == '*':
		return True
	if state.depth == MAX_DEPTH:
		return True
	if IS_MOVES_SET and time.time() - start_time > TIME_PER_MOVE:
		TIME_EXCEEDED = True
		return True
	return False


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

def runDfs(matrix, i, j, new_depth, total_score, flag):

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
	state.score = total_score + flag * (score ** 2)
	state.matrix = gravity(matrix)
	state.depth = new_depth
	state.remove_list = remove_list
	return state


def actions(state, flag):

	global count
	global MOVES
	global IS_MOVES_SET
	global TIME_PER_MOVE

	actions_list = []
	matrix = state.matrix
	done_list = []
	for j in range(N):
		for i in range(N-1, -1, -1):
			if matrix[i][j] == '*':
				break
			if ((i, j) not in done_list):
				new_matrix = getNewMatrix(matrix)
				new_state = runDfs(new_matrix, i, j, state.depth + 1, state.score, flag)
				actions_list.append(new_state)
				done_list = done_list + new_state.remove_list

	actions_list = sorted(actions_list, key = lambda x: x.value, reverse=True)

	if not IS_MOVES_SET:
		MOVES = len(actions_list)
		IS_MOVES_SET = True

		if MOVES > 4:
			TIME_PER_MOVE = (2.0 * float(TIME) * 0.8) / float(MOVES)
		else:
			TIME_PER_MOVE = (2.0 * float(TIME) * 0.9) / float(MOVES)
		print TIME_PER_MOVE
		set_max_depth(init=0)
	return actions_list


def utility(state, fn):

	if TIME_EXCEEDED:
		if fn == "min":
			state.value = float(999999999)
		else:
			state.value = float(-999999999)
	else:
		score = state.score
		state.value = float(score)
	return state

def alphaBetaSearch(state):
	state, move = maxValue(state, -99999999, 999999999)
	state.move = move
	return state

def maxValue(state, alpha, beta):

	if terminalTest(state):
		s = utility(state, "max")
		return s, s.move

	v = -99999999
	move = None
	for a_state in actions(state, 1):
		minValueState, ignore = minValue(a_state, alpha, beta)
		
		if v < minValueState.value:
			v = minValueState.value
			move = minValueState.move
			state.matrix = minValueState.matrix
			state.value = minValueState.value
			state.score = minValueState.score

		if v >= beta:
			return state, move
		alpha = max(alpha, v)
	return state, move

def minValue(state, alpha, beta):

	if terminalTest(state):
		s = utility(state, "min")
		return s, s.move

	v = 99999999
	move = None
	for a_state in actions(state, -1):
		maxValueState, ignore = maxValue(a_state, alpha, beta)

		if v > maxValueState.value:
			v = maxValueState.value
			move = maxValueState.move
			state.matrix = maxValueState.matrix
			state.value = maxValueState.value
			state.score = maxValueState.score

		if v <= alpha:
			return state, move
		beta = min(beta, v)
	return state, move

def set_max_depth(init=1):

	global MAX_DEPTH
	global N

	if init == 1:
		if N < 8:
			MAX_DEPTH = 5
		elif N >= 8 and N <= 13:
			MAX_DEPTH = 4
		else:
			MAX_DEPTH = 3

	if init == 0 and N > 13:
		if IS_MOVES_SET and MOVES > 40:
			MAX_DEPTH = 3
		elif MOVES <= 40 and MOVES > 20:
			MAX_DEPTH = 4
		else:
			MAX_DEPTH = 5

def main():

	global N
	global start_time
	global TIME
	global count
	global MOVES
	global IS_MOVES_SET
	global TIME_PER_MOVE
	global TIME_EXCEEDED

	MOVES = None
	IS_MOVES_SET = False
	TIME_PER_MOVE = None
	TIME_EXCEEDED = False

	start_time = time.time()

	with open("input.txt", "r") as f:

		inp = f.read().strip().split("\n")
		N = int(inp[0]) # N x N matrix
		P = int(inp[1]) # Number of kinds of fruits
		TIME = float(inp[2]) # Time remaining to make a move
		set_max_depth(init=1)

		matrix = []
		m = inp[3:]

		i = 0
		j = 0
		for i in range(N):
			tmp = []
			for j in range(N):
				tmp.append(m[i][j])
			matrix.append(tmp)

		init_matrix = copy.deepcopy(matrix)
		state = State()
		state.value = 0
		state.score = 0
		state.matrix = matrix
		state.depth = 0
		state.move = None

		absearch = alphaBetaSearch(state)

		temp = runDfs(init_matrix, absearch.move[0], absearch.move[1], 0, 0, 0)
		absearch.matrix = temp.matrix
		absearch.score = temp.value

		fp = open("output.txt", "w")
		fp.write(chr(absearch.move[1] + 65) + str(absearch.move[0] + 1) + "\n")
		
		matrix = absearch.matrix
		for i in range(N):
			fp.write("".join(matrix[i]) + "\n")

		fp.close()

if __name__ == "__main__":

	main()