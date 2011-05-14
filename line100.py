from game import *
from tty_player import *
from computer_player import *

class ConsoleRunner(object):
	def run(self, args=None):
		game = self.setup_game(args)

		while not game.is_over():
			move = game.players[game.current_player].get_move(game)
			game.record_move(move)
			game.toggle_player()

		self.show_results(game)
	
	def setup_game(self, args):
		players = [ HumanPlayer(), ComputerPlayer() ]
		return Game(players)

	def show_results(self, game):
		game.board.render()
		print
		if game.is_draw():
			print " === DRAW === "
		elif game.is_won():
			print " === " + str(game.winner) + " IS THE WINNER === "
		print

if __name__ == "__main__":
	runner = ConsoleRunner()
	runner.run()

