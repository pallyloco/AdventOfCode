from __future__ import annotations
from typing import Any, Optional, Iterable
import itertools as it
from collections import UserList


class Range:
    """similar to range, but with added methods, but step must always be 1"""
    def __init__(self, start: int, stop: int):
        self.start = start
        self.stop = stop
        self.range = range(start,stop)

    def __contains__(self, item):
        return item in self.range

    def __len__(self):
        return len(self.range)

    def __lt__(self, other: Range):
        return self.start < other.start

    def __eq__(self, other: Range):
        return self.start == other.start and self.stop == other.stop

    def overlap(self, other) -> bool:
        return self.start in other or other.start in self

    def merge(self, other) -> tuple[Range, Optional[Range]]:
        one, two = sorted((self, other))
        if self.overlap(other) or one.end == two.start:
            return Range(one.start, two.end), None
        else:
            return self, other

    def __str__(self):
        return str(f"({self.start},{self.stop})")

    def __repr__(self):
        return str(self)


def find_empty_ranges(data: list[Range]) -> Iterable:
    data.sort()
    for one, two in it.pairwise(data):
        if one.stop < two.start:
            yield Range(one.stop, two.start+1)

def merged_ranges(data: list[Range] | tuple[Range]):
    if len(data) > 0:
        start = data[0].start
        for one, two in it.pairwise(data):
            if one.stop < two.start:
                yield Range(start, one.stop)
                start = two.start


