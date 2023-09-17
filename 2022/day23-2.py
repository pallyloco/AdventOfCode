import re                           # regular expressions
from astar import AStar             # A* algorithm
import time
import itertools
import math
from open_grid import open_grid

# ----------------------------------------------------------------------------
# main code
# ----------------------------------------------------------------------------
MOVES = 10000000

def main():
    
    grid = open_grid()
    file = open("day23_input.txt", 'r')
    for row, line in enumerate(map(str.rstrip,file)):
        for col,char in enumerate(line):
            if char == '#':
                grid.set_value(row,col,char)
    
    current_order = ['north','south','west','east']
    #print(grid)

    for cycle in range(MOVES):
        num_elves_moved = move_elves(grid,current_order)
        if num_elves_moved == 0:
            print (cycle+1)
            break
        change_direction_order(current_order)
        #print(grid)
    print (f"empty tiles: {grid.empty()}")

# =============================================================================
# Move elves
# =============================================================================
#
def move_elves(grid,current_order):
    proposed_moves = {}
    num_elves_moved = 0
    
    # ---------------------------------------------------------------------
    # During the first half of each round, each Elf considers the eight 
    # positions adjacent to themself. 
    # ---------------------------------------------------------------------
    for elf in grid.get_row_col_pairs():
        row,col = elf

        
        # If no other Elves are in one of any of its eight neighbours, 
        # the Elf does not do anything during this round. 
        all_empty = True
        for neighbour in grid.neighbours(row,col):
            r,c = neighbour
            if grid.get_value(r,c) is not None:
                all_empty = False
                break
        if all_empty: continue

        # Otherwise, the Elf looks in each of four directions in the order specified by current_order
        # and proposes moving one step in the first valid direction:
        for direction in current_order:
        
            # If there is no Elf in the N, NE, or NW adjacent positions, 
            # the Elf proposes moving north one step.
            if direction == 'north':
                if grid.get_value(grid.N(row,col)[0] ,  grid.N(row,col)[1]) is None and \
                   grid.get_value(grid.NE(row,col)[0] , grid.NE(row,col)[1]) is None and \
                   grid.get_value(grid.NW(row,col)[0] , grid.NW(row,col)[1]) is None:
                    if grid.N(row,col) not in proposed_moves:
                        proposed_moves[grid.N(row,col)] = []
                    proposed_moves[grid.N(row,col)].append(elf) 
                    break

            # If there is no Elf in the S, SE, or SW adjacent positions, 
            # the Elf proposes moving south one step.
            elif direction == 'south':
                if grid.get_value(grid.S(row,col)[0] ,  grid.S(row,col)[1]) is None and \
                   grid.get_value(grid.SE(row,col)[0] , grid.SE(row,col)[1]) is None and \
                   grid.get_value(grid.SW(row,col)[0] , grid.SW(row,col)[1]) is None:
                    if grid.S(row,col) not in proposed_moves:
                        proposed_moves[grid.S(row,col)] = []
                    proposed_moves[grid.S(row,col)].append(elf) 
                    break

            # If there is no Elf in the W, NW, or SW adjacent positions, 
            # the Elf proposes moving west one step.
            elif direction == 'west':
                if grid.get_value(grid.W(row,col)[0] ,  grid.W(row,col)[1]) is None and \
                   grid.get_value(grid.SW(row,col)[0] , grid.SW(row,col)[1]) is None and \
                   grid.get_value(grid.NW(row,col)[0] , grid.NW(row,col)[1]) is None:
                    if grid.W(row,col) not in proposed_moves:
                        proposed_moves[grid.W(row,col)] = []
                    proposed_moves[grid.W(row,col)].append(elf) 
                    break

            # If there is no Elf in the E, NE, or SE adjacent positions, 
            # the Elf proposes moving east one step.
            elif direction == 'east':
                if grid.get_value(grid.E(row,col)[0] ,  grid.E(row,col)[1]) is None and \
                   grid.get_value(grid.SE(row,col)[0] , grid.SE(row,col)[1]) is None and \
                   grid.get_value(grid.NE(row,col)[0] , grid.NE(row,col)[1]) is None:
                    if grid.E(row,col) not in proposed_moves:
                        proposed_moves[grid.E(row,col)] = []
                    proposed_moves[grid.E(row,col)].append(elf) 
                    break
    
    # ---------------------------------------------------------------------
    # After each Elf has had a chance to propose a move, the second half of 
    # the round can begin. 
    # ---------------------------------------------------------------------
    for proposal in proposed_moves:

        # If two or more Elves propose moving to the same position, 
        # none of those Elves move.
        if len(proposed_moves[proposal]) > 1:
            continue
        
        # Simultaneously, each Elf moves to their proposed destination tile 
        # if they were the only Elf to propose moving to that position. 
        new_row,new_col = proposal
        old_row,old_col = proposed_moves[proposal][0]
        grid.set_value(new_row,new_col,"#")
        grid.set_value(old_row,old_col,None)

        num_elves_moved += 1
    
    return num_elves_moved

# ===================================================================
# change_direction_order
# ===================================================================
# Finally, at the end of the round, the first direction the Elves considered is moved to the end 
# of the list of directions. For example, during the second round, the Elves would try proposing 
# a move to the south first, then west, then east, then north. On the third round, the Elves 
# would first consider west, then east, then north, then south.
def change_direction_order(current_order):
    old = current_order.pop(0)
    current_order.append(old)
    return current_order


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
 
