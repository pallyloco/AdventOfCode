from __future__ import annotations

from typing import Any


class Coord:
    def __init__(self, row, col, value: Any = None):
        self.row: int = row
        self.col: int = col
        self.value = value

    def __hash__(self):
        return hash(str(self))

    def direction_to(self, other):
        new: Coord = other - self
        return new.dir()

    def dir(self):
        nr = 0
        if self.row < 0:
            nr = -1
        elif self.row > 0:
            nr = 1
        nc = 0
        if self.col < 0:
            nc = -1
        elif self.col > 0:
            nc = 1
        return Coord(nr, nc)

    def row_col(self) -> tuple[int, int]:
        return self.row, self.col

    def between(self, cmin: Coord, cmax: Coord) -> bool:
        return cmin.row <= self.row <= cmax.row and cmin.col <= self.col <= cmax.col

    def scale(self, scale: int) -> Coord:
        return Coord(int(self.row * scale), int(self.col * scale))

    def __sub__(self, other) -> Coord:
        return Coord(self.row - other.row, self.col - other.col, self.value)

    def __eq__(self, other) -> bool:
        return self.row == other.row and self.col == other.col

    def __add__(self, other) -> Coord:
        return Coord(self.row + other.row, self.col + other.col, self.value)

    def __str__(self):
        return f"({self.row},{self.col}):{self.value}"

    def __repr__(self):
        return str(self)
