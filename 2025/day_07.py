from typing import Optional

from grid import Grid
from coord import DataInCell, Direction

data=""".......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""
data = list(map(str.rstrip,data.splitlines()))
fh = open("day_07.txt", "r")
data = list(map(str.rstrip, fh.readlines()))

def tachyon_manifold():
    tmap = Grid(data)
    beams = list(tmap.get_coordinates_with_value("S"))
    beams[0].value = "1"
    hit_splitter = 0

    for row in tmap.row_range:
        print(tmap)
        for beam in (cell for cell in tmap.get_row_values(row) if cell is not None and cell.value.isdigit()):
            below = tmap.south(beam)
            if below is None or below.value != "^":
                tmap.set_value( merge_tachyon_paths(row+1, beam.col, beam, below))
            else:
                tmap.set_value( merge_tachyon_paths(row+1, beam.col-1, beam, tmap.get_data_point(row+1, beam.col-1)))
                tmap.set_value( merge_tachyon_paths(row+1, beam.col+1, beam, tmap.get_data_point(row+1, beam.col+1)))
                hit_splitter += 1

    print( f"hit_splitter: {hit_splitter}")

    unique_paths = 0
    for beam in (cell for cell in tmap.get_row_values(tmap.max_row) if cell is not None and cell.value.isdigit()):
        unique_paths += int(beam.value)
    print( f"unique paths: {unique_paths}")


def merge_tachyon_paths(row, col, p1: DataInCell, p2: Optional[DataInCell] = None):
    if p2 is None:
        return DataInCell(row, col, p1.value)
    return DataInCell(row, col, str(int(p1.value) + int(p2.value)))

if __name__ == "__main__":
    tachyon_manifold()



