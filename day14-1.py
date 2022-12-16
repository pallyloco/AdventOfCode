import re
import DynamicGrid as dg
import os
from time import sleep


def main():
    file = open("day14_input.txt", 'r')

    minr = None
    minc = None
    maxr = None
    maxc = None
    grid = dg.DynamicGrid()


    coords_re = re.compile(r'\d+,\d+')
    row_col_re = re.compile(r'(\d+),(\d+)')

    # Inputs look like
    # 498,4 -> 498,6 -> 496,6
    # 503,4 -> 502,4 -> 502,9 -> 494,9
    # where each pt -> pt is a straight horizontal or vertical line
    for r,line in enumerate(map(str.rstrip,file)):
        startr = None
        startc = None
        for coord_match in coords_re.finditer(line):
            row = int(row_col_re.search(coord_match.group()).group(2))
            col = int(row_col_re.search(coord_match.group()).group(1))
            minr = row if minr is None else min(minr,row)
            maxr = row if maxr is None else max(maxr,row)
            minc = col if minc is None else min(minc,col)
            maxc = col if maxc is None else max(maxc,col)

            if startr is not None and startr != row:
                s,e = (startr, row) if startr < row else (row,startr)
                for r in range(s,e+1):
                    grid.add(r,col,"#")
                     
            elif startc is not None and startc != col:
                s,e = (startc, col) if startc < col else (col,startc)
                for c in range(s,e+1):
                    grid.add(row,c,"#")
            startr = row
            startc = col


    # drop sand

    # Sand is produced one unit at a time, and the next unit of sand is not produced until the 
    # previous unit of sand comes to rest. A unit of sand is large enough to fill one tile of 
    # air in your scan.
    sandcount = 0
    grid.add(0,500,"+")
    while grid.get(0,500) == '+':

        # The sand is pouring into the cave from point 500,0.
        row = 0
        col = 500

        while True:

            #if sandcount%100 == 0: print_map(grid,minr,minc,maxr+2,maxc)

            # A unit of sand always falls down one step if possible. 
            if grid.get(row+1,col) is None and row+1 < maxr+2:
                row += 1
                continue

            # If the tile immediately below is blocked (by rock or sand), 
            # the unit of sand attempts to instead move diagonally one  step down and to the left. 
            if grid.get(row+1,col-1) is None and row+1 < maxr+2:
                row = row+1
                col = col-1
                minc = min(col,minc)
                continue
                
            # If that tile is blocked, the unit of sand attempts to instead move diagonally 
            # one step down and to the right. 
            if grid.get(row+1,col+1) is None and row+1 < maxr+2:
                row = row+1
                col = col+1
                maxc = max(col,maxc)
                continue
            
            # If all three possible destinations are blocked, the unit of sand comes to rest and no 
            # longer moves, at which point the next unit of sand is created back at the source.
            grid.add(row,col,"o")  
            break      


        sandcount = sandcount + 1
    print_map(grid,minr,minc,maxr+2,maxc)
    print (sandcount)


def print_map(dg,minr,minc,maxr,maxc):
    os.system('clear')
    print()
    for r in range(0,maxr+1):    
        for c in range(minc,maxc+1):
            d = dg.get(r,c)
            if d is None: d = "."
            print (d,end="")
        print()
# ===================================================================
# Entry point
# ===================================================================
if __name__ == '__main__':
    main()