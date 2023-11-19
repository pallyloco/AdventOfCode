from typing import Callable
import numpy as np
import math

"""
The navigation instructions (your puzzle input) consists of a sequence of single-character
actions paired with integer input values.

Action N means to move north by the given value.
Action S means to move south by the given value.
Action E means to move east by the given value.
Action W means to move west by the given value.
Action L means to turn left the given number of degrees.
Action R means to turn right the given number of degrees.
Action F means to move forward by the given value in the direction the ship is currently facing.

The ship starts by facing east. Only the L and R actions change the direction the ship is facing.
(That is, if the ship is facing east and the next instruction is N10,
the ship would move north 10 units, but would still move east if the following action were F.)

Figure out where the navigation instructions lead. What is the Manhattan distance
between that location and the ship's starting position?

--- Part Two ---
Before you can give the destination to the captain, you realize that the actual action 
meanings were printed on the back of the instructions the whole time.

Almost all of the actions indicate how to move a waypoint which is relative to the ship's position:

Action N means to move the waypoint north by the given value.
Action S means to move the waypoint south by the given value.
Action E means to move the waypoint east by the given value.
Action W means to move the waypoint west by the given value.
Action L means to rotate the waypoint around the ship left (counter-clockwise) the given number of degrees.
Action R means to rotate the waypoint around the ship right (clockwise) the given number of degrees.
Action F means to move forward to the waypoint a number of times equal to the given value.

The waypoint starts 10 units east and 1 unit north relative to the ship. 
The waypoint is relative to the ship; that is, if the ship moves, the waypoint moves with it.


"""
global way_point
way_point = (1, 0)


def rotate(pos, deg: int):
    global way_point
    rad = deg / 180. * math.pi
    r = np.array([[math.cos(rad), math.sin(rad)], [-math.sin(rad), math.cos(rad)]])
    n = np.matmul(r, np.array(way_point))
    way_point = tuple(map(round, n))
    return pos


def move_forward(pos, value: int):
    return tuple(np.add(pos, np.array(way_point) * value))


actions: dict[str, Callable[[str, tuple[int, int]], tuple[int, int]]] = dict()
actions['N'] = lambda pos, value: (pos[0], pos[1] + value)
actions['S'] = lambda pos, value: (pos[0], pos[1] - value)
actions['E'] = lambda pos, value: (pos[0] + value, pos[1])
actions['W'] = lambda pos, value: (pos[0] - value, pos[1])
actions['R'] = lambda pos, value: rotate(pos, value)
actions['L'] = lambda pos, value: rotate(pos, -value)
actions['F'] = lambda pos, value: move_forward(pos, value)


def main(part: int = 1):
    global way_point
    if part == 2:
        way_point = (10, 1)
    file = open('day12_input.txt', 'r')
    current_position = (0, 0)
    for input_thing in map(str.rstrip, file):
        action = input_thing[0]
        value = int(input_thing[1:])
        if part == 2 and action != 'F' and action != "R" and action != "L":
            way_point = actions[action](way_point, value)
        else:
            current_position = actions[action](current_position, value)
    print("answer is", math.fabs(current_position[0]) + math.fabs(current_position[1]))


if __name__ == "__main__":
    main(1)
    main(2)
