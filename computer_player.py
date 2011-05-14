
from random import Random

class ComputerPlayer(object):
	rng = Random()

	def get_move(self, game):
		return self.rng.choice(game.get_legal_moves())

