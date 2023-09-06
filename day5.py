from collections import deque
import re


def main(day):
    num_of_stacks = 10

    # initialize the stacks with no blocks
    stacks: list[deque] = list()
    for i in range(num_of_stacks):
        stacks.append(deque(list()))

    with open('day5_input.txt', 'r') as file:

        # --------------------------------------------------------------------
        # read file until we have the line giving the stack numbers
        # --------------------------------------------------------------------
        for line in file:
            if line[1:2] == "1":
                break

            # add blocks to the appropriate stacks
            for i in range(len(stacks)):
                index = 1 + 4 * i
                c = line[index:index + 1]
                if c != " " and c != "":
                    stacks[i].append(c)

        # --------------------------------------------------------------------
        # process the commands
        # --------------------------------------------------------------------
        for line in file:
            cmd = re.match(r'move (\d+) from (\d+) to (\d+)', line)
            if cmd:
                (amt, from_stack, to_stack) = map(int, cmd.groups())
                if day == 1:
                    for _ in range(amt):
                        stacks[to_stack - 1].appendleft(stacks[from_stack - 1].popleft())
                else:
                    stacks[to_stack - 1].extendleft(reversed(list(stacks[from_stack - 1])[0:amt]))
                    for _ in range(amt):
                        stacks[from_stack - 1].popleft()

        # --------------------------------------------------------------------
        # print results
        # --------------------------------------------------------------------
        for stack in stacks:
            if stack:
                print(stack[0], end="")
        print()


if __name__ == '__main__':
    main(1)
    main(2)

"""
Crates need to be rearranged.

The ship has a crane capable of moving crates between stacks. The crane operator will rearrange them 
in a series of steps. After the crates are rearranged, the desired crates will be at the top of each 
stack.

They have a drawing of the starting stacks of crates and the rearrangement procedure (your puzzle input). 
For example:

    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2

After the rearrangement procedure completes, what crate ends up on top of each stack?

Your puzzle answer was TGWSMRBPN.

--- Part Two ---

... new features: the ability to pick up and move multiple crates at once.

After the rearrangement procedure completes, what crate ends up on top of each stack?

Your puzzle answer was TZLTLWRNF.

"""
