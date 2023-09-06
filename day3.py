import itertools
import functools


def read_n_lines_at_a_time(file, n) -> list[str]:
    lines: list[str] = list()
    for counter, line in enumerate(map(str.rstrip, file)):
        lines.append(line)
        if (counter + 1) % n == 0:
            yield lines
            lines.clear()


def main(day):
    score = 0
    if day == 1:
        num_of_lines = 1
    else:
        num_of_lines = 3

    with open('day3_input.txt', 'r') as file:
        for lines in read_n_lines_at_a_time(file, num_of_lines):

            if day == 1:
                line: str = lines[0]
                length = len(line) // 2
                first = set(line[0:length])
                last = set(line[length:])

                result = first.intersection(last)
            else:
                rucksacks = map(set, lines)
                result = functools.reduce(set.intersection, rucksacks)

            if result:
                c, *_ = result
                if c.isupper():
                    score = score + ord(c) - ord("A") + 27
                else:
                    score = score + ord(c) - ord("a") + 1

        print(f"score is {score}")


if __name__ == '__main__':
    main(1)
    main(2)

"""
Each rucksack has two large compartments. 
All items of a given type are meant to go into exactly one of the two compartments. 
The Elf that did the packing failed to follow this rule for exactly one item type per rucksack.

The Elves have made a list of all of the items currently in each rucksack (your puzzle input), 
but they need your help finding the errors. 
Every item type is identified by a single lowercase or uppercase letter 
(that is, a and A refer to different types of items).

The list of items for each rucksack is given as characters all on a single line. 
A given rucksack always has the same number of items in each of its two compartments, 
so the first half of the characters represent items in the first compartment, 
while the second half of the characters represent items in the second compartment.

To help prioritize item rearrangement, every item type can be converted to a priority:

Lowercase item types a through z have priorities 1 through 26.
Uppercase item types A through Z have priorities 27 through 52.

Find the item type that appears in both compartments of each rucksack. 
What is the sum of the priorities of those item types?

Your puzzle answer was 7990.

--- Part Two ---
For safety, the Elves are divided into groups of three. 
Every Elf carries a badge that identifies their group. For efficiency, within each group of three Elves, 
the badge is the only item type carried by all three Elves. 
That is, if a group's badge is item type B, then all three Elves will have item type B 
somewhere in their rucksack, and at most two of the Elves will be carrying any other item type.

The problem is that someone forgot to put this year's updated authenticity sticker on the badges. 
All of the badges need to be pulled out of the rucksacks so the new authenticity stickers can be attached.

Additionally, nobody wrote down which item type corresponds to each group's badges. 
The only way to tell which item type is the right one is by finding the one item type that 
is common between all three Elves in each group.

Every set of three lines in your list corresponds to a single group, but each group can have a 
different badge item type. 

Priorities for these items must still be found to organize the sticker attachment efforts: 

Find the item type that corresponds to the badges of each three-Elf group. 
What is the sum of the priorities of those item types?

Your puzzle answer was 2602.
"""
