import re                           # regular expressions
from astar import AStar             # A* algorithm
import time
import itertools
import math

# ----------------------------------------------------------------------------
# main code
# ----------------------------------------------------------------------------
map_lines = []
#########
FACE_SIZE=50
#########
faces = {}


def main():

    ##############
    # NOTE: only good for real input, not test input
    ##############
    # number, min_row, min_col,
    faces[1] = Face(1,0,FACE_SIZE)
    faces[2] = Face(2,0,2*FACE_SIZE)
    faces[3] = Face(3,FACE_SIZE,FACE_SIZE)
    faces[4] = Face(4,2*FACE_SIZE,0)
    faces[5] = Face(5,2*FACE_SIZE,FACE_SIZE)
    faces[6] = Face(6,3*FACE_SIZE,0)

    faces[1].transition_max_row = lambda r,c : (3, r+1, c, 'down')
    faces[3].transition_min_row = lambda r,c : (1, r-1, c, 'up')

    faces[1].transition_min_row = lambda r,c : (6, faces[6].min_row + c - faces[1].min_col, faces[6].min_col, 'right')
    faces[6].transition_min_col = lambda r,c : (1, faces[1].min_row, faces[1].min_col + r - faces[6].min_row, 'down')

    faces[1].transition_max_col = lambda r,c : (2, r, c+1, 'right')
    faces[2].transition_min_col = lambda r,c : (1, r, c-1, 'left')
    
    faces[1].transition_min_col = lambda r,c : (4, faces[4].min_row + faces[1].max_row - r, faces[4].min_col, 'right') 
    faces[4].transition_min_col = lambda r,c : (1, faces[1].min_row + faces[4].max_row - r, faces[1].min_col, 'right')
    
    faces[2].transition_min_row = lambda r,c : (6, faces[6].max_row, faces[6].min_col + c - faces[2].min_col, 'up')
    faces[6].transition_max_row = lambda r,c : (2, faces[2].min_row, faces[2].min_col + c - faces[6].min_col, 'down')

    faces[2].transition_max_row = lambda r,c : (3, faces[3].min_row + c - faces[2].min_col, faces[3].max_col, 'left')
    faces[3].transition_max_col = lambda r,c : (2, faces[2].max_row, faces[2].min_col + r - faces[3].min_row, 'up')

    faces[2].transition_max_col = lambda r,c : (5, faces[5].min_row + faces[2].max_row - r, faces[5].max_col, 'left') 
    faces[5].transition_max_col = lambda r,c : (2, faces[2].min_row + faces[5].max_row - r, faces[2].max_col, 'left')

    faces[3].transition_max_row = lambda r,c : (5, r+1, c, 'down')
    faces[5].transition_min_row = lambda r,c : (3, r-1, c, "up")

    faces[3].transition_min_col = lambda r,c : (4, faces[4].min_row, faces[4].min_col + r - faces[3].min_row, 'down')
    faces[4].transition_min_row = lambda r,c : (3, faces[3].min_row + c - faces[4].min_col, faces[3].min_col, 'right')

    faces[4].transition_max_row = lambda r,c : (6, r+1, c, 'down')
    faces[6].transition_min_row = lambda r,c : (4, r-1, c, 'up')

    faces[4].transition_max_col = lambda r,c : (5, r, c+1, 'right')
    faces[5].transition_min_col = lambda r,c : (4, r, c-1, 'left')

    faces[5].transition_max_row = lambda r,c : (6, faces[6].min_row + c - faces[5].min_col, faces[6].max_col, 'left')
    faces[6].transition_max_col = lambda r,c : (5, faces[5].max_row, faces[5].min_col + r - faces[6].min_row, 'up')

    #
    #  /--------------\         /--------\
    #  |              |         |        |
    #  |            . . . . . . . .      |
    #  |  /---------. 1 1 . . 2 2 . -\   |
    #  |  |         . 1 1 . . 2 2 .  |   |
    #  |  |         . . . . . . . .  |   |
    #  |  |         . . . .     |    |   |
    #  |  |         . 3 3 .     |    |   |
    #  |  |     /---. 3 3 .-----/    |   |
    #  |  |     |   . . . .          |   |
    #  |  | . . . . . . . .          |   |
    #  |  | . 4 4 . . 5 5 .          |   |
    #  |  \-. 4 4 . . 5 5 .----------/   |
    #  |    . . . . . . . .              |
    #  |    . . . .   |                  |
    #  \----. 6 6 .---/                  |
    #       . 6 6 .                      |
    #       . . . .                      |
    #           |                        |
    #           \------------------------/





    # 126070 too high
    # 1571 too low
    # 34571 not the right answer
    # 15410

    file = open("day22_input.txt", 'r')
    pre_map_lines = []
    for line in map(str.rstrip,file):
        if re.match(r"\s*$",line): break
        pre_map_lines.append(line)
    for line in map(str.rstrip,file):
        instructions = line
    max_col = max(len(l) for l in pre_map_lines)
    for line in pre_map_lines:
        map_lines.append(line + " "*(max_col-len(line)))

    positions = {"right":(0,1),"left":(0,-1),"up":(-1,0),"down":(1,0)}
    
    ############
    dir_name = 'right'
    pos = (faces[1].min_row,faces[1].min_col-1)
    face = 1
    #############

    grid = [None]*(4*FACE_SIZE)
    for i in range(4*FACE_SIZE):
        grid[i] = [None]*(4*FACE_SIZE)
    for row,line in enumerate(map_lines):
        for col in range(len(line)):
            grid[row][col]=line[col]
    test_positions = [
        ('up',1,(faces[1].min_row,faces[1].max_col-1)), 
        ('left',1,(faces[1].min_row+1,faces[1].min_col)),
        ('left',3,(faces[3].min_row+1,faces[3].min_col))
        ]
    for distance,direction_change in re.findall(r'(\d+)([RL]?)',instructions):
        r,c = pos
        r1 = r
        c1 = c
        for _ in range(int(distance)):
            new_face = face
            dr,dc = positions[dir_name]
            new_row = r1 + dr 
            new_col = c1 + dc
            new_dir_name = dir_name

            if new_row > faces[new_face].max_row:
                new_face,new_row,new_col,new_dir_name = faces[face].transition_max_row(r1,c1)
    
            if new_row < faces[new_face].min_row:
                new_face,new_row,new_col,new_dir_name = faces[face].transition_min_row(r1,c1)
            
            if new_col > faces[new_face].max_col:
                new_face,new_row,new_col,new_dir_name = faces[face].transition_max_col(r1,c1)

            if new_col < faces[new_face].min_col:
                new_face,new_row,new_col,new_dir_name = faces[face].transition_min_col(r1,c1)

            r1 = new_row
            c1 = new_col

            if map_lines[new_row][new_col] == "#": break
            dir_name = new_dir_name
            pos = [new_row, new_col]
            face = new_face
            symbol = ">"
            if dir_name == 'left': symbol = "<"
            if dir_name == "up": symbol = "^"
            if dir_name == 'down': symbol = 'v'
            grid[new_row][new_col]=symbol

        # R = clockwise [0,1]=>[1,0]=>[0,-1]=>[-1,0]
        if direction_change == "R":
            if dir_name == 'right': dir_name = "down"
            elif dir_name == 'down': dir_name = 'left'
            elif dir_name == "left": dir_name = "up"
            elif dir_name == "up": dir_name = "right"
        elif direction_change == "L":
            if dir_name == 'right': dir_name = 'up'
            elif dir_name == 'up': dir_name = 'left'
            elif dir_name == 'left': dir_name = 'down'
            elif dir_name == 'down': dir_name = 'right'
    
    print ()
    for line in grid:
        for char in range(len(line)):
            if line[char] is None or line[char] == '.': 
                line[char] = ' ' 
            print (f"{line[char]}",end="")
        print()
    print ()
    print ()
    answer = (pos[0]+1)*1000 + (pos[1]+1)*4
    
    
    # Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^)
    if dir_name == 'right': answer = answer
    if dir_name == 'down': answer += 1
    if dir_name == 'left': answer += 2
    if dir_name == 'up': answer += 3
    print(answer)


class Face:
    def __init__ (self,id,min_row,min_col):
        self.min_col = min_col
        self.min_row = min_row
        self.max_col = min_col + FACE_SIZE-1
        self.max_row = min_row + FACE_SIZE-1
        self.id = id
        self.transition_max_row = None
        self.transition_min_row = None
        self.transition_max_col = None
        self.transition_min_col = None

                          
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
 
