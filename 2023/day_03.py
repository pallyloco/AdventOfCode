from typing import Optional

from GridN import GridN
import re


class Spot:
    coords: list[int]
    value: str

    def __init__(self, coords: list[int], value: Optional[str]):
        if value == ".":
            value = None
        self.coords = coords
        self.value = value


def main():
    file = open("day_03_input.txt", 'r')
    grid = GridN()
    gears: dict[str, list[str]] = dict()
    row = 0
    ans = 0
    lines = list()

    # Create the grid
    for line in map(str.rstrip, file):
        for col, char in enumerate(line):
            grid.set_value(Spot([row, col], char))
        lines.append(line)
        row = row + 1

    row = 0
    for line in lines:

        # find the numbers in the line
        numbers: list[str] = [n for n in re.split(r"\D+", line) if len(n) != 0]

        index = 0
        for number in numbers:

            # is this number a valid number (i.e. does its neighbours have a symbol
            # other than a digit or "."
            valid_part_number = False
            index = line.find(number, index)

            # check neighbours for all digits of number
            for digit, char in enumerate(number):
                if valid_part_number:
                    continue
                for neighbour in grid.neighbours(grid.get_data_point(row, index + digit)):
                    if neighbour.value is not None and not neighbour.value.isdigit():
                        valid_part_number = True

                        # gears are "*" symbols.  keep track of which numbers are attached to a gear.
                        if neighbour.value == "*":
                            key = grid.key(neighbour)
                            if key not in gears:
                                gears[key] = list()
                            gears[key].append(number)

                        break

            # for part 1
            if valid_part_number:
                ans = ans + int(number)
            index = index + len(number)
        row += 1
    print("part 1:", ans)

    # for part 2
    ans2 = 0
    for gear in gears:
        if len(gears[gear]) == 2:
            ans2 = ans2 + int(gears[gear][0]) * int(gears[gear][1])
    print("part 2:", ans2)


if __name__ == "__main__":
    main()
