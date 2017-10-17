import copy
import time

def getMaxFruit(game_board, i, j):
	stack = []
	stack.append((i, j))
	count = 1
	fruit_type = game_board[i][j]
	game_board[i][j] = '*'
	exclude = []
	coordinates = [(0,1),(1,0),(0,-1),(-1,0)]
	while len(stack)!=0:
		x, y = stack.pop()
		for (temp_x,temp_y) in coordinates:
			new_x,new_y = x+temp_x,y+temp_y
			if (new_x)>=0 and (new_x)<length and (new_y)>=0 and (new_y)<length and game_board[new_x][new_y]==fruit_type:
				game_board[new_x][new_y] = '*'
				exclude.append((new_x,new_y))
				count += 1
				stack.append((new_x,new_y))
	return game_board,count,exclude

class Node():
	def __init__(self):
		self.total_score = 0
		self.depth = 0
		self.move = None
		self.game_board = None
		self.value = 0

def isEmpty(node):
	game_board = node.game_board
	value = node.value
	score = node.total_score

	all_items = {}
	for row in game_board:
		for item in row:
			if item in all_items.keys():
				all_items[item] += 1
			else:
				all_items[item] = 1

	if len(all_items.keys()) == 1 and all_items.keys()[0] == '*':
		node.value = float(score)
		return True,node
	
	if node.depth == MAX_DEPTH:
		max_score = 0
		for k in all_items.keys():
			if k!='*':
				max_score += all_items[k]
		# node.value = float(score)/(max_score**2)
		node.value = float(score)
		return True,node

	return False, node

def applyGravity(game_board):
	game_board = list(map(list,zip(*game_board)))
	for row in game_board:
		for i in range(length-1):
			if row[i]!='*' and row[i+1]=='*':
				row[i+1]=row[i]
				del row[i]
				row.insert(0,'*')
	game_board = list(map(list,zip(*game_board)))
	return game_board


def getAvailableMoves(node,player):
	global total_time

	moves = []
	game_board = node.game_board
	exclude_list = []
	for i in range(length):
		for j in range(length):
			if game_board[i][j] != '*'  and ((i, j) not in exclude_list):
				new_gameboard = copy.deepcopy(game_board)
				res = getMaxFruit(new_gameboard, i, j)
				new_node = Node()
				new_node.game_board = applyGravity(res[0])
				new_node.value = res[1] ** 2
				new_node.move = (i,j)
				new_node.depth = node.depth + 1
				new_node.total_score = node.total_score + player * new_node.value
				new_node.exclude = res[2]
				exclude_list = exclude_list + res[2]
				moves.append(new_node)

	return sorted(moves, key = lambda x: x.value, reverse=True)

def minPlay(node,alpha,beta):
	isLeaf,node = isEmpty(node)
	if isLeaf:
		return node, node.move
	v = float('inf')
	move = None
	player = -1
	for action in getAvailableMoves(node,player):
		res,temp = maxPlay(action, alpha, beta)
		if v > res.value:
			v = res.value
			move = res.move
			node.value = res.value
			node.total_score = res.total_score
			node.game_board = res.game_board
		if v <= alpha:
			return node,move
		beta = min(beta, v)
	return node,move

def maxPlay(node,alpha,beta):
	isLeaf,node = isEmpty(node)
	if isLeaf:
		return node, node.move
	v = float('-inf')
	move = None
	player = 1
	for action in getAvailableMoves(node, player):
		res,temp = minPlay(action, alpha, beta)	
		if v < res.value:
			v = res.value
			move = res.move
			node.value = res.value
			node.total_score = res.total_score
			node.game_board = res.game_board
		if v >= beta:
			return node,move
		alpha = max(alpha, v)
	return node,move

def minimaxDecision(node):
	game_board = copy.deepcopy(node.game_board)
	res,move = maxPlay(node,float('-inf'),float('inf'))
	res.move = move
	op = []
	mat = applyGravity(getMaxFruit(game_board,res.move[0],res.move[1])[0])
	for row in mat:
		op.append("".join(row))

	ascii_uppercase = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
	cell = ascii_uppercase[move[1]] + str(move[0]+1)
	# output = cell + "\n" + "\n".join(op)
	s = "24\n2\n300\n" + "\n".join(op)
	open("out.txt","w").write(s)
	# open("input.t,"xt","w").write(output)

	return move


def preProcess():
	game_board = []
	f = open("input.txt").read().strip().split("\n")
	length = int(f[0])
	fruits = int(f[1])
	total_time = float(f[2])
	for line in f[3:]:
		game_board.append(list(line))
	return fruits,length,game_board,total_time

def main():
	global length
	global total_time
	fruits,length,game_board,total_time = preProcess()
	node = Node()
	node.total_score = 0
	node.value = 0
	node.game_board = game_board
	node.move = None
	node.depth = 0
	return minimaxDecision(node)

MAX_DEPTH = 3


if __name__ == "__main__":
	main()
