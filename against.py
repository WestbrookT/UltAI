from player import netPlayer, humanPlayer, montePlayer
from board import Board



layers = [90,90,90]
b = Board()

p1 = humanPlayer()

p2 = montePlayer(layers=layers)

p2.load('monte100')
p2.net.set_board(b)



while True:

	b.print()
	bx, by, x, y = p1.move(b.valid_move, b.get_state())
	if x == None:
		p2.clear()
		b.reset()
		break

	b.move(bx, by, x, y)
	if b.winner != None:

		p2.train(20)

		p2.clear()
		b.reset()


	b.print()
	bx, by, x, y = p2.move(b.valid_move, b.get_state())
	if x == None:
		b.reset()
		p2.clear()
		break
	b.move(bx, by, x, y)
	print('\n', flush=True)

