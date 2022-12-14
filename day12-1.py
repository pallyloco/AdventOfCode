import re
import math
import Grid
import astar


def main():
    terrain = Terrain("day12_input.txt")

    find_path = astar.AStar(terrain.start)
    print (f"end pt is {terrain.end.key}")
    final_node = find_path.find_until(terrain.end.key)
    print(f"Final node id: {final_node.id}")
    print(f"Cost to get to final node: {final_node.cost}")
    print("Path to get there:")
    nodes = find_path.get_path(final_node)
    
    
    map_result = [ ["#" for i in range(terrain.width)] for j in range(terrain.height)]
    for node in find_path._all_nodes.values():
        map_result[node.obj.r][node.obj.c] = "."
    prev_node = None
    dirs = [ " ","V",">"," ","<","^"]
    for node in nodes:
        if prev_node is not None:
            symbol = (prev_node.obj.r - node.obj.r + 1 )* 2 + (prev_node.obj.c - node.obj.c + 1)
            map_result[prev_node.obj.r][prev_node.obj.c] = dirs[symbol]
        prev_node = node
    print ()
    for i in range(terrain.height):
        for j in range(terrain.width):
            print(map_result[i][j],end="")
        print ()


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