import re
from dataclasses import dataclass
from time import sleep

from grid import Grid
from coord import Coord, Direction
from reading import read_paragraphs

#https://www.youtube.com/shorts/i2gHt6_xKKk

# input_data = [
#     "##########",
#     "#..O..O.O#",
#     "#......O.#",
#     "#.OO..O.O#",
#     "#..O@..O.#",
#     "#O#..O...#",
#     "#O..O..O.#",
#     "#.OO.O.OO#",
#     "#....O...#",
#     "##########",
#     "",
#     "<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^",
#     "vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v",
#     "><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<",
#     "<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^",
#     "^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><",
#     "^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^",
#     ">^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^",
#     "<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>",
#     "^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>",
#     "v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^",
# ]

# input_data = [
# "####################",
# "##[]..[]......[][]##",
# "##[]...........[].##",
# "##..........[].@[]##",
# "##............[]..##",
# "##..##[]..[].[][].##",
# "##...[]...[]..[]..##",
# "##.....[]..[].[][]##",
# "##........[]......##",
# "####################",
# "",
# "vvvv"
# ]


fh = open("day_15.txt", "r")
input_data = list(map(str.rstrip, fh))

def main(data):
    map_data, movement_data = [d for d in read_paragraphs(data)]
    warehouse, warehouse2, robot, robot2 = read_map(map_data)
    print(warehouse2)

    direction_symbols = {"^": Direction.NORTH, "<": Direction.WEST, "v": Direction.SOUTH, ">": Direction.EAST}
    movements = "".join(movement_data)
    for i, movement in enumerate(movements):
        print()
        print(movement)
        robot2.value = movement
        robot.direction = direction_symbols[movement]
        move(robot, warehouse)
        robot2.direction = direction_symbols[movement]
        move2(robot2, warehouse2)
        print(warehouse2)
        # robot.direction = direction_symbols[movement]
        # move2(robot, warehouse)
        # print(warehouse)
    #print(warehouse)
    print(warehouse2)
    gps_sum = 0
    gps_sum2 = 0
    for cell in warehouse.data:
        if cell.value == "O":
            gps_sum += 100 * cell.row + cell.col
    print(gps_sum)
    for cell in warehouse2.data:
        if cell.value == "[":
            gps_sum2 += 100 * cell.row + cell.col
    print(gps_sum2)


def move2(robot, warehouse):
    spot = warehouse.get_forward_cell(robot)
    if spot is None:
        warehouse.remove_data_point(robot.row, robot.col)
        robot.move(1)
        warehouse.set_value(robot)
    elif spot.value == "#":
        return
    elif spot.value == "[" or spot.value == "]":
        if can_move_box2(spot, robot.direction, warehouse):
            warehouse.remove_data_point(robot.row, robot.col)
            robot.move(1)
            warehouse.set_value(robot)


def can_move_box2(box, direction, warehouse) -> bool:
    if direction == Direction.WEST or direction == Direction.EAST:
        return can_move_wide_box_horizontal(box, direction, warehouse)
    else:
        return move_wide_box_vertical(box, direction, warehouse)


def move_wide_box_vertical(box: Coord, direction, warehouse: Grid):
    boxes_to_move = []
    reverse_direction = False if direction == Direction.NORTH else True
    if can_move_wide_box_vertical(box, direction, warehouse, boxes_to_move):
        sign = -1 if direction == Direction.NORTH else 1
        for box in sorted(boxes_to_move, key=lambda x: (x.row, x.col), reverse=reverse_direction):
            warehouse.remove_data_point(box.row, box.col)
            warehouse.set_value(Coord(box.row + sign, box.col, box.value))
            #print(warehouse)
        return True
    else:
        return False


def can_move_wide_box_vertical(box: Coord, direction: Direction, warehouse: Grid, boxes_to_move: list[Coord]):
    box2 = warehouse.get_data_point(box.row, box.col - 1) if box.value == "]" \
        else warehouse.get_data_point(box.row, box.col + 1)
    row, col = box.row, box.col
    boxes_to_move.append(box)
    boxes_to_move.append(box2)

    row = row + direction.value[0]
    next1 = warehouse.get_data_point(row, box.col)
    next2 = warehouse.get_data_point(row, box2.col)
    if next1 is None and next2 is None:
        return True
    if (next1 is not None and next1.value == "#") or (next2 is not None and next2.value == "#"):
        return False

    if next1 is not None:
        result1 = can_move_wide_box_vertical(next1, direction, warehouse, boxes_to_move)
        if not result1:
            return False
    if next2 is not None:
        result2 = can_move_wide_box_vertical(next2, direction, warehouse, boxes_to_move)
        if not result2:
            return False
    return True


def can_move_wide_box_horizontal(box, direction, warehouse):
    row, col = box.row, box.col

    for _ in range(100000):  # while True
        row, col = row + direction.value[0], col + direction.value[1]
        cell = warehouse.get_data_point(row, col)
        if cell is None:
            horizontal_box_shift(box, col, direction, warehouse)
            return True
        if cell.value == "#":
            return False


def horizontal_box_shift(box, final_col, direction, warehouse):
    sign = 1 if direction == Direction.WEST else -1
    for col in range(final_col, box.col, sign):
        value = warehouse.get_data_point(box.row, col + sign).value
        warehouse.set_value(Coord(box.row, col, value))
    warehouse.remove_data_point(box.row, box.col)


def move(robot, warehouse):
    spot = warehouse.get_forward_cell(robot)
    if spot is None:
        warehouse.remove_data_point(robot.row, robot.col)
        robot.move(1)
        warehouse.set_value(robot)
    elif spot.value == "#":
        return
    elif spot.value == "O":
        if can_move_box(spot, robot.direction, warehouse):
            warehouse.remove_data_point(robot.row, robot.col)
            robot.move(1)
            warehouse.set_value(robot)


def can_move_box(box, direction, warehouse) -> bool:
    row, col = box.row, box.col
    for _ in range(100000):
        row, col = row + direction.value[0], col + direction.value[1]
        cell = warehouse.get_data_point(row, col)
        if cell is None:
            warehouse.remove_data_point(box.row, box.col)
            warehouse.set_value(Coord(row, col, box.value))
            return True
        if cell.value == "#":
            return False


def read_map(data) -> tuple[Grid, Grid, Coord, Coord]:
    warehouse = Grid()
    warehouse2 = Grid()
    robot = Coord(0, 0)
    robot2 = Coord(0, 0)
    for row, line in enumerate(data):
        for col, value in enumerate(line):
            wide_col = 2 * col
            if value != "." and value != "@":
                warehouse.set_value(Coord(row, col, value))
                if value == "O":
                    warehouse2.set_value(Coord(row, wide_col, "["))
                    warehouse2.set_value(Coord(row, wide_col + 1, "]"))
                if value == "#":
                    warehouse2.set_value(Coord(row, wide_col, "#"))
                    warehouse2.set_value(Coord(row, wide_col + 1, "#"))
            if value == "@":
                robot = Coord(row, col, "@")
                robot2 = Coord(row, wide_col, "@")
    return warehouse, warehouse2, robot, robot2


main(input_data)
