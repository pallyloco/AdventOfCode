import sys


def calories_gen():
    with open('day1_input1.txt', 'r') as file:
        elf_total = 0
        for data in map(str.rstrip, file):
            if data:
                elf_total = elf_total + int(data)
            else:
                yield elf_total
                elf_total = 0


def main():
    calories = list(calories_gen())
    calories.sort()

    print(f"Day 1 answer is: {max(calories)}")
    print(f"Day 2 answer is: {sum(calories[-3:])}")


if __name__ == '__main__':
    main()

"""
DAY 1

The Elves take turns writing down the number of Calories contained by the various meals, 
snacks, rations, etc. that they've brought with them, one item per line. Each Elf separates 
their own inventory from the previous Elf's inventory (if any) by a blank line.

Find the Elf carrying the most Calories. How many total Calories is that Elf carrying?

Your puzzle answer was 71471.

DAY 2

The Elves would instead like to know the total Calories carried by the top three Elves 
carrying the most Calories. 

Find the top three Elves carrying the most Calories. How many Calories are those Elves carrying in total?

Your puzzle answer was 211189.

"""
