from __future__ import annotations

from typing import Any

from grid import Grid
from coord import Coord

from explore import Explore

input_data = [
    "RRRRIICCFF",
    "RRRRIICCCF",
    "VVRRRCCFFF",
    "VVRCCCJFFF",
    "VVVVCJJCFE",
    "VVIVCCJJEE",
    "VVIIICJJEE",
    "MIIIIIJJEE",
    "MIIISIJEEE",
    "MMMISSJEEE",
]
input_data = [
"OOOOO",
"O.O.O",
"OOOOO",
"O.O.O",
"OOOOO",
]

fh = open("day_12.txt", "r")

# too low: 884864
# too high: 908784
# too low: 899900
input_data = list(map(str.rstrip, fh))


class Plot:
    def __init__(self, plot: Coord, garden: Grid):
        self.plot = plot
        self.garden = garden

    def obj(self) -> Any:
        return self.plot

    def key(self) -> str:
        return str(self.plot)

    def children(self) -> list[Plot]:
        neighbours = [Plot(c, self.garden) for c in self.garden.ordinal_neighbours(self.plot) if c is not None]
        return [n for n in neighbours if n.obj().value == self.plot.value]

    def __str__(self):
        return str(self.plot)

    def __repr__(self):
        return str(self.plot)


def main(data):
    garden: Grid = read_map(data)
    plots = garden.data
    price = 0
    price2 = 0
    while len(plots) > 0:
        explore = Explore()
        start_plot = Plot(plots[0], garden)
        print(f"processing seeds {start_plot.plot.value}", end=" ")
        region = explore.go_explore(start_plot)
        print(len(region), end=" ")
        perimeter = 0
        for plot in region:
            perimeter += 4 - len(plot.children())
        print(perimeter, end = " ")

        temp_garden = Grid()
        for plot in region:
            temp_garden.set_value(Coord(plot.obj().row, plot.obj().col))
            garden.remove_data_point(plot.obj().row, plot.obj().col)
        plots = garden.data
        num_sides = temp_garden.number_of_sides()
        print(num_sides)

        price += perimeter * len(region)
        price2 += num_sides * len(region)
    print(price, price2)


def read_map(data):
    garden = Grid()
    for row, line in enumerate(data):
        for col, seed in enumerate(line):
            garden.set_value(Coord(row, col, seed))
    return garden


main(input_data)
