from __future__ import annotations
from typing import Protocol, Optional, Any


# no limits on r,c numbers

class DataPoint(Protocol):
    row: int
    col: int
    value: Any


class Grid:
    """
    A self with no limits on the row number or column number.

    Only saves data that is relevant
    """

    def __init__(self):
        self._data: dict[str, DataPoint] = dict()
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
    def key(data_point: DataPoint):
        return Grid.create_key(data_point.row, data_point.col)

    @property
    def data(self) -> list[DataPoint]:
        return list(self._data.values())

    def clear(self):
        self._data.clear()
        self._row_max = 0
        self._row_min = 0
        self._col_max = 0
        self._col_min = 0

    def set_value(self, data_point: DataPoint):
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

    def get_data_point(self, r, c) -> Optional[DataPoint]:
        return self._data.get(Grid.create_key(r, c), None)

    def north(self, data_point: DataPoint) -> Optional[DataPoint]:
        return self.get_data_point(data_point.row - 1, data_point.col)

    def south(self, data_point: DataPoint) -> Optional[DataPoint]:
        return self.get_data_point(data_point.row + 1, data_point.col)

    def west(self, data_point: DataPoint) -> Optional[DataPoint]:
        return self.get_data_point(data_point.row, data_point.col - 1)

    def east(self, data_point: DataPoint) -> Optional[DataPoint]:
        return self.get_data_point(data_point.row, data_point.col + 1)

    def north_by_coords(self, row, col) -> Optional[DataPoint]:
        return self.get_data_point(row - 1, col)

    def south_by_coords(self, row, col) -> Optional[DataPoint]:
        return self.get_data_point(row + 1, col)

    def west_by_coords(self, row, col) -> Optional[DataPoint]:
        return self.get_data_point(row, col - 1)

    def east_by_coords(self, row, col) -> Optional[DataPoint]:
        return self.get_data_point(row, col + 1)

    def north_east(self, data_point: DataPoint) -> Optional[DataPoint]:
        return self.get_data_point(data_point.row - 1, data_point.col + 1)

    def north_west(self, data_point: DataPoint) -> Optional[DataPoint]:
        return self.get_data_point(data_point.row - 1, data_point.col - 1)

    def south_east(self, data_point: DataPoint) -> Optional[DataPoint]:
        return self.get_data_point(data_point.row + 1, data_point.col + 1)

    def south_west(self, data_point: DataPoint) -> Optional[DataPoint]:
        return self.get_data_point(data_point.row + 1, data_point.col - 1)

    def neighbours(self, data_point: DataPoint) -> tuple[Optional[DataPoint], ...]:
        return (self.north(data_point), self.north_east(data_point),
                self.east(data_point), self.south_east(data_point),
                self.south(data_point), self.south_west(data_point),
                self.west(data_point), self.north_west(data_point))

    def ordinal_neighbours(self, data_point: DataPoint) -> tuple[Optional[DataPoint], ...]:
        return (self.north(data_point),
                self.east(data_point),
                self.south(data_point),
                self.west(data_point),)

    def get_row_values(self, row) -> tuple[DataPoint, ...]:
        return tuple(self.get_data_point(row, col)
                     for col in range(self.min_col(), self.max_col() + 1))

    def get_valid_dps_from_row(self, row: int) -> list[DataPoint]:
        l = [self._data[k] for k in self._data if Grid.row_from_key(k) == row]
        l.sort(key=lambda x: x.col)
        return l

    def get_rows(self) -> list[int]:
        return [Grid.row_from_key(key) for key in self._data]

    def min_row(self) -> int:
        return self._row_min

    def max_row(self) -> int:
        return self._row_max

    def num_rows(self) -> int:
        return self.max_row() - self.min_row() + 1

    def get_col_values(self, col) -> tuple[DataPoint, ...]:
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

    def copy(self)->Grid:
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
