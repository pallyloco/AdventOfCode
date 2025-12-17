from __future__ import annotations
import itertools as it
from dataclasses import dataclass

data = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""
data = list(map(str.rstrip,data.splitlines()))
fh = open("day_09.txt", "r")
data = list(map(str.rstrip, fh.readlines()))



def theatre():
    tiles: list[Coord] = list(Coord(int(row), int(col)) for col,row in (line.split(",") for line in data))
    rectangles = [Rectangle(a,b) for a,b in it.combinations(tiles,2)]
    rectangles.sort(reverse=True)
    print(f"Answer 1: biggest rectangle {rectangles[0].area}")

    lines = []
    for a,b in it.pairwise(tiles+[tiles[0]],):
        line = Line(a,b)
        lines.append(line)

    for rectangle in rectangles:
        if any(rectangle.is_point_in(p) for p in tiles):
            continue

        if rectangle_inside_polygon(tiles, lines, rectangle):
            print(f"Answer 2: biggest rectangle in polygon is {rectangle.area}")
            break
    pass

def cross_line(v_line, h_line):
    return (v_line.p1.row < h_line.p1.row < v_line.p2.row and
            h_line.p1.col < v_line.p1.col < h_line.p2.col)


def rectangle_inside_polygon(points, lines, rectangle):
    # no other points inside rectangle
    if any(rectangle.is_point_in(p) for p in points):
        return False

    print()
    print()
    print(f"=== {rectangle} ===")
    # no lines crossing into the rectangle
    horizontal_lines = [line for line in lines if line.horizontal]
    vertical_lines = [line for line in lines if line.vertical]
    for v_line in vertical_lines:
        if cross_line(v_line, rectangle.top):
            print(f"Rectangle top {rectangle.top} crossed line {v_line}")
            return False

        if cross_line(v_line, rectangle.bottom):
            print(f"Rectangle bottom {rectangle.bottom} crossed line {v_line}")
            return False

    for h_line in horizontal_lines:
        if cross_line(rectangle.left,h_line):
            print(f"rectangle left {rectangle.left} crossed line {h_line}")
            return False

        if  cross_line(rectangle.right, h_line):
            print(f"rectangle right {rectangle.right} crossed line {h_line}")
            return False

    return True



class Coord:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.lines = []

    def __lt__(self, other):
        return (self.row, self.col) < (other.row, other.col)
    def __str__(self):
        return f"({self.row},{self.col})"
    def __repr__(self):
        return str(self)


@dataclass
class Rectangle:
    p1: Coord
    p2: Coord

    @property
    def area(self):
        return (self.max_row - self.min_row + 1) * (self.max_col - self.min_col + 1)

    @property
    def bottom_left(self):
        return Coord(self.max_row, self.min_col)

    @property
    def top_left(self):
        return Coord(self.min_row, self.min_col)

    @property
    def bottom_right(self):
        return Coord(self.max_row, self.max_col)

    @property
    def top_right(self):
        return Coord(self.min_row, self.max_col)

    @property
    def min_row(self):
        return min(self.p1.row, self.p2.row)

    @property
    def max_row(self):
        return max(self.p1.row, self.p2.row)

    @property
    def min_col(self):
        return min(self.p1.col, self.p2.col)

    @property
    def max_col(self):
        return max(self.p1.col, self.p2.col)

    @property
    def top(self) -> Line:
        return Line(self.top_left, self.top_right)

    @property
    def bottom(self) -> Line:
        return Line(self.bottom_left, self.bottom_right)

    @property
    def right(self)->Line:
        return Line(self.top_right, self.bottom_right)

    @property
    def left(self)->Line:
        return Line(self.top_left, self.bottom_left)

    def is_point_in(self, p: Coord):
        return self.min_row < p.row < self.max_row and self.min_col < p.col < self.max_col

    def __lt__(self,other):
        return self.area < other.area

    def __str__(self):
        return f"{self.p1}-{self.p2} [{self.area}]"
    def __repr__(self):
        return str(self)

class Line:
    def __init__(self, p1:Coord, p2:Coord):
        """join two points"""
        self.p1, self.p2 = sorted((p1,p2))

    @property
    def vertical(self):
        return self.p1.col == self.p2.col

    @property
    def horizontal(self):
        return self.p1.row == self.p2.row

    def __str__(self):
        return f"({self.p1.row},{self.p1.col}) -> ({self.p2.row},{self.p2.col})"

    def __repr__(self):
        return str(self)



if __name__ == "__main__":
    theatre()