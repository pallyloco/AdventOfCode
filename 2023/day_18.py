from Polygon import Polygon
from Coords import Coord


def main(part: int = 1):
    # dig: 0 means R, 1 means D, 2 means L, and 3 means U.
    move_coords: dict[str:Coord] = {
        "D": Coord(1, 0),
        "U": Coord(-1, 0),
        "R": Coord(0, 1),
        "L": Coord(0, -1),
        "0": Coord(0, 1),
        "1": Coord(1, 0),
        "2": Coord(0, -1),
        "3": Coord(-1, 0),
    }

    # ------ PART 1
    file = open("day_18_input.txt", 'r')
    poly = Polygon()
    current: Coord = Coord(0, 0)
    poly.add_inside_vertex(current)

    # define outline of lava pool
    for line in map(str.rstrip, file):
        direction, value, colour = line.split()
        value: int = int(value)
        current = current + move_coords[direction].scale(value)
        poly.add_inside_vertex(current)
    file.close()

    print(poly.outer_volume())


    # PART 2
    file = open("day_18_input.txt", 'r')
    poly = Polygon()
    current: Coord = Coord(0, 0)
    poly.add_inside_vertex(current)

    # define outline of lava pool
    for line in map(str.rstrip, file):
        _, _, colour = line.split()
        value = int(colour[2:7], 16)
        direction = colour[-2]

        current = current + move_coords[direction].scale(value)
        poly.add_inside_vertex(current)

    print(poly.outer_volume())


if __name__ == "__main__":
    main()


"""
#######
#.....#
###...#
..#...#
..#...#
###.###
#...#..
##..###
.#....#
.######
"""