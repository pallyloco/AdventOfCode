from __future__ import annotations
from typing import Protocol, TypeVar, Generic


class Comparable(Protocol):
    """What we need for 'costing' ASTAR compatible objects"""

    def __lt__(self: T, other: T) -> bool: pass

    def __add__(self: T, other: T) -> T: pass

    def __sub__(self: T, other: T) -> T: pass

    def __gt__(self: T, other: T) -> T: pass


T = TypeVar("T", bound=Comparable)


class MyRange(Generic[T]):
    def __init__(self, low: T, high: T):
        self.low: T = low
        self.high: T = high

    def __len__(self):
        return max(0, self.high - self.low + 1)

    def len(self) -> int:
        return len(self)

    def set_to_zero(self):
        self.low = 1
        self.high = +1

    def set_low(self, low: T) -> bool:
        if self.low > self.high:
            return False
        self.low = max(self.low, low)
        return True

    def set_high(self, high: T) -> bool:
        if self.high < self.low:
            return False
        self.high = min(self.high, high)
        return True

    def __str__(self):
        return f"({self.low},{self.high})"

    def __repr__(self):
        return str(self)
