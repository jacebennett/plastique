from gameboard import *

GROUP_SIZE = 4

PLAYER1 = 0
PLAYER2 = 1

class Game(object):
	def __init__(self, players):
		self.board = GameBoard()
		self.current_player_index = PLAYER1
		self.history = []
		self.winner = None
		self.players = players
	
	def current_player(self):
		return self.players[self.current_player_index]

	def record_move(self, column):
		final_position = self.board.add_piece(self.current_player_index, column)
		self.history.append(final_position)
		if self.check_for_victory():
			self.winner = self.current_player()
		else:
			self.toggle_player()

	def undo(self):
		if len(self.history) < 2:
			"How should I throw?"
		self.rollback(2)

	def rollback(self, count):
		for i in range(count):
			col,row = self.history.pop()
			self.board.remove_last_piece_in(col)
			self.toggle_player()

	def check_for_victory(self):
		won = False
		for group in self.possible_winning_groups_containing(self.last_move()):
			won = won or [self.board.get_piece_at(x,y) for x,y in group].count(self.current_player_index) == len(group)
		return won

	def toggle_player(self):
		self.current_player_index = PLAYER2 if self.current_player_index == PLAYER1 else PLAYER1

	def get_legal_moves(self):
		return [i for i in range(self.board.NUM_COLUMNS) if not self.board.column_full(i)]

	def last_move(self):
		return self.history[-1]

	def is_won(self):
		return self.winner != None

	def is_draw(self):
		return len(self.get_legal_moves()) == 0 and not self.is_won()

	def is_over(self):
		return self.is_won() or self.is_draw()

	def possible_winning_groups_containing(self,element):
		return [group for group in self.all_possible_winning_groups() if group.count(element) > 0]

	def all_possible_winning_groups(self):
		V_HEADROOM = self.board.NUM_ROWS - GROUP_SIZE
		H_HEADROOM = self.board.NUM_COLUMNS - GROUP_SIZE

		base_vertical_group = [(0,i) for i in range(GROUP_SIZE)]
		base_horizontal_group = [(i,0) for i in range(GROUP_SIZE)]
		base_diagonal_group_ne = [(i,i) for i in range(GROUP_SIZE)]
		base_diagonal_group_nw = [(i, (GROUP_SIZE-1) - i) for i in range(GROUP_SIZE)]

		max_offsets_for_vertical_groups = (self.board.NUM_COLUMNS-1, V_HEADROOM)
		max_offsets_for_horizontal_groups = (H_HEADROOM, self.board.NUM_ROWS-1)
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
