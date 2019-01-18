import random

# returns indices at single square
def square_to_bit(square):

    bit = (8 - square) * 2
    return [bit, bit + 1]


def swap_bits(board, b1, b2): 
  
    s1 =  (board >> b1) & 1 
    
    s2 =  (board >> b2) & 1 
   
    xor = (s1 ^ s2) 
   
    xor = (xor << b1) | (xor << b2) 
   
    return board ^ xor

    
def bin_len(num):
    return len(bin(num)) - 2


def add_bit_at(num, index):

    num |= 1 << index

    
# adds a symbol to the board given square and player
def add_square(board, square, player):

    bits = square_to_bit(square)

    if player == 0:
        add_bit_at(board, bits[0])
    else:
        add_bit_at(board, bits[1])

        
# returns board number with added move
def get_move_update(board, square, pn):
    
    shift = (8 - (square)) * 2
    symbol = 1 + pn
    new = symbol << shift
    to_return = board + new
    return to_return


# takes in prob and returns true for sample less than prob and false otherwise
def bin_random(prob):

    return random.random() < prob


# returns board as string repersentation
def string_board(board):
        
    string = "\n"
    count = 0
    for i in range (17, 0, -2):
        string += str_square(board, i, i-1)
        count += 1
        if count == 3:
            string += '\n'
            count = 0
    return string

# helper method for string_board
def str_square(board, first, second):
        
    string = '|_'

    if bit_at(board, first):
        string += "O"
    elif bit_at(board, second):
        string += "X"
    else:
        string += "_"
        
    return string


#returns the bit at index of a board
def bit_at(board, index):

    return (board >> index) & 1

# returns bits at square
def bit_at_square(board, square):

    bits = []
    indices = square_to_bit(square)
    for index in indices:
        bits.append(bit_at(board, index))

    return bits
    

#returns the give boad but flipped over the given axis
def flip_board(board, axis):

    flipped = board
    for i in range(len(axis)):
    
        if axis[i] == 'M':
        
            flipped = swap_squares(flipped, 0, 2)
            flipped = swap_squares(flipped, 3, 5)
            flipped = swap_squares(flipped, 6, 8)
        
        if axis[i] == 'H':

            flipped = swap_squares(flipped, 0, 6)
            flipped = swap_squares(flipped, 1, 7)
            flipped = swap_squares(flipped, 2, 8)
    
        if axis[i] == 'L':

            flipped = swap_squares(flipped, 1, 3)
            flipped = swap_squares(flipped, 2, 6)
            flipped = swap_squares(flipped, 5, 7)

        if axis[i] == 'R':
                    
            flipped = swap_squares(flipped, 0, 8)
            flipped = swap_squares(flipped, 1, 5)
            flipped = swap_squares(flipped, 3, 7)
        
    return flipped


# swaps squares on the board and returns the swapped board
def swap_squares(board, s1, s2):

    sb1 = square_to_bit(s1)
    sb2 = square_to_bit(s2)

    new = swap_bits(board, sb1[0], sb2[0])
    new = swap_bits(new, sb1[1], sb2[1])

    return new


    # takes in a single board and searches to find it in val_tab and returns its number (board) and rotation
def search_equiv(board, valueTable):
    
    rotates = gen_flips(board)

    for b in rotates:
        if b[0] in valueTable.states:
            return b

 # takes in a board and returns the board and its 9 other flips
def gen_flips(b1):

    boards = []
    boards.append([b1, ''])

    string = 'MHLR'
    count = 0
    for i in string:
        
        flip = None
        
        flip = flip_board(b1, i)
        boards.append([flip, i])
        
        for j in range (count + 1, len(string)):
            toadd = flip_board(flip, string[j])
            boards.append([toadd, i+string[j]])
            
        count += 1

    return boards