from dataclasses import dataclass
from Grid import Grid
import itertools


@dataclass
class DataPoint:
    row: int
    col: int
    value: str


def main():
    file = open("day14_input.txt", 'r')
    # NOTE: there are no negative numbers in the input

    grid = Grid()

    """
    Your scan traces the path of each solid rock structure and reports the x,y coordinates 
    that form the shape of the path, where x represents distance to the right and y represents 
    distance down. Each path appears as a single line of text in your scan. 
    After the first point of each path, each point indicates the end of a straight horizontal 
    or vertical line to be drawn from the previous point. 
    
    For example:
    498,4 -> 498,6 -> 496,6
    503,4 -> 502,4 -> 502,9 -> 494,9
    """
    for r, line in enumerate(map(str.rstrip, file)):
        pts: list[list] = [list(map(int, x.split(","))) for x in line.split(" -> ")]

        # pt consists of col,row NOT row,col
        for pt1, pt2 in itertools.pairwise(pts):
            start_row = min(pt1[1], pt2[1])
            end_row = max(pt1[1], pt2[1])
            start_col = min(pt1[0], pt2[0])
            end_col = max(pt1[0], pt2[0])

            for row in range(start_row, end_row + 1):
                for col in range(start_col, end_col + 1):
                    grid.set_value(DataPoint(row, col, "#"))

    floor = grid.max_row() + 1

    """
    The sand is pouring into the cave from point 500,0.

    Sand is produced one unit at a time, and the next unit of sand is not produced 
    until the previous unit of sand comes to rest. 
    A unit of sand is large enough to fill one tile of air in your scan.
    """
    grid.set_value(DataPoint(0, 500, "+"))

    """
    Using your scan, simulate the falling sand. How many units of sand come to rest 
    before sand starts flowing into the abyss below?
    """
    sand_count = 0
    for sand_count in itertools.count():
        if not falling_sand(grid, floor):
            print(f"{sand_count} grains of sand stopped before falling to the floor")
            break

    """
    You realize you misread the scan. 
    There isn't an endless void at the bottom of the scan - there's floor, 
    and you're standing on it!
    """
    for more_sand in itertools.count(sand_count+1):
        falling_sand(grid, floor)
        if grid.get_data_point(0, 500).value == "o":
            print(f"{more_sand+1} grains of sand dropped before blocking source")
            break


def falling_sand(grid: Grid, floor: int) -> bool:
    """
    Sand keeps moving as long as it is able to do so, at each step trying to move down,
    then down-left, then down-right.
    If all three possible destinations are blocked, the unit of sand comes to rest and no
    longer moves, at which point the next unit of sand is created back at the source.
    """

    row, col = (0, 500)  # starting point
    while True:

        # A unit of sand always falls down one step if possible.
        if grid.get_data_point(row + 1, col) is None:
            row += 1

        # If the tile immediately below is blocked (by rock or sand),
        # the unit of sand attempts to instead move diagonally one  step down and to the left.
        elif grid.get_data_point(row + 1, col - 1) is None:
            row = row + 1
            col = col - 1

        # If that tile is blocked, the unit of sand attempts to instead move diagonally
        # one step down and to the right.
        elif grid.get_data_point(row + 1, col + 1) is None:
            row = row + 1
            col = col + 1

        # If all three possible destinations are blocked, the unit of sand comes to rest and no
        # longer moves, at which point the next unit of sand is created back at the source.
        else:
            grid.set_value(DataPoint(row, col, "o"))
            return True

        # you don't have time to scan the floor, so assume the floor is an infinite horizontal
        # line with a y coordinate equal to two plus the highest y coordinate of any point in your scan.
        if row == floor:
            grid.set_value(DataPoint(row, col, "o"))
            return False


# ===================================================================
# Entry point
# ===================================================================
if __name__ == '__main__':
    main()

"""
--- Day 14: Regolith Reservoir ---

You scan a two-dimensional vertical slice of the cave above you (your puzzle input) and 
discover that it is mostly air with structures made of rock.

Your scan traces the path of each solid rock structure and reports the x,y coordinates 
that form the shape of the path, where x represents distance to the right and y represents 
distance down. Each path appears as a single line of text in your scan. 
After the first point of each path, each point indicates the end of a straight horizontal 
or vertical line to be drawn from the previous point. For example:

498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
This scan means that there are two paths of rock; the first path consists of two straight lines, and the second path 
consists of three straight lines. (Specifically, the first path consists of a line of rock from 498,4 through 498,6 and 
another line of rock from 498,6 through 496,6.)

The sand is pouring into the cave from point 500,0.

Sand is produced one unit at a time, and the next unit of sand is not produced 
until the previous unit of sand comes to rest. 
A unit of sand is large enough to fill one tile of air in your scan.

Sand keeps moving as long as it is able to do so, at each step trying to move down, 
then down-left, then down-right. 
If all three possible destinations are blocked, the unit of sand comes to rest and no 
longer moves, at which point the next unit of sand is created back at the source.

Using your scan, simulate the falling sand. How many units of sand come to rest 
before sand starts flowing into the abyss below?

Your puzzle answer was 843.

--- Part Two ---
You realize you misread the scan. 
There isn't an endless void at the bottom of the scan - there's floor, and you're standing on it!

You don't have time to scan the floor, so assume the floor is an infinite horizontal 
line with a y coordinate equal to two plus the highest y coordinate of any point in your scan.

To find somewhere safe to stand, you'll need to simulate falling sand until a unit of sand comes to rest at 500,0, 
blocking the source entirely and stopping the flow of sand into the cave. 

Your puzzle answer was 27625.

"""
