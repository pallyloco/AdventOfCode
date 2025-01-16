from grid import Grid, Coord, Direction

"""
part 1
This word search allows words to be horizontal, vertical, diagonal, written backwards,
or even overlapping other words. you need to find all of XMAS.

part2
it's an X-MAS puzzle in which you're supposed to find two MAS in the shape of an X.
"""

input_data = [
    "MMMSXXMASM",
    "MSAMXMSMSA",
    "AMXSXMAAMM",
    "MSAMASMSMX",
    "XMASAMXAMM",
    "XXAMMXXAMA",
    "SMSMSASXSS",
    "SAXAMASAAA",
    "MAMMMXMMMM",
    "MXMXAXMASX",
]

fh = open("day_04.txt", "r")
input_data = [line.rstrip() for line in fh]

star_directions=(Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST,
                      Direction.NORTH_WEST, Direction.NORTH_EAST, Direction.SOUTH_WEST, Direction.SOUTH_EAST)

cross_directions=(Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST)

def main(data):
    xmas_grid = Grid(data)
    total = 0
    exes = list(xmas_grid.get_coordinates_with_value("X"))
    ayes = list(xmas_grid.get_coordinates_with_value("A"))

    # part 1
    for coord in exes:
        total += how_many_strings(xmas_grid, coord, "XMAS", star_directions)
    print(total)

    # part 2
    total = 0
    for coord in ayes:
        total += x_mas(coord.row, coord.col, xmas_grid)
    print(total)


def x_mas(row, col, grid:Grid):
    """Find if MAS forms an 'x' shape (2 strings)"""
    if row == 0 or row == grid.max_row():
        return 0
    if col == 0 or col == grid.max_col():
        return 0

    s3 = grid.get_data_point(row - 1,col - 1).value + "A" + grid.get_data_point(row + 1,col + 1).value
    s4 = grid.get_data_point(row - 1,col + 1).value + "A" + grid.get_data_point(row + 1,col - 1).value
    if (s3 == "MAS" or s3 == "SAM") and (s4 == "SAM" or s4 == "MAS"):
        return 1
    return 0


def how_many_strings(grid: Grid, coord: Coord, look_for: str, directions) -> int:
    total_found = 0
    for direction in directions:
        walker = Coord(coord.row, coord.col, direction=direction)
        found = True
        for char in look_for:
            if grid.get_data_point(walker.row, walker.col) is None \
                    or grid.get_data_point(walker.row, walker.col).value != char:
                found = False
                break
            walker.move()
        total_found = total_found + 1 if found else total_found
    return total_found


main(input_data)
