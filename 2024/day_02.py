"""
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""
from typing import Iterable

datas = [
    [7, 6, 4, 2, 1],
    [1, 2, 7, 8, 9],
    [9, 7, 6, 2, 1],
    [1, 3, 2, 4, 5],
    [8, 6, 4, 4, 1],
    [1, 3, 6, 7, 9],
]


def main(test_flag=True):
    bad = []
    if test_flag:
        ds = datas
    else:
        fh = open("day_02.txt", "r")
        ds:list[list[int]] = [ (list(map(int,line.split())))  for line in fh]
    total = 0
    for d in ds:
        if is_good(d):
            total = total + 1
        else:
            bad.append(d)

    print(total)

    # part 2 , really inefficient
    for d in bad:
        for i in range(len(d)):
            t = d[:i] + d[i+1:]
            if is_good(t):
                total = total + 1
                break
    print(total)


def is_good(data: Iterable) -> bool:
    """
    The levels are either all increasing or all decreasing.
    Any two adjacent levels differ by at least one and at most three.
    """
    up = all((a > b for a, b in zip(data[:-1], data[1:])))
    down = all((a < b for a, b in zip(data[:-1], data[1:])))
    differ = all((1 <= abs(a - b) <= 3) for a, b in zip(data[:-1], data[1:]))
    return (up or down) and differ


if __name__ == "__main__":
    main(False)
