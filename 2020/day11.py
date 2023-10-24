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
    seating: Grid = Grid.Grid()

    for row, line in enumerate(map(str.rstrip, file)):
        for col, seat in enumerate(line):
            seating.set_value(DataPoint(row, col, seat))

    while True:
        print(seating)
        print()
        new_seating = Grid.Grid()
        nochange = True
        for row in range(seating.max_row()+1):
            for col in range(seating.max_col()+1):
                seat: DataPoint = seating.get_data_point(row,col)
                value = seat.value

                occupied = sum((1 for s in seating.neighbours(seat) if s is not None and s.value == "#"))
                if seat.value == "L":
                    if occupied == 0:
                        value = "#"
                        nochange = False

                elif seat.value == "#":
                    if occupied >= 4:
                        value = "L"
                        nochange = False

                new_seating.set_value(DataPoint(row,col,value))

        if nochange:
            break
        seating = new_seating
    print (seating)
    print ("Occupied seats:", sum((1 for s in seating.data if s is not None and s.value == "#")))

if __name__ == '__main__':
    main(1)
