import sys
sys.path.append('/home/toby/tictak/util')
from Util import *


# takes in a board state and a player and returns true if win state false if not
def win_state(board, player):
    
    # columns
    for i in range(3):
        squares = [i, i + 3, i + 6]
        count = 0
        for square in squares:
            if bit_at_square(board, square)[player] == 1:
                count += 1

        if count == 3:
            return True

    #rows
    for i in range(0, 7, 3):

        squares = [i, i+1, i+2]
        count = 0
        for square in squares:
            if bit_at_square(board, square)[player] == 1:
                
                count += 1
        if count == 3:
            return True

    #L diag
    squares = [0 , 4, 8]
    count = 0
    for square in squares:
        if bit_at_square(board, square)[player] == 1:
            count += 1
    if count == 3:
        return True

    #R diag
    squares = [2 , 4, 6]
    count = 0
    for square in squares:
        if bit_at_square(board, square)[player] == 1:
            count += 1
    if count == 3:
        return True





sym_list_f = open('all_sym_states', 'r')
sym_list = sym_list_f.read().split('\n')
sym_list = sym_list[:len(sym_list)-1]
sym_list = [int(sym) for sym in sym_list]

p1_wins = []
p2_wins = []
all_other = []
for sym in sym_list:

    check = 0
    if win_state(sym, 0):
        check += 1
        p1_wins.append(sym)

    if win_state(sym, 1):
        check += 1
        p2_wins.append(sym)

    if check == 0:
        all_other.append(sym)
'''      
for win in p1_wins:

    print(win)
'''
    
#print(len(p1_wins))

print(p1_wins[23], string_board(p1_wins[23]))
'''
for win in p2_wins:

    print(win)
    
#print(len(p2_wins))

for state in all_other:

    print(state)
'''
#print(len(all_other))

