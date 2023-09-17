import re                           # regular expressions
from astar import AStar             # A* algorithm
import time
import itertools

num_rocks_falling = 2022
chamber_width = 7

# The five types of rocks have the following peculiar shapes, where # is rock and . is empty space:
#         #     #   #     
# ####   ###    #   #     ##
#         #   ###   #     ##
#                   #

# The tall, vertical chamber is exactly seven units wide. Each rock appears so that its left 
# edge is two units away from the left wall 

# each shape will be represented by a 7 bit number(s), in its starting position (two from left) 
falling_rock_shapes = (
    [0b0011110,],
    [0b0001000,
     0b0011100,
     0b0001000],
    [0b0011100,
     0b0000100,
     0b0000100],
    [0b0010000,
     0b0010000,
     0b0010000,
     0b0010000],
    [0b0011000,
     0b0011000]
)

wind_pattern = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
num_rocks = 5


# ----------------------------------------------------------------------------
# main code
# ----------------------------------------------------------------------------
def main():
    
    # starting with the floor of the chamber
    chamber: [int] = [0b1111111]
    current_height:int  = 0
    wind_num = 0
    file = open("day17_input.txt", 'r')

    # read the input and create "Vent" objeccts
    for line in map(str.rstrip,file):
        #wind_pattern = line
        pass
    
    num_wind_gusts = len(wind_pattern)
    print (f"Pattern repeat {num_wind_gusts*5}")
    
    prev_current_height = 0
    for r in range(num_rocks_falling):
        
        # The rocks fall in the order shown above: 
        # first the - shape, then the + shape, and so on. 
        # Once the end of the list is reached, the same order repeats:
        rock: [int] = falling_rock_shapes[r%num_rocks]
        if not r%num_rocks:

            print (r, "   ", end="")
            for bit in range(chamber_width-1,-1,-1):
                if 1<<bit & chamber[current_height]:
                    print ("#",end="")
                else:
                    print (".",end="")
            print(f"   {current_height} delta: {current_height-prev_current_height} {wind_num%num_wind_gusts}")
            prev_current_height = current_height

        # ... and its bottom edge is three units above the 
        # highest rock in the room (or the floor, if there isn't one).
        if current_height + 4 + len(rock) > len(chamber):
            chamber += [0]*(3 + len(rock))
        bottom_edge = current_height + 4
        print_chamber(chamber,rock,bottom_edge)

        while True:

            # In jet patterns, < means a push to the left, while > means a push to the right. 
            # If the end of the list is reached, it repeats.
            gust: str = wind_pattern[wind_num%num_wind_gusts]
            wind_num+=1

            # After a rock appears, it alternates between being pushed by a jet of hot gas one unit 
            # and then falling one unit down. 
            # If any movement would cause any part of the rock to move into the walls, floor, 
            # or a stopped rock, the movement instead does not occur. 
            if gust == ">":

                can_move = True
                for rock_height, rock_girth in enumerate(rock):
                    if rock_girth & 1 : 
                        can_move = False
                        break
                    rock_girth = rock_girth>>1
                    if chamber[rock_height+bottom_edge] & rock_girth:
                        can_move = False
                        break
                if can_move:
                    rock = list(map(lambda x: x>>1, rock))
                #print_chamber(chamber,rock,bottom_edge)

            if gust == "<":

                can_move = True
                for rock_height, rock_girth in enumerate(rock):
                    if rock_girth &  1<<(chamber_width-1): 
                        can_move = False
                        break
                    rock_girth = rock_girth<<1
                    if chamber[rock_height+bottom_edge] & rock_girth:
                        can_move = False
                        break
                if can_move:
                    rock = list(map(lambda x: x<<1, rock))
                tmp_chamber = [i for i in chamber]
                for rock_height, rock_girth in enumerate(rock):
                    tmp_chamber[rock_height+bottom_edge] |= rock_girth

                #print_chamber(chamber,rock,bottom_edge)

            # If a downward movement would have caused a falling rock to move into the floor or 
            # an already-fallen rock, the falling rock stops where it is (having landed on something) 
            # and a new rock immediately begins falling.
            stop_downward = False
            for rock_height, rock_girth in enumerate(rock):
                if chamber[bottom_edge-1+rock_height] & rock[rock_height]:
                    stop_downward = True


            if stop_downward:
                
                # fix rock where it is
                current_height = max(current_height,(bottom_edge-1) + len(rock))
                for rock_height, rock_girth in enumerate(rock):
                    chamber[rock_height+bottom_edge] |= rock_girth
                break

            bottom_edge-=1

    print(r,current_height)        
            

def print_chamber(chamber: [int], rock: [int], bottom: int):
    return
    print()
    chmbr_height = len(chamber)
    rock_height = len(rock)
    for i,slice in enumerate(reversed(chamber)):
        for bit in range(chamber_width-1,-1,-1):
            if bottom <= chmbr_height-i-1 < rock_height + bottom: 
                if 1<<bit & rock[chmbr_height-i-bottom-1]:
                    print ("@",end="")
                else:
                    print(".",end="")
            elif 1<<bit & slice:
                print ("#",end="")
            else:
                print (".",end="")
        print()
    print()


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
 
def testBit(int_type: int, offset: int) -> bool:
    mask = 1 << offset
    return(int_type & mask)