"""
--- Day 14: Docking Data ---
The initialization program (your puzzle input) can either update the bitmask or write a value to memory.

Example
    mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
    mem[8] = 11
    mem[7] = 101
    mem[8] = 0

Values and memory addresses are both 36-bit unsigned integers.
For example, ignoring bitmasks for a moment, a line like mem[8] = 11 would write the value 11 t
o memory address 8.

The bitmask is always given as a string of 36 bits, written with the most significant bit
(representing 2^35) on the left and the least significant bit (2^0, that is, the 1s bit) on the right.
The current bitmask is applied to values immediately before they are written to memory:
a 0 or 1 overwrites the corresponding bit in the value, while an X leaves the bit in the value unchanged.

To initialize your ferry's docking program, you need the sum of all values left in memory after
the initialization program completes.
(The entire 36-bit address space begins initialized to the value 0 at every address.)

What is the sum of all values left in memory after it completes? (Do not truncate the sum to 36 bits.)

========== Part 2
If the bitmask bit is 0, the corresponding memory address bit is unchanged.
If the bitmask bit is 1, the corresponding memory address bit is overwritten with 1.
If the bitmask bit is X, the corresponding memory address bit is floating.
"""


def main(part: int = 1):
    file = open("day14_input.txt", "r")
    mask = "X" * 36

    memory: dict[int, int] = dict()
    for line in map(str.rstrip, file):
        command, value = line.split(" = ")
        if command == "mask":
            mask = value

        elif command[0:3] == "mem":
            index = int(command[4:-1])
            num = int(value)
            if part == 1:
                part1(index, mask, num, memory)
            else:
                part2(index, mask, num, memory)

    ans = sum(memory.values())
    print(ans)


def part1(index, mask, num, memory):
    num_str = "{0:b}".format(num).zfill(36)
    new_str = ""
    for n, m in zip(num_str, mask):
        if m == 'X':
            new_str = new_str + n
        else:
            new_str = new_str + m
    memory[index] = int("0b" + new_str, 2)


def part2(index, mask, num, memory):
    index_str = "{0:b}".format(index).zfill(36)
    new_str = ""
    for i, m in zip(index_str, mask):
        if m == 'X':
            new_str = new_str + 'X'
        else:
            new_str = new_str + str(int(i) | int(m))
    floating(new_str, num, memory)


def floating(mem_index_str, num, memory):
    if "X" in mem_index_str:
        floating(mem_index_str.replace("X", "0", 1), num, memory)
        floating(mem_index_str.replace("X", "1", 1), num, memory)
    else:
        memory[int(mem_index_str)] = num


if __name__ == "__main__":
    main(1)
    main(2)
