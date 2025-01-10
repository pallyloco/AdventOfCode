import re
from dataclasses import dataclass

from grid import Grid
from coord import Coord

# 11 tiles wide and 7 tiles tall
WIDTH = 101
HEIGHT = 103

input_data = [
    "p=0,4 v=3,-3",
    "p=6,3 v=-1,-3",
    "p=10,3 v=-1,2",
    "p=2,0 v=2,-1",
    "p=0,0 v=1,3",
    "p=3,0 v=-2,-2",
    "p=7,6 v=-1,-3",
    "p=3,0 v=-1,-2",
    "p=9,3 v=2,3",
    "p=7,3 v=-1,2",
    "p=2,4 v=2,-3",
    "p=9,5 v=-3,-3",
]

# too low: 77423040
fh = open("day_14.txt", "r")
input_data = list(map(str.rstrip, fh))


@dataclass
class Guard:
    px: int
    py: int
    vx: int
    vy: int

    def move(self):
        self.px = (self.px + self.vx) % WIDTH
        self.py = (self.py + self.vy) % HEIGHT
        return self

    def __str__(self):
        return f"{self.px} {self.py} {self.vx} {self.vy}"



def main(data):
    guards = []
    for line in data:
        match = re.match(r".*?=(-?\d+),(-?\d+) .*?=(-?\d+),(-?\d+)", line)
        px, py, vx, vy = list(map(int, match.groups()))
        guards.append(Guard(px, py, vx, vy))

    for i in range(10000):
        area = Grid()
        center_num = 0
        for guard in guards:
            area.set_value(Coord(guard.py, guard.px))
            if int(WIDTH/2) - 10 < guard.px < int(WIDTH/2) + 10 and int(HEIGHT/2) - 10 < guard.py < int(HEIGHT/2) + 10:
                center_num += 1
        if 6510 < i < 6520:
            print(i, center_num)
            print(area)

        for guard in guards:
            guard.move()

    region1 = 0
    region2 = 0
    region3 = 0
    region4 = 0

    for guard in guards:
        x, y = guard.px, guard.py
        if 0 <= x < int(WIDTH / 2) and 0 <= y < int(HEIGHT / 2):
            region1 += 1
        elif int(WIDTH / 2) < x < WIDTH and 0 <= y < int(HEIGHT / 2):
            region2 += 1
        elif int(WIDTH / 2) < x < WIDTH and int(HEIGHT / 2) < y < HEIGHT:
            region3 += 1
        elif 0 <= x < int(WIDTH / 2) and int(HEIGHT / 2) < y < HEIGHT:
            region4 += 1
    print(region1 * region2 * region3 * region4)


main(input_data)

