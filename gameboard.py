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



