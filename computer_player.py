from random import Random

class ComputerPlayer(object):
	def __init__(self, strategy, token):
		self.name = "COMPUTER(%s)" % strategy.name
		self.token = token
		self.strategy = strategy

	def get_move(self, game):
		return self.strategy.get_move(game)

class RandomStrategy(object):
	name = "Random"
	rng = Random()
	
	def get_move(self, game):
		return self.rng.choice(game.get_legal_moves())

class MinimaxStrategy(object):
	def get_move(self, game):
		"Magic happens here"
