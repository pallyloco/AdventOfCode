from dataclasses import dataclass

import Grid

"""
All decisions are based on the number of occupied seats adjacent to a given seat
(one of the eight positions immediately up, down, left, right, or diagonal from the seat).
The following rules are applied to every seat simultaneously:

If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat
becomes empty.

Otherwise, the seat's state does not change.

Floor (.) never changes; seats don't move, and nobody sits on the floor.

Simulate your seating area by applying the seating rules repeatedly until no seats change state. 
How many seats end up occupied?
"""


@dataclass
class DataPoint:
    row: int
    col: int
    value: str


def main(part: int = 1):
    file = open('day11_input.txt', 'r')
    original_seating: Grid = Grid.Grid()

    for row, line in enumerate(map(str.rstrip, file)):
        for col, seat in enumerate(line):
            original_seating.set_value(DataPoint(row, col, seat))
    row_range = range(original_seating.max_row() + 1)
    col_range = range(original_seating.max_col() + 1)

    # ========================================================================
    # Part 1
    # ========================================================================
    seating_p1: Grid = original_seating
    seating_p2: Grid = original_seating
    while True:
        new_p1_seating: Grid = Grid.Grid()
        new_p2_seating: Grid = Grid.Grid()
        nochange = True
        for row in row_range:
            for col in col_range:
                nochange = adjust_seating(1, seating_p1, new_p1_seating, row, col) and nochange
                nochange = adjust_seating(2, seating_p2, new_p2_seating, row, col) and nochange
        print(seating_p2)
        print()

        if nochange:
            break
        seating_p1 = new_p1_seating
        seating_p2 = new_p2_seating

    print("Occupied seats (Part 1):", sum((1 for s in seating_p1.data if s is not None and s.value == "#")))
    print("Occupied seats (Part 2):", sum((1 for s in seating_p2.data if s is not None and s.value == "#")))


def adjust_seating(part: int, seating: Grid, new_seating: Grid, row: int, col: int) -> bool:
    """
    PART I
    If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
    If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat
    becomes empty.

    PART II
    Now, instead of considering just the eight immediately adjacent seats,
    consider the first seat in each of those eight directions.
    """

    seat: DataPoint = seating.get_data_point(row, col)
    nochange: bool = True
    value = seat.value
    neighbours: list[DataPoint] = list()
    if value == ".":
        new_seating.set_value(DataPoint(row, col, value))
        return True

    if part == 1:
        max_occupied = 4
        neighbours = seating.neighbours(seat)
    else:
        max_occupied = 5
        for direction in (seating.north, seating.south, seating.east, seating.west,
                          seating.north_east, seating.north_west, seating.south_west,
                          seating.south_east):
            neighbour = direction(seat)
            while neighbour is not None and neighbour.value == ".":
                neighbour = direction(neighbour)
            neighbours.append(neighbour)

    occupied = sum((1 for s in neighbours if s is not None and s.value == "#"))
    if seat.value == "L":
        if occupied == 0:
            value = "#"
            nochange = False

    elif seat.value == "#":
        if occupied >= max_occupied:
            value = "L"
            nochange = False

    new_seating.set_value(DataPoint(row, col, value))
    return nochange


if __name__ == '__main__':
    main(1)
