from typing import Optional
import time
from grid import Grid
from coord import Coord

"""
The map shows the current position of the guard with ^ (to indicate the guard is currently 
facing up from the perspective of the map). Any obstructions - crates, desks, alchemical reactors, etc. - 
are shown as #.

Lab guards in 1518 follow a very strict patrol protocol which involves repeatedly following these steps:

If there is something directly in front of you, turn right 90 degrees.
Otherwise, take a step forward.
"""

data = [
    "....#.....",
    ".........#",
    "..........",
    "..#.......",
    ".......#..",
    "..........",
    ".#..^.....",
    "........#.",
    "#.........",
    "......#...",
]


def main():
    # part 1
    # Predict the path of the guard. How many distinct positions will
    # the guard visit before leaving the mapped area?
    fh = open("day_06.txt", "r")
    data = list(map(str.rstrip, fh))
    guard, plan = read_map(data)
    fh.close()
    patrol(guard, plan)
    total = sum(1 for x in plan.data if x.value == "X")
    print(total)

    # part 2
    # You need to get the guard stuck in a loop by adding a single new obstruction.
    # How many different positions could you choose for this obstruction?
    t1 = time.time()
    guarded_spots = [x for x in plan.data if x.value == "X"]
    obstacles = 0
    print("Please wait, this takes time, ~ 1/2 minute")
    for gs in guarded_spots:
        guard, plan = read_map(data)
        plan.set_value(Coord(gs.row, gs.col, "O"))
        result = patrol(guard, plan)
        if result:
            obstacles += 1
    t2 = time.time()
    print(f"Time taken = {int(t2 - t1)} seconds")
    print(obstacles)


def patrol(guard, plan):
    max_row = plan.max_row()
    max_col = plan.max_col()
    positions_and_directions = set()
    while 0 <= guard.row <= max_row and 0 <= guard.col <= max_col:
        if is_obstacle_in_path(guard, plan):
            guard.rotate_90_clockwise()
            if f"({guard.row},{guard.col}) {guard.direction}" in positions_and_directions:
                return True
            positions_and_directions.add(f"({guard.row},{guard.col}) {guard.direction}")
            continue

        plan.set_value(Coord(guard.row, guard.col, "X"))
        guard.move(1)
    return False


def is_obstacle_in_path(guard, plan) -> bool:
    row = guard.direction.value[0] + guard.row
    col = guard.direction.value[1] + guard.col
    coord = plan.get_data_point(row, col)
    if coord is None:
        return False
    return coord.value == "#" or coord.value == "O"


def read_map(lines) -> tuple[Coord, Grid]:
    plan = Grid(lines)
    guard = [dp for dp in plan.data if dp.value == "^"][0]
    guard.value = "#"
    plan.set_value(guard)
    return guard, plan


main()
