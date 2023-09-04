import re                           # regular expressions
from astar import AStar             # A* algorithm
import time
import itertools
import math
# 149110 is too high
# ----------------------------------------------------------------------------
# main code
# ----------------------------------------------------------------------------
map_lines = []
def main():
    
    file = open("day22_input.txt", 'r')
    pre_map_lines = []
    for line in map(str.rstrip,file):
        if re.match("\s*$",line): break
        pre_map_lines.append(line)
    for line in map(str.rstrip,file):
        instructions = line
    max_col = max(len(l) for l in pre_map_lines)
    max_row = len(pre_map_lines)
    for line in pre_map_lines:
        map_lines.append(line + " "*(max_col-len(line)))

    pos = [0,0]
    dir = [0,1]

    for distance,direction_change in re.findall(r'(\d+)([RL])',instructions):
        dr,dc = dir
        r,c = pos
        print (distance,direction_change)
        r1 = r
        c1 = c
        for _ in range(int(distance)):
            valid = False
            while not valid:
                valid = True
                new_row = r1 + dr 
                new_col = c1 + dc
                new_row = 0 if new_row >= max_row else new_row
                new_row = max_row-1 if new_row < 0 else new_row
                new_col = 0 if new_col >= max_col else new_col
                new_col = max_col-1 if new_col < 0 else new_col
                if map_lines[new_row][new_col] == " " : valid=False
                r1 = new_row
                c1 = new_col
            if map_lines[new_row][new_col] == "#": break
            pos = [new_row, new_col]
        
        dr,dc = dir
        # R = clockwise [0,1]=>[1,0]=>[0,-1]=>[-1,0]
        if direction_change == "R":
            if dr == 0 and dc == 1: 
                dr = 1
                dc = 0
            elif dr == 1 and dc == 0:
                dr = 0
                dc = -1
            elif dr == 0 and dc == -1:
                dr = -1
                dc = 0
            elif dr == -1 and dc == 0:
                dr = 0
                dc = 1
        else:
            # L = anti-clockwise [0,1]=>[-1,0]=>[0,-1]=>[1,0]
            if dr == 0 and dc == 1: 
                dr = -1
                dc = 0
            elif dr == -1 and dc == 0:
                dr = 0
                dc = -1
            elif dr == 0 and dc == -1:
                dr = 1
                dc = 0
            elif dr == 1 and dc == 0:
                dr = 0
                dc = 1
        dir = [dr,dc]
        print (pos)
    
    answer = (pos[0]+1)*1000 + (pos[1]+1)*4
    # Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^)
    if dr == 0 and dc == 1: answer = answer
    if dr == 1 and dc == 0: answer += 1
    if dr == 0 and dc == -1: answer += 2
    if dr == -1 and dc == 0: answer += 3
    print(answer)

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
 
