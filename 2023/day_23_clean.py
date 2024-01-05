from __future__ import annotations
from typing import Any, Optional

from Grid import Grid, DataPoint
from Coords import Coord

grid = Grid()
nodes: list[ForestSpot] = list()
all_paths = list()
rock = ","


def main(part: int = 1):
    grid.clear()
    nodes.clear()
    all_paths.clear()

    file = open("day_23_input.txt", 'r')
    for row, line in enumerate(map(str.rstrip, file)):
        for col, char in enumerate(line):
            if char == "#":
                char = rock
            grid.set_value(ForestSpot(row, col, char))

    # find all nodes
    start = grid.get_data_point(0, 1)
    end = grid.get_data_point(grid.max_row(), grid.max_col() - 1)
    start.isNode = True
    end.isNode = True
    nodes.append(start)
    nodes.append(end)
    for spot in grid.data:
        if spot.value == rock:
            continue
        kids = spot.children(part)
        if len(kids) > 2:
            nodes.append(spot)
            spot.isNode = True

    # find the distance between all nodes
    for node in nodes:
        for kid in node.children(part):
            spot = kid
            cells = list()

            # keep going until you can't go any further, or have stumbled onto another node
            while True:
                cells.append(spot)

                if spot.isNode:
                    node.add_connection(spot, cells)
                    break

                # look for next available spot
                k = [c for c in spot.children(part) if c not in cells and c != node]
                if len(k) == 0:
                    break

                # rinse and repeat
                spot = k[0]

    find_all_paths(start, end)
    max_path = max(all_paths)
    print("Answer:",max_path[0])


def find_all_paths(start: ForestSpot, end: ForestSpot, distance: int = 0, path=""):
    path += f"{start} "
    if start == end:
        all_paths.append((distance, path))
        path += f"{end} "
        return

    for node, length, cells in start.connected_to:
        if str(node) not in path:
            find_all_paths(node, end, distance + length, path)


class ForestSpot(Coord):
    def __init__(self, row: int, col: int, value: Any):
        self.coord = Coord(row, col,value)
        super().__init__(row, col, value)
        self._children: Optional[list[ForestSpot]] = None
        self.connected_to: list[(ForestSpot, len, list[ForestSpot])] = list()
        self.isNode = False

    def add_connection(self, other: ForestSpot, connected_by: [ForestSpot]):
        self.connected_to.append((other, len(connected_by), connected_by))

    def children(self, part) -> list[ForestSpot]:
        if part == 1 and self.value == ">":
            kids = [n for n in [grid.east(self.coord)] if n is not None and n.value != rock]
        elif part == 1 and self.coord.value == "<":
            kids = [n for n in [grid.west(self.coord)] if n is not None and n.value != rock]
        elif part == 1 and self.coord.value == "^":
            kids = [n for n in [grid.north(self.coord)] if n is not None and n.value != rock]
        elif part == 1 and self.coord.value == "v":
            kids = [n for n in [grid.south(self.coord)] if n is not None and n.value != rock]
        else:
            kids = [n for n in grid.ordinal_neighbours(self.coord) if n is not None and n.value != rock]
        return kids

if __name__ == "__main__":
    main(1)
    main(2)
