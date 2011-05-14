import unittest
from game import Game

class PlayerStub(object):
	"Stub"


player1, player2 = PlayerStub(), PlayerStub()

class GameTests(unittest.TestCase):
	def setUp(self):
		self.game = Game([player1, player2])

	def tearDown(self):
		self.game = None

	def test_player_toggling(self):
		self.assertNotEqual(player1, player2)
		self.assertEqual(self.game.current_player(), player1)

		self.game.toggle_player()
		
		self.assertEqual(self.game.current_player(), player2)

		self.game.toggle_player()
		
		self.assertEqual(self.game.current_player(), player1)

	def test_recording_a_move_should_apply_the_move_to_the_board(self):
		self.game.record_move(3)
		self.assertEqual(self.game.board.get_piece_at(3,0), 0)
	
	def test_recording_a_move_should_log_it_in_history(self):
		self.assertEqual(len(self.game.history), 0)

		self.game.record_move(3)
		
		self.assertEqual(len(self.game.history), 1)
		self.assertEqual(self.game.last_move(), (3,0))

		self.game.record_move(4)
	
		self.assertEqual(len(self.game.history), 2)
		self.assertEqual(self.game.last_move(), (4,0))

	def test_recording_a_move_should_toggle_the_player(self):
		self.assertEqual(self.game.current_player(), player1)

		self.game.record_move(3)

		self.assertEqual(self.game.current_player(), player2)
	
	def test_rolling_back_moves_should_remove_them_from_the_board(self):
		self.game.record_move(3)
		
		self.game.rollback(1)

		self.assertEqual(self.game.board.get_piece_at(3,0), None)
	
	def test_rolling_back_a_move_should_remove_it_from_history(self):
		self.game.record_move(3)
		
		self.game.rollback(1)
		
		self.assertEqual(len(self.game.history), 0)

	def test_rolling_back_a_move_should_toggle_the_player(self):
		self.game.record_move(3)
		
		self.assertEqual(self.game.current_player(), player2)

		self.game.rollback(1)
		
		self.assertEqual(self.game.current_player(), player1)

	def test_undo_should_rollback_2_plays(self):
		self.game.record_move(3)
		self.game.record_move(4)

		self.game.undo()

		self.assertEqual(self.game.board.get_piece_at(3,0), None)
		self.assertEqual(len(self.game.history), 0)

	def test_undo_should_fail_on_current_players_first_move(self):
		self.assertRaises(IndexError, lambda: self.game.undo())

	def test_should_detect_victory(self):
		self.game.record_move(3) #Player 1
		self.game.record_move(6) #Player 2
		self.game.record_move(2) #Player 1
		self.game.record_move(6) #Player 2
		self.game.record_move(1) #Player 1
		self.game.record_move(6) #Player 2

		self.assertFalse(self.game.is_won())

		self.game.record_move(0) #Player 1

		self.assertTrue(self.game.is_won())
		self.assertEqual(self.game.winner, player1)


