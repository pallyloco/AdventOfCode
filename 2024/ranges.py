from __future__ import annotations
from typing import Any, Optional
import itertools as it


class Range:
    def __init__(self, start: int, size: int, value: Any = None):
        self.start = start
        self.size = size
        self.value = value

    def __lt__(self, other):
        return self.start < other.start

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    @property
    def end(self):
        return self.start + self.size - 1

    def overlap(self, other) -> bool:
        return self.start <= other.start <= self.end or self.start <= other.end <= self.end

    def merge(self, other) -> tuple[Range, Optional[Range]]:
        one, two = sorted((self, other))
        if self.overlap(other) or one.end + 1 == two.start:
            return Range(one.start, two.end, self.value), None
        else:
            return self, other

    def __str__(self):
        return str(f"{self.value}:({self.start},{self.end})")

    def __repr__(self):
        return str(self)


class Ranges:


    def __init__(self):
        self._ranges: list[Range] = []
        for v in dir(self._ranges):
            if v[0] != "_":
                x = getattr(self._ranges, v)
                setattr(self, v, x)


    def find_empty_ranges(self) -> Ranges:
        self._ranges.sort()
        empties = Ranges()
        for one, two in it.pairwise(self._ranges):
            if one.end + 1 < two.start:
                empties.append(Range(one.end + 1, two.start - one.end - 1))
        return empties

    def order_by_size(self, do_reversed=False):
        self._ranges.sort(key=lambda x: x.size, reverse=do_reversed)
        return self

    def order_by_location(self, do_reversed=False):
        self._ranges.sort(key=lambda x: x.start, reverse=do_reversed)
        return self

    def find_with_value(self,value):
        return [r for r in self._ranges if r.value == value]

    def __len__(self):
        return len(self._ranges)

    def __iter__(self):
        return iter(self._ranges)

    def __str__(self):
        return str(f"{self._ranges})")

    def __repr__(self):
        return str(self)

if __name__ == "__main__":
    r = Ranges()