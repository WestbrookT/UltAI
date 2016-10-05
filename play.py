from board import Board
from player import netPlayer, humanPlayer, randPlayer

layers = [90, 90, 90]

p1 = randPlayer()
p2 = netPlayer(layers)



b = Board()

p1.set_board(b)
p2.set_board(b)
count = 0


def train(player):
	global b
	if b.winner != 1:
		player.train(20, False)
	else:
		player.train(20, True)




while count < 1000:

	bx, by, x, y = p1.move(b.valid_move, b.get_state())
	if x == None:
		p2.clear()
		b.reset()
		continue

	b.move(bx, by, x, y)
	if b.winner != None:

		p2.train(20)

		p2.clear()
		b.reset()



	bx, by, x, y = p2.move(b.valid_move, b.get_state())
	if x == None:
		train(p2)
		b.reset()
		p2.clear()
		continue
	b.move(bx, by, x, y)


	if b.winner != None:
		train(p2)


		p2.clear()
		b.reset()

	count += 1
	if count % 50 == 0:
		print(count)
	if count >= 1000:
		p2.save('net.h5')
		exit()


