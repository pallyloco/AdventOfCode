from __future__ import annotations

from typing import Any


class Coord:
    def __init__(self, row, col, value:Any = None):
        self.row: int = row
        self.col: int = col
        self.value = value

    def between(self, cmin: Coord, cmax: Coord) -> bool:
        return cmin.row <= self.row <= cmax.row and cmin.col <= self.col <= cmax.col

    def scale(self, scale: int) -> Coord:
        return Coord(self.row * scale, self.col * scale)

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
