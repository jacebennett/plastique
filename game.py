from gameboard import *

PLAYER1 = 0
PLAYER2 = 1

class Game(object):
	board = GameBoard()
	current_player = PLAYER1
	history = []
	winner = None

	def __init__(self, players):
		self.players = players

	def record_move(self, move):
		self.board.add_piece(self.current_player, move)
		self.history.append( (move, len(self.board.columns[move])-1) )
		if self.check_for_victory():
			self.winner = self.current_player

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
			won = won or [self.board.get_piece_at(x,y) for x,y in group].count(self.current_player) == len(group)
		return won

	def toggle_player(self):
		self.current_player = PLAYER2 if self.current_player == PLAYER1 else PLAYER1

	def get_legal_moves(self):
		return [i for i in range(len(self.board.columns)) if not self.board.column_full(i)]

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
