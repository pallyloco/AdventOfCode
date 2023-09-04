import re                           # regular expressions
from astar import AStar             # A* algorithm
import time
import itertools
import math


# Start:    1,2,-3,3,-2,0,4
# Moved 1:  2,1,-3,3,-2,0,4
# Moved 2:  1,-3,2,3,-2,0,4
# Moved -3: 1,2,3,-2,-3,0,4
# Moved 3:  1,2,-2,-3,0,3,4
# Moved -2: 1,2,-3,0,3,4,-2
# Moved 0;  1,2,-3,0,3,4,-2
# Moved 4:  1,2,-3,4,0,3,-2
# ----------------------------------------------------------------------------
# main code
# ----------------------------------------------------------------------------
encryption_key = 811589153
num_times_mix = 10
def main():
    file = open("day20_input.txt", 'r')
    inputs = []
    repeats = {}
    for line in map(int,map(str.rstrip,file)):
        if line not in repeats: repeats[line] = 1
        else: 
            repeats[line] += 1
        inputs.append((line*encryption_key ,repeats[line]))
    #for i in range(1,1,):
    #1,2,-3,3,-2,0,4
    #inputs = [(1*encryption_key,1),(2*encryption_key,2),(-3*encryption_key,3),(3*encryption_key,4),(-2*encryption_key,5),(0*encryption_key,1),(4*encryption_key,1)]
    number = len(inputs)
    new_array = [i for i in inputs]
    #print (new_array)
    
    for mix_num in range(num_times_mix):
        #print (f"{mix_num}\t",new_array)
        for item,item_repeat in inputs:
            if item == 0 : continue

            item_num = new_array.index( (item,item_repeat) )
            new_array.remove( (item,item_repeat))

            move_to = (item_num + item%(number-1))%(number-1)
            if move_to == 0:
                new_array = new_array + [(item,item_repeat)] 
            else:
                new_array = new_array[:move_to] + [(item,item_repeat)] + new_array[move_to:]
        
        





    zeroth_index = new_array.index((0,1))
    num1 = new_array[(zeroth_index+1000)%number][0]
    num2 = new_array[(zeroth_index+2000)%number][0]
    num3 = new_array[(zeroth_index+3000)%number][0]
    #print(f"{item=}, {move_to=}, {zeroth_index=}, {num1=}, {num2=}, {num3=}")
    print (f"Anser is: {num1+num2+num3}")

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
 
