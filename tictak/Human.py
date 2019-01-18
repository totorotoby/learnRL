

class Human:

    def __init__(self, number):
        self.number = number
        

    def play(self):
 
        square = -1
        while True:
            square = input("Player " + str(self.number) + " where would you like to play?\n\n")
            
            try:
                if int(square) not in range(9):
                    print('########################\nplease only enter a number from 0 to 8\n')
                
                else:
                    break

            except ValueError:
                print('######################\nplease only enter a number from 0 to 8\n')
 
        return int(square)
