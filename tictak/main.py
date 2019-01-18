from refLearn.RLplayer import RLplayer
from Human import Human
from Game import Board
from Util import *


def main():

    print('######################################################')
    print('Tobs Tic Tak Bots\n\n')
    print('Pick a type of Tic Tak Bot to Train and/or Play: ')
    print('(0) Uniformly Random')
    print('(1) Q Learn with Value Table')
    print('######################################################\n') 

    bot_num = int(input())

    if bot_num == 0:

        print('program this')

    if bot_num == 1:

        print('\nTrain against what other type:')
        print('(0) Uniformly Random')
        print('(1) Q Learn with Value Table\n')
        op_num = int(input())

        print('\nNumber Training Games, Learning Rate, Exploration rate? (Comma space seperated)')
        param = str(input())
        param = param.split(', ')
        param[0] = int(param[0])
        param[1] = float(param[1])
        param[2] = float(param[2])


        if op_num == 1:

            player0 = RLplayer(0, param[1], param[2])
            player1 = RLplayer(1, param[1], param[2])

            for _ in range(param[0]):
                board = Board()
                player0.update_board(board)
                player1.update_board(board)
                board.start_game(player0, player1)
                player0.update_values()
                player1.update_values() 
                print("\r\n{0}".format((float(_)/param[0])*100)),
                print('win percentage player0: ', player0.getWinPer())

            # Add win percentage data blah blah


            print('Would you like to play a game? [y/n]\n')
            a = str(input())

            if a == 'y':

                print('Change Learning Rate, Exploration rate to? (Comma space seperated)')
                n_l, e_l = [float(i) for i in str(input()).split(', ')]
                player0.changeRates(n_l, e_l)

                while a == 'y':

                    human = Human(1)
                    newGame = Board()
                    player0.update_board(newGame)
                    newGame.start_game(player0,human)
                    player0.update_values()

                    print('Another Game?')
                    a = str(input())
    
    

    
#comment out to run graph_states        
main()
