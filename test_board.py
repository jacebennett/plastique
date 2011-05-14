import unittest
from gameboard import GameBoard

class GameBoardTests(unittest.TestCase):
	def test_adding_piece_should_return_pieces_final_position(self):
		g = GameBoard()
		result = g.add_piece(0, 3)
		self.assertEqual(result, (3,0))

	def test_adding_pieces_should_places_pieces_in_lowest_unoccupied_cell_in_column(self):
		g = GameBoard()
		g.add_piece(0, 3)
		result = g.add_piece(0, 3)

		self.assertEqual(result, (3, 1))

	def test_testing_for_a_full_column(self):
		g = GameBoard()
		for i in range(g.NUM_ROWS):
			g.add_piece(0, 3)

		self.assertTrue(g.column_full(3))
	
	def test_adding_piece_to_full_column_shoul_throw(self):
		g = GameBoard()

		while not g.column_full(3):
			g.add_piece(0, 3)

		self.assertRaises(IndexError, lambda: g.add_piece(0, 3))

	def test_getting_the_piece_at_a_given_location(self):
		g = GameBoard()

		g.add_piece(0, 3)
		g.add_piece(1, 4)

		self.assertEquals(g.get_piece_at(3,0), 0)
		self.assertEquals(g.get_piece_at(4,0), 1)
		self.assertEquals(g.get_piece_at(5,0), None)
