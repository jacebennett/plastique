MAX_COLUMN_SIZE=6
NUM_COLUMNS=7

PLAYER1 = 0
PLAYER2 = 1

class GameBoard(object):
	def __init__(self):
		self.columns = [];
		for i in range(NUM_COLUMNS):
			self.columns.append([])

	def add_piece(self, pieceType, column_index):
		if len(self.columns[column_index]) >= MAX_COLUMN_SIZE:
			"How should I throw?"
		self.columns[column_index].append(pieceType)
	
	def remove_last_piece_in(self, column_index):
		if len(self.columns[column_index]) == 0:
			"How should I throw?"
		self.columns[column_index].pop()
	
	def render(self):
		for row in range(5, -1, -1):
			row_strings = []
			for col in range(NUM_COLUMNS):
				if len(self.columns[col]) > row:
					row_strings.append(str(self.columns[col][row]))
				else:
					row_strings.append(".")
			print "".join(row_strings)

class Game(object):
	def __init__(self, players):
		self.board = GameBoard()
		self.players = players
		self.current_player = PLAYER1
		self.history = []
		self.winner = None

	def play(self):
		while not self.is_over():
			move = self.players[self.current_player].get_move(self)
			self.record_move(move)
			self.check_for_victory()
			self.toggle_player()
	
	def record_move(self, move):
		self.board.add_piece(self.current_player, move)
		self.history.append(move)

	def undo(self):
		if len(self.history) < 2:
			"How should I throw?"
		self.rollback(2)

	def rollback(self, count):
		for i in range(count):
			col = self.history.pop()
			self.board.remove_last_piece_in(col)
			self.toggle_player()

	def check_for_victory(self):
		"Not Implemented"

	def toggle_player(self):
		self.current_player = PLAYER2 if self.current_player == PLAYER1 else PLAYER1

	def get_legal_moves(self):
		result = []
		for i in range(len(self.board.columns)):
			if len(self.board.columns[i]) < MAX_COLUMN_SIZE:
				result.append(i)
		return result
	
	def last_move(self):
		return self.history[-1]

	def is_won(self):
		return self.winner != None

	def is_draw(self):
		return len(self.get_legal_moves()) == 0 and not self.is_won()

	def is_over(self):
		return self.is_won() or self.is_draw()

from random import Random

class ComputerPlayer(object):
	def __init__(self):
		self.rng = Random()

	def get_move(self, game):
		return self.rng.choice(game.get_legal_moves())

class HumanPlayer(object):
	def get_move(self, game):
		if len(game.history) > 0:
			print
			print "Computer played in column " + str(game.last_move() + 1)
			print
		game.board.render()
		print
		while(True):
			command = raw_input("Which column (1-7, q=quit, u=undo)? ")
			if command == "q":
				exit()
			if command == "u":
				if len(game.history) < 2:
					print "Nothing to undo"
				else:
					game.undo()
					print
					game.board.render()
					print
			elif command.isdigit():
				col = int(command) - 1
				if game.get_legal_moves().count(col) > 0:
					return col
				else:
					print command + " is not a legal move"
			else:
				print "Unknown command"

if __name__ == "__main__":
	players = [ HumanPlayer(), ComputerPlayer() ]
	game = Game(players)
	
	game.play()

	game.board.render()
	print
	if game.is_draw():
		print " === DRAW === "
	elif game.is_won():
		print " === " + game.winner + " IS THE WINNER === "
	print

