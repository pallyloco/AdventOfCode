from __future__ import annotations
from typing import Optional

from Astar import CostProtocol, AStar, DijkstraObject, Cost, Node, NodeNotFoundError
from Coords import Coord
import re


class CityBlock:
    def __init__(self, row, col, value=0):
        self.row: int = row
        self.col: int = col
        self.value: int = value


Grid = list[str]


class Crucible:
    max_straight = 11
    min_straight = 4

    def __init__(self, head: Coord, city_blocks: Grid,
                 end_coord: Coord, body: Optional[str] = None,
                 parent: Optional[Coord] = None):
        self.head = head
        self.city_blocks: Grid = city_blocks
        self.end_coord: Coord = end_coord
        self.body: str = body
        self.parent: Optional[Coord] = parent

        if body is None:
            self.body = "." * self.max_straight

        self.valid_moves: list[(Coord, str)] = self._valid_moves()

        tmp: Coord = end_coord - self.head
        self._edge_cost: int = 0
        self._eta: int = tmp.row + tmp.col
        self._dir = ">"

    def _valid_moves(self) -> list[(Coord, str)]:
        valid: list[(Coord, str, int)] = list()
        for move in ((Coord(1, 0), "v"), (Coord(-1, 0), "^"),
                     (Coord(0, 1), ">"), (Coord(0, -1), "<")):
            add: Coord = move[0]
            new_spot: Coord = add + self.head
            new_dir: str = move[1]
            new_body: str = new_dir + self.body
            new_body = new_body[:self.max_straight]
            cost = 0

            # can't go out of bounds
            if new_spot.between(Coord(0, 0), self.end_coord):
                cost = int(self.city_blocks[new_spot.row][new_spot.col])

                # can't turn on itself
                if self.parent is not None and self.parent == new_spot:
                    continue

                # can't go in same directions for more than self.max_straight
                if self.max_straight and re.search(r"^(.)\1*$", new_body):
                    continue

                # cannot turn unless we have gone is a straight direction for min_straight
                if self.max_straight and new_dir != self.body[0]:
                    cost = 0
                    new_body = self.body
                    new_spot = self.head
                    for _ in range(self.min_straight):
                        new_body = new_dir + new_body
                        new_spot = add + new_spot
                        if not new_spot.between(Coord(0, 0), self.end_coord):
                            continue
                        cost += int(self.city_blocks[new_spot.row][new_spot.col])
                    if not new_spot.between(Coord(0, 0), self.end_coord):
                        continue

                valid.append((new_spot, new_body[:self.max_straight], cost))
        return valid

    def key(self):
        return str(self)

    def children(self) -> list[Crucible]:
        kids: list[Crucible] = list()
        for block, new_body, cost in self.valid_moves:
            child = Crucible(block, self.city_blocks, self.end_coord, new_body, self.head)
            child._edge_cost = cost
            kids.append(child)
        return kids

    def edge_cost(self, prev: Optional[DijkstraObject] = None) -> Cost:
        return self._edge_cost

    def eta(self, node=None) -> Cost:
        return self._eta

    def __str__(self):
        return f"{self.head}({self.body})"

    def __repr__(self):
        return str(self)


# ========================================================================================
# Main
# ========================================================================================
def main(part: int = 1):

    # parse
    file = open("day_17_input.txt", 'r')
    city: Grid = list()
    for row, line in enumerate(map(str.rstrip, file)):
        city.append(line)
    max_row = len(city) - 1
    max_col = len(city[0]) - 1

    # part 1
    # part 1
    Crucible.max_straight = 4
    Crucible.min_straight = 1

    start: Crucible = Crucible(Coord(0, 0), city, Coord(max_row, max_col))
    astar = AStar(start)
    final_node: Node = astar.find_until(
        lambda x: x.head == Coord(max_row, max_col), 1000)

    print(f"Cost to get to final node: {final_node.cumulative_cost}")

    # part 2
    Crucible.max_straight = 11
    Crucible.min_straight = 4

    start: Crucible = Crucible(Coord(0, 0), city, Coord(max_row, max_col))
    astar = AStar(start)
    final_node: Node = astar.find_until(
        lambda x: x.head == Coord(max_row, max_col))

    print(f"Cost to get to final node: {final_node.cumulative_cost}")


if __name__ == "__main__":
    main()

"""
1 3 26 23 (0,0)(>:...) => (1,0)(v:>..)
2 4 27 23 (0,0)(>:...) => (0,1)(>:>..)
3 5 27 22 (1,0)(v:>..) => (1,1)(>:v>.)
4 5 27 22 (0,1)(>:>..) => (0,2)(>:>>.)
5 6 27 21 (1,1)(>:v>.) => (1,2)(>:>v>)
6 6 27 21 (0,2)(>:>>.) => (1,2)(v:>>>)
7 6 28 22 (0,1)(>:>..) => (1,1)(v:>>.)
8 6 28 22 (1,0)(v:>..) => (2,0)(v:v>.)
9 7 28 21 (1,1)(>:v>.) => (2,1)(v:>v>)
10 7 28 21 (1,1)(v:>>.) => (1,2)(>:v>>)
"""

# should be:
"""
1  3 26 23 (0,0) >:... => (1,0) v:>..
2  4 27 23 (0,0) >:... => (0,1) >:>..
3  5 27 22 (1,0) v:>.. => (1,1) >:v>.
4  5 27 22 (0,1) >:>.. => (0,2) >:>>.
5  6 27 21 (1,1) >:v>. => (1,2) >:>v>
6  6 27 21 (0,2) >:>>. => (1,2) v:>>>
7  6 28 22 (0,1) >:>.. => (1,1) v:>>.
8  6 28 22 (1,0) v:>.. => (2,0) v:v>.
9  7 28 21 (1,1) >:v>. => (1,2) >:>v>
10 7 28 21 (1,1) v:>>. => (2,1) v:v>>
"""

"""
0 0 0 24 None=> (0,0):[(-1,-1), (-1,-1), (-1,-1)]
1 3 26 23 (0,0):[(-1,-1), (-1,-1), (-1,-1)] => (1,0):[(0,0), (-1,-1), (-1,-1)]
2 4 27 23 (0,0):[(-1,-1), (-1,-1), (-1,-1)] => (0,1):[(0,0), (-1,-1), (-1,-1)]
3 5 27 22 (1,0):[(0,0), (-1,-1), (-1,-1)] => (1,1):[(1,0), (0,0), (-1,-1)]
4 5 27 22 (0,1):[(0,0), (-1,-1), (-1,-1)] => (0,2):[(0,1), (0,0), (-1,-1)]
5 6 27 21 (1,1):[(1,0), (0,0), (-1,-1)] => (1,2):[(1,1), (1,0), (0,0)]
6 6 27 21 (0,2):[(0,1), (0,0), (-1,-1)] => (1,2):[(0,2), (0,1), (0,0)]
7 6 28 22 (0,1):[(0,0), (-1,-1), (-1,-1)] => (1,1):[(0,1), (0,0), (-1,-1)]
8 6 28 22 (1,0):[(0,0), (-1,-1), (-1,-1)] => (2,0):[(1,0), (0,0), (-1,-1)]
9 7 28 21 (1,1):[(0,1), (0,0), (-1,-1)] => (1,2):[(1,1), (0,1), (0,0)]
10 7 28 21 (1,1):[(1,0), (0,0), (-1,-1)] => (2,1):[(1,1), (1,0), (0,0)]
"""

"""
40 13 33 20 (2,1)(vv>) => (2,2)(>vv)
41 13 33 20 (2,1)(v>>) => (2,2)(vv>)
42 13 33 20 (0,3)(>>>) => (1,3)(>>>)
43 14 34 20 (0,3)(^>>) => (0,4)(>^>)
44 14 34 20 (2,1)(<v>) => (3,1)(v<v)
45 15 34 19 (2,2)(>>v) => (3,2)(v>>)
46 12 34 22 (1,2)(^>v) => (0,2)(>^>)
47 13 34 21 (0,2)(^>v) => (0,3)(>^>)
48 11 34 23 (1,1)(v>>) => (1,0)(<v>)
49 15 34 19 (3,1)(v>v) => (3,2)(vv>)
50 12 34 22 (1,0)(v>>) => (2,0)(<v>)


40 13 33 20 (2,1):[(1,1), (0,1), (0,0)] => (2,2):[(2,1), (1,1), (0,1)]
41 13 33 20 (0,3):[(0,2), (0,1), (0,0)] => (1,3):[(0,3), (0,2), (0,1)]
42 11 34 23 (0,2):[(1,2), (1,1), (1,0)] => (0,1):[(0,2), (1,2), (1,1)]
43 15 34 19 (2,2):[(1,2), (0,2), (0,1)] => (3,2):[(2,2), (1,2), (0,2)]
44 15 34 19 (1,3):[(1,2), (0,2), (0,1)] => (1,4):[(1,3), (1,2), (0,2)]
45 11 34 23 (1,1):[(1,2), (0,2), (0,1)] => (1,0):[(1,1), (1,2), (0,2)]
46 15 34 19 (2,2):[(1,2), (1,1), (1,0)] => (3,2):[(2,2), (1,2), (1,1)]
47 13 34 21 (2,2):[(2,1), (1,1), (1,0)] => (1,2):[(2,2), (2,1), (1,1)]
48 14 34 20 (2,1):[(1,1), (1,2), (0,2)] => (3,1):[(2,1), (1,1), (1,2)]
49 12 34 22 (1,2):[(1,1), (2,1), (2,0)] => (0,2):[(1,2), (1,1), (2,1)]
50 13 34 21 (2,0):[(2,1), (1,1), (1,0)] => (3,0):[(2,0), (2,1), (1,1)]


50 12 34 22 (1,0)(v>>) => (2,0)(<v>)
50 13 34 21 (2,0):[(2,1), (1,1), (1,0)] => (3,0):[(2,0), (2,1), (1,1)]

60 16 35 19 (2,2):[(2,1), (1,1), (1,0)] => (3,2):[(2,2), (2,1), (1,1)]
60 16 35 19 (1,3)(>>v) => (2,3)(>>>)

70 11 35 24 (0,1):[(1,1), (1,0), (0,0)] => (0,0):[(0,1), (1,1), (1,0)]
70 11 35 24 (0,1)(>v>) => (0,0)(^>v)


80 15 36 21 (0,2)(>^>) => (0,3)(^>^)
80 16 35 19 (2,2):[(1,2), (0,2), (0,1)] => (2,3):[(2,2), (1,2), (0,2)]

100 15 36 21 (2,0)(<v>) => (3,0)(v<v)
100 18 37 19 (1,3):[(0,3), (0,2), (0,1)] => (2,3):[(1,3), (0,3), (0,2)]

"""
