MAX_COLUMN_SIZE=6
NUM_COLUMNS=7

PLAYER_PIECE = '0'
COMPUTER_PIECE = '1'

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



def victory(board):
	return False

board = GameBoard()
board.render()

while(victory(board) != True):
	command = raw_input("Which column (1-7, q=quit)? ")
	if(command == "q"):
		exit()
	elif(command.isdigit()):
		col = int(command)
		if col < 1 or col > 7:
			print "please choose a number between 1 and 7"
		else:
			board.add_piece(PLAYER_PIECE, col-1)
			board.render()
	else:
		print "Unknown command"
