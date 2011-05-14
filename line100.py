from game import *
from tty_player import *
from computer_player import *

class ConsoleBoardRenderer(object):
	def render_board(self, game):
		for row in range(game.board.NUM_ROWS-1, -1, -1):
			row_strings = []
			for col in range(game.board.NUM_COLUMNS):
				owner = game.board.get_piece_at(col,row)
				if owner == None:
					row_strings.append(".")
				else:
					row_strings.append(game.players[owner].token)
			print "".join(row_strings)

class ConsoleRunner(object):
	renderer = ConsoleBoardRenderer()

	def run(self, args=None):
		game = self.setup_game(args)

		while not game.is_over():
			move = game.current_player().get_move(game)
			game.record_move(move)

		self.show_results(game)
	
	def setup_game(self, args):
		strategy = RandomStrategy()
		players = [ TtyPlayer("JACE", "X", self.renderer), ComputerPlayer(strategy, "O") ]
		return Game(players)

	def show_results(self, game):
		self.renderer.render_board(game)
		print
		if game.is_draw():
			print " === DRAW === "
		elif game.is_won():
			print " === " + game.winner.name + " IS THE WINNER === "
		print

if __name__ == "__main__":
	runner = ConsoleRunner()
	runner.run()

