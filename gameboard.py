NUM_ROWS=6
NUM_COLUMNS=7
GROUP_SIZE = 4

class GameBoard(object):
	columns = [[] for i in range(NUM_COLUMNS)]

	def add_piece(self, pieceType, column_index):
		if len(self.columns[column_index]) >= NUM_ROWS:
			"How should I throw?"
		self.columns[column_index].append(pieceType)
	
	def remove_last_piece_in(self, column_index):
		if len(self.columns[column_index]) == 0:
			"How should I throw?"
		self.columns[column_index].pop()
	
	def column_full(self, column_index):
		return len(self.columns[column_index]) >= NUM_ROWS
	
	def get_piece_at(self, x, y):
		if not len(self.columns[x]) > y:
			return None
		return self.columns[x][y]

	def render(self):
		for row in range(NUM_ROWS-1, -1, -1):
			row_strings = []
			for col in range(NUM_COLUMNS):
				if len(self.columns[col]) > row:
					row_strings.append(str(self.columns[col][row]))
				else:
					row_strings.append(".")
			print "".join(row_strings)



