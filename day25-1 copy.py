from __future__ import annotations
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
    with open("day25_input.txt", 'r') as file:
        total = sum(map(SNAFU,  file), start=SNAFU())
    print(total)

class SNAFU:
    digit_value = {'2':2,'1':1,'0':0,'-':-1,'=':-2}
    number_repr = {0:(0,0),1:(0,1),2:(0,2),3:(1,-2),4:(1,-1),5:(1,0),
                    -1:(0,-1),-2:(0,-2),-3:(-1,2),-4:(-1,1),-5:(-1,0)}
    value_digit = {v: k for k, v in digit_value.items()}

    def __init__(self, snafu_string='0'):
        self.value = snafu_string.strip()
        if not re.match(r'[-210=]+$', self.value):
            raise ValueError("invalid characters for a SNAFU object")


    def __add__(self, other: SNAFU) -> SNAFU:
        if not isinstance(other,SNAFU):
            raise TypeError("can only add snafu's")

        added = ""
        carry = 0

        for d1,d2 in itertools.zip_longest(reversed(self.value), reversed(other.value), fillvalue='0'):
            d3 = self.digit_value[d1] + self.digit_value[d2] + carry
            carry,digit = self.number_repr[d3]
            added = self.value_digit[digit] + added
        if carry != 0:
            added = self.value_digit[carry] + added

        return type(self)(added)
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return repr(self.value)
    

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
 
