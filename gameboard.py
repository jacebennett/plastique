MAX_COLUMN_SIZE=6
NUM_COLUMNS=7

PLAYER = '0'
COMPUTER = '1'

class GameBoard(object):
	def __init__(self):
		self.columns = [];
		for i in range(NUM_COLUMNS):
			self.columns.append([])


	def add_piece(self, pieceType, column_index):
		self.columns[column_index].append(pieceType)

	
	def render(self):
		for h in range(5, -1, -1):
			row_str = ''
			for w in range(NUM_COLUMNS):
				if len(self.columns[w]) > h:
					row_str += self.columns[w][h]
				else:
					row_str += "."
			print row_str


class Game(object):
	def __init__(self):
		self.board = GameBoard()
		self.current_player = PLAYER

	def play(self, player, move):
		self.board.add_piece(player, move)
		self.toggle_player()

	def toggle_player(self):
		self.current_player = COMPUTER if self.current_player == PLAYER else PLAYER

	def get_legal_moves(self):
		result = []
		for i in range(len(self.board.columns)):
			if(len(self.board.columns[i]) < MAX_COLUMN_SIZE):
				result.append(i)
		return result
	
	def has_victor(self):
		return False

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
					print str(col) + " is not a legal move"
			else:
				print "Unknown command"

if __name__ == "__main__":
	game = Game()
	player = HumanPlayer()
	opponent = ComputerPlayer()

	while(game.has_victor != True):
		if game.current_player == PLAYER:
			move = player.get_move(game)
			game.play(PLAYER, move)
		else:
			move = opponent.get_move(game)
			game.play(COMPUTER, move)


