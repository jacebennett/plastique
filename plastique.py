import sys
from game import *
from tty_player import *
from computer_player import *

PLAYER1_TOKEN = "0"
PLAYER2_TOKEN = "1"

class ConsoleBoardRenderer(object):
    def render_board(self, game):
        for row in range(game.board.NUM_ROWS - 1, -1, -1):
            row_strings = []
            for col in range(game.board.NUM_COLUMNS):
                owner = game.board.get_piece_at(col, row)
                if owner is None:
                    row_strings.append(".")
                else:
                    row_strings.append(game.players[owner].token)
            print "".join(row_strings)


class ConsoleRunner(object):
    renderer = ConsoleBoardRenderer()

    def run(self, args):
        game = self.setup_game(args)

        while not game.is_over():
            move = game.current_player().get_move(game)
            game.record_move(move)

        self.show_results(game)

    def setup_game(self, args):
        mode = ""

        if len(args) > 1:
            mode = args[1].lower()

        if mode == "hard":
            name = raw_input("What's your name? ")
            strategy = NegaScoutStrategy(9, NaiveHeuristic())
            players = [ TtyPlayer(name, PLAYER1_TOKEN, self.renderer), ComputerPlayer(strategy, PLAYER2_TOKEN) ]
        elif mode == "easy":
            name = raw_input("What's your name? ")
            strategy = NegaMaxStrategy(3, NaiveHeuristic())
            players = [ TtyPlayer(name, PLAYER1_TOKEN, self.renderer), ComputerPlayer(strategy, PLAYER2_TOKEN) ]
        elif mode == "cagematch":
            player1strategy = NegaMaxWithAlphaBetaPruningStrategy(3, NaiveHeuristic())
            player2strategy = NegaScoutStrategy(8, NaiveHeuristic())
            players = [ ComputerPlayer(player1strategy, PLAYER1_TOKEN), ComputerPlayer(player2strategy, PLAYER2_TOKEN) ]
        else:
            name = raw_input("What's your name? ")
            strategy = NegaScoutStrategy(7, NaiveHeuristic())
            players = [ TtyPlayer(name, PLAYER1_TOKEN, self.renderer), ComputerPlayer(strategy, PLAYER2_TOKEN) ]

        return Game(players)


    def show_results(self, game):
        self.renderer.render_board(game)
        print
        if game.is_draw():
            print " === DRAW === "
        elif game.is_won():
            print " === " + game.winner.token + " (" + game.winner.name + ") IS THE WINNER === "
        print

if __name__ == "__main__":
    runner = ConsoleRunner()
    runner.run(sys.argv)

