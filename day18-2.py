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
cube_sides = {}
outer_sides = {}
minx=None
miny=None
minz=None
maxx=None
maxy=None
maxz=None

# answer 1 1966 is too low

# ----------------------------------------------------------------------------
# main code
# ----------------------------------------------------------------------------
def main():

    global minx,miny,minz,maxx,maxy,maxz
    # To approximate the surface area, count the number of sides 
    # of each cube that are not immediately connected to another cube.

    
    file = open("day18_input.txt", 'r')
    for line in map(str.rstrip,file):
        regex = re.match(r'(\d+),(\d+),(\d+)',line)
        x,y,z = map(int,regex.groups())
#    for x,y,z in test_data:            
        sides = (f"{x},{y},{z}-{x+1},{y+1},{z}",
                 f"{x},{y},{z}-{x+1},{y},{z+1}",
                 f"{x},{y},{z}-{x},{y+1},{z+1}",

                 f"{x},{y},{z+1}-{x+1},{y+1},{z+1}",
                 f"{x+1},{y},{z}-{x+1},{y+1},{z+1}",
                 f"{x},{y+1},{z}-{x+1},{y+1},{z+1}"
        )

        if minx is None:
            minx,maxx = (x,x)
            miny,maxy = (y,y)
            minz,maxz = (z,z)
        else:
            minx = min(minx,x)
            maxx = max(maxx,x)
            miny = min(miny,y)
            maxy = max(maxy,y)
            minz = min(minz,z)
            maxz = max(maxz,z)

        for side in sides:
            if side in cube_sides:
                cube_sides.pop(side)
            else:
                cube_sides[side]="A"


    # The cooling rate depends on exterior surface area, 
    # but the above calculation also include2 the surface area of air pockets trapped 
    # in the lava droplet.

    # Instead, consider only cube sides that could be reached by the water and steam as 
    # the lava droplet tumbles into the pond. The steam will expand to reach as much 
    # as possible, completely displacing any air on the outside of the lava droplet 
    # but never expanding diagonally.
    flow2(  )

    print (len(cube_sides))
    print (sum(1 for c in cube_sides.values() if c=="W"))

def flow2 ( water = {}, processed = {}):
    
    for y in range(miny-1,maxy+2):
        for x in range(minx-1,maxx+2):
            water[f"{x},{y},{minz-1}"] = "W"
            water[f"{x},{y},{maxz+1}"] = "W"
    for z in range(minz-1,maxz+2):
        for x in range(minx-1,maxx+2):
            water[f"{x},{miny-1},{z}"] = "W"
            water[f"{x},{maxy+1},{z}"] = "W"

    for z in range(minz-1,maxz+2):
        for y in range(miny-1,maxy+2):
            water[f"{minx-1},{y},{z}"] = "W"
            water[f"{maxx+1},{y},{z}"] = "W"

    change = True
    loop = 0
    while change:
        change = False
        loop+=1
        if loop > 10000:
            break
        for z in range(minz-1,maxz+2):
            for y in range(miny-1, maxy+2):
                for x in range(minx-1,maxx+2):
#                    print(x,y,z)

                    if f"{x},{y},{z}" not in water: continue 
                    #if f"{x},{y}.{z}" in processed: continue
                    
                    # left
                    wall = hit_x_wall(x,y,z)
                    if wall is None:
                        change = f"{x-1},{y},{z}" not in water or change
                        water[f"{x-1},{y},{z}"] = "W"
#                        print("no left wall", wall)
                    else:
#                        print ("Wall: ",wall)
                        change = cube_sides[wall] != "W"  or change
                        cube_sides[wall]="W"

                    # right
                    wall = hit_x_wall(x+1,y,z)
                    if wall is None:
                        change = f"{x+1},{y},{z}" not in water  or change
                        water[f"{x+1},{y},{z}"] = "W"
#                        print("no right wall")
                    else:
                        change = cube_sides[wall] != "W"  or change
                        cube_sides[wall]="W"
#                        print ("Wall: ",wall)
                     
                    # forward
                    wall = hit_y_wall(x,y,z)
                    if wall is None:
                        change = f"{x},{y-1},{z}" not in water  or change
                        water[f"{x},{y-1},{z}"] = "W"
#                        print ("no forward wall")
                    else:
                        change = cube_sides[wall] != "W"  or change
#                        print ("Wall: ",wall)
                        cube_sides[wall]="W"

                    # backward
                    wall = hit_y_wall(x,y+1,z)
                    if wall is None:
                        change = f"{x},{y+1},{z}" not in water  or change
                        water[f"{x},{y+1},{z}"] = "W"
#                        print ("no up wall")
                    else:
                        change = cube_sides[wall] != "W"  or change
#                        print ("Wall: ",wall)
                        cube_sides[wall]="W"

                    # down
                    wall = hit_z_wall(x,y,z)
                    if wall is None:
#                        print ('no down wall')
                        change = f"{x},{y},{z-1}" not in water  or change
                        water[f"{x},{y},{z-1}"] = "W"
                    else:
                        change = cube_sides[wall] != "W"  or change
                        cube_sides[wall]="W"
#                        print ("Wall: ",wall)

                    # up
                    wall = hit_z_wall(x,y,z+1)
                    if wall is None:
                        change = f"{x},{y},{z+1}" not in water  or change
                        water[f"{x},{y},{z+1}"] = "W"
                    else:
                        change = cube_sides[wall] != "W"  or change
                        cube_sides[wall]="W"
#                        print ("Wall: ",wall)
    print (f"{loop=}")
 
    # for z in range(minz,maxz+1):
    #     print(f"{z=}")
    #     for y in range(miny,maxy+1):
    #         print()
    #         for x in range(minx,maxx+1):
    #             if f"{x},{y},{z+1}" in water:
    #                 print("W",end="")
    #             else:
    #                 print (".",end="")
    #     print()
    #     print()


def hit_x_wall(x,y,z):
    key = f"{x},{y},{z}-{x},{y+1},{z+1}"
    if key in cube_sides: return key
    return

def hit_y_wall(x,y,z):
    key = f"{x},{y},{z}-{x+1},{y},{z+1}"
    if key in cube_sides: return key
    return

def hit_z_wall(x,y,z):
    key = f"{x},{y},{z}-{x+1},{y+1},{z}"
    if key in cube_sides: return key
    return

  
# ===================================================================
# WaterSource                           y
#  __________     ______________        ^
# |_________ |___|   ___________|       |
#           |________|                  ---> x
# ===================================================================
      

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
 
