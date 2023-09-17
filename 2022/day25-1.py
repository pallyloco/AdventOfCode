import re                           # regular expressions
from astar import AStar             # A* algorithm
import time
import itertools
import math

# "SNAFU works the same way, except it uses powers of five instead of ten. Starting 
# from the right, you have a ones place, a fives place, a twenty-fives place, 
# a one-hundred-and-twenty-fives place, and so on. It's that easy!"

# Instead of using digits four through zero, 
# the digits are 2, 1, 0, minus (written -), and double-minus (written =). 
# Minus is worth -1, and double-minus is worth -2."

# ----------------------------------------------------------------------------
# main code
# ----------------------------------------------------------------------------
def main():
    total = '0'
    file = open("day25_input.txt", 'r')
    for row, line in enumerate(map(str.rstrip,file)):
        total = snafu_add(total,line)
    print(total)
    pass


digit_value = {'2':2,'1':1,'0':0,'-':-1,'=':-2}
number_repr = {0:(0,0),1:(0,1),2:(0,2),3:(1,-2),4:(1,-1),5:(1,0),\
                -1:(0,-1),-2:(0,-2),-3:(-1,2),-4:(-1,1),-5:(-1,0)}
value_digit = {2:'2',1:'1',0:'0',-1:'-',-2:'='}

def snafu_add (num1:str,num2:str) ->str:
    added = ""
    carry = 0
    for i in range(0,max(len(num1),len(num2))):
        d1,d2 = ('0','0')
        if i < len(num1):
            d1 = num1[-i-1]
        if i < len(num2):
            d2 = num2[-i-1]
        d3 = digit_value[d1] + digit_value[d2] + carry
        carry,digit = number_repr[d3]
        added = value_digit[digit] + added
    if carry != 0:
        added = value_digit[carry] + added

    return added

# ===================================================================
# Entry point
# ===================================================================
if __name__ == '__main__':
    global start
    start = time.time()
    main()    
    end = time.time()

    total_time = end - start
    print("\n"+ str(total_time))
 
