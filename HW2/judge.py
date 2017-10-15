import homework
import compete
import random

player1_score = 0
player2_score = 0
movePossible = 0


def checkMove(matrix):

	global movePossible
	s = set()
	for row in matrix:
		s.update(set(row))
	s = list(s)
	if len(s) == 1 and s[0] == '*':
		movePossible = 1



MIN_SIZE = 5
MAX_SIZE = 5
N = random.randint(MIN_SIZE, MAX_SIZE)

MIN_FRUIT_TYPE = 0
MAX_FRUIT_TYPE = 9

s = ""
for i in range(N):
	for j in range(N):
		s += str(random.randint(MIN_FRUIT_TYPE, MAX_FRUIT_TYPE))
	s += "\n"

with open("input.txt", "w") as f:
	
	f.write(str(N) + "\n")
	f.write(str(MAX_FRUIT_TYPE) + "\n")
	f.write("300.0\n")
	f.write(s)


# while True:
# 	print "Calling Player2 code......"
# 	score, matrix = compete.main()
# 	player2_score += score
# 	print "player2's total score: " + str(player2_score)
# 	checkMove(matrix)
# 	print "Done\n"
	

# 	if movePossible == 1:
# 		break

# 	print "Calling Player1 code......."
# 	score, matrix = homework.main()
# 	player1_score += score
# 	print "player1 total score: " + str(player1_score)
# 	checkMove(matrix)
# 	print "Done\n"

# 	if movePossible == 1:
# 		break

# if player1_score > player2_score:
# 	print "Player1 WINS!!"
# 	print "player1 total score: " + str(player1_score)
# 	print "player2's total score: " + str(player2_score)

# elif player2_score > player1_score:
# 	print "Player2 WINS!!"
# 	print "player1 total score: " + str(player1_score)
# 	print "player2 total score: " + str(player2_score)

# else:
# 	print "DRAW!"
# 	print "player1 total score: " + str(player1_score)
# 	print "player2 total score: " + str(player2_score)

# fp = open("input_temp.txt", "r")
# fp2 = open("input.txt", "w")
# fp2.write(fp.read())
# fp.close()
# fp2.close()