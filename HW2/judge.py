import homework
import compete

your_score = 0
opponenet_score = 0
movePossible = 0


def checkMove(matrix):

	global movePossible
	s = set()
	for row in matrix:
		s.update(set(row))
	s = list(s)
	if len(s) == 1 and s[0] == '*':
		movePossible = 1


while True:
	print "Calling Anish's code......"
	score, matrix = compete.main()
	opponenet_score += score
	print "Opponent's total score: " + str(opponenet_score)
	checkMove(matrix)
	print "Done\n"
	

	if movePossible == 1:
		break

	print "Calling Anirudh code......."
	score, matrix = homework.main()
	your_score += score
	print "Your total score: " + str(your_score)
	checkMove(matrix)
	print "Done\n"

	if movePossible == 1:
		break

if your_score > opponenet_score:
	print "YOU WIN!!"
	print "Your total score: " + str(your_score)
	print "Opponent's total score: " + str(opponenet_score)

elif opponenet_score > your_score:
	print "opponent wins :("
	print "Your total score: " + str(your_score)
	print "Opponent's total score: " + str(opponenet_score)

else:
	print "DRAW!"
	print "Your total score: " + str(your_score)
	print "Opponent's total score: " + str(opponenet_score)