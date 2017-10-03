import copy
import random
import time
import math

class Queue():
	def __init__(self):
		self.queue = []

	def isEmpty(self):
		if len(self.queue) == 0:
			return True
		return False

	def get(self):
		if not self.isEmpty():
			first = self.queue.pop(0)
			return first
		return False

	def add(self, value):
		if isinstance(value, list):
			for v in value:
				self.queue.append(v)
		else:
			self.queue.append(value)

	def printQueue(self):
		for i in self.queue:
			print i.x, i.y


class Node():
	def __init__(self):
		self.x = -1
		self.y = -1
		self.parent_list = []
		self.num_queens = 0


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
		if isinstance(value, list):
			for v in value:
				self.stack.insert(0, v)
		else:
			self.stack.insert(0, value)


def checkAxes(matrix, x, y):

	X = len(matrix)
	Y = len(matrix[0])

	for i in range(y+1, Y):
		if matrix[x][i] == 2:
			break
		elif matrix[x][i] == 1:
			return False

	for i in range(y-1, -1, -1):
		if matrix[x][i] == 2:
			break
		elif matrix[x][i] == 1:
			return False

	for i in range(x+1, X):
		if matrix[i][y] == 2:
			break
		elif matrix[i][y] == 1:
			return False

	for i in range(x-1, -1, -1):
		if matrix[i][y] == 2:
			break
		elif matrix[i][y] == 1:
			return False
			
	return True	

def checkDiagonals(matrix, x_s, y_s, x_skip=1, y_skip=1):

	X = len(matrix)
	Y = len(matrix[0])

	while True:
		x_s += x_skip
		y_s += y_skip

		if x_s >= X or x_s < 0 or y_s >= Y or y_s < 0:
			break

		if matrix[x_s][y_s] == 1:
			return False

		elif matrix[x_s][y_s] == 2:
			return True

	return True

def checkIfLizardCanBePlaced(matrix, x, y):

	if x < 0 or y < 0:
		return False

	#Check if cell is valid
	if matrix[x][y] != 0:
		return False

	#Check row, column
	rowRes = checkAxes(matrix, x, y)
	
	if not rowRes:
		return rowRes

	#Check Diagonals
	columnRes = checkDiagonals(matrix, x, y) and checkDiagonals(matrix, x, y, 1, -1) and checkDiagonals(matrix, x, y, -1, -1) and checkDiagonals(matrix, x, y, -1, 1)

	if not columnRes:
		return columnRes

	return True


def checkNotConflict(matrix, x, y):

	if matrix[x][y] != 1:
		return False

	#Check row, column
	rowRes = checkAxes(matrix, x, y)
	if not rowRes:
		return rowRes

	#Check Diagonals
	columnRes = checkDiagonals(matrix, x, y) and checkDiagonals(matrix, x, y, 1, -1) and checkDiagonals(matrix, x, y, -1, -1) and checkDiagonals(matrix, x, y, -1, 1)

	if not columnRes:
		return columnRes

	return True

def placeLizard(matrix, x, y):
	matrix[x][y] = 1
	return matrix


def initialiseMatrix(X, Y):
	matrix = []
	for i in range(X):
		t = []
		for j in range(Y):
			t.append(0)
		matrix.append(t)

	return matrix


def plotParents(matrix, parent_list):
	for i, j in parent_list:
		matrix[i][j] = 1

	return matrix


class BFS():
	def __init__(self, X, Y, matrix):
		self.X = X
		self.Y = Y
		self.queue = Queue()
		self.queue.add(Node())
		self.init_matrix = matrix
		self.start_time = time.time()

	def bfs(self, max_node, MAX_LIZ):

		while not self.queue.isEmpty():

			if max_node.num_queens >= MAX_LIZ:
				return max_node

			if time.time() - self.start_time > 280:
				return max_node

			node = self.queue.get()
			x = node.x
			y = node.y

			num_max_node = MAX_LIZ - node.num_queens

			matrix = copy.deepcopy(self.init_matrix)
			
			parent_list = node.parent_list
			matrix = plotParents(matrix, parent_list)

			if x > -1 and y > -1:
				matrix = placeLizard(matrix, x, y)
				node.num_queens += 1

			if x == -1 and y == -1:
				new_x = 0
				new_y = 0

			elif y < self.Y - 2:
				new_x, new_y = x, y+2

			else:
				new_x, new_y = x + 1, 0

			l = []
			flag = 0

			for j in range(new_x, self.X):
				for k in range(self.Y):

					if j == new_x and k == 0:
						k = new_y
					
					if checkIfLizardCanBePlaced(matrix, j, k):

						new_node = Node()
						new_node.x = j
						new_node.y = k
						new_node.num_queens = node.num_queens
						if x>-1 and y>-1:
							new_node.parent_list = copy.deepcopy(node.parent_list) + [[x, y]]
						else:
							new_node.parent_list = copy.deepcopy(node.parent_list)

						l.append(new_node)
						if len(l) >= num_max_node:
							flag = 1
							break

				if flag == 1:
					break

			for val in range(len(l)):
				self.queue.add(l[val])

			if node.num_queens > max_node.num_queens:
				max_node = node

		return max_node


class DFS():
	def __init__(self, X, Y, matrix):
		self.X = X
		self.Y = Y
		self.stack = Stack()
		self.stack.add(Node())
		self.init_matrix = matrix
		self.start_time = time.time()

	def dfs(self, max_node, MAX_LIZ):

		while not self.stack.isEmpty():

			if max_node.num_queens >= MAX_LIZ:
				return max_node

			if time.time() - self.start_time > 280:
				return max_node

			node = self.stack.get()
			x = node.x
			y = node.y

			num_max_node = MAX_LIZ - node.num_queens

			matrix = copy.deepcopy(self.init_matrix)
			
			parent_list = node.parent_list
			matrix = plotParents(matrix, parent_list)

			if x > -1 and y > -1:
				matrix = placeLizard(matrix, x, y)
				node.num_queens += 1

			if x == -1 and y == -1:
				new_x = 0
				new_y = 0

			elif y < self.Y - 2:
				new_x, new_y = x, y+2

			else:
				new_x, new_y = x + 1, 0

			l = []
			flag = 0

			for j in range(new_x, self.X):
				for k in range(self.Y):

					if j == new_x and k == 0:
						k = new_y
					
					if checkIfLizardCanBePlaced(matrix, j, k):

						new_node = Node()
						new_node.x = j
						new_node.y = k
						new_node.num_queens = node.num_queens
						if x>-1 and y>-1:
							new_node.parent_list = copy.deepcopy(node.parent_list) + [[x, y]]
						else:
							new_node.parent_list = copy.deepcopy(node.parent_list)

						l.append(new_node)
						if len(l) >= num_max_node:
							flag = 1
							break

				if flag == 1:
					break

			for val in range(len(l)-1, -1, -1):
				self.stack.add(l[val])

			if node.num_queens > max_node.num_queens:
				max_node = node

		return max_node


class SimulatedAnnealing():
	def __init__(self, X, Y, matrix):
		self.X = X
		self.Y = Y
		self.init_matrix = matrix
		self.T = 5000.0
		self.init_t = 5000.0
		self.start = time.time()
		self.flag = 0

	def schedule(self, time):
		
		if time > 270:
			self.T = 0

		elif time > 100 and self.flag == 0:
			self.T = self.init_t
			self.flag = 1

		elif time > 160 and self.flag == 1:
			self.T = self.init_t
			self.flag = 2

		else:
			self.T = (self.T * 9.952) / (10.2332)
			
		return self.T

	def probability(self, p):
		r = random.uniform(0, 1)

		if r <= p:
			return True
		return False

	def generateRandomPosition(self, matrix):

		while True:
			x = int(random.randint(0, self.X-1))
			y = int(random.randint(0, self.Y-1))

			if matrix[x][y] == 0:
				return x, y

	def numberOfConflicts(self, matrix):

		total = 0
		conflict_list = []
		for i in range(self.X):
			for j in range(self.Y):
				if matrix[i][j] == 1 and not checkNotConflict(matrix, i, j):
					conflict_list.append((i, j))
					total += 1

		return total, conflict_list


	def changePosition(self, matrix, old_x, old_y, new_x, new_y):

		matrix[old_x][old_y] = 0
		matrix[new_x][new_y] = 1
		return matrix

	def sa(self, MAX_LIZ):

		matrix = self.init_matrix
		for i in range(MAX_LIZ):
			x, y = self.generateRandomPosition(matrix)
			matrix[x][y] = 1

		# Get total conflicts and their positions
		min_total_conflicts, min_conflict_list = self.numberOfConflicts(matrix)
		while True:

			if min_total_conflicts == 0:
				return matrix

			if self.T == 0:
				return "FAIL"

			# Get a random conflicting value
			x, y = min_conflict_list[random.randint(0, min_total_conflicts-1)]

			# Randomly move the lizard to new position
			new_x, new_y = self.generateRandomPosition(matrix)

			# Change lizard to new position to calculate conflicts
			matrix = self.changePosition(matrix, x, y, new_x, new_y)
			total_conflicts, conflict_list = self.numberOfConflicts(matrix)

			# If number of conflicts decreases
			if min_total_conflicts > total_conflicts:
				min_total_conflicts = total_conflicts
				min_conflict_list = conflict_list

			# Boltzman formula to get probability and then decide
			else:
				delta_E = min_total_conflicts - total_conflicts
				p = math.exp(float(delta_E)/self.T)

				if self.probability(p):
					min_total_conflicts = total_conflicts
					min_conflict_list = conflict_list
				else:
					# Reset moved values
					matrix = self.changePosition(matrix, new_x, new_y, x, y)

			self.schedule(int(time.time() - self.start))


if __name__ == "__main__":

	with open("input.txt", "r") as f:
		data = f.read().strip().split("\n")
		X = Y = int(data[1])
		MAX_LIZ = int(data[2])
		matrix_str = data[3:]

		matrix = []

		tree_count = 0
		for r in matrix_str:
			t = []
			for c in r:
				temp = int(c)
				if temp == 2:
					tree_count += 1
				t.append(temp)
			matrix.append(t)

		if MAX_LIZ > X + tree_count or MAX_LIZ + tree_count > X*X:
			fp = open("output.txt", "w")
			fp.write("FAIL")
			fp.close()

		elif data[0] == "DFS":
			dfs = DFS(X, Y, matrix)
			m = dfs.dfs(Node(), MAX_LIZ)

			parent_list = m.parent_list

			for x, y in parent_list:
				matrix[x][y] = 1

			if m.x > -1 and m.y > -1:
				matrix[m.x][m.y] = 1

			fp = open("output.txt", "w")
			if m.num_queens != MAX_LIZ:
				fp.write("FAIL")
			else:
				fp.write("OK\n")

				for i in range(X):
					for j in range(Y):
						fp.write(str(matrix[i][j]))
					fp.write("\n")

			fp.close()

		elif data[0] == "BFS":
			bfs = BFS(X, Y, matrix)
			m = bfs.bfs(Node(), MAX_LIZ)
			parent_list = m.parent_list

			for x, y in parent_list:
				matrix[x][y] = 1

			if m.x > -1 and m.y > -1:
				matrix[m.x][m.y] = 1

			fp = open("output.txt", "w")
			if m.num_queens != MAX_LIZ:
				fp.write("FAIL")
			else:
				fp.write("OK\n")

				for i in range(X):
					for j in range(Y):
						fp.write(str(matrix[i][j]))
					fp.write("\n")
			fp.close()

		elif data[0] == "SA":
			sa = SimulatedAnnealing(X, Y, matrix)
			m = sa.sa(MAX_LIZ)

			fp = open("output.txt", "w")
			if m == "FAIL":
				fp.write("FAIL")
			else:
				fp.write("OK\n")

				for i in range(X):
					for j in range(Y):
						fp.write(str(m[i][j]))
					fp.write("\n")
			fp.close()