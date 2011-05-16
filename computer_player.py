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

class TreeSearchStrategy(object):
    name_format = "TreeSearch(%d)"

    def __init__(self, lookahead, heuristic):
        self.lookahead = lookahead
        self.heuristic = heuristic
        self.name = self.name_format % lookahead
        self.rng = Random()

    def get_move(self, game):
        start = datetime.now()

        scores = []
        available_moves = game.get_legal_moves()
        for move in available_moves:
            scores.append((self.get_score(game, move), move))

        chosen_move = self.choose_move(scores)

        end = datetime.now()
        elapsed = end - start

        print
        print "After deliberating for " + str(elapsed) + ", " + self.name + " scores his moves as follows:"
        print "  (" + ",".join([str(score) for score, move in scores]) + ")"
        print "  And chooses: " + str(chosen_move)
        print

        return chosen_move

    def choose_move(self, scores):
        best_score = -INF
        best_moves = []
        for score, move in scores:
            if score > best_score:
                best_score = score
                best_moves = [ move ]
            elif score == best_score:
                best_moves.append(move)

        return self.rng.choice(best_moves)

    def get_score(self, game, move):
        pass


class NegaMaxStrategy(TreeSearchStrategy):
    name_format = "NegaMax(%d)"

    def get_score(self, game, move):
        return -self.negamax(game, move, self.lookahead)

    def negamax(self, game, move, lookahead):
        game.record_move(move)

        if game.is_over() or lookahead <= 0:
            score = self.heuristic.score(game, lookahead)
            game.rollback(1)
            return score

        alpha = -INF

        for child_move in game.get_legal_moves():
            alpha = max(alpha, -self.negamax(game, child_move, lookahead - 1))

        game.rollback(1)
        return alpha


class NegaMaxWithAlphaBetaPruningStrategy(TreeSearchStrategy):
    name_format = "NegaMaxAB(%d)"

    def get_score(self, game, move):
        return -self.negamax(game, move, self.lookahead, -INF, INF)

    def negamax(self, game, move, lookahead, alpha, beta):
        game.record_move(move)

        if game.is_over() or lookahead <= 0:
            score = self.heuristic.score(game, lookahead)
            game.rollback(1)
            return score

        for child_move in game.get_legal_moves():
            alpha = max(alpha, -self.negamax(game, child_move, lookahead - 1, -beta, -alpha))
            if alpha >= beta:
                break

        game.rollback(1)
        return alpha

class NegaScoutStrategy(TreeSearchStrategy):
    name_format = "NegaScout(%d)"

    def get_score(self, game, move):
        return -self.negascout(game, move, self.lookahead, -INF, INF)

    def negascout(self, game, move, lookahead, alpha, beta):
        game.record_move(move)

        if game.is_over() or lookahead <= 0:
            score = self.heuristic.score(game, lookahead)
            game.rollback(1)
            return score

        b = beta
        i = 0

        for child_move in game.get_legal_moves():
            i += 1
            a = -self.negascout(game, child_move, lookahead - 1, -b, -alpha)
            if alpha < a < beta and i > 1:
                a = -self.negascout(game, child_move, lookahead - 1, -beta, -alpha)
            alpha = max(alpha, a)
            if alpha >= beta:
                break
            b = alpha + 1
        
        game.rollback(1)
        return alpha


class NaiveHeuristic(object):
    def score(self, game, lookahead):
        raw_score = 0
        if game.is_won():
            #I just lost... poop
            raw_score -= 1000

        # scale scores by lookahead to discourage apathy.
        # makes distant losses better than near term ones
        # and near term wins better than distant ones
        coeff = (lookahead + 4) * 0.25
        return coeff * raw_score
