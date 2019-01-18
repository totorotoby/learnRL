import math
from scipy.special import comb

states = 1

for i in range (1, 10):
    
    top = math.factorial(9)/math.factorial(9-i)
    
    
    try:
        bottom = math.factorial((i+1)//2)*math.factorial(i//2)
    except ValueError:
        bottom = 1
        
    states += (top/bottom)


states = states - 8*(comb(6,5) + comb(6,4) + comb(6,3) + 2*(comb(6,4)))
print(states)

