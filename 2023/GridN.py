from __future__ import annotations
from itertools import product
from typing import Protocol, Optional, Any, Generator


# no limits on index numbers
# dimension of self depends on the number of coords in DataPoints

class DataPoint(Protocol):
    coords: list[int]
    value: Any


class GridN:
    """
    A self with no limits on the indices.

    Only saves data that is relevant
    """

    def __init__(self):
        self._data: dict[str, DataPoint] = dict()

    @staticmethod
    def create_key(coords: list[int]) -> str:
        return ",".join(map(str,coords))

    @staticmethod
    def coords_from_key(key: str) -> list[int]:
        return [int(i) for i in key.split(",")]

    @staticmethod
    def key(data_point: DataPoint):
        return GridN.create_key(data_point.coords)

    @property
    def data(self) -> list[DataPoint]:
        return list(self._data.values())

    def set_value(self, data_point: DataPoint):
        self._data[GridN.key(data_point)] = data_point

    def get_data_point(self, *coords) -> Optional[DataPoint]:
        return self._data.get(GridN.create_key(list(coords)), None)

    def neighbours(self, data_point: DataPoint) -> tuple[Optional[DataPoint], ...]:
        dim = len(data_point.coords)
        n: list[DataPoint] = list()
        offset_bases = ((-1, 0, 1),) * dim
        for offset in product(*offset_bases):
            if all(x == 0 for x in offset):
                continue
            new_coord = [og + off for og, off in zip(data_point.coords, offset)]
            point: Optional[DataPoint] = self.get_data_point(*new_coord)
            if point is not None:
                n.append(point)
        return tuple(n)

    def ordinal_neighbours_gen(self, data_point: DataPoint) -> Generator[Optional[DataPoint], None, None]:
        dim = len(data_point.coords)
        for index, offset in product(range(dim), (-1, 1)):
            new_coord = list(data_point.coords)
            new_coord[index] += offset
            yield self.get_data_point(*new_coord)

    def ordinal_neighbours(self, data_point: DataPoint) -> tuple[Optional[DataPoint], ...]:
        return tuple(self.ordinal_neighbours_gen(data_point))


