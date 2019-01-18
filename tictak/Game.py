
    # board is a total of 18 bits
    # two bits per square
    # 00 = blank
    # 01 = X
    # 10 = O
    # example:
    #_________
    #|0 |__|0 |
    #|0 |x |__|
    #|x_|__|__|
    #
    #
    # Would be: 010001011000100000
    #
    #
    # Also for reference:
    #
    #____________
    # 0 | 1 | 2 |
    # 3 | 4 | 5 |
    # 6 | 7 | 8 |
    #
    # __________________________
    # 17, 16 | 15, 14 | 13, 12 |
    # 11, 10 | 9 , 8  | 7 , 6  |
    # 5 , 4  | 3 , 2  | 1 , 0  |


import operator
from util.Util import *
from Human import Human

class Board:

    def __init__(self):

        self.tic = 0b0
        self.play_num = [0,0]
        self.play_counter = 0
        self.won = 0
        self.tie = False
        
    def __str__(self):
        
        string = "\n"
        count = 0
        for i in range (17, 0, -2):
            string += self.str_square(i,i-1)
            count += 1
            if count == 3:
                string += '\n'
                count = 0
        return string

    def str_square(self, first, second):
        
        string = '|_'

        if bit_at(self.tic, first):
            string += "O"
        elif bit_at(self.tic, second):
            string += "X"
        else:
            string += "_"
        
        return string

    def clear_board(self):

        self.tic = 0
    
    
    def start_game(self, player0, player1):

        players = [player0, player1]
        won = False
        tie = False

        #loop taking turns till winner
        while self.won == 0 and self.tie == False:

            square = players[self.play_counter%2].play()
            self.play(square, self.play_counter, players)
            if self.won == 0:
                self.tie_condition()
            self.play_counter = int(not self.play_counter)
            if type(players[0]) == Human or type(players[1]) == Human:
                print('current board: ', self)
        #print after winner
        
        if type(players[0]) == Human or type(players[1]) == Human:
            if self.won > 0:
                print("Player " + str(self.won-1) + " Has won!")
            else:
                print("The game is a tie")
            

    # takes in square num where 0 is top left and player
    def play(self, square, pn, players):
        
        occ, shift = self.occupied(square, pn)
        
        if not occ:
            
            # logging the move number
            self.play_num[pn] += 1
            # getting the bits conrisponding to the the player
            symbol = 1 + pn
            new = symbol << shift
            # adding to board
            self.tic = self.tic + new

            if self.win_condition(square, pn):

                self.won = pn + 1
            
        else:
            print("######################\nThat square is occupied, try another move\n")
            square = players[pn].play()
            self.play(square, pn, players)


            
    # function to check if square is occupied
    def occupied(self, square, pn, board=None):

        if board == None:
            board = self.tic
        
        shift = (8 - (square)) * 2
        if (bit_at(board, shift) ==  1) or (bit_at(board, shift+1) == 1):
            return True, shift
        
        return False, shift

    
    def tie_condition(self, board=None):
        
        if board == None:
            board = self.tic
        
        count = 0
        for index in range(0, 18, 2):
            if bit_at(board, index) or bit_at(board, index + 1) == 1:
                count += 1
                
        if count == 9:
            self.tie = True


    # returns empty squares
    def unoccupied(self, board=None):
        empty = []
        for square in range(9):
            if not self.occupied(square, 0, board)[0]:
                empty.append(square)
    
        return empty

    # check if someone won or not
    def win_condition(self,square, pn, board=None):

        if board == None:
            board = self.tic

        r = self.row_column(square)
        check = False
        
        #check row
        row = r[0]
        stop = 17 - (row*6) + pn
        start = stop - 5
        check = self.win_sec_check(board, start, stop, 2)
        if check == True:
            return check
        
        ####################
        
        #check column
        col = r[1]
        stop = 18 - (col * 2) - (1-pn)
        
        start = stop - 13
        check = self.win_sec_check(board, start, stop, 6)
        if check == True:
            return check
        
        #####################

        #diag check
        
        if square == 0 or square == 8 or square == 4 :
            start = 1 - (1-pn)
            stop = 18 - (1-pn)
            check = self.win_sec_check(board, start, stop, 8)
            if check == True:
                return check
            
        if square == 2 or square == 6 or square == 4:
            
            start = 5 - (1-pn)
            stop = 14 - (1-pn)
            check = self.win_sec_check(board, start, stop, 4)
            if check == True:
                return check


        return check
            
        ######################

    def win_sec_check(self,board, start, stop, step):
        
        count = 0
        for index in range(start, stop, step):
            if bit_at(board, index):
                count += 1
        if count == 3:
            return True

        return False
 
    def row_column(self, square):

        r = [0,0]

        #getting columns
        if (square - 1) % 3 == 0:
            r[1] = 1
        if (square - 2) % 3 == 0:
            r[1] = 2

        if square in range (3,6):
            r[0] = 1
        if square in range (6,9):
            r[0] = 2

        return r