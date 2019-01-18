import sys
sys.path.append('/home/toby/tictak/util')
sys.path.append('/home/toby/tictak/refLearn')
from RLclasses import *
from Util import *
import random


class RLplayer:

    
    def __init__(self, number, learn_rate, explore_rate):

        self.number = number
        self.board = None
        self.valueTable = ValueTable(number)
        self.gameData = GameData(self.valueTable, number)
        self.learn_rate = learn_rate
        self.explore_rate = explore_rate
        self.game_num = 0
        self.win_num = 0

    
    def changeRates(self,learn_rate=None, explore_rate=None):

        if learn_rate != None:
            self.learn_rate = learn_rate
        if explore_rate != None:
            self.explore_rate = explore_rate

    def getWinPer(self):

        return self.win_num/self.game_num

    # takes in new board, and resets gL
    def update_board(self, board):
        self.board = board
        self.gameData.clear(self.valueTable)
        self.game_num += 1
    

    def final_state_helper(self):
        
        #get last gamestate if lost
        if self.number + 1 != self.board.won and self.board.tie == False:
            self.gameData.update(board=self.board.tic)
        #get last gamestate if tie and player was not last to play
        if self.board.tie == True and (self.board.tic not in self.gameData.boards()):
            self.gameData.update(board=self.board.tic)

        
    #updates all of the values in val_tab after game is finished
    def update_values(self):

        #getting final state for the loser
        self.final_state_helper()

        if self.board.won == self.number + 1:
            self.win_num += 1


        preValue = self.gameData.currentLast().value
        toUpdate = self.gameData.toUpdate()

        for i in range(len(toUpdate)-1, -1, -1):

            new_value = toUpdate[i].value + self.learn_rate * (preValue - toUpdate[i].value)
            self.valueTable.updateValue(toUpdate[i].symboard, new_value)
            preValue = self.valueTable.getValue(toUpdate[i].symboard)


    # returns the next move being random with probablity explore_rate, or maximize with 1 - expolore_rate
    def play(self):

        # first update gameData with the last play
        if len(self.gameData) > 1 or self.number == 1:
            self.gameData.update(board=self.board.tic)

        # for the second player
        p_type = bin_random(self.explore_rate)
                
        if p_type:
            random_move = self.random_square()
            self.gameData.update(move=random_move)
            
            return random_move

        if not p_type:
            max_move = self.max_square()
            self.gameData.update(move=max_move)
            return max_move

    
    # returns completely random square that can be played from the current board
    def random_square(self):

        to_choose = self.board.unoccupied()
        new_square = random.choice(to_choose)
        return new_square

    # returns square with highest value
    def max_square(self):

        to_choose = self.board.unoccupied()

        values = []
        # get all of the values of possible next states
        for square in to_choose:

            value = self.valueTable.getValue(search_equiv(get_move_update(self.board.tic, square, self.number),self.valueTable)[0])
            values.append(value)

        # return the square that creates max value
        return to_choose[values.index(max(values))]