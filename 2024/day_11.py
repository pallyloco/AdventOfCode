from __future__ import annotations

from dataclasses import dataclass

input_data = "125 17"
input_data = "28591 78 0 3159881 4254 524155 598 1"
number_blinks = 75
TOTAL = 0


# Note... in spite of instructions, do not need to keep order of all the stones.


class Node:
    def __init__(self, number, blinked=0, right_node=None, factor=1):
        self.right: Node = right_node
        self.value = number
        self.blinked = blinked
        self.factor = factor

    def __str__(self):
        return f"({self.factor:1d}) blinked-{self.blinked:2d} [{self.value:10d}] "

    def __repr__(self):
        return str(self)


def main3(data):
    stones = map(int, input_data.split())
    stones_dict: dict[int: Node] = {s: Node(s, factor=1) for s in stones}

    for _ in range(number_blinks):
        answer_dict = {}
        for s in stones_dict.values():
            process_node(s)

            for result_stone in walk_stones(s):
                answer_dict[result_stone.value] = answer_dict.get(result_stone.value, 0) + result_stone.factor

        stones_dict: dict[int: Node] = {key: Node(key, factor=value) for key, value in answer_dict.items()}

    print(sum((value for value in answer_dict.values())))


def walk_stones(stone: Node):
    current_stone = stone
    yield current_stone
    while current_stone.right is not None:
        current_stone = current_stone.right
        yield current_stone


def process_node(stone: Node):
    #    print(stone)
    digits = str(stone.value)
    if stone.blinked == 1:
        return
    stone.blinked += 1

    # If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
    if stone.value == 0:
        stone.value = 1
        process_node(stone)

    # If the stone is engraved with a number that has an even number of digits, it is replaced by two stones.
    # The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved
    # on the new right stone.
    # (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
    elif len(digits) % 2 == 0:
        left, right = int(digits[:len(digits) // 2]), int(digits[len(digits) // 2:])
        right_node = stone.right
        stone.value = left
        new_node = Node(right, blinked=stone.blinked, right_node=right_node, factor=stone.factor)
        stone.right = new_node

        process_node(stone)
        process_node(new_node)

    # If none of the other rules apply, the stone is replaced by a new stone;
    # the old stone's number multiplied by 2024 is engraved on the new stone.
    else:
        stone.value = stone.value * 2024
        process_node(stone)


main3(input_data)
