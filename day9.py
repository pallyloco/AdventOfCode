from __future__ import annotations
import re
import math
from os import system, name
import time

# data determined after solving the puzzle.  Used for printing snake movement because it is fun
MIN_ROW = -120
MIN_COL = -40
MAX_ROW = 90
MAX_COL = 115
do_print = False
do_output = False


# ===================================================================
# main
# ===================================================================
def main(num_knots: int):
    file = open('day9_input.txt', 'r')
    knots: list[Knot] = list()
    nodes_visited: set[str] = set()
    for _ in range(num_knots):
        knots.append(Knot(6, 10))

    nodes_visited.add(str(knots[-1]))

    for line in file:
        line = line.rstrip()

        """
        Then, by following a hypothetical series of motions (your puzzle input)
        """
        regex = re.match(r"(.)\s(\d+)", line)

        if regex.group(1) == "L":
            move(knots, nodes_visited, int(regex.group(2)), 0, -1)
        elif regex.group(1) == "R":
            move(knots, nodes_visited, int(regex.group(2)), 0, 1)
        elif regex.group(1) == "U":
            move(knots, nodes_visited, int(regex.group(2)), 1, 0)
        elif regex.group(1) == "D":
            move(knots, nodes_visited, int(regex.group(2)), -1, 0)

    answer = len(nodes_visited)
    output(nodes_visited)
    print(f"answer: {answer}")


# ===================================================================
# move
# ===================================================================
def move(knots, nodes_visited, amount, row_dir, col_dir):
    """
    Consider a rope with a knot at each end; these knots mark the head and the tail of the rope.
    If the head moves far enough away from the tail, the tail is pulled toward the head.

    Due to the aforementioned Planck lengths, the rope must be quite short; in fact, the head (H) and
    tail (T) must always be touching (diagonally adjacent and even overlapping both count as touching):

    If the head is ever two steps directly up, down, left, or right from the tail, the tail must
    also move one step in that direction so it remains close enough:

    Otherwise, if the head and tail aren't touching and aren't in the same row or column, the tail
    always moves one step diagonally to keep up:

    After simulating the rope, you can count up all of the positions the tail visited at least once.

    Part 2:
    Rather than two knots, you now must simulate a rope consisting of ten knots. One knot is still
    the head of the rope and moves according to the series of motions.
    Each knot further down the rope follows the knot in front of it using the same rules as before.

    """
    for i in range(amount):

        # move the first knot
        prev_knot = knots[0]
        prev_knot.row = prev_knot.row + row_dir
        prev_knot.col = prev_knot.col + col_dir

        for knot_number, knot in enumerate(knots[1:]):

            # reset prev_knot
            prev_knot = knots[knot_number]

            # If the previous knot is ever two steps directly up, down, left, or right
            # from the tail, the tail must also move one step in that 
            # direction so that it remains close enough:
            if abs(knot.row - prev_knot.row) == 2 and knot.col == prev_knot.col:
                knot.row += math.copysign(1, prev_knot.row - knot.row)
            elif abs(knot.col - prev_knot.col) == 2 and knot.row == prev_knot.row:
                knot.col += math.copysign(1, prev_knot.col - knot.col)

            # Otherwise, if the previous knot and tail aren't touching and aren't
            # in the same row or column, the tail always moves one step 
            # diagonally to keep up:
            elif abs(knot.row - prev_knot.row) > 1 or abs(knot.col - prev_knot.col) > 1:
                knot.row += math.copysign(1, prev_knot.row - knot.row)
                knot.col += math.copysign(1, prev_knot.col - knot.col)

            else:
                break
            nodes_visited.add(str(knots[-1]))
            print_snake(knots)


# ===================================================================
# print snake
# ===================================================================
def print_snake(knots: list[Knot]):
    if do_print:
        clear()
        for row in range(MAX_ROW, MIN_ROW - 1, -1):
            line = ""
            for col in range(MIN_COL, MAX_COL + 1):
                symbol = " "
                for knot in knots:
                    if knot.row == row and knot.col == col:
                        symbol = "#"
                        break

                line = line + symbol
            print(line)
        time.sleep(1 / 1000)


# ===================================================================
# print output
# ===================================================================
def output(nodes_visited: set[str]):
    if do_output:
        print()
        for row in range(MAX_ROW, MIN_ROW - 1, -1):
            for col in range(MIN_COL, MAX_COL + 1):
                if str(Knot(row, col)) in nodes_visited:
                    print("#", end="")
                else:
                    print(".", end="")
            print()


# ===================================================================
# define our clear function
# ===================================================================
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


# ===================================================================
# Knot
# ===================================================================
class Knot:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    def __str__(self):
        return f"{int(self.row)},{int(self.col)}"

    def __repr__(self):
        return str(self)

    row: int
    col: int


# ===================================================================
# Entry point
# ===================================================================
if __name__ == '__main__':
    main(2)
    main(10)
