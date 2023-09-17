from __future__ import annotations

from typing import Optional
from itertools import zip_longest


def main():
    score: int = 0
    file = open("day13_input.txt", 'r')
    for pair_num, packets in enumerate(read_n_lines_at_a_time(file, 3)):
        if is_in_order(eval(packets[0]), eval(packets[1])):
            print(pair_num)
            score += pair_num + 1
    print(f"score: {score}")


def read_n_lines_at_a_time(file, n) -> list[str]:
    lines: list[str] = list()
    for counter, line in enumerate(map(str.rstrip, file)):
        lines.append(line)
        if (counter + 1) % n == 0:
            yield lines
            lines.clear()
    return lines


def is_in_order(pair1: list[list | int], pair2: list[list | int], depth=0) -> Optional[bool]:

    for p1, p2 in zip_longest(pair1, pair2):

        # If the left list runs out of items first, the inputs are in the right order.
        # If the right list runs out of items first, the inputs are not in the right order.
        if p1 is None:
            return True
        if p2 is None:
            return False

        # If both values are integers, the lower integer should come first.
        # If the left integer is lower than the right integer, the inputs are in the right order. 
        # If the left integer is higher than the right integer, the inputs are not in the right order. 
        # Otherwise, if the inputs are the same integer; continue checking the next part of the input.
        if isinstance(p1, int) and isinstance(p2, int):
            if p1 == p2:
                continue
            return p1 < p2

        # If both values are lists, compare the first value of each list, then the second value, and so on. 
        # If the lists are the same length and no comparison makes a decision about the order,
        # continue checking the next part of the input.
        elif isinstance(p1, list) and isinstance(p2, list):
            result = is_in_order(p1, p2, depth+1)
            if result is not None:
                return result

        # If exactly one value is an integer, convert the integer to a list which contains that integer 
        # as its only value, then retry the comparison. 
        # For example, if comparing [0,0,0] and 2, convert the right value to [2] (a list containing 2); 
        # the result is then found by instead comparing [0,0,0] and [2].
        elif isinstance(p1, int):
            result = is_in_order([p1], p2, depth+1)
            if result is not None:
                return result
        elif isinstance(p2, int):
            result = is_in_order(p1, [p2], depth+1)
            if result is not None:
                return result

    # if we got this far, then the two sides are equal, which is true, only if
    # we are at the beginning of this recursion
    if depth == 0:
        return True
    return None


# ===================================================================
# Entry point
# ===================================================================
if __name__ == '__main__':
    main()
