import math

from coord import Coord
import itertools as it


"""
PART 1
In particular, an antinode occurs at any point that is perfectly in line with two antennas 
of the same frequency - but only when one of the antennas is twice as far away as the other.

This means that for any pair of antennas with the same frequency, there are two antinodes, 
one on either side of them.

PART 2
After updating your model, it turns out that an antinode occurs at any grid position exactly 
in line with at least two antennas of the same frequency, regardless of distance. 
This means that some of the new antinodes will occur at the position of each antenna

"""

input_data = [
    "............",
    "........0...",
    ".....0......",
    ".......0....",
    "....0.......",
    "......A.....",
    "............",
    "............",
    "........A...",
    ".........A..",
    "............",
    "............",
]

MAX_ROW = 9
MAX_COL = 9

fh = open("day_08.txt", "r")
input_data = list(map(str.rstrip, fh))


def main(data):
    antennas = read_antennas(data)

    node_points: set[tuple[int, int]] = set()
    part_2_nodes: set[tuple[int, int]] = set()
    grouped_antennas: dict[str, list[Coord]] = dict()

    for antenna_type in set((a.value for a in antennas)):
        grouped_antennas[antenna_type] = [a for a in antennas if a.value == antenna_type]
        find_nodes(grouped_antennas[antenna_type], node_points)
        find_nodes_2(grouped_antennas[antenna_type], part_2_nodes)
    print(len(node_points))
    print(len(part_2_nodes))


def find_nodes(antennas: list[Coord], node_points: set[tuple[int, int]]):
    # part 1
    # How many unique locations within the bounds of the map contain an antinode?

    for a, b in it.combinations(antennas, 2):
        pts: list[tuple[int, int]] = [
            (2 * b.row - a.row, 2 * b.col - a.col),
            (2 * a.row - b.row, 2 * a.col - b.col),
        ]

        for r, c in pts:
            if 0 <= r <= MAX_ROW and 0 <= c <= MAX_COL:
                node_points.add((r, c))


def find_nodes_2(antennas: list[Coord], node_points: set[tuple[int, int]]):
    # part 2
    # How many unique locations within the bounds of the map contain an antinode?
    for a, b in it.combinations(antennas, 2):
        gcd = math.gcd(abs(b.row - a.row), abs(b.col - a.col))
        d_row = int((b.row - a.row) / gcd)
        d_col = int((b.col - a.col) / gcd)

        r = a.row
        c = a.col
        while 0 <= r <= MAX_ROW and 0 <= c <= MAX_COL:
            node_points.add((r, c))
            r += d_row
            c += d_col

        r = a.row
        c = a.col
        while 0 <= r <= MAX_ROW and 0 <= c <= MAX_COL:
            node_points.add((r, c))
            r -= d_row
            c -= d_col


def read_antennas(inputs) -> list[Coord]:
    global MAX_COL
    global MAX_ROW
    antennas = []
    for row, line in enumerate(inputs):
        MAX_ROW = row
        for col, char in enumerate(line):
            if char != ".":
                antennas.append(Coord(row, col, char))
            MAX_COL = col
    return antennas


main(input_data)
