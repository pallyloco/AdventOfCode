from __future__ import annotations
from typing import Optional

NUM_ROWS: Optional[int] = None
NUM_COLS: Optional[int] = None

myMap = list[str]
Char = str  # single character


def main():
    global NUM_ROWS, NUM_COLS
    file = open("day_16_input.txt", 'r')
    contraption: myMap = list()
    energized: myMap = list()
    for line in map(str.rstrip, file):
        contraption.append(line)
        energized.append("." * len(line))

    NUM_ROWS = len(contraption)
    NUM_COLS = len(contraption[0])
    been_there_done_that: set[str] = set()
    trace_light_path(PassingLight(0, -1, "east"), been_there_done_that, contraption)

    print("answer 1 = ", calculate_energy(been_there_done_that))

    ans2 = 0
    for row in range(NUM_ROWS):
        been_there_done_that: set[str] = set()
        trace_light_path(PassingLight(row, -1, "east"), been_there_done_that, contraption)
        tmp_ans = calculate_energy(been_there_done_that)
        ans2 = max(ans2, tmp_ans)

        been_there_done_that: set[str] = set()
        trace_light_path(PassingLight(row, NUM_COLS, "west"), been_there_done_that, contraption)
        tmp_ans = calculate_energy(been_there_done_that)
        ans2 = max(ans2, tmp_ans)

    for col in range(NUM_COLS):
        been_there_done_that: set[str] = set()
        trace_light_path(PassingLight(-1, col, "south"), been_there_done_that, contraption)
        tmp_ans = calculate_energy(been_there_done_that)
        ans2 = max(ans2, tmp_ans)

        been_there_done_that: set[str] = set()
        trace_light_path(PassingLight(NUM_ROWS, col, "north"), been_there_done_that, contraption)
        tmp_ans = calculate_energy(been_there_done_that)
        ans2 = max(ans2, tmp_ans)

    print("Answer 2 = ", ans2)


def calculate_energy(been_there_done_that):
    energized: set[str] = set()

    for beam_str in been_there_done_that:
        energized.add(beam_str[1:])
    return len(energized)


def trace_light_path(beam: PassingLight, btdt: set[str], thingy: myMap):
    while True:

        if not beam.move():
            return

        if str(beam) in btdt:
            return

        btdt.add(str(beam))

        cell = thingy[beam.row][beam.col]
        split_beam = beam.interact(cell)

        if split_beam is not None:
            trace_light_path(split_beam, btdt, thingy)


class PassingLight:
    def __init__(self, row: int, col: int, direction: str):
        self.row: int = row
        self.col: int = col
        self.direction: str = direction

    @staticmethod
    def create_beam(info: str) -> PassingLight:
        direction, coords = info.split()
        r, c = coords.split(",")
        row = int(r[1:])
        col = int(c[:-1])

        if direction == "<":
            return PassingLight(row, col, "west")
        if direction == ">":
            return PassingLight(row, col, "east")
        if direction == "^":
            return PassingLight(row, col, "north")
        if direction == "v":
            return PassingLight(row, col, "south")

    def move(self) -> bool:
        if self.direction == 'east':
            self.col += 1
        elif self.direction == 'west':
            self.col -= 1
        elif self.direction == "north":
            self.row -= 1
        elif self.direction == "south":
            self.row += 1
        else:
            raise ValueError

        if NUM_ROWS is not None and NUM_COLS is not None:
            if 0 <= self.row < NUM_ROWS and 0 <= self.col < NUM_COLS:
                return True
            else:
                return False
        return True

    def interact(self, cell: Char) -> Optional[PassingLight]:
        translate: dict[str, dict[str, str]] = {
            "\\": {"north": "west", "south": "east", "west": "north", "east": "south"},
            "/": {"north": "east", "east": "north", "south": "west", "west": "south"},
            "|": {"north": "north", "south": "south", "west": "north south", "east": "north south"},
            "-": {"north": "east west", "south": "east west", "west": "west", "east": "east"},
            ".": {"north": "north", "south": "south", "east": "east", "west": "west"}
        }
        new_dir = translate[cell][self.direction]
        dirs = new_dir.split()
        self.direction = dirs[0]
        new_beam: Optional[PassingLight] = None
        if len(dirs) > 1:
            new_beam = PassingLight(self.row, self.col, dirs[1])

        return new_beam

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __str__(self):
        if self.direction == f"west":
            return f"< ({self.row},{self.col})"
        if self.direction == "east":
            return f"> ({self.row},{self.col})"
        if self.direction == "north":
            return f"^ ({self.row},{self.col})"
        if self.direction == "south":
            return f"v ({self.row},{self.col})"
        raise ValueError

    def __repr__(self):
        return str(self)


if __name__ == "__main__":
    main()
