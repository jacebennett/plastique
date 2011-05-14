import unittest
from game import Game

class PlayerStub(object):
	"Stub"

class GameTests(unittest.TestCase):
	def test_player_toggling(self):
		player1, player2 = PlayerStub(), PlayerStub()
		self.assertNotEqual(player1, player2)
		
		game = Game([player1, player2])
		self.assertEqual(game.current_player(), player1)

		game.toggle_player()
		self.assertEqual(game.current_player(), player2)

	def test_recording_a_move_should_apply_the_move_to_the_board(self):
		player1, player2 = PlayerStub(), PlayerStub()
		game = Game([player1, player2])

		game.record_move(3)
		self.assertEqual(game.board.get_piece_at(3,0), 0)
	
	def test_recording_a_move_should_log_it_in_history(self):
		player1, player2 = PlayerStub(), PlayerStub()
		game = Game([player1, player2])
		
		self.assertEqual(len(game.history), 0)

		game.record_move(3)
		
		self.assertEqual(len(game.history), 1)
		self.assertEqual(game.last_move(), (3,0))

		game.record_move(4)
	
		self.assertEqual(len(game.history), 2)
		self.assertEqual(game.last_move(), (4,0))

	def test_recording_a_move_should_toggle_the_player(self):
		player1, player2 = PlayerStub(), PlayerStub()
		game = Game([player1, player2])
		
		self.assertEqual(game.current_player(), player1)

		game.record_move(3)

		self.assertEqual(game.current_player(), player2)
	
	def test_rolling_back_moves_should_remove_them_from_the_board(self):
		player1, player2 = PlayerStub(), PlayerStub()
		game = Game([player1, player2])
		game.record_move(3)
		
		game.rollback(1)

		self.assertEqual(game.board.get_piece_at(3,0), None)
	
	def test_rolling_back_a_move_should_remove_it_from_history(self):
		player1, player2 = PlayerStub(), PlayerStub()
		game = Game([player1, player2])
		game.record_move(3)
		
		game.rollback(1)
		
		self.assertEqual(len(game.history), 0)

	def test_rolling_back_a_move_should_toggle_the_player(self):
		player1, player2 = PlayerStub(), PlayerStub()
		game = Game([player1, player2])
		game.record_move(3)
		
		self.assertEqual(game.current_player(), player2)

		game.rollback(1)
		
		self.assertEqual(game.current_player(), player1)

	def test_undo_should_rollback_2_plays(self):
		player1, player2 = PlayerStub(), PlayerStub()
		game = Game([player1, player2])
		
		game.record_move(3)
		game.record_move(4)

		game.undo()

		self.assertEqual(game.board.get_piece_at(3,0), None)
		self.assertEqual(len(game.history), 0)
