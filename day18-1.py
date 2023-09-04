import re                           # regular expressions
import time
import itertools
import math

test_data = [
(2,2,2),
(1,2,2),
(3,2,2),
(2,1,2),
(2,3,2),
(2,2,1),
(2,2,3),
(2,2,4),
(2,2,6),
(1,2,5),
(3,2,5),
(2,1,5),
(2,3,5),
]

# ----------------------------------------------------------------------------
# main code
# ----------------------------------------------------------------------------
def main():

    cube_sides = {}
    
    # To approximate the surface area, count the number of sides 
    # of each cube that are not immediately connected to another cube.

    file = open("day18_input.txt", 'r')
    for line in map(str.rstrip,file):
        regex = re.match(r'(\d+),(\d+),(\d+)',line)
        x,y,z = map(int,regex.groups())
    
    #for x,y,z in test_data:
        sides = (f"{x-1},{y-1},{z-1}-{x},{y},{z-1}",
                 f"{x-1},{y-1},{z}-{x},{y},{z}",
                 f"{x-1},{y-1},{z-1}-{x-1},{y},{z}",
                 f"{x},{y-1},{z-1}-{x},{y},{z}",
                 f"{x-1},{y-1},{z-1}-{x},{y-1},{z}",
                 f"{x-1},{y},{z-1}-{x},{y},{z}"
        )
        for side in sides:
            if side in cube_sides:
                cube_sides.pop(side)
            else:
                cube_sides[side]=1
    print (len(cube_sides))

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
 
