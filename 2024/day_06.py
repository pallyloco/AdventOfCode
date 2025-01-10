from typing import Optional

from grid import Grid
from coord import Coord

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
    fh = open("day_06.txt", "r")
    data = list(map(str.rstrip,fh))
    guard, plan = read_map(data)
    fh.close()
    patrol(guard, plan)
    total = sum(1 for x in plan.data if x.value == "X")

    # part 2
    guarded_spots = [x for x in plan.data if x.value == "X"]
    obstacles = 0
    for gs in guarded_spots:
        guard, plan = read_map(data)
        plan.set_value(Coord(gs.row, gs.col, "O"))
        if gs.row == 6 and gs.col == 3:
            pass
        result = patrol(guard,plan,False)
        if result:
            obstacles += 1
    print(obstacles)


def patrol(guard, plan, save_positions=True):
    max_row = plan.max_row()
    max_col = plan.max_col()
    positions_and_directions = []
    n = 0
    while 0 <= guard.row <= max_row and 0 <= guard.col <= max_col:
        n = n+1
        if is_obstacle_in_path(guard, plan):
            guard.rotate_90_clockwise()
            continue
        if save_positions:
            pass
        else:
            if (guard.row, guard.col, guard.direction) in positions_and_directions:
                return True
        positions_and_directions.append((guard.row, guard.col, guard.direction))
        plan.set_value(Coord(guard.row,guard.col,"X"))
        guard.move(1)
        if n > 100000:
            exit()
#        print(plan)
    return False


def is_obstacle_in_path(guard, plan) -> bool:
    row = guard.direction.value[0] + guard.row
    col = guard.direction.value[1] + guard.col
    coord = plan.get_data_point(row, col)
    if coord is None:
        return False
    return coord.value == "#" or coord.value == "O"


def read_map(lines) -> tuple[Coord, Grid]:
    guard: Coord = Coord(0, 0, ".")
    plan = Grid()
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == "^":
                guard: Coord = Coord(row, col, "X")
                plan.set_value(guard)
            else:
                plan.set_value(Coord(row, col, char))
    return guard, plan


main()
