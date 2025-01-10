from __future__ import annotations
from typing import Optional
from coord import Coord, Direction


class Grid:
    """
    A self with no limits on the row number or column number.

    Only saves data that is relevant
    """

    def __init__(self):
        self._data: dict[str, Coord] = dict()
        self._row_max = None
        self._row_min = None
        self._col_max = None
        self._col_min = None
        self.null_char = "."

    @staticmethod
    def create_key(r: int, c: int) -> str:
        return f"{r},{c}"

    @staticmethod
    def row_from_key(key: str) -> int:
        row, _ = key.split(",")
        return int(row)

    @staticmethod
    def col_from_key(key: str) -> int:
        _, col = key.split(",")
        return int(col)

    @staticmethod
    def key(data_point: Coord):
        return Grid.create_key(data_point.row, data_point.col)

    @property
    def data(self) -> list[Coord]:
        return list(self._data.values())

    @property
    def area(self) -> int:
        return len(self._data.values())

    def number_of_sides(self) -> int:
        """number of sides this region has (vertical/horizontal) inside and outside"""
        edge_cells = set()
        sides = 0
        for datum in self.data:
            walkers = self.on_edge(datum)
            for walker in walkers:
                if str(walker) not in edge_cells:
                    sides += self._walk_edges(walker, edge_cells)

        return sides

    def on_edge(self, cell: Coord):
        """List coordinates, with direction, where coordinate has an empty cell to its left"""
        walkers = []
        cell.direction = Direction.EAST
        for i in range(4):
            if self.get_left_cell(cell) is None:
                walkers.append(Coord(cell.row, cell.col, direction=cell.direction))
            cell.rotate_90_clockwise()
        return walkers

    def _walk_edges(self, walker: Coord, edge_cells: set) -> int:
        """given a particular coordinate with direction, walk around the edge,
        calculating how many sides it has (horizontal/vertical)"""

        sides = 0
        been_there = set()

        # walk to the first turn
        while self.get_left_cell(walker) is None and self.get_forward_cell(walker) is not None:
            walker.move(1)
        if self.get_left_cell(walker) is not None:
            walker.rotate_90_counter_clockwise()
            walker.move(1)
        else:
            walker.rotate_90_clockwise()

        # Go around the edges
        while str(walker) not in been_there:
            been_there.add(str(walker))
            edge_cells.add(str(walker))
            while self.get_left_cell(walker) is None and self.get_forward_cell(walker) is not None:
                walker.move(1)
                edge_cells.add(str(walker))
            sides += 1
            if self.get_left_cell(walker) is not None:
                walker.rotate_90_counter_clockwise()
                walker.move(1)
                edge_cells.add(str(walker))
            else:
                walker.rotate_90_clockwise()
                edge_cells.add(str(walker))
        return sides

    def get_left_cell(self, walker: Coord) -> Optional[Coord]:
        row = walker.row + walker.direction.left().value[0]
        col = walker.col + walker.direction.left().value[1]
        return self.get_data_point(row, col)

    def get_forward_cell(self, walker: Coord) -> Optional[Coord]:
        row = walker.row + walker.direction.value[0]
        col = walker.col + walker.direction.value[1]
        return self.get_data_point(row, col)

    def clear(self):
        self._data.clear()
        self._row_max = 0
        self._row_min = 0
        self._col_max = 0
        self._col_min = 0

    def set_value(self, data_point: Coord):
        self._data[Grid.key(data_point)] = data_point
        if self._col_min is None:
            self._col_min = data_point.col
        else:
            self._col_min = min(self._col_min, data_point.col)
        if self._col_max is None:
            self._col_max = data_point.col
        else:
            self._col_max = max(self._col_max, data_point.col)

        if self._row_min is None:
            self._row_min = data_point.row
        else:
            self._row_min = min(self._row_min, data_point.row)
        if self._row_max is None:
            self._row_max = data_point.row
        else:
            self._row_max = max(self._row_max, data_point.row)

    def remove_data_point(self, r, c):
        self._data.pop(Grid.create_key(r, c), None)

    def get_data_point(self, r, c) -> Optional[Coord]:
        return self._data.get(Grid.create_key(r, c), None)

    def north(self, data_point: Coord) -> Optional[Coord]:
        return self.get_data_point(data_point.row - 1, data_point.col)

    def south(self, data_point: Coord) -> Optional[Coord]:
        return self.get_data_point(data_point.row + 1, data_point.col)

    def west(self, data_point: Coord) -> Optional[Coord]:
        return self.get_data_point(data_point.row, data_point.col - 1)

    def east(self, data_point: Coord) -> Optional[Coord]:
        return self.get_data_point(data_point.row, data_point.col + 1)

    def north_by_coords(self, row, col) -> Optional[Coord]:
        return self.get_data_point(row - 1, col)

    def south_by_coords(self, row, col) -> Optional[Coord]:
        return self.get_data_point(row + 1, col)

    def west_by_coords(self, row, col) -> Optional[Coord]:
        return self.get_data_point(row, col - 1)

    def east_by_coords(self, row, col) -> Optional[Coord]:
        return self.get_data_point(row, col + 1)

    def north_east(self, data_point: Coord) -> Optional[Coord]:
        return self.get_data_point(data_point.row - 1, data_point.col + 1)

    def north_west(self, data_point: Coord) -> Optional[Coord]:
        return self.get_data_point(data_point.row - 1, data_point.col - 1)

    def south_east(self, data_point: Coord) -> Optional[Coord]:
        return self.get_data_point(data_point.row + 1, data_point.col + 1)

    def south_west(self, data_point: Coord) -> Optional[Coord]:
        return self.get_data_point(data_point.row + 1, data_point.col - 1)

    def neighbours(self, data_point: Coord) -> tuple[Optional[Coord], ...]:
        return (self.north(data_point), self.north_east(data_point),
                self.east(data_point), self.south_east(data_point),
                self.south(data_point), self.south_west(data_point),
                self.west(data_point), self.north_west(data_point))

    def ordinal_neighbours(self, data_point: Coord) -> tuple[Optional[Coord], ...]:
        return (self.north(data_point),
                self.east(data_point),
                self.south(data_point),
                self.west(data_point),)

    def get_row_values(self, row) -> tuple[Coord, ...]:
        return tuple(self.get_data_point(row, col)
                     for col in range(self.min_col(), self.max_col() + 1))

    def get_valid_dps_from_row(self, row: int) -> list[Coord]:
        data_points = [self._data[k] for k in self._data if Grid.row_from_key(k) == row]
        data_points.sort(key=lambda x: x.col)
        return data_points

    def get_rows(self) -> list[int]:
        return [Grid.row_from_key(key) for key in self._data]

    def min_row(self) -> int:
        return self._row_min

    def max_row(self) -> int:
        return self._row_max

    def set_max_row(self, num:int):
        self._row_max = num

    def set_min_row(self, num:int):
        self._row_min = num

    def set_max_col(self, num:int):
        self._col_max = num

    def set_min_col(self, num:int):
        self._col_min = num

    def set_boundaries(self,row_min, row_max, col_min, col_max):
        self.set_max_row(row_max)
        self.set_min_row(row_min)
        self.set_max_col(col_max)
        self.set_min_col(col_min)


    def num_rows(self) -> int:
        return self.max_row() - self.min_row() + 1

    def get_col_values(self, col) -> tuple[Coord, ...]:
        return tuple(self.get_data_point(row, col)
                     for row in range(self.min_row(), self.max_row() + 1))

    def get_cols(self) -> tuple[int, ...]:
        return tuple(Grid.col_from_key(key) for key in self._data)

    def min_col(self) -> int:
        return self._col_min

    def max_col(self) -> int:
        return self._col_max

    def num_cols(self) -> int:
        return self.max_col() - self.min_col() + 1

    def copy(self) -> Grid:
        other = Grid()
        for dp in self._data.values():
            other.set_value(dp)
        return other

    def __str__(self):
        result = ""
        for r in range(self.min_row(), self.max_row() + 1):
            for c in range(self.min_col(), self.max_col() + 1):
                dp = self.get_data_point(r, c)
                if dp is None:
                    result += self.null_char
                else:
                    result += str(dp.value)[0]
            result += "\n"
        return result

    def __repr__(self):
        return f"({self.min_row()}, {self.min_col()}) ({self.max_row()}, {self.max_col()})"
