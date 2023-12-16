import itertools as it
import re
from typing import Callable, Optional


def main(part: int = 1):
    num_cycles = 1_000_000_000
    file = open("day_14_input.txt", 'r')
    lines_p1 = list()
    lines_p2 = list()
    for l in map(str.rstrip, file):
        lines_p1.append(l)
        lines_p2.append(l)

    max_col = len(lines_p1[0])
    repeat = (roll_north, roll_west, roll_south, roll_east)

    # ====================================================================
    # part 1
    # ====================================================================
    roll_north(lines_p1, max_col)
    line_str = "".join(lines_p1)
    print("answer 1: ", calculate_answer_from_pattern(line_str, max_col))

    # ====================================================================
    # part 2
    # ====================================================================
    patterns, cycle, start = get_all_patterns(lines_p2, repeat, num_cycles)
    print("cycle info is: ", cycle, start)

    index = (num_cycles - start) % cycle + (start - 1)
    print("calculated index is:", index)

    final = patterns[index]
    a = calculate_answer_from_pattern(final, max_col)
    print(index, "answer 2:", a)


def calculate_answer_from_pattern(p: str, max_col):
    re_str = "." * max_col
    lines = re.findall(re_str, p)

    lines.reverse()
    ans1 = 0
    for r, l in enumerate(lines):
        O = len(re.findall(r"O", l))
        ans1 += O * (r + 1)
    return ans1


def get_all_patterns(lines: list[str], repeat: tuple[Callable, ...], max_count: int) -> tuple[list[str], int, int]:
    max_col = len(lines[0])
    pattern: set[str] = set()
    patternl: list[str] = list()

    start_cycle: Optional[int] = None
    cycle: Optional[int] = None

    for i in range(max_count):

        # cycle
        for roll in repeat:
            roll(lines, max_col)

        line_str = "".join(lines)
        pattern.add(line_str)
        patternl.append(line_str)

        if cycle is None and len(pattern) != i + 1:

            for j, p in enumerate(patternl):
                if p == line_str:
                    print(i, j)
                    start_cycle = j
                    cycle = i - start_cycle
                    return patternl, cycle, start_cycle

    return patternl, cycle, start_cycle


# 99380 answer too low
# answer 2: 100064

def roll_north(lines, max_col):
    for col in range(max_col):
        done = False
        while not done:
            done = True
            for row, (r1, r2) in enumerate(it.pairwise(lines)):
                if r2[col] == "O" and r1[col] == ".":
                    lines[row] = lines[row][:col] + "O" + lines[row][col + 1:]
                    lines[row + 1] = lines[row + 1][:col] + "." + lines[row + 1][col + 1:]
                    done = False


def roll_south(lines, max_col):
    lines.reverse()
    roll_north(lines, max_col)
    lines.reverse()


"""
After 1 cycle:
.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....

After 2 cycles:
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O

After 3 cycles:
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O"""


def roll_west(lines, max_col):
    roll_east(lines, max_col, "w")


def reverse_slicing(s):
    return s[::-1]


def roll_east(lines, max_col, dir="e"):
    for row, line in enumerate(lines):
        if dir == "w":
            line = reverse_slicing(line)
        done = False
        while not done:
            done = True
            for col, (c1, c2) in enumerate(it.pairwise(line)):
                if c1 == "O" and c2 == ".":
                    line = line[:col] + ".O" + line[col + 2:]
                    done = False
                    lines[row] = line
        if dir == "w":
            line = reverse_slicing(line)
            lines[row] = line


if __name__ == "__main__":
    main()

"""
after 24 cycles
        123456789112345678921234
indices:0123456789012345678901234567890
        xyz                     |
           abcdef               |
                 abcdef         |
                       abcdef   |
                             abc|    def
                     
what is the answer at 28
cycle = 9 - 3 = 6 (yes)
start = 3

24-3 = 21 contains the repeating part

21%6 = 3

add the start back

3 + 3 = 6 

subtract 1 because we are not '0- indexed'

"""
