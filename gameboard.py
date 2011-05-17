class GameBoard(object):
	NUM_ROWS=6
	NUM_COLUMNS=7
	
	def __init__(self):
		self.columns = [[] for i in range(self.NUM_COLUMNS)]
		self.heights = [0 for i in range(self.NUM_COLUMNS)]

	def add_piece(self, pieceType, column_index):
		if self.heights[column_index] >= self.NUM_ROWS:
			raise IndexError("Column full")
		
		self.columns[column_index].append(pieceType)
		self.heights[column_index] += 1
		return (column_index, self.heights[column_index]-1)
	
	def remove_last_piece_in(self, column_index):
		if self.heights[column_index] == 0:
			"How should I throw?"
		self.columns[column_index].pop()
		self.heights[column_index] -= 1
	
	def column_full(self, column_index):
		return self.heights[column_index] >= self.NUM_ROWS
	
	def get_piece_at(self, x, y):
		if self.heights[x] <= y:
			return None
		return self.columns[x][y]




