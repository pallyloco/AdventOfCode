from __future__ import annotations

from typing import Any

from grid import Grid
from coord import Coord, Direction
from astar import AStar, Node

input_data = [
    "5,4",
    "4,2",
    "4,5",
    "3,0",
    "2,1",
    "6,3",
    "2,4",
    "1,5",
    "0,6",
    "3,3",
    "2,6",
    "5,1",
    "1,2",
    "5,5",
    "2,5",
    "6,5",
    "1,4",
    "0,4",
    "6,4",
    "1,1",
    "6,1",
    "1,0",
    "0,5",
    "1,6",
    "2,0",
]


fh = open("day_18.txt", "r")
input_data = list(map(str.rstrip, fh))

class You(Coord):

    def __init__(self, size: int, grid: Grid, row: int, col: int, value: Any = None, *, direction=Direction.NORTH):
        super().__init__(row, col, value, direction=direction)
        self.grid = grid
        self.size = size

    def key(self) -> str:
        return str(self)

    def children(self) -> list[You]:
        viable_children = []
        for direction in (Direction.EAST, Direction.WEST, Direction.SOUTH, Direction.NORTH):
            row = self.row + direction.value[0]
            col = self.col + direction.value[1]
            if 0 <= row <= self.size and 0 <= col <= self.size:
                if self.grid.get_data_point(row, col) is None or self.grid.get_data_point(row, col).value != "#":
                    viable_children.append(You(self.size, self.grid, row, col))
        return viable_children

    def edge_cost(self, prev: You) -> int:
        return 1

    def eta(self, node=None) -> int:
        return abs(self.row - self.size) + abs(self.col - self.size)


def main(data, max_bytes, size):
    byte_grid = Grid()

    def cb_function(r: You) -> bool:
        return r.row == size and r.col == size

    for num_bytes, line in enumerate(data):
        col, row = list(map(int, line.split(",")))
        byte_grid.set_value(Coord(row, col, "#"))

        if num_bytes == max_bytes:
            astar = AStar(You(size,byte_grid,0,0))
            final_node: Node = astar.find_until(cb_function)
            print(f"{num_bytes:5d} Cost to get to final node: {final_node.cumulative_cost}")

        if num_bytes > max_bytes:

            astar = AStar(You(size,byte_grid,0,0))
            final_node: Node = astar.find_until(cb_function)
            if final_node is None:
                print(f"{col},{row}")
                break


main(input_data,1024,70)