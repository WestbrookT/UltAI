import pprint

class Board():

	history = []
	state = None
	print_state = False
	last_move = None # (x, y)
	current_player = 1 #1 or -1
	winner = None
	moves = 0

	finished_boards = []
	gameboard = [[None, None, None] for i in range(0, 3)]

	# [board [col1 [small_board [small_col1] ...sb] ...cols] ...board]

	def __init__(self):
		self.state = self.make_board()


	def reset(self):
		self.history = []
		self.state = self.make_board()
		self.print_state = False
		self.last_move = None  # (x, y)
		self.current_player = 1  # 1 or -1
		self.winner = None
		self.moves = 0

		self.finished_boards = []
		self.gameboard = [[None, None, None] for i in range(0, 3)]

	def make_small_board(self):

		return [[0, 0, 0] for i in range(0, 3)]

	def make_col(self):

		return [self.make_small_board() for i in range(0, 3)]

	def make_board(self):
		return [self.make_col() for i in range(0, 3)]

	def print(self, board=None):

		board = self.state if board == None else board
		outs = {1: 'X', -1: 'O', 0: '.'}

		for grow in range(0, 3):
			for row in range(0, 3):
				for gcol in range(0, 3):
					for col in range(0, 3):
						print(outs[self.state[gcol][grow][col][row]], end=' ', flush=True)
					if gcol != 2:
						print(end='| ')

				print(flush=True)
			if grow != 2:
				print( end='-' * 21 + '\n', flush=True)

	def get_state(self):
		#returns a tuple (hashable board state, possible next move locations)

		board_state = [self.state[gcol][grow][col][row] for col in range(0,3) for gcol in range(0, 3) for row in range(0, 3) for grow in range(0, 3)]
		move_state = self.valid_boards()
		try:
			return board_state + move_state
		except:
			pass



	def tup(self, t):

		return tuple(map(self.tup, t)) if isinstance(t, (list, tuple)) else t

	def move(self, bx, by, x, y):
		# coords = (x1, y1, x2, y2)
		self.moves += 1
		if len(self.finished_boards) == 9:
			if self.print_state:
				print('draw')
			self.winner = 0
			return True

		if self.valid_move(bx, by, x, y):
			self.state[bx][by][x][y] = self.current_player

			self.last_move = (x, y)

			if self.board_won(bx, by, x, y):
				self.gameboard[bx][by] = self.current_player
				self.finished_boards.append((bx, by))
				if self.print_state:
					print('board won')

				if self.game_won(bx, by):
					if self.print_state:
						print('game won', self.current_player)
					self.winner = self.current_player
					return True
			elif self.board_filled(bx, by):
				self.finished_boards.append((bx, by))
				self.gameboard[bx][by] = 0


			self.current_player *= -1

			if self.print_state:
				self.print()

			return False
		else:
			return False

	def valid_move(self, bx, by, x, y):

		if (bx, by) not in self.finished_boards:

			if self.last_move in self.finished_boards and self.state[bx][by][x][y] == 0:
				return True

			if self.last_move == None or (bx == self.last_move[0] and by == self.last_move[1]):

				if self.state[bx][by][x][y] == 0:
					return True
		return False

	def valid_boards(self):
		if self.last_move == None:
			return [1 for i in range(0, 9)]

		if self.last_move in self.finished_boards:
			temp = []
			for row in range(0, 3):
				for col in range(0, 3):
					if self.gameboard[col][row] == None:
						temp.append(1)
					else:
						temp.append(0)
			return temp

		out = [0] * 9

		out[self.last_move[1] * 3 + self.last_move[0]] = 1
		return out


	def board_won(self, bx, by, x, y):

		board = self.state[bx][by]

		if board[0][y] == board[1][y] == board [2][y]:
			return True

		#check if previous move caused a win on horizontal line
		if board[x][0] == board[x][1] == board [x][2]:
			return True

		#check if previous move was on the main diagonal and caused a win
		if x == y and board[0][0] == board[1][1] == board [2][2]:
			return True

		#check if previous move was on the secondary diagonal and caused a win
		if x + y == 2 and board[0][2] == board[1][1] == board [2][0]:
			return True

		return False

	def game_won(self, bx, by):
		board = self.gameboard

		#check if previous move caused a win on vertical line
		if board[0][by] == board[1][by] == board [2][by]:
			return True

		#check if previous move caused a win on horizontal line
		if board[bx][0] == board[bx][1] == board [bx][2]:
			return True

		#check if previous move was on the main diagonal and caused a win
		if bx == by and board[0][0] == board[1][1] == board [2][2]:
			return True

		#check if previous move was on the secondarby diagonal and caused a win
		if bx + by == 2 and board[0][2] == board[1][1] == board [2][0]:
			return True

		return False

	def board_filled(self, bx, by):

		board = self.state[bx][by]

		for row in range(0, 3):
			for col in range(0, 3):
				if board[col][row] == 0:
					return False
		return True




