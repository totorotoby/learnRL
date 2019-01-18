import sys
sys.path.append('/home/toby/tictak/util')
from Util import *

class ValueTable:

	"""
	ValueTable is a dictonary with keys as the symmetric equivlences of the tictaktoe board,
	 and values as the updating probabilities of winning a game.
	"""

	def __init__(self, playerNum):
		
		self.table = self.readinBoards(playerNum)
		self.states = self.table.keys()

	def __str__ (self):

		string = ''

		for board, value in self.table.items():
			string += '\nBoard: ' + string_board(board) + 'Value: ' + str(value) + '\n'

		return string

	# function that takes in a board in bits and prints it as string plus its value
	def printValue(self, bits):

		try:
			print('Board: ', string_board(bits), 'Value: ', self.table[bits])

		except KeyError:
			print('Cannot print, Board is not in the symmetry table.')

	# Sets up the table to its intial values
	def readinBoards(self, playerNum):

		table = {}

		filenames = ['refLearn/p0_wins', 'refLearn/all_other_states', 'refLearn/p1_wins']

		to_update = []
		for i in range(3):
			file = open(filenames[i], 'r')
			flist = file.read().split('\n')
			to_update.append(flist)

		vals = [1, .5, 0]
		
		if playerNum == 1:
			to_update.reverse()
		for i in range(3):
			for j in range(len(to_update[i])-1):
				table[int(to_update[i][j])] = vals[i]

		return table


	def getValue(self, bits):

		return self.table[bits]

	def updateValue(self, bits, value):

		self.table[bits] = value


class RLstate:

	def __init__(self, old_board, valueTable, playerNum=None, move=None):

		if playerNum == None and move == None:

			self.board = old_board
			self.move = None
			self.symboard, self.rotation = search_equiv(self.board, valueTable)
			self.value = valueTable.getValue(self.symboard)

		else:
			
			self.board = get_move_update(old_board, move, playerNum)
			self.move = move
			self.symboard, self.rotation = search_equiv(self.board, valueTable)
			self.value = valueTable.getValue(self.symboard)


class GameData:

	def __init__(self, valTable, pn):
		
		self.gL = [RLstate(0, valTable)]
		self.currentBoard = self.gL[len(self.gL)-1].board
		self.valTable = valTable
		self.playerNum = pn

	def __str__(self):

		string = ''

		count = 0

		for entry in self.gL:
			string += '----------------------------\n'
			string += 'move: ' + str(count) + '\n'
			string += 'board: ' + string_board(entry.board) + '\n'
			string += 'value: ' + str(entry.value) + '     rotation: ' + str(entry.rotation) + '\n'
			count += 1

		return string


	def __len__(self):

		return len(self.gL)

	def boards(self):

		return [entry.board for entry in self.gL]

	def update(self, move=None, board=None):


		if board == None:
			newState = RLstate(self.currentBoard, self.valTable, self.playerNum, move)
			self.gL.append(newState)
			self.currentBoard = self.gL[len(self.gL)-1].board

		if move == None:

			newState = RLstate(board, self.valTable)
			self.gL.append(newState)
			self.currentBoard = self.gL[len(self.gL)-1].board

	def clear(self, valTable):

		self.gL = [RLstate(0, self.valTable)]
		self.currentBoard = self.gL[len(self.gL)-1].board
		self.valueTable = valTable


	def currentLast(self):

		return self.gL[len(self.gL)-1]

	def toUpdate(self):

		return self.gL[:len(self.gL)-1]