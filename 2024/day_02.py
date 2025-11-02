from typing import Iterable

"""
The  data consists of many reports, one report per line. Each report is a 
list of numbers called levels that are separated by spaces.
"""
input_data = [
    [7, 6, 4, 2, 1],
    [1, 2, 7, 8, 9],
    [9, 7, 6, 2, 1],
    [1, 3, 2, 4, 5],
    [8, 6, 4, 4, 1],
    [1, 3, 6, 7, 9],
]

fh = open("day_02.txt", "r")
input_data = [(list(map(int, line.split()))) for line in fh]



def main(data):
    bad = []
    total = 0
    for d in data:
        if is_good(d):
            total = total + 1
        else:
            bad.append(d)

    print(total)

    # part 2 , really inefficient
    """
    Now, the same rules apply as before, except if removing a single level from an unsafe report 
    would make it safe, the report instead counts as safe.
    """
    for d in bad:
        for i in range(len(d)):
            t = d[:i] + d[i + 1:]
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
    main(input_data)
