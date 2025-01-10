import re
from dataclasses import dataclass

input_data = [
    "Button A: X+94, Y+34",
    "Button B: X+22, Y+67",
    "Prize: X=8400, Y=5400",
    "",
    "Button A: X+26, Y+66",
    "Button B: X+67, Y+21",
    "Prize: X=12748, Y=12176",
    "",
    "Button A: X+17, Y+86",
    "Button B: X+84, Y+37",
    "Prize: X=7870, Y=6450",
    "",
    "Button A: X+69, Y+23",
    "Button B: X+27, Y+71",
    "Prize: X=18641, Y=10279",
]


fh = open("day_13.txt", "r")
input_data = list(map(str.rstrip, fh))

# too low:
# 6298134667057

def main(data):
    spent_tokens = 0
    for i, game in enumerate(triplet(data)):
        denominator = game.ax * game.by - game.bx * game.ay
        if denominator != 0:
            numerator = (game.ax * game.dy - game.ay * game.dx)
            if numerator % denominator == 0:
                b_press = numerator / denominator
                if (game.dx - b_press * game.bx)%game.ax == 0:
                    a_press = (game.dx - b_press * game.bx) / game.ax
                    spent_tokens += 3*a_press + b_press
    print(spent_tokens)




def triplet(data):
    lines = iter(data)

    while True:
        try:
            line = next(lines)
            if line.strip() == "":
                line = next(lines)
        except StopIteration:
            break
        match = re.match(r".*?:.*?\+(\d+),.*?\+(\d+)", line)
        ax, ay = list(map(int,match.groups()))
        line = next(lines)
        match = re.match(r".*?:.*?\+(\d+),.*?\+(\d+)", line)
        bx, by = list(map(int,match.groups()))
        line = next(lines)
        match = re.match(r".*?:.*?=(\d+),.*?=(\d+)", line)
        dx, dy = list(map(int,match.groups()))
        dx += 10000000000000
        dy += 10000000000000


        yield Game(ax, ay, bx, by, dx, dy)


@dataclass
class Game:
    ax: int
    ay: int
    bx: int
    by: int
    dx: int
    dy: int

main(input_data)