from player import netPlayer, humanPlayer, montePlayer, randPlayer
from board import Board



layers = [90,90,90]
b = Board()


p1s = [randPlayer(), netPlayer(layers=layers)]

p2 = montePlayer(layers=layers)

p2.net_rate = 6


p2.net.set_board(b)

p1s[1].set_board(b)
p1s[0].set_board(b)
count = 0
wins = 0
losses = 0
scratches = 0

def train(player):
	global b
	if b.winner != 1:
		player.train(27, False)
	else:
		player.train(27, True)


while count < 10000:
	p1 = p1s[count%2]

	bx, by, x, y = p1.move(b.valid_move, b.get_state())
	if x == None:
		p2.clear()
		b.reset()
		count += 1
		continue

	done = b.move(bx, by, x, y)
	if done:

		p2.train(27, True)
		losses += 1

		p2.clear()
		b.reset()
		count += 1



	bx, by, x, y = p2.move(b.valid_move, b.get_state())
	if x == None:
		train(p2)
		scratches += 1

		b.reset()
		p2.clear()
		count += 1
		continue
	done = b.move(bx, by, x, y)


	if done and b.winner < 1:
		train(p2)
		wins += 1


		p2.clear()
		b.reset()
		count += 1

	#count += 1

	if count%100 == 0:
		print(wins, losses, scratches, count)
		if count % 1000 == 0:
			p2.save('defender')
			p1s[1].save('attackerNet.h5')
		count += 1

	if count >= 10000:
		p2.save('monte_final1')

		exit()

p2.save('monte_final1')
