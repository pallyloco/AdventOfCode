from __future__ import annotations
from Grid import Grid, DataPoint
from Coords import Coord
from Astar import AStar

MAX_ROW = 0
MAX_COL = 0


class GardenPlot:
    def __init__(self, row: int, col: int, grid: Grid = None):
        self.row: int = row
        self.col: int = col
        self.grid: Grid = grid

    def key(self):
        return str(self)

    def children(self) -> list[GardenPlot]:
        kids: list[GardenPlot] = list()
        for cd in (Coord(self.row + 1, self.col), Coord(self.row - 1, self.col),
                   Coord(self.row, self.col + 1), Coord(self.row, self.col - 1)):
            friend = self.grid.get_data_point(cd.row % (MAX_ROW + 1), cd.col % (MAX_COL + 1))
            if friend.value != "#":
                kids.append(GardenPlot(cd.row, cd.col, self.grid))

        return kids

    def eta(self, _=None) -> int:
        return 0

    def edge_cost(self, _) -> int:
        return 1

    def __str__(self):
        return f"({self.row},{self.col})"

    def __repr__(self):
        return str(self)


def is_valid_plot_point(num_steps_to_get_there: int, unarity: int, max_num_steps):
    return num_steps_to_get_there <= max_num_steps and num_steps_to_get_there % 2 == unarity


def main(num_plots=64):
    global MAX_ROW, MAX_COL
    file = open("day_21_input.txt", 'r')
    start = None
    grid = Grid()

    # read the input data and save it in grid
    for row, line in enumerate(map(str.rstrip, file)):
        for col, c in enumerate(line):
            grid.set_value(Coord(row, col, c))
            if c == "S":
                start = GardenPlot(row, col, grid)

    # define some variables
    min_grid_multiplier = 2
    MAX_COL = grid.max_col()
    MAX_ROW = grid.max_row()
    area_height = MAX_ROW + 1
    num_areas = num_plots // (2 * area_height)
    remainder = num_plots % (2 * area_height)

    # use dijkstra to get all the possible nodes
    # ... minimize the search by using the grid multiplier if necessary
    astar = AStar(start)
    if num_areas <= min_grid_multiplier:
        num_plots_to_astar = num_plots
    else:
        num_plots_to_astar = min_grid_multiplier * 2 * area_height + remainder

    astar.max_cost = num_plots_to_astar + 1
    astar.find_all()

    # get sum for all rows of areas (area being a 2x2 of original data)
    row_sum = dict()
    total_sum = 0
    centre_sum = 0
    for node in astar.all_nodes.values():
        dijkstra_obj = node.obj
        area_row = dijkstra_obj.row // (2 * area_height)
        area_col = dijkstra_obj.col // (2 * area_height)

        if is_valid_plot_point(node.cumulative_cost, num_plots % 2, num_plots_to_astar):
            if area_row == 0 and area_col == 0:
                centre_sum += 1
            if area_row not in row_sum:
                row_sum[area_row] = 0
            row_sum[area_row] += 1
            total_sum += 1

    # find solution for bigger areas
    n = (num_plots - remainder) // 2 // area_height - min_grid_multiplier
    if n < 0:
        print(f"{num_plots=}: {total_sum=}")
    else:
        total_sum += n * (row_sum[-1] + row_sum[+1] + 2 * centre_sum) + \
                     2 * centre_sum * n * (n + 1)
        print(f"{num_plots=}: {total_sum=}")


if __name__ == "__main__":
    main(64)
    main(26501365)
