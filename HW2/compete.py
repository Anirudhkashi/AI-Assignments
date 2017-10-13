import copy

def getMaxFruit(game_board, i, j):
	stack = []
	stack.append((i, j))
	score = 1
	fruit_type = game_board[i][j]
	game_board[i][j] = '*'
	exclude = []
	coordinates = [(0,1),(1,0),(0,-1),(-1,0)]
	while len(stack)>0:
		x, y = stack.pop()
		for (temp_x,temp_y) in coordinates:
			new_x,new_y = x+temp_x,y+temp_y
			if (new_x)>=0 and (new_x)<size and (new_y)>=0 and (new_y)<size and game_board[new_x][new_y]==fruit_type:
				game_board[new_x][new_y] = '*'
				exclude.append((new_x,new_y))
				score += 1
				stack.append((new_x,new_y))
	return game_board,score,exclude


class Node():
	def __init__(self):
		self.total_score = None
		self.move = None
		self.game_board = None
		self.depth = 0
		self.value = None

MAX_DEPTH = 5


def isEmpty(state):
	game_board = state.game_board
	value = state.value
	score = state.total_score

	all_items = {}
	for row in game_board:
		for item in row:
			if item in all_items.keys():
				all_items[item] += 1
			else:
				all_items[item] = 1

	if len(all_items.keys()) == 1 and all_items.keys()[0] == '*':
		state.value = float(score)
		return True,state
	if state.depth == MAX_DEPTH:
		max_score = all_items[sorted(all_items,key=lambda x:all_items[x],reverse=True)[0]]
		state.value = float(score)/max_score
		return True,state

	return False, state

def applyGravity(game_board):
	game_board = list(map(list,zip(*game_board)))
	for row in game_board:
		# if '*' in row:
		# 	for i in range(len(row)-1):
		# 		if row[i]!='*' and row[i+1]=='*':
		# 			j = i
		# 			while j>=0 and row[j]!='*' and row[j+1]=='*':
		# 				row[j],row[j+1]=row[j+1],row[j]
		# 				j = j-1
		for i in range(size-1):
			if row[i]!='*' and row[i+1]=='*':
				row[i+1]=row[i]
				del row[i]
				row.insert(0,'*')
	game_board = list(map(list,zip(*game_board)))
	return game_board


def gravity(game_board):
	for j in range(size):
		m = size-1
		n = size-1
		while n >= 0:
			if game_board[n][j] != '*' and m == n:
				n -= 1
				m -= 1
			elif game_board[n][j] == '*':
				n -= 1
			elif game_board[n][j] != '*' and n < m:
				game_board[m][j] = game_board[n][j]
				n -= 1
				m -= 1

		if m > n:
			while m >= 0:
				game_board[m][j] = '*'
				m -= 1
	return game_board

import time


def getAvailableMoves(node,player):
	moves = []
	game_board = node.game_board
	done_list = []
	for i in range(size):
		for j in range(size):
			if game_board[i][j] != '*'  and ((i, j) not in done_list):
				res = getMaxFruit(game_board, i, j)
				new_node = Node()
				time1 = time.time()
				new_node.game_board = applyGravity(res[0])
				time2 = time.time()
				# print time2-time1
				new_node.value = res[1]
				new_node.move = (i,j)
				new_node.depth = node.depth + 1
				new_node.total_score = node.total_score + player * (new_node.value**2)
				new_node.exclude = res[2]
				done_list = done_list + res[2]
				moves.append(new_node)
	return moves


def minPlay(node,alpha,beta, t1):
	isLeaf,state = isEmpty(node)
	if isLeaf:
		return state, state.move
	v = float('inf')
	move = None
	player = -1
	for action in getAvailableMoves(node,player):
		res,temp = maxPlay(action, alpha, beta, t1)
		if v > res.total_score:
			v = res.total_score
			move = res.move
			node.game_board = res.game_board
			node.value = res.value
			node.total_score = res.total_score
		if v <= alpha:
			return node,move
		beta = min(beta, v)
	return node,move

def maxPlay(node,alpha,beta, t1):
	isLeaf,state = isEmpty(node)
	if isLeaf:
		return state, state.move
	v = float('-inf')
	move = None
	player = 1
	for action in getAvailableMoves(node, player):
		res,temp = minPlay(action, alpha, beta, t1)	
		if v < res.value:
			v = res.value
			move = res.move
			node.game_board = res.game_board
			node.value = res.value
			node.total_score = res.total_score
		if v >= beta:
			return node,move
		alpha = max(alpha, v)
	return node,move

def minimaxDecision(node):
	game_board = copy.deepcopy(node.game_board)
	for row in node.game_board:
		print row
	print "*" * 50
	t1 = time.time() + 1
	res,move = maxPlay(node,float('-inf'),float('inf'), t1)
	print move
	res.move = move
	res_matrix = applyGravity(getMaxFruit(game_board,res.move[0],res.move[1])[0])
	for row in res_matrix:
		print row 
	output(res_matrix)
	return res_matrix, res.total_score

size = 0
def preProcess():
	game_board = []
	f = open("input_comp.txt").read().strip().split("\n")
	size = int(f[0])
	fruits = int(f[1])
	total_time = float(f[2])
	for line in f[3:]:
		game_board.append(list(line))
	return fruits,size,game_board,total_time

def output(game_board):
	f = open("input_comp.txt").read().strip().split("\n")
	size = int(f[0])
	fruits = int(f[1])
	total_time = float(f[2])
	res = ["".join(row) for row in game_board]
	f[3:] = res
	open("input.txt","w").write("\n".join(f))

def main():
	fruits,length,game_board,total_time = preProcess()
	global size
	size = length
	node = Node()
	node.total_score = 0
	node.value = 0
	node.game_board = game_board
	node.move = None
	node.depth = 0
	matrix, score = minimaxDecision(node)
	return score, matrix[:size]


if __name__ == "__main__":
	main()