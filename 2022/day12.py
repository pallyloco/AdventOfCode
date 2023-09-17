from __future__ import annotations
from typing import Optional, Protocol
import math
from Grid import Grid
from Astar import AStar, Node, NodeNotFoundError


def main():
    terrain: Terrain = Terrain('day12_input.txt')
    min_low_point_hike: Optional[int] = None

    for low_point in terrain.low_points:

        astar = AStar(low_point, zero=0, print_at_n_intervals=0)

        try:
            final_node: Optional[Node] = astar.find_until(reached_end)
            low_cost = final_node.cumulative_cost
            if low_point == terrain.start:
                print("Minimum distance Start to End is:", low_cost)

            if min_low_point_hike is None:
                min_low_point_hike = low_cost
            min_low_point_hike = min(min_low_point_hike, low_cost)

        except NodeNotFoundError:
            continue

    print("lowest distance hike form 'a' to 'z' is:", min_low_point_hike)


def reached_end(pt: TerrainPoint) -> bool:
    return pt == pt.terrain.end


class TerrainPoint:
    def __init__(self, r: int, c: int, height: int, terrain: Terrain):
        self.row = r
        self.col = c
        self.height = height
        self.terrain = terrain

    def key(self) -> str:
        return f"{self.row},{self.col}"

    def edge_cost(self, other: TerrainPoint) -> int:
        return 1

    def eta(self, node=None) -> int:
        end_pt = self.terrain.end
        return int(math.sqrt((self.row - end_pt.row) ** 2 + (self.col - end_pt.col) ** 2))

    def children(self) -> list[TerrainPoint]:
        kids = self.terrain.ordinal_neighbours(self)
        good_kids: list[TerrainPoint] = list()
        for kid in kids:
            if kid is not None and kid.height - self.height < 2:
                good_kids.append(kid)
        return good_kids

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col


class Terrain:
    def __init__(self, filename: str):
        file = open(filename)
        self.grid = Grid()
        self.start: Optional[TerrainPoint] = None
        self.end: Optional[TerrainPoint] = None
        self.low_points: list[TerrainPoint] = list()

        for row, line in enumerate(map(str.rstrip, file)):
            for col, symbol in enumerate(line):
                height = ord(symbol) - ord('a')
                dp = TerrainPoint(row, col, height, self)

                if symbol == "S":
                    dp.height = 0
                    self.start = dp

                if symbol == "E":
                    dp.height = ord('z') - ord('a')
                    self.end = dp

                self.grid.set_value(dp)

                if dp.height == 0:
                    self.low_points.append(dp)

    def ordinal_neighbours(self, dp: TerrainPoint) -> tuple[Optional[TerrainPoint], ...]:
        return self.grid.ordinal_neighbours(dp)


# ===================================================================
# Entry point
# ===================================================================
if __name__ == '__main__':
    main()

"""

You ask the device for a heightmap of the surrounding area (your puzzle input). 
The heightmap shows the local area from above broken into a grid; 
    the elevation of each square of the grid is given by a single lowercase letter, 
    where a is the lowest elevation, b is the next-lowest, and so on up to the highest elevation, z.

Also included on the heightmap are marks for your current position (S) and 
the location that should get the best signal (E). 
Your current position (S) has elevation a, and 
the location that should get the best signal (E) has elevation z.

You'd like to reach E, but to save energy, you should do it in as few steps as possible. 
During each step, you can move exactly one square up, down, left, or right. 
The elevation of the destination square can be at most one higher than the elevation of your current square

What is the fewest steps required to move from your current position to the location that 
should get the best signal?

Your puzzle answer was 481.

--- Part Two ---
As you walk up the hill, you suspect that the Elves will want to turn this into a hiking trail. 
The beginning isn't very scenic, though; perhaps you can find a better starting point.

To maximize exercise while hiking, the trail should start as low as possible: elevation a. 
The goal is still the square marked E. However, the trail should still be direct, taking the 
fewest steps to reach its goal. 

So, you'll need to find the shortest path from any square at elevation a to the square marked E.

What is the fewest steps required to move starting from any square with elevation a to the location 
that should get the best signal?

Your puzzle answer was 480.

"""