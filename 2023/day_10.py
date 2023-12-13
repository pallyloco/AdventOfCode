"""
| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile,
  but your sketch doesn't show what shape the pipe has.
"""
from __future__ import annotations
import re

MAX_ROW: int = 0
MAX_COL: int = 0
MIN_ROW: int = 0
MIN_COL: int = 0
from typing import Any, Optional
from Grid import Grid, DataPoint


# 931 too high
# 712 too high
# 684 too high
class Pipe:
    def __init__(self, row: int, col: int, value: str):
        self.row = row
        self.col = col
        self.value = value

    def __eq__(self, other):
        if other is None:
            return False
        return self.row == other.row and self.col == other.col

    def __str__(self):
        return f"({self.row},{self.col}) = {self.value}"

    def __repr__(self):
        return str(self)


def main():
    global MIN_COL, MIN_ROW, MAX_COL, MAX_ROW
    file = open("day_10_input.txt", 'r')
    pipe_grid = Grid()
    new_grid = Grid()
    start = None
    for row, line in enumerate(map(str.rstrip, file)):
        for col, char in enumerate(line):
            pipe_grid.set_value(Pipe(row, col, char))
            if char == "S":
                start = Pipe(row, col, char)

    current: list[tuple[Pipe, Pipe]] = list()
    current.append((start, start))
    new_grid.set_value(start)

    # what two pipes connect to start position?
    connectors: list[Optional[Pipe]] = list()
    if pipe_grid.north(start) is not None and pipe_grid.north(start).value in "|7F":
        connectors.append(pipe_grid.north(start))
    if pipe_grid.south(start) is not None and pipe_grid.south(start).value in "|LJ":
        connectors.append(pipe_grid.south(start))
    if pipe_grid.east(start) is not None and pipe_grid.east(start).value in "-J7":
        connectors.append(pipe_grid.east(start))
    if pipe_grid.west(start) is not None and pipe_grid.west(start).value in "-LF":
        connectors.append(pipe_grid.west(start))

    current.append((connectors[0], connectors[1]))
    new_grid.set_value(start)
    new_grid.set_value(connectors[0])

    if pipe_grid.west(start) in connectors and pipe_grid.east(start) in connectors:
        start.value = "-"
    elif pipe_grid.north(start) in connectors and pipe_grid.south(start) in connectors:
        start.value = "|"
    elif pipe_grid.west(start) in connectors and pipe_grid.north(start) in connectors:
        start.value = "J"
    elif pipe_grid.east(start) in connectors and pipe_grid.north(start) in connectors:
        start.value = "L"
    elif pipe_grid.south(start) in connectors and pipe_grid.east(start) in connectors:
        start.value = "F"
    elif pipe_grid.west(start) in connectors and pipe_grid.south(start) in connectors:
        start.value = "7"

    pipe_grid.set_value(start)
    loop = list()
    loop.append(start)
    loop.append(current[-1][0])
    new_grid = Grid()
    new_grid.set_value(start)
    new_grid.set_value(loop[-1])
    num = 0
    while loop[0] != loop[-1]:
        if num > 200000:
            break
        num += 1
        right = loop[-1]
        prev_right = loop[-2]
        n2 = next_pipe(pipe_grid, right, prev_right)
        new_grid.set_value(n2)
        loop.append(next_pipe(pipe_grid, right, prev_right))

    print("answer 1:", (len(loop)) // 2)

    # ========= PART 2
    MIN_ROW = new_grid.min_row()
    MAX_ROW = new_grid.max_row()
    MIN_COL = new_grid.min_col()
    MAX_COL = new_grid.max_col()

    # find an outside edge
    cell = None
    for col in range(MIN_COL, MAX_COL + 1):
        cell: Optional[DataPoint | Pipe] = new_grid.get_data_point(MIN_ROW, col)
        if cell is not None:
            break

    # go over the loop and mark any adjacent water
    loopy(new_grid, cell)
    fill_in_water(new_grid)

    font_change = {"F":"╭", "L":"╰", "J":"╯ ", "7":"╮", "-":"─","|":"│","~":" "}
    ans2 = 0
    for row in range(MIN_ROW, MAX_ROW+1):
        for col in range(MIN_COL, MAX_COL+1):
            pt = new_grid.get_data_point(row,col)
            if pt is None:
                ans2 += 1
                new_grid.set_value(Pipe(row,col, "▒"))
            else:
                new_grid.set_value(Pipe(row, col, font_change[pt.value]))
    print(new_grid)

    print("Answer 2:", ans2)



def fill_in_water(grid: Grid):
    done = False
    while not done:
        done = True
        for r in range(MIN_ROW, MAX_ROW + 1):
            for c in range(MIN_COL, MAX_COL + 1):
                pt = grid.get_data_point(r, c)
                if pt is None:
                    for n in grid.ordinal_neighbours(Pipe(r, c, " ")):
                        if n is not None and n.value == "~":
                            grid.set_value(Pipe(r, c, "~"))
                            done = False
                            break

def loopy(grid: Grid, pipe:Pipe):
    direction = "east"
    r, c = (0, 0)
    pipe_start = pipe
    # stuck on start at (41,91)
    while True:
        if pipe.value == "-" and (direction == "north" or direction == "south"):
            pass
        if pipe.value == "|" and (direction == "east" or direction == "west"):
            pass

        if pipe.value == "|":
            if direction == "north":
                mark_outside("west", grid, pipe.row, pipe.col)
                pipe = grid.north(pipe)
            elif direction == "south":
                mark_outside("east", grid, pipe.row, pipe.col)
                pipe = grid.south(pipe)

        elif pipe.value == "-":
            if direction == "east":
                r, c = mark_outside("north", grid, pipe.row, pipe.col)
                pipe = grid.east(pipe)
            elif direction == "west":
                r, c = mark_outside("south", grid, pipe.row, pipe.col)
                pipe = grid.west(pipe)

        elif pipe.value == "J":
            if direction == "south":
                r, c = mark_outside("east", grid, pipe.row, pipe.col)
                r, c = mark_outside("south", grid, r, c)
                r, c = mark_outside("west", grid, r, c)
                direction = "west"
                pipe = grid.west(pipe)
            elif direction == "east":
                pipe = grid.north(pipe)
                direction = "north"

        elif pipe.value == "L":
            if direction == "west":
                r, c = mark_outside("west", grid, pipe.row, pipe.col)
                r, c = mark_outside("south", grid, r, c)
                r, c = mark_outside("east", grid, r, c)
                direction = "north"
                pipe = grid.north(pipe)
            elif direction == "south":
                direction = "east"
                pipe = grid.east(pipe)

        elif pipe.value == "7":
            if direction == "east":
                r, c = mark_outside("north", grid, pipe.row, pipe.col)
                r, c = mark_outside("east", grid, r, c)
                r, c = mark_outside("south", grid, r, c)
                pipe = grid.south(pipe)
                direction = "south"
            elif direction == "north":
                pipe = grid.west(pipe)
                direction = "west"

        elif pipe.value == "F":
            if direction == "north":
                r, c = mark_outside("west", grid, pipe.row, pipe.col)
                r, c = mark_outside("north", grid, r, c)
                r, c = mark_outside("east", grid, r, c)
                pipe = grid.east(pipe)
                direction = "east"
            elif direction == "west":
                pipe = grid.south(pipe)
                direction = "south"
            elif direction == "east":
                r, c = mark_outside("west", grid, pipe.row, pipe.col)
                r, c = mark_outside("north", grid, r, c)
                r, c = mark_outside("east", grid, r, c)
                pipe = grid.east(pipe)

        if pipe == pipe_start:
            break

def set_water(grid, row, col):
    if inside_grid_area(row, col):
        pt = grid.get_data_point(row, col)
        if pt is None:
            grid.set_value(Pipe(row, col, "~"))

def inside_grid_area(row: int, col: int) -> bool:
    return MIN_ROW <= row <= MAX_ROW and MIN_COL <= col <= MAX_COL

def mark_outside(direction: str, grid: Grid, r, c) -> tuple[int, int]:
    if direction == "north":
        r = r - 1
        c = c
    elif direction == "south":
        r = r + 1
        c = c
    elif direction == "west":
        r = r
        c = c - 1
    elif direction == "east":
        r = r
        c = c + 1
    set_water(grid, r, c)
    return r, c

def next_pipe(grid: Grid, pipe: Pipe, previous: Pipe) -> Pipe | DataPoint:
    if pipe.value == "|":
        if grid.north(pipe) != previous:
            return grid.north(pipe)
        return grid.south(pipe)
    if pipe.value == "-":
        if grid.west(pipe) != previous:
            return grid.west(pipe)
        return grid.east(pipe)
    if pipe.value == "L":
        if grid.north(pipe) != previous:
            return grid.north(pipe)
        return grid.east(pipe)
    if pipe.value == "J":
        if grid.north(pipe) != previous:
            return grid.north(pipe)
        return grid.west(pipe)
    if pipe.value == "7":
        if grid.south(pipe) != previous:
            return grid.south(pipe)
        return grid.west(pipe)
    if pipe.value == "F":
        if grid.south(pipe) != previous:
            return grid.south(pipe)
        return grid.east(pipe)


if __name__ == "__main__":
    main()
