import unittest
import gameboard

class GameBoardTests(unittest.TestCase):
	def test_playing_the_first_piece(self):
		g = gameboard.GameBoard()
		g.add_piece(gameboard.PLAYER1, 1)
		
		column_sizes = map((lambda c: len(c)), g.columns)

		self.assertEqual(column_sizes, [0,1,0,0,0,0,0])
