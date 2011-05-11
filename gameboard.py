MAX_COLUMN_SIZE=6
NUM_COLUMNS=7

class GameBoard(object):
	def __init__(self):
		self.columns = [];
		for i in range(NUM_COLUMNS):
			self.columns.append([])


	def add_piece(self, column_index):
		self.columns[column_index].append(1)
