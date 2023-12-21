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

from typing import Any, Optional
from Grid import Grid, DataPoint
from Polygon import Polygon
from Coords import Coord

def main():
    file = open("day_10_input.txt", 'r')
    pipe_pieces_grid = Grid()
    cleaned_grid = Grid()
    start = None

    # set the pipes onto the grid, and find the starting
    # location (indicated by 'S')
    for row, line in enumerate(map(str.rstrip, file)):
        for col, char in enumerate(line):
            pipe_pieces_grid.set_value(Coord(row, col, char))
            if char == "S":
                start = Coord(row, col, char)

    # find one pipe piece that is allowed to connect to the start position?
    piece: Optional[Coord] = None
    if pipe_pieces_grid.north(start) is not None and pipe_pieces_grid.north(start).value in "|7F":
        piece = pipe_pieces_grid.north(start)
    elif pipe_pieces_grid.south(start) is not None and pipe_pieces_grid.south(start).value in "|LJ":
        piece = pipe_pieces_grid.south(start)
    elif pipe_pieces_grid.east(start) is not None and pipe_pieces_grid.east(start).value in "-J7":
        piece = pipe_pieces_grid.east(start)
    elif pipe_pieces_grid.west(start) is not None and pipe_pieces_grid.west(start).value in "-LF":
        piece = pipe_pieces_grid.west(start)
    if piece is None:
        raise ValueError

    # start at start, pick one connector and follow it
    pipe: list[Coord] = list()
    pipe.append(start)
    pipe.append(piece)
    cleaned_grid.set_value(start)
    cleaned_grid.set_value(piece)

    # loop until we come back to where we came from
    # use a for loop to make sure we don't have an infinite loop
    for _ in range(200000):
        if pipe[0] == pipe[-1]:
            break
        current = pipe[-1]
        prev = pipe[-2]
        n2 = next_pipe(pipe_pieces_grid, current, prev)
        pipe.append(n2)
        cleaned_grid.set_value(n2)

    print("answer 1:", (len(pipe)) // 2)

    # PART 2 - Find the inner volume that the pipes enclose
    pipe_vertices: Polygon = Polygon()
    for piece in pipe:
        if piece.value != "|" and piece.value != "-":
            pipe_vertices.add_inside_vertex(piece)

    print("answer 2:", pipe_vertices.inner_volume())

def next_pipe(grid: Grid, pipe: Coord, previous: Coord) -> Coord | DataPoint:
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

