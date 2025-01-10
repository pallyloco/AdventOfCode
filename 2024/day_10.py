from grid import Grid
from coord import Coord

input_data = [
    "89010123",
    "78121874",
    "87430965",
    "96549874",
    "45678903",
    "32019012",
    "01329801",
    "10456732",
]


fh = open("day_10.txt", "r")
input_data = list(map(str.rstrip, fh))


def main(data):
    terrain: Grid = read_map(data)
    trail_heads = [c for c in terrain.data if c.value == 0]
    total = 0
    total2 = 0
    for trail_head in trail_heads:
        trails = set()
        find_trails(trail_head, terrain, "", trails)

        peaks = set()
        for trail in trails:
            spots = trail.split()
            peaks.add(spots[-1])
        #print (len(peaks))
        #print("DONE")
        total += len(peaks)
        total2 += len(trails)
    print(total)
    print(total2)


def valid_moves(location, terrain, been_there: str) -> list[Coord]:
    result = []
    for n in terrain.ordinal_neighbours(location):
        if n is None:
            continue
        if n.value == -1:
            continue
        if str(n) not in been_there and n.value - location.value == 1:
            result.append(n)
    return result


def find_trails(location, terrain, been_there: str, trails: set):
    been_there += f"{location} "
    if location.value == 9:
        #print(been_there)
        trails.add(been_there)

    new_moves = valid_moves(location, terrain, been_there)
    if len(new_moves) == 0:
        return

    for n in new_moves:
        find_trails(n, terrain, been_there, trails)

    return

def read_map(data):
    terrain = Grid()
    for row, line in enumerate(data):
        for col, height in enumerate(line):
            v = int(height) if height != "." else -1
            terrain.set_value(Coord(row, col, v))
    return terrain

main(input_data)