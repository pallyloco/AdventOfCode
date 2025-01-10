from __future__ import annotations
from typing import Any

from grid import Grid
from coord import Coord, Direction
from astar import AStar, Node, DijkstraObject

CHEAT_LENGTH = 20

input_data = [
    "###############",
    "#...#...#.....#",
    "#.#.#.#.#.###.#",
    "#S#...#.#.#...#",
    "#######.#.#.###",
    "#######.#.#...#",
    "#######.#.###.#",
    "###..E#...#...#",
    "###.#######.###",
    "#...###...#...#",
    "#.#####.#.###.#",
    "#.#...#.#.#...#",
    "#.#.#.#.#.#.###",
    "#...#...#...###",
    "###############",
]

fh = open("day_20.txt", "r")
input_data = list(map(str.rstrip, fh))

viable_cheats = set()
start_point: Coord = Coord(0, 0)
end_point: Coord = Coord(0, 0)


class DijkstraObj(Coord):
    def __init__(self, grid: Grid, row: int, col: int, value: Any = None, *,
                 direction=Direction.NORTH):
        super().__init__(row, col, value, direction=direction)
        self.grid = grid

    def key(self) -> str:
        return f"({self.row},{self.col})"

    def copy(self):
        return type(self)(self.grid, self.row, self.col, self.value)

    def children(self) -> list[DijkstraObj]:
        empty_neighbours = []
        for r in self.ordinal_neighbours():
            if self.grid.min_col() <= r.col <= self.grid.max_col() and \
                    self.grid.min_row() <= r.row <= self.grid.max_row():
                dp = self.grid.get_data_point(r.row, r.col)
                if dp is None or (dp.value != "#" and dp.value != "+"):
                    empty_neighbours.append(r)

        return empty_neighbours

    def edge_cost(self, prev: DijkstraObj) -> int:
        """How much does it cost to get from prev to self"""
        return 1

    def eta(self, node=None) -> int:
        return 0


def main(data):
    global start_point, end_point
    maze, start_point, end_point = read_map(data)

    def cb(coord: DijkstraObj) -> bool:
        return coord.row == end_point.row and coord.col == end_point.col

    # solve for all cells using dijkstra, with no cheats
    start = DijkstraObj(maze, start_point.row, start_point.col)
    astar = AStar(start)
    final_node = astar.find_until(cb)

    # save all the costs to reach each cell on the normal path
    max_cost = final_node.cumulative_cost
    path_nodes = astar.get_path(final_node)

    print(f"Cost to get to final node: {final_node.cumulative_cost}")

    # at each point along the path, check for cheating
    results = {}
    for node in path_nodes:
        start_point = node.obj
        initial_cost = node.cumulative_cost
        for re_enter_node in reversed(path_nodes):
            cheat_length = start_point.manhatten_distance(re_enter_node.obj)
            if cheat_length > CHEAT_LENGTH:
                continue
            to_finish_cost = max_cost - re_enter_node.cumulative_cost
            cost = initial_cost + cheat_length + to_finish_cost
            saved = max_cost - cost
            if saved >= 50:
                if saved not in results:
                    results[saved] = set()
                results[saved].add(f"{start_point.key()}-{re_enter_node.obj.key()}")

    answer_1 = sum([len(num) for speed, num in results.items() if speed >= 100])
    print(answer_1)


def read_map(data) -> tuple[Grid, Coord, Coord]:
    maze = Grid()
    start = Coord(0, 0)
    end = Coord(0, 0)
    for row, line in enumerate(data):
        for col, value in enumerate(line):
            if value == "#":
                maze.set_value(DijkstraObj(maze, row, col, value))
            if value == "S":
                start = DijkstraObj(maze, row, col, "S")
            if value == "E":
                end = DijkstraObj(maze, row, col, "E")
                maze.set_value(DijkstraObj(maze, row, col, value))
    return maze, start, end


main(input_data)
