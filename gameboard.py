NUM_ROWS=6
NUM_COLUMNS=7

PLAYER1 = 0
PLAYER2 = 1

class GameBoard(object):
	def __init__(self):
		self.columns = [];
		for i in range(NUM_COLUMNS):
			self.columns.append([])

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
			if self.check_for_victory():
				self.winner = self.current_player
			else:
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
		won = False
		for group in self.possible_winning_groups_containing(self.last_move()):
			won = won or [self.board.get_piece_at(x,y) for x,y in group].count(self.current_player) == len(group)
		return won

	def toggle_player(self):
		self.current_player = PLAYER2 if self.current_player == PLAYER1 else PLAYER1

	def get_legal_moves(self):
		return [i for i in range(len(self.board.columns)) if not self.board.column_full(i)]

	def last_move(self):
		col = self.history[-1]
		row = len(self.board.columns[col]) - 1
		return (col,row)

	def is_won(self):
		return self.winner != None

	def is_draw(self):
		return len(self.get_legal_moves()) == 0 and not self.is_won()

	def is_over(self):
		return self.is_won() or self.is_draw()

	def possible_winning_groups_containing(self,element):
		return [group for group in self.all_possible_winning_groups() if group.count(element) > 0]

	def all_possible_winning_groups(self):
		NUM_COLUMNS = 7
		NUM_ROWS = 6
		GROUP_SIZE = 4

		V_HEADROOM = NUM_ROWS - GROUP_SIZE
		H_HEADROOM = NUM_COLUMNS - GROUP_SIZE

		base_vertical_group = [(0,i) for i in range(GROUP_SIZE)]
		base_horizontal_group = [(i,0) for i in range(GROUP_SIZE)]
		base_diagonal_group_ne = [(i,i) for i in range(GROUP_SIZE)]
		base_diagonal_group_nw = [(i, (GROUP_SIZE-1) - i) for i in range(GROUP_SIZE)]

		max_offsets_for_vertical_groups = (NUM_COLUMNS-1, V_HEADROOM)
		max_offsets_for_horizontal_groups = (H_HEADROOM, NUM_ROWS-1)
		max_offsets_for_diagonal_groups = (H_HEADROOM, V_HEADROOM)

		winning_group_definitions = [ 
			(base_vertical_group, max_offsets_for_vertical_groups),
			(base_horizontal_group, max_offsets_for_horizontal_groups),
			(base_diagonal_group_ne, max_offsets_for_diagonal_groups),
			(base_diagonal_group_nw, max_offsets_for_diagonal_groups),
			]

		return [
			[(x + dx, y + dy) for x,y in base_group]
			for base_group, max_offset in winning_group_definitions
			for dx in range(max_offset[0]+1)
			for dy in range(max_offset[1]+1)
			]

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
			print "Computer played in column " + str(game.last_move()[0] + 1)
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
		print " === " + str(game.winner) + " IS THE WINNER === "
	print

