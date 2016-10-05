from player import netPlayer, humanPlayer, montePlayer
from board import Board

from flask import Flask, render_template

app = Flask(__name__)





layers = [90,90,90]
b = Board()



p2 = montePlayer(layers=layers)

p2.load('monte')
p2.net.set_board(b)



def conv(num):
	if num == 0:
		return " "
	elif num == 1:
		return 'X'
	else:
		return 'O'

@app.route('/')
def start():
	global b, p2, layers

	b.reset()

	p2.clear()

	return render_template('main.html', state = b.state, conv=conv, last=[None, None])

@app.route('/<int:bx>/<int:by>/<int:x>/<int:y>')
def index(bx, by, x, y):

	if b.valid_move(bx, by, x, y) == False:
		return render_template('main.html', state=b.state, conv=conv, last=b.last_move)

	if b.move(bx, by, x, y)== True:
		return render_template('winner.html', state=b.state, conv=conv, last=b.last_move)
	bx, by, x, y = p2.move(b.valid_move, b.get_state())
	if b.move(bx, by, x, y) == True:
		return render_template('loser.html', state=b.state, conv=conv, last=b.last_move)




	return render_template('main.html', state = b.state, conv = conv, last=b.last_move)

app.run(debug=True)

#
# while True:
#
# 	b.print()
# 	bx, by, x, y = p1.move(b.valid_move, b.get_state())
# 	if x == None:
# 		p2.clear()
# 		b.reset()
# 		break
#
# 	b.move(bx, by, x, y)
# 	if b.winner != None:
#
# 		p2.train(20)
#
# 		p2.clear()
# 		b.reset()
#
#
# 	b.print()
# 	bx, by, x, y = p2.move(b.valid_move, b.get_state())
# 	if x == None:
# 		b.reset()
# 		p2.clear()
# 		break
# 	b.move(bx, by, x, y)
# 	print('\n', flush=True)

