from __future__ import annotations

from typing import Optional
from itertools import zip_longest


def main():
    score: int = 0
    file = open("day13_input.txt", 'r')
    for pair_num, packets in enumerate(read_n_lines_at_a_time(file, 3)):
        if is_in_order(eval(packets[0]), eval(packets[1])) < 1:
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


def is_in_order(pair1: list[list | int], pair2: list[list | int], depth=0) -> int:
    result = 0
    for p1, p2 in zip_longest(pair1, pair2):

        # If the left list runs out of items first, the inputs are in the right order.
        # If the right list runs out of items first, the inputs are not in the right order.
        if p1 is None:
            return -1
        if p2 is None:
            return 1

        # If both values are integers, the lower integer should come first.
        # If the left integer is lower than the right integer, the inputs are in the right order. 
        # If the left integer is higher than the right integer, the inputs are not in the right order. 
        # Otherwise, if the inputs are the same integer; continue checking the next part of the input.
        if isinstance(p1, int) and isinstance(p2, int):
            if p1 == p2:
                continue
            return p1 - p2

        # If both values are lists, compare the first value of each list, then the second value, and so on. 
        # If the lists are the same length and no comparison makes a decision about the order,
        # continue checking the next part of the input.
        elif isinstance(p1, list) and isinstance(p2, list):
            result = is_in_order(p1, p2, depth+1)
            if result:
                return result

        # If exactly one value is an integer, convert the integer to a list which contains that integer 
        # as its only value, then retry the comparison. 
        # For example, if comparing [0,0,0] and 2, convert the right value to [2] (a list containing 2); 
        # the result is then found by instead comparing [0,0,0] and [2].
        elif isinstance(p1, int):
            result = is_in_order([p1], p2, depth+1)
            if result:
                return result
        elif isinstance(p2, int):
            result = is_in_order(p1, [p2],depth+1)
            if result:
                return result

    # if we got this far, then the two sides are equal, which is true, only if
    # we are at the beginning of this recursion
    return result


# ===================================================================
# Entry point
# ===================================================================
if __name__ == '__main__':
    main()

"""
--- Day 13: Distress Signal ---

You'll need to re-order the list of received packets (your puzzle input) to decode the message.

Your list consists of pairs of packets; pairs are separated by a blank line. 
You need to identify how many pairs of packets are in the right order.

Packet data consists of lists and integers. Each list starts with [, ends with ], and contains 
zero or more comma-separated values (either integers or other lists).
 Each packet is always a list and appears on its own line.

When comparing two values, the first value is called left and the second value is called right. Then:

If both values are integers, the lower integer should come first. If the left integer is lower than the right integer, the inputs are in the right order. If the left integer is higher than the right integer, the inputs are not in the right order. Otherwise, the inputs are the same integer; continue checking the next part of the input.
If both values are lists, compare the first value of each list, then the second value, and so on. If the left list runs out of items first, the inputs are in the right order. If the right list runs out of items first, the inputs are not in the right order. If the lists are the same length and no comparison makes a decision about the order, continue checking the next part of the input.
If exactly one value is an integer, convert the integer to a list which contains that integer as its only value, then retry the comparison. For example, if comparing [0,0,0] and 2, convert the right value to [2] (a list containing 2); the result is then found by instead comparing [0,0,0] and [2].
Using these rules, you can determine which of the pairs in the example are in the right order:

What are the indices of the pairs that are already in the right order? 
(The first pair has index 1, the second pair has index 2, and so on.) 

Determine which pairs of packets are already in the right order. What is the sum of the indices of those pairs?

Your puzzle answer was 6395.

--- Part Two ---
Now, you just need to put all of the packets in the right order. 
Disregard the blank lines in your list of received packets.

The distress signal protocol also requires that you include two additional divider packets:

[[2]]
[[6]]
Using the same rules as before, organize all packets - the ones in your list of received packets as 
well as the two divider packets - into the correct order.

Afterward, locate the divider packets. To find the decoder key for this distress signal, 
you need to determine the indices of the two divider packets and multiply them together. 
(The first packet is at index 1, the second packet is at index 2, and so on.) 

Organize all of the packets into the correct order. What is the decoder key for the distress signal?

Your puzzle answer was 24921.

"""

