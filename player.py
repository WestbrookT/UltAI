import random
from keras.models import Sequential
from keras.layers import Dense
from numpy import array
import json, pickle
from time import sleep

class player:

	history = []

	def set_board(self, b):
		self.board = b
	def __init__(self, layers=None):
		pass

	def train(self, moves=30):
		pass

	def move(self, validator, state):



		pass

	def valid_board_list(self):
		boards = self.board.valid_boards()

		temp = []

		for i, val in enumerate(boards):
			if val == 1:
				row = int(i / 3)
				col = i%3
				temp.append([col, row])

		return temp


class randPlayer(player):

	def __init__(self):
		super().__init__(None)

	def move(self, validator, state=None):
		if len(self.valid_board_list()) == 0:
			return [None] * 4
		valid_boards = self.valid_board_list()
		if len(valid_boards) == 0:
			print(valid_boards)
			print(self.valid_board_list())
			print(self.board.gameboard)

		bx, by = valid_boards[random.randint(0, len(valid_boards)-1)]
		current_board = self.board.state[bx][by]
		temp = []

		for row in range(0, 3):
			for col in range(0, 3):
				if current_board[col][row] == 0:
					temp.append([col, row])
		if len(temp) == 0:
			print(current_board)
			print(valid_boards)
			print(self.board.valid_boards())
			print(self.board.last_move)
			print(bx, by)
			self.board.print()
		x, y = temp[random.randint(0, len(temp)-1)]
		return bx, by, x, y


class netPlayer(player):

	moves = 0

	def __init__(self, layers):
		super().__init__(layers)

		self.model = Sequential()
		self.model.add(Dense(input_dim=90, output_dim=layers[0], activation='tanh'))

		for layer in layers[1:]:
			self.model.add(Dense(output_dim=layer, activation='tanh'))

		self.model.add((Dense(output_dim=18, activation='tanh')))

		self.model.compile(optimizer='RMSprop', loss='mse')

	def move(self, validator, state=None):
		if len(self.valid_board_list()) == 0:
			return [None]*4



		prediction = self.model.predict(array([state]), batch_size=1)[0]

		bx = 0
		by = 0
		x = 0
		y = 0



		for row in range(0, 3):
			for col in range(0, 3):
				if prediction[row *3 + col] > prediction[by * 3 + bx]:
					bx = col
					by = row

		for row in range(0, 3):
			for col in range(0, 3):
				if prediction[row * 3 + col +9] > prediction[y * 3 + x + 9]:
					x = col
					y = row

		if validator(bx, by, x, y):
			pass
		else:
			valid_boards = self.valid_board_list()
			if len(valid_boards) == 0:
				print(valid_boards)
				print(self.valid_board_list())
				print(self.board.gameboard)
				self.board.print()

			bx, by = valid_boards[random.randint(0, len(valid_boards) - 1)]
			current_board = self.board.state[bx][by]
			temp = []
			for row in range(0, 3):
				for col in range(0, 3):
					if current_board[col][row] == 0:
						temp.append([col, row])
			x, y = temp[random.randint(0, len(temp) - 1)]


		newp = []

		for i, val in enumerate(prediction):
			if i == by * 3 + bx or i == y * 3 + x + 9:
				newp.append(1.0)
			else:
				newp.append(val)

		prediction = array(newp)

		self.history.append((array(state), prediction))
		return bx, by, x, y







	def train(self, moves=30, loss=False):

		ins = array([i[0] for i in self.history])


		out = None

		if loss == False:
			out = array([i[1] for i in self.history])
		else:
			out = array([self.invert(i[1], i[0]) for i in self.history])


		self.model.fit(ins, out, nb_epoch=10*(30-moves), batch_size=4, verbose=False)



	def clear(self):
		self.history = []

	def invert(self, answer, state):

		playable_boards = state[-9:]

		played_board = answer[:9]

		small_board = answer[9:]

		index = 0
		for i, val in enumerate(played_board):
			if val == 1.0:
				index = i * 9

		temp = []

		for i, val in enumerate(playable_boards):
			if val == 1.0 and played_board[i] == 1:
				temp.append(0)
			else:
				temp.append(val)

		small_temp = []
		for row in range(0, 3):
			for col in range(0, 3):
				if state[index + row * 3 + col] == 1 and small_board[row * 3 + col] == 1:
					small_temp.append(0)
				else:
					small_temp.append(state[index + row * 3 + col])
		#print(temp+small_temp)
		return array(temp + small_temp)



	def predict(self, state):
		state = array([state])
		prediction = self.model.predict([state], batch_size=1)

		return prediction

	def save(self, filename):

		self.model.save(filename)

	def load(self, filename):

		self.model.load_weights(filename)

class humanPlayer(player):

	def move(self, validator, state):

		temp = input("Col Row, X, Y: ")
		bx, by, x, y = temp.split(' ')
		bx = int(bx)
		by = int(by)
		x = int(x)
		y = int(y)

		while validator(bx, by, x, y) == False:
			bx, by, x, y = input("Col Row, X, Y: ").split(' ')
			bx = int(bx)
			by = int(by)
			x = int(x)
			y = int(y)

		return bx, by, x, y



class montePlayer(player):

	history = []
	net_rate = 1

	def __init__(self, treeFile=None, netFile=None, layers=[1]):
		super().__init__(layers)

		self.net = netPlayer(layers)
		if netFile != None:
			self.net.load(netFile)

		if treeFile != None:
			tree = {}
			with open(treeFile, 'r') as f:
				tree = json.load(f)
			self.tree = tree
		else:
			self.tree = {}
	def move(self, validator, state):
		key = tuple(state)
		bx, by, x, y = None, None, None, None
		if key in self.tree:
			temp = self.get_best(key)
			if temp == None:

				bx, by, x, y = self.net.move(validator, list(state))
				if bx == None:
					return [None]*4

			else:

				bx, by, x, y = temp
		else:
			bx, by, x, y = self.net.move(validator, state)
			if bx == None:
				return [None]*4

		self.history.append((tuple(state), (bx, by, x, y)))

		return bx, by, x, y

	def train(self, moves=30, loss=False):

		if loss == False:
			for i in self.history:
				state = i[0]
				if state not in self.tree:
					self.tree[state] = {}
				if i[1] in self.tree[state]:
					self.tree[state][i[1]][0] += 1
				else:
					self.tree[state][i[1]] = [1, 2]

			self.net_train(moves, loss)

		else:

			for i in self.history:
				state = i[0]
				if state not in self.tree:
					self.tree[state] = {}

				if i[1] in self.tree[state]:
					self.tree[state][i[1]][1] += 1
				else:
					self.tree[state][i[1]] = [2, 1]
			self.net_train(moves, loss)

	def to_net_out(self, bx, by, x, y):

		out = [0]*18

		out[by*3+bx] = 1
		out[y*3+x+9] = 1

		return out

	def net_train(self,moves=10, loss=False):

		history = [(array(list(i[0])), self.to_net_out(i[1][0], i[1][1], i[1][2], i[1][3])) for i in self.history]

		self.net.history = history
		try:
			self.net.train(moves, loss)
		except:
			print(history)


	def clear(self):

		self.history = []
		self.net.clear()



	def get_best(self, key):

		if random.randint(0, 10) >= self.net_rate or key not in self.tree:
			return None

		max = tuple(self.tree[key].keys())[0]

		# i = [wins, losses, (bx, by, x, y)]
		for i, coords in enumerate(self.tree[key]):

			try:
				if self.tree[key][coords][0]/self.tree[key][coords][1] > self.tree[key][max][0]/self.tree[key][max][1]:
					max = coords
			except:
				print(coords, max, self.tree[key])

		return max



	def save(self, filestart):

		with open(filestart+'.pickle', 'wb') as f:

			pickle.dump(self.tree, f)
		self.net.save(filestart+'.h5')

	def load(self, filestart):

		with open(filestart+'.pickle', 'rb') as f:
			self.tree = pickle.load(f)
		self.net.load(filestart+'.h5')












