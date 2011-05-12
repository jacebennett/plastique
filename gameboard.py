MAX_COLUMN_SIZE=6
NUM_COLUMNS=7

PLAYER1 = '0'
PLAYER2 = '1'

class GameBoard(object):
	def __init__(self):
		self.columns = [];
		for i in range(NUM_COLUMNS):
			self.columns.append([])


	def add_piece(self, pieceType, column_index):
		self.columns[column_index].append(pieceType)

	
	def render(self):
		for row in range(5, -1, -1):
			row_strings = []
			for col in range(NUM_COLUMNS):
				if len(self.columns[col]) > row:
					row_strings.append(self.columns[col][row])
				else:
					row_strings.append(".")
			print "".join(row_strings)


class Game(object):
	def __init__(self, players):
		self.board = GameBoard()
		self.players = players
		self.current_player = PLAYER1

	def run(self):
		while(not self.is_over()):
			move = self.players[self.current_player].get_move(self)
			self.play(move)

	def play(self, move):
		self.board.add_piece(self.current_player, move)
		self.toggle_player()

	def toggle_player(self):
		self.current_player = PLAYER2 if self.current_player == PLAYER1 else PLAYER1

	def get_legal_moves(self):
		result = []
		for i in range(len(self.board.columns)):
			if(len(self.board.columns[i]) < MAX_COLUMN_SIZE):
				result.append(i)
		return result
	
	def has_victor(self):
		return False

	def is_draw(self):
		return len(self.get_legal_moves()) == 0 and not self.has_victor()

	def is_over(self):
		return self.has_victor() or self.is_draw()

from random import Random

class ComputerPlayer(object):
	def __init__(self):
		self.rng = Random()

	def get_move(self, game):
		move = self.rng.choice(game.get_legal_moves())
		print
		print "Computer plays in column " + str(move + 1)
		print
		return move


class HumanPlayer(object):
	def get_move(self, game):
		game.board.render()
		while(True):
			command = raw_input("Which column (1-7, q=quit)? ")
			if(command == "q"):
				exit()
			elif(command.isdigit()):
				col = int(command) - 1
				if game.get_legal_moves().count(col) > 0:
					return col
				else:
					print command + " is not a legal move"
			else:
				print "Unknown command"

if __name__ == "__main__":
	players = { PLAYER1: HumanPlayer(), PLAYER2: ComputerPlayer() }
	game = Game(players)
	
	game.run()

	game.board.render()
	print
	if game.is_draw():
		print " === DRAW === "
	elif game.has_victor():
		print " === " + game.current_player + " IS THE WINNER === "
	print

