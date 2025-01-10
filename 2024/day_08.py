import math

from grid import Grid
from coord import Coord
import itertools as it

data = [
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


def main():
    # part 1
    fh = open("day_08.txt", "r")
    data = list(map(str.rstrip, fh))
    antennas = read_antennas(data)

    node_points: set[tuple[int, int]] = set()
    part_2_nodes: set[tuple[int, int]] = set()
    grouped_antennas: dict[str, list[Coord]] = {b.value: [] for b in antennas}
    for antenna_type in grouped_antennas:
        grouped_antennas[antenna_type] = [a for a in antennas if a.value == antenna_type]
        find_nodes(grouped_antennas[antenna_type], node_points)
        find_nodes_2(grouped_antennas[antenna_type], part_2_nodes)
    print(len(node_points))
    print(len(part_2_nodes))


def find_nodes(antennas: list[Coord], node_points: set[tuple[int, int]]):
    for a, b in it.combinations(antennas, 2):
        pts: list[tuple[int, int]] = [
            (2 * b.row - a.row, 2 * b.col - a.col),
            (2 * a.row - b.row, 2 * a.col - b.col),
        ]
        if (a.row - b.row) % 3 == 0 and (a.col - b.col) % 3 == 0:
            d_row = int((b.row - a.row) / 3)
            d_col = int((b.col - a.col) / 3)
            pts.append((a.row + 2 * d_row, a.col + 2 * d_col))
            pts.append((a.row + d_row, a.col + d_col))

        for r, c in pts:
            if 0 <= r <= MAX_ROW and 0 <= c <= MAX_COL:
                node_points.add((r, c))


def find_nodes_2(antennas: list[Coord], node_points: set[tuple[int, int]]):
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


main()
#find_nodes_2([Coord(0,0),Coord(1,3),Coord(2,1)],set())
