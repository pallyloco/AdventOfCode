from dataclasses import dataclass

from Grid import Grid
import re


@dataclass
class DataPoint:
    row: int
    col: int
    value: str


# Sensor at x=2, y=18: closest beacon is at x=-2, y=15
parse = re.compile(r'.*?x=(-?\d+).*?y=(-?\d+).*?x=(-?\d+).*?y=(-?\d+)')

"""
Consult the report from the sensors you just deployed. In the row where y=2000000, 
how many positions cannot contain a beacon?
"""
row_of_interest = 2000000

"""
The distress beacon is not detected by any sensor, but the distress beacon must have 
x and y coordinates each no lower than 0 and no larger than 4000000.
"""
real_max = 4000000
max_row = real_max
max_col = real_max


def main():
    grid = Grid()
    file = open("day15_input.txt", 'r')

    # all_ranges contain the ranges where a beacon can exist for a specific row
    all_ranges = [[(0, max_col)] for _ in range(max_row + 1)]

    for line in map(str.rstrip, file):
        """
        It doesn't take long for the sensors to report back their positions and closest 
        beacons (your puzzle input). 

        Sensor at x=2, y=18: closest beacon is at x=-2, y=15
        """
        print(line)
        sensor_col, sensor_row, beacon_col, beacon_row = map(int, parse.match(line).groups())
        distance = abs(sensor_col - beacon_col) + abs(sensor_row - beacon_row)

        """
        Sensors can only lock on to the one beacon closest to the sensor as measured 
        by the Manhattan distance.
        ... if a sensor detects a beacon, 
        you know there are no other beacons that close or closer to that sensor. 
        """
        if sensor_row - distance <= row_of_interest <= sensor_row + distance:
            r = row_of_interest
            for c in range(sensor_col - distance, sensor_col + distance + 1):
                if abs(sensor_col - c) + abs(sensor_row - r) > distance:
                    continue
                if grid.get_data_point(r, c) is None:
                    grid.set_value(DataPoint(r, c, "#"))
        grid.set_value(DataPoint(sensor_row, sensor_col, "S"))
        grid.set_value(DataPoint(beacon_row, beacon_col, "B"))

        """
        Your handheld device indicates that the distress signal is coming from a beacon nearby. 
        The distress beacon is not detected by any sensor, but the distress beacon must have 
        x and y coordinates each no lower than 0 and no larger than 4000000.
        """
        row_start = max(0, sensor_row - distance)
        row_end = min(max_row, sensor_row + distance)
        for r in range(row_start, row_end + 1):
            col_start = max(0, sensor_col - (distance - abs(r - sensor_row)))
            col_end = min(max_col, sensor_col + (distance - abs(r - sensor_row)))

            remove_ranges(all_ranges, r, col_start, col_end)

    print()

    """
    Consult the report from the sensors you just deployed. In the row where y=2000000, 
    how many positions cannot contain a beacon?
    """
    score = 0
    for c in range(grid.min_col(), grid.max_col() + 1):
        if grid.get_data_point(row_of_interest, c) is not None \
                and grid.get_data_point(row_of_interest, c).value == "#":
            score += 1
    print(f"Number of positions where there are no beacons for sure: {score}")

    """
    To isolate the distress beacon's signal, you need to determine its tuning frequency, 
    which can be found by multiplying its x coordinate by 4000000 and then adding its y coordinate.

    Find the only possible position for the distress beacon. What is its tuning frequency?
    """
    for r, ranges in enumerate(all_ranges):
        if len(ranges) != 0:
            print("Tuning Frequency: ", r + ranges[0][0] * real_max)


def remove_ranges(all_ranges, r, cl, ch):
    ranges = all_ranges[r]
    new_ranges = []
    for cs, ce in ranges:

        # [cs .. (cl,ch) .. ce]
        if cs <= cl <= ce and cs <= ch <= ce:
            if cl - cs != 0:
                new_ranges.append((cs, cl - 1))
            if ch - ce != 0:
                new_ranges.append((ch + 1, ce))
            continue

        #  if [cs .. (cl .. ce] .. ch)
        if cs <= cl <= ce:
            if cs - cl != 0:
                new_ranges.append((cs, cl - 1))
            continue

        # if (cl .. [cs .. ch) .. ce]
        if cs <= ch <= ce:
            if ch - ce != 0:
                new_ranges.append((ch + 1, ce))
            continue

        # if (cl .. [cs,ce] .. ch)
        if cl <= cs and ce <= ch:
            continue

        new_ranges.append((cs, ce))
    all_ranges[r] = new_ranges


# ===================================================================
# Entry point
# ===================================================================
if __name__ == '__main__':
    main()

"""
--- Day 15: Beacon Exclusion Zone ---
Sensors and beacons always exist at integer coordinates. 
Each sensor knows its own position and can determine the position of a beacon precisely; 
however, sensors can only lock on to the one beacon closest to the sensor as measured 
by the Manhattan distance. 
(There is never a tie where two beacons are the same distance to a sensor.)

It doesn't take long for the sensors to report back their positions and closest 
beacons (your puzzle input). For example:

Sensor at x=2, y=18: closest beacon is at x=-2, y=15
So, consider the sensor at 2,18; the closest beacon to it is at -2,15. 

Each sensor only identifies its closest beacon, if a sensor detects a beacon, 
you know there are no other beacons that close or closer to that sensor. 
There could still be beacons that just happen to not be the closest beacon to any sensor. 

This sensor's closest beacon is at 2,10, and so you know there are no beacons that 
close or closer (in any positions marked #).

None of the detected beacons seem to be producing the distress signal, 
so you'll need to work out where the distress beacon is by working out where it isn't. 
For now, keep things simple by counting the positions where a beacon cannot possibly 
be along just a single row.

Consult the report from the sensors you just deployed. In the row where y=2000000, 
how many positions cannot contain a beacon?

Your puzzle answer was 4725496.

--- Part Two ---
Your handheld device indicates that the distress signal is coming from a beacon nearby. 
The distress beacon is not detected by any sensor, but the distress beacon must have 
x and y coordinates each no lower than 0 and no larger than 4000000.

To isolate the distress beacon's signal, you need to determine its tuning frequency, 
which can be found by multiplying its x coordinate by 4000000 and then adding its y coordinate.

Find the only possible position for the distress beacon. What is its tuning frequency?

Your puzzle answer was 12051287042458.

"""
