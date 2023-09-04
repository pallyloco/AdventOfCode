import re                           # regular expressions
from astar import AStar             # A* algorithm
import time
import itertools
import math
from open_grid import open_grid

# ----------------------------------------------------------------------------
# main code
# ----------------------------------------------------------------------------
max_rows = 0
max_cols = 0
all_maps = []
end_pt = (26,120)
#end_pt = (5,6)
start_pt = (0,1)
flag1 = False
flag2 = False
def main():
    global max_rows,max_cols
    start_map = []
    this_map = []
    file = open("day24_input.txt", 'r')
    for row, line in enumerate(map(str.rstrip,file)):
        this_map.append([])
        start_map.append([])
        for c in line:
            this_map[row].append([c])
            start_map[row].append(c)
    max_rows = len(this_map)
    max_cols = len(this_map[0])

    # find all possible configurations
    find_all_maps(this_map,start_map)

    # astar
    search_obj = AStar(position(0,1,-1))
    x = search_obj.find_until(is_done)
    print (f"answer={x[0].cost}")
    pass

def is_done(astar_obj,node):
    pos = node.obj
    if not pos.flag1 and pos.row == end_pt[0] and pos.col == end_pt[1]:
        pos.flag1 = True
        print ('flag1 is done',node.cost)
        return False
    elif not pos.flag2 and pos.flag1 and pos.row == start_pt[0] and pos.col == start_pt[1]:
        pos.flag2 = True
        print ('flag2 is done',node.cost)
        return False
    elif pos.flag1 and pos.flag2 and pos.row == end_pt[0] and pos.col == end_pt[1]:
        return True
    return False



# ===================================================================
# ===================================================================
def find_all_maps(this_map,start_map):
    repeated = False
    count = 0
    while not repeated:
        repeated = True
        if count > max_rows * max_cols * 5: break
        new_map = [None]*max_rows
        for r in range(max_rows):
            new_map[r] = [None]*max_cols
            for c in range(max_cols):
                new_map[r][c]=[]
        all_maps.append(new_map)
        count += 1
        for row in range(max_rows):
            for col in range(max_cols):
                for char in this_map[row][col]:
                    
                    if char == '<': 
                        new_col = col - 1
                        if new_col < 1: new_col = max_cols - 2
                        new_map[row][new_col].append(char)
                        if start_map[row][new_col] != char: repeated = False
                    
                    if char == '>': 
                        new_col = col + 1
                        if new_col > max_cols - 2: new_col = 1
                        new_map[row][new_col].append(char)
                        if start_map[row][new_col] != char: repeated = False

                    if char == '^': 
                        new_row = row - 1
                        if new_row < 1: new_row = max_rows - 2
                        new_map[new_row][col].append(char)
                        if start_map[new_row][col] != char: repeated = False
                    
                    if char == 'v': 
                        new_row = row + 1
                        if new_row > max_rows - 2 : new_row = 1
                        new_map[new_row][col].append(char)
                        if start_map[new_row][col] != char: repeated = False
                    if char == "#":
                        new_map[row][col] = ["#"]
        this_map = new_map

# ===================================================================
# ===================================================================
def print_map(m):
    print()
    for row in range(max_rows):
        for col in range(max_cols):
            if len(m[row][col]) == 0 :
                print ("+",end="")
            elif len(m[row][col]) == 1:
                print (" ",end="")
                #print (m[row][col][0],end="")
            else:
                print (" ",end="")
                #print (len(m[row][col]),end="")
        print ()
    print()

# ===================================================================
# ===================================================================
class position:
    def __init__(self,row,col,level,flag1=False,flag2=False):
        self.row = row
        self.col = col
        self.level = level
        self.cost = 1
        self.key = f"{row},{col},{level}"
        self.flag1 = flag1
        self.flag2 = flag2
    
    def eta(self,node_obj=None):
        eta_cost = 0
        if not self.flag1:
            eta_cost += math.sqrt( (self.row-end_pt[0])*(self.row-end_pt[0]) + (self.col-end_pt[1])*(self.col-end_pt[1]))
            eta_cost += 2 * math.sqrt( (start_pt[0]-end_pt[0])*(start_pt[0]-end_pt[0]) + (start_pt[0]-end_pt[1])*(start_pt[0]-end_pt[1]))
            return eta_cost
        if not self.flag2:
            eta_cost += math.sqrt( (self.row-start_pt[0])*(self.row-start_pt[0]) + (self.col-start_pt[1])*(self.col-start_pt[1]))
            eta_cost += math.sqrt( (start_pt[0]-end_pt[0])*(start_pt[0]-end_pt[0]) + (start_pt[0]-end_pt[1])*(start_pt[0]-end_pt[1]))
            return eta_cost
        
        return math.sqrt( (self.row-end_pt[0])*(self.row-end_pt[0]) + (self.col-end_pt[1])*(self.col-end_pt[1]))
    
    def children(self,astar_obj=None,node_obj=None):
        m = all_maps[(self.level+1)%len(all_maps)]
        kids = []
        row = self.row
        col = self.col
        if len(m[row][col]) == 0:
            kids.append(position(row,col,self.level+1,self.flag1,self.flag2))
        row = self.row+1
        col = self.col
        if row < max_rows and len(m[row][col]) == 0:
            kids.append(position(row,col,self.level+1,self.flag1,self.flag2))
        row = self.row-1
        col = self.col
        if row > -1 and len(m[row][col]) == 0:
            kids.append(position(row,col,self.level+1,self.flag1,self.flag2))
        row = self.row
        col = self.col+1
        if col < max_cols and len(m[row][col]) == 0:
            kids.append(position(row,col,self.level+1,self.flag1,self.flag2))
        row = self.row
        col = self.col-1
        if col > -1 and len(m[row][col]) == 0:
            kids.append(position(row,col,self.level+1,self.flag1,self.flag2))
        
        return kids

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
 
