import re
import math
import Grid
import astar


def main():
    terrain = Terrain("day12_input.txt")
    min_path = None

    for i,start in enumerate(terrain.starts):
        try:
            find_path = astar.AStar(start)
            final_node = find_path.find_until(terrain.end.key)
            if min_path is None:
                min_path = final_node.cost
            else:
                min_path = min(min_path, final_node.cost)
        except:
            continue
        print(i,min_path)

    print ("minimum path starting at height zero is: ",min_path)




class TerrainPoint(Grid.DataPoint):
    def __init__(self,r,c,height,terrain,cost = 1):
        self.cost = cost
        self.key = f"{r},{c}"
        self.r = r
        self.c = c
        self.height = height
        self.eta = 0.0
        self.terrain = terrain
    
    def children(self):
        kids = [kid.value for kid in self.terrain.ordinal_children(self.r,self.c) if kid.value.height - self.height < 2]
        return kids
   

    def __str__(self):
        return f" {chr(self.height+ord('a')) } "
    
    def __repr__(self):
        return self.__str__()
    

class Terrain():
    def __init__(self, filename):
        file = open(filename, 'r')
        self.start = None
        self.end = None
        terrain_map = None
        self.width = None
        self.height = None
        self.starts = list()

        for r,line in enumerate(map(str.rstrip,file)):
            if terrain_map is None:
                terrain_map = Grid.Grid(len(line))
                self.width = len(line)
            for c,height in enumerate(map(lambda x:ord(x)-ord('a'),line)):
                tp = None
                if height == ord('S') - ord('a'):
                    height = 0
                    tp = TerrainPoint(r,c,height,terrain_map)
                    self.start = tp
                elif height == ord('E') - ord('a'):
                    height = ord('z') - ord('a')
                    tp = TerrainPoint(r,c,height,terrain_map)
                    self.end = tp
                else:
                    tp = TerrainPoint(r,c,height,terrain_map)
                if height == 0:
                    self.starts.append(tp)
                terrain_map.add(r,c,tp)
        
        self.height = r+1

        for pt in terrain_map.get_all():
            pt.value.eta = math.sqrt((self.end.r-self.end.r)*(pt.value.r-self.end.r) + \
                (pt.value.c-self.end.c)*(pt.value.c-self.end.c) )



# ===================================================================
# Entry point
# ===================================================================
if __name__ == '__main__':
    main()