from __future__ import annotations
from typing import Any, Optional, Iterable
import itertools as it
from collections import UserList


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


class Ranges(UserList):

    def find_empty_ranges(self) -> Iterable:
        self.data.sort()
        for one, two in it.pairwise(self.data):
            if one.end + 1 < two.start:
                yield Range(one.end + 1, two.start - one.end - 1)

    def order_by_size(self, do_reversed=False):
        self.data.sort(key=lambda x: x.size, reverse=do_reversed)
        return self

    def order_by_location(self, do_reversed=False):
        self.data.sort(key=lambda x: x.start, reverse=do_reversed)
        return self

    def find_with_value(self, value) -> Iterable:
        return (r for r in self.data if r.value == value)
