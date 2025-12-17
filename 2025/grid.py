from __future__ import annotations
from typing import Optional, Any, Iterator, Generator, Callable
from coord import DataInCell, Direction
import tkinter as tk
tk_size = 15

KEY=str

class Grid:
    """
    A self with no limits on the row number or column number.

    Only saves data that is relevant
    """

    def __init__(self, data=None, null_char=".", convert_value: Callable[[str], Any] = lambda x: x):
        self._data: dict[str, DataInCell] = dict()
        self.null_char = null_char
        if data is not None:
            self.read_data(data, convert_value)

    # -----------------------------------------------------------------------------------------------------------------
    # static methods
    # -----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def create_key(r: int, c: int) -> KEY:
        return f"{r},{c}"

    @staticmethod
    def row_from_key(key: KEY) -> int:
        row, _ = key.split(",")
        return int(row)

    @staticmethod
    def col_from_key(key: KEY) -> int:
        _, col = key.split(",")
        return int(col)

    @staticmethod
    def key(data_point: DataInCell):
        return Grid.create_key(data_point.row, data_point.col)

    # -----------------------------------------------------------------------------------------------------------------
    # properties
    # -----------------------------------------------------------------------------------------------------------------
    @property
    def data(self) -> list[DataInCell]:
        return list(self._data.values())

    @property
    def area(self) -> int:
        return len(self._data.values())

    @property
    def row_range(self) -> range:
        return range(self.min_row, self.max_row + 1)

    @property
    def col_range(self) -> range:
        return range(self.min_col, self.max_col + 1)

    @property
    def _rows(self) -> set:
        return set(Grid.row_from_key(key) for key in self._data)

    @property
    def min_row(self) -> int:
        return min(self._rows)

    @property
    def max_row(self) -> int:
        return max(self._rows)

    @property
    def num_rows(self) -> int:
        return self.max_row - self.min_row + 1

    @property
    def _cols(self) -> set:
        return set(Grid.col_from_key(key) for key in self._data)

    @property
    def min_col(self) -> int:
        return min(self._cols)

    @property
    def max_col(self) -> int:
        return max(self._cols)

    @property
    def num_cols(self) -> int:
        return self.max_col - self.min_col + 1


    # -----------------------------------------------------------------------------------------------------------------
    # read data
    # -----------------------------------------------------------------------------------------------------------------
    def read_data(self, data: tuple[str, ...], convert_value: Callable[[str], Any] = lambda x: x):
        """read map from a tuple of strings"""
        for row, line in enumerate(data):
            for col, char in enumerate(line):
                if char != self.null_char:
                    self.set_value(DataInCell(row, col, convert_value(char)))

    def copy(self) -> Grid:
        other = Grid()
        for dp in self._data.values():
            other.set_value(dp)
        return other

    # -----------------------------------------------------------------------------------------------------------------
    # adding and removing data
    # -----------------------------------------------------------------------------------------------------------------
    def clear(self):
        self._data.clear()

    def set_value(self, data_point: DataInCell):
        self._data[Grid.key(data_point)] = data_point

    def remove_data_point(self, r, c):
        self._data.pop(Grid.create_key(r, c), None)

    # -----------------------------------------------------------------------------------------------------------------
    # informational
    # -----------------------------------------------------------------------------------------------------------------
    def get_data_point(self, r, c) -> Optional[DataInCell]:
        """gets data from row, column, returns None if no data is stored"""
        return self._data.get(Grid.create_key(r, c), None)

    def get_coordinates_with_value(self,value:Any) -> Generator[DataInCell, Any, None]:
        """return all coordinate objects that have the specified value"""
        return (coord for coord in self.data if coord.value == value)

    def is_inside_grid_limits(self, coord:DataInCell) -> bool:
        """is the coordinate contained within the grid"""
        return self.min_row <= coord.row <= self.max_row and self.min_col <= coord.col <= self.max_col

    def get_row_values(self, row) -> tuple[DataInCell, ...]:
        return tuple(self.get_data_point(row, col)
                     for col in range(self.min_col, self.max_col + 1))

    def get_col_values(self, col) -> tuple[DataInCell, ...]:
        return tuple(self.get_data_point(row, col)
                     for row in range(self.min_row, self.max_row + 1))


    # -----------------------------------------------------------------------------------------------------------------
    # neighbours
    # -----------------------------------------------------------------------------------------------------------------
    def get_left_cell(self, walker: DataInCell) -> Optional[DataInCell]:
        row = walker.row + walker.direction.left().value[0]
        col = walker.col + walker.direction.left().value[1]
        return self.get_data_point(row, col)

    def get_forward_cell(self, walker: DataInCell) -> Optional[DataInCell]:
        row = walker.row + walker.direction.value[0]
        col = walker.col + walker.direction.value[1]
        return self.get_data_point(row, col)

    def north(self, data_point: DataInCell) -> Optional[DataInCell]:
        return self.get_data_point(data_point.row - 1, data_point.col)

    def south(self, data_point: DataInCell) -> Optional[DataInCell]:
        return self.get_data_point(data_point.row + 1, data_point.col)

    def west(self, data_point: DataInCell) -> Optional[DataInCell]:
        return self.get_data_point(data_point.row, data_point.col - 1)

    def east(self, data_point: DataInCell) -> Optional[DataInCell]:
        return self.get_data_point(data_point.row, data_point.col + 1)

    def north_by_coords(self, row, col) -> Optional[DataInCell]:
        return self.get_data_point(row - 1, col)

    def south_by_coords(self, row, col) -> Optional[DataInCell]:
        return self.get_data_point(row + 1, col)

    def west_by_coords(self, row, col) -> Optional[DataInCell]:
        return self.get_data_point(row, col - 1)

    def east_by_coords(self, row, col) -> Optional[DataInCell]:
        return self.get_data_point(row, col + 1)

    def north_east(self, data_point: DataInCell) -> Optional[DataInCell]:
        return self.get_data_point(data_point.row - 1, data_point.col + 1)

    def north_west(self, data_point: DataInCell) -> Optional[DataInCell]:
        return self.get_data_point(data_point.row - 1, data_point.col - 1)

    def south_east(self, data_point: DataInCell) -> Optional[DataInCell]:
        return self.get_data_point(data_point.row + 1, data_point.col + 1)

    def south_west(self, data_point: DataInCell) -> Optional[DataInCell]:
        return self.get_data_point(data_point.row + 1, data_point.col - 1)

    def neighbours(self, data_point: DataInCell) -> tuple[Optional[DataInCell], ...]:
        return (self.north(data_point), self.north_east(data_point),
                self.east(data_point), self.south_east(data_point),
                self.south(data_point), self.south_west(data_point),
                self.west(data_point), self.north_west(data_point))

    def ordinal_neighbours(self, data_point: DataInCell) -> tuple[Optional[DataInCell], ...]:
        return (self.north(data_point),
                self.east(data_point),
                self.south(data_point),
                self.west(data_point),)

    # -----------------------------------------------------------------------------------------------------------------
    # edges
    # -----------------------------------------------------------------------------------------------------------------
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

    def on_edge(self, cell: DataInCell):
        """List coordinates, with direction, where coordinate has an empty cell to its left"""
        walkers = []
        cell.direction = Direction.EAST
        for i in range(4):
            if self.get_left_cell(cell) is None:
                walkers.append(DataInCell(cell.row, cell.col, direction=cell.direction))
            cell.rotate_90_clockwise()
        return walkers

    def _walk_edges(self, walker: DataInCell, edge_cells: set) -> int:
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

        # Go around the springs
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

    # -----------------------------------------------------------------------------------------------------------------
    # iterators
    # -----------------------------------------------------------------------------------------------------------------
    def _generator(self):
        for row in self.row_range:
            for col in self.col_range:
                cell_data = self.get_data_point(row,col)
                if cell_data is not None:
                    yield cell_data

    def __iter__(self):
        return self._generator()

    # -----------------------------------------------------------------------------------------------------------------
    # built-ins
    # -----------------------------------------------------------------------------------------------------------------
    def __str__(self):
        result = ""
        for r in range(self.min_row, self.max_row + 1):
            for c in range(self.min_col, self.max_col + 1):
                dp = self.get_data_point(r, c)
                if dp is None:
                    result += self.null_char
                else:
                    result += str(dp.value)[0]
            result += "\n"
        return result

    def __repr__(self):
        return f"({self.min_row}, {self.min_col}) ({self.max_row}, {self.max_col})"



class TkGrid(Grid):
    def __init__(self, row_min, row_max, col_min, col_max, data=None, null_char=".", convert_value: Callable[[str], Any] = lambda x: x):
        self.mw = tk.Tk()
        self.canvas = tk.Canvas(self.mw, height=(row_max-row_min+1)*tk_size, width=(col_max-col_min+1)*tk_size)
        self.ymin = row_min
        self.xmin = col_min
        super().__init__(data, null_char, convert_value)
        self._canvas_objs: dict[str,int] = {}
        self.canvas.pack()


    def set_value(self, data_point: DataInCell):
        super().set_value(data_point)
        tag = self._canvas_objs.get(Grid.key(data_point), None)
        if tag is not None:
            self.canvas.delete(tag)
        self._canvas_objs [Grid.key(data_point)] = self.canvas.create_text((self.xmin + data_point.col + 1) * tk_size,
                                                                           (self.ymin+data_point.row+1) * tk_size,
                                                                           text=data_point.value, anchor='nw')
        self.mw.update()

    def clear(self):
        super().clear()
        for tag in self._canvas_objs:
            self.canvas.delete(tag)
        self._canvas_objs.clear()
        self.mw.update()

    def remove_data_point(self, r, c):
        super().remove_data_point(r,c)
        tag = self._canvas_objs.pop(Grid.create_key(r, c), None)
        self.canvas.delete(tag)
        self.mw.update()







