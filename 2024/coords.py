from __future__ import annotations
from enum import Enum

from typing import Any, Optional


class Direction(Enum):
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    EAST = (0, 1)
    WEST = (0, -1)
    NORTH_WEST = (-1, -1)
    NORTH_EAST = (-1, 1)
    SOUTH_WEST = (1, -1)
    SOUTH_EAST = (1, 1)

    def __str__(self):
        return str(self.value)


class Coord:
    def __init__(self, row, col, value: Any = None):
        self.row: int = row
        self.col: int = col
        self.value = value
        self.direction = Direction.NORTH

    def move(self, amount: int, direction: Optional[Direction] = None):
        if direction is None:
            direction = self.direction
        self.row = self.row + direction.value[0]
        self.col = self.col + direction.value[1]

    def rotate_45_clockwise(self):
        if self.direction == Direction.NORTH:
            self.direction = Direction.NORTH_EAST
        elif self.direction == Direction.NORTH_EAST:
            self.direction = Direction.EAST
        elif self.direction == Direction.EAST:
            self.direction = Direction.SOUTH_EAST
        elif self.direction == Direction.SOUTH_EAST:
            self.direction = Direction.SOUTH
        elif self.direction == Direction.SOUTH:
            self.direction = Direction.SOUTH_WEST
        elif self.direction == Direction.SOUTH_WEST:
            self.direction = Direction.WEST
        elif self.direction == Direction.WEST:
            self.direction = Direction.NORTH_WEST
        elif self.direction == Direction.NORTH_WEST:
            self.direction = Direction.NORTH

    def rotate_90_clockwise(self):
        self.rotate_45_clockwise()
        self.rotate_45_clockwise()

    def rotate_90_counter_clockwise(self):
        self.rotate_90_clockwise()
        self.rotate_90_clockwise()
        self.rotate_90_clockwise()

    def direction_to(self, other) -> Direction:
        new: Coord = other - self
        if new.row < 0 and new.col == 0:
            return Direction.NORTH
        if new.row < 0 < new.col:
            return Direction.NORTH_EAST
        if new.row < 0 and new.col < 0:
            return Direction.NORTH_WEST
        if new.row > 0 and new.col == 0:
            return Direction.SOUTH
        if new.row > 0 and new.col > 0:
            return Direction.SOUTH_EAST
        if new.row > 0 > new.col:
            return Direction.SOUTH_WEST
        if new.row == 0 and new.col > 0:
            return Direction.EAST
        if new.row == 0 and new.col < 0:
            return Direction.WEST

    def row_col(self) -> tuple[int, int]:
        return self.row, self.col

    def between(self, cmin: Coord, cmax: Coord) -> bool:
        """are you in between two coordinates"""
        return cmin.row <= self.row <= cmax.row and cmin.col <= self.col <= cmax.col

    def scale(self, scale: int) -> Coord:
        """change scale"""
        return Coord(int(self.row * scale), int(self.col * scale))

    def __sub__(self, other) -> Coord:
        return Coord(self.row - other.row, self.col - other.col, self.value)

    def __eq__(self, other) -> bool:
        return self.row == other.row and self.col == other.col

    def __add__(self, other) -> Coord:
        return Coord(self.row + other.row, self.col + other.col, self.value)

    def __lt__(self, other):
        if self.row == other.row:
            return self.col < other.col
        return self.row < other.row

    def __str__(self):
        return f"({self.row},{self.col}):{self.value}"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(str(self))
