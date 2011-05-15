from random import Random
from datetime import datetime

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


INF = 10000000

class MinimaxStrategy(object):
    name = "Minimax"

    def get_move(self, game):
        start = datetime.now()
        scores = []
        available_moves = game.get_legal_moves()
        for move in available_moves:
            scores.append((-self.score_move(game, move, 5), move))

        end = datetime.now()
        elapsed = end - start
        print
        print "After deliberating for " + str(elapsed) + ", Computer scores his moves as follows:"
        for score, move in scores:
            print "\t" + str(move) + ": " + str(score)
        print

        best = -INF
        for score, move in scores:
            if score >= best:
                best = score
                chosen_move = move

        return chosen_move

    def score_move(self, game, move, lookahead):
        game.record_move(move)

        if game.is_over() or lookahead <= 0:
            score = self.heuristic_score(game)
            game.rollback(1)
            return score

        alpha = -INF

        for child_move in game.get_legal_moves():
            child_score = self.score_move(game, child_move, lookahead - 1)
            alpha = max(alpha, -child_score)
        
        game.rollback(1)
        return alpha

    def heuristic_score(self, game):
        if game.is_won():
            return -999
        if game.is_draw():
            return 100
        return 0



