from __future__ import annotations
from typing import Any, Callable, Optional

from grid import Grid
from coord import Coord, Direction
from astar import AStar, Node

input_data = [
    "##################",
    "# ...#...#...#..E#",
    "# .#.#.#.#.#.#.#.#",
    "# .#.#.#...#...#.#",
    "# .#.#.#.###.#.#.#",
    "# ...#.#.#.....#.#",
    "# .#.#.#.#.#####.#",
    "# .#...#.#.#.....#",
    "# .#.#####.#.###.#",
    "# .#.#.......#...#",
    "# .#.###.#####.###",
    "# .#.#...#.....#.#",
    "# .#.#.#####.###.#",
    "# .#.#.........#.#",
    "# .#.#.#########.#",
    "# S#.............#",
    "#################",
]

fh = open("day_16.txt", "r")
input_data = list(map(str.rstrip, fh))


class Reindeer(Coord):
    @staticmethod
    def copy(r: Reindeer):
        return Reindeer(r.grid, r.row, r.col, r.value, direction=r.direction)

    def __init__(self, grid: Grid, row: int, col: int, value: Any = None, *, direction=Direction.NORTH):
        super().__init__(row, col, value, direction=direction)
        self.grid = grid

    def key(self) -> str:
        return str(self)

    def children(self) -> list[Reindeer]:
        r1 = Reindeer.copy(self)
        r1.rotate_90_clockwise()
        r2 = Reindeer.copy(self)
        r2.rotate_90_counter_clockwise()
        r3 = Reindeer.copy(self)
        r3.move(1)
        viable_children = []
        for r in (r1, r2, r3):
            if self.grid.get_data_point(r.row, r.col) is None:
                viable_children.append(r)
        return viable_children

    def edge_cost(self, prev: Reindeer) -> int:
        """How much does it cost to get from prev to self"""
        if self.direction == prev.direction:
            return 1
        else:
            return 1000

    def eta(self, node=None) -> int:
        return 0


def main(data):
    maze, start, end = read_map(data)
    start.direction = Direction.EAST

    def cb_function(r: Reindeer) -> bool:
        return r.row == end.row and r.col == end.col

    reindeer_start = Reindeer(maze, start.row, start.col, start.value, direction=start.direction)
    astar = AStar(reindeer_start)

    final_node: Node = astar.find_until(cb_function)

    print(f"Cost to get to final node: {final_node.cumulative_cost}")

    states = set()
    seen = set(f"{start.row},{start.col}")

    get_all_paths(reindeer_start,final_node.obj,final_node.cumulative_cost, states)
    print("Number of best seats: ",len(states))



def get_all_paths(start: Reindeer, end: Reindeer, max_cost, states: set ):
    astar_forward = AStar(start)
    astar_forward.find_all()
    forward_nodes = [n for n in astar_forward.all_nodes.values() if n.cumulative_cost <= max_cost]

    # to set end position, reverse direction
    end.reverse_direction()
    astar_backward = AStar(end)
    astar_backward.find_all()
    backward_node_keys = astar_backward.all_nodes

    for forward_node in forward_nodes:
        forward_node.obj.reverse_direction()
        if forward_node.obj.key() in backward_node_keys:
            backward_node = astar_backward.all_nodes[forward_node.obj.key()]
            if (forward_node.cumulative_cost + backward_node.cumulative_cost) <= max_cost:
                states.add(f"{forward_node.obj.row},{forward_node.obj.col}")


def read_map(data) -> tuple[Grid, Coord, Coord]:
    maze = Grid()
    start = Coord(0, 0)
    end = Coord(0, 0)
    for row, line in enumerate(data):
        for col, value in enumerate(line):
            if value == "#":
                maze.set_value(Coord(row, col, value))
            if value == "S":
                start = Coord(row, col, "S")
            if value == "E":
                end = Coord(row, col, "S")
    return maze, start, end


main(input_data)
