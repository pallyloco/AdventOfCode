from __future__ import annotations
from enum import Enum

from typing import Any, Optional, Self


class Direction(Enum):
    """tuple representing direction"""
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    EAST = (0, 1)
    WEST = (0, -1)
    NORTH_WEST = (-1, -1)
    NORTH_EAST = (-1, 1)
    SOUTH_WEST = (1, -1)
    SOUTH_EAST = (1, 1)
    NONE = (0, 0)

    def left(self) -> Direction:
        if self == Direction.NORTH:
            return Direction.WEST
        if self == Direction.SOUTH:
            return Direction.EAST
        if self == Direction.WEST:
            return Direction.SOUTH
        if self == Direction.EAST:
            return Direction.NORTH
        return Direction.NORTH

    def opposite(self)-> Direction:
        if self == Direction.NORTH:
            return Direction.SOUTH
        if self == Direction.SOUTH:
            return Direction.NORTH
        if self == Direction.WEST:
            return Direction.EAST
        if self == Direction.EAST:
            return Direction.WEST
        return Direction.NORTH

    def __str__(self):
        return str(self.name)


class Coord:
    """a 2d point with value and direction (row, col, value, direction)"""
    def __init__(self, row, col, value: Any = None, *, direction: Direction=Direction.NORTH):
        self.row: int = row
        self.col: int = col
        self.value = value
        self.direction = direction

    def copy(self):
        return type(self)(self.row, self.col, self.value, direction=self.direction)

    def move(self, amount: int=1, direction: Optional[Direction] = None):
        """Move the coordinate by amount in direction.  If direction is None, move in coordinates direction"""
        if direction is None:
            direction = self.direction
        for _ in range(amount):
            self.row = self.row + direction.value[0]
            self.col = self.col + direction.value[1]

    def manhatten_distance(self,other):
        return abs(self.row - other.row) + abs(self.col - other.col)

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
        """changed the direction by rotating 90 degrees clockwise"""
        self.rotate_45_clockwise()
        self.rotate_45_clockwise()

    def rotate_90_counter_clockwise(self):
        """changed the direction by rotating 90 degrees counter clockwise"""
        self.rotate_90_clockwise()
        self.rotate_90_clockwise()
        self.rotate_90_clockwise()

    def reverse_direction(self):
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



    def ordinal_neighbours(self) -> tuple[Self, Self, Self, Self]:
        n1 = self.copy()
        n2 = self.copy()
        n3 = self.copy()
        n4 = self.copy()
        n1.move(1)
        n2.rotate_90_clockwise()
        n2.move(1)
        n3.reverse_direction()
        n3.move()
        n4.rotate_90_counter_clockwise()
        n4.move()
        return n1, n2, n3, n4

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
        s = f"({self.row},{self.col}):{self.value}"
        if self.direction == Direction.NORTH:
            s += " ^ "
        elif self.direction == Direction.SOUTH:
            s += " v "
        elif self.direction == Direction.WEST:
            s += " < "
        elif self.direction == Direction.EAST:
            s += " > "
        return s

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(str(self))
