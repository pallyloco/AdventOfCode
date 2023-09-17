import DictionaryGrid as dg
import re

# Sensor at x=2, y=18: closest beacon is at x=-2, y=15
parse = re.compile(r'.*?x=(-?\d+).*?y=(-?\d+).*?x=(-?\d+).*?y=(-?\d+)')

def main():
    file = open("day15_test_input.txt", 'r')
    row_of_interest = 2000000
    grid = dg.DictionaryGrid()
    for line in map(str.rstrip,file):
        print(line,end="\t")
        sc,sr,bc,br = map(int,parse.match(line).groups())
        grid.add(sr,sc,"S")
        grid.add(br,bc,"B")

        # manhattan distance
        distance = abs(sc - bc) + abs(sr - br)
        print (distance)

        if sr-distance <= row_of_interest <= sr+distance:
            for c in range(sc-distance,sc+distance+1):
                r = row_of_interest
                if abs(sc - c) + abs(sr - r) > distance: continue
                if grid.get(r,c) is None: grid.add(r,c,"#")
        print_map(grid,0,0,20,20)
        input("hit return")

    score = 0
    for c in range(grid.min_col,grid.max_col+1):
        if grid.get(row_of_interest,c) == "#": score += 1
    print (f"SCORE: {score}")

#    print_map(grid,grid.min_row,grid.min_col,grid.max_row,grid.max_col)

def print_map(grid,minr,minc,maxr,maxc):
    print()
    for r in range(0,maxr+1): 
        print(r,"\t",end="")   
        for c in range(minc,maxc+1):
            d = grid.get(r,c)
            if d is None: d = "."
            print (d,end="")
        print()

# ===================================================================
# Entry point
# ===================================================================
if __name__ == '__main__':
    main()