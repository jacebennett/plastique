
class HumanPlayer(object):
	def get_move(self, game):
		if len(game.history) > 0:
			print
			print "Computer played in column " + str(game.last_move()[0] + 1)
			print
		game.board.render()
		print
		while(True):
			command = raw_input("Which column (1-7, q=quit, u=undo)? ")
			if command == "q":
				exit()
			elif command == "u":
				if len(game.history) < 2:
					print "Nothing to undo"
				else:
					game.undo()
					print
					game.board.render()
					print
			elif command.isdigit():
				col = int(command) - 1
				if game.get_legal_moves().count(col) > 0:
					return col
				else:
					print command + " is not a legal move"
			else:
				print "Unknown command"
