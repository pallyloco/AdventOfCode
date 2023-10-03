from typing import *
"""
Due to the local geology, trees in this area only grow on exact integer coordinates in a grid. You make a map
(your puzzle input) of the open squares (.) and trees (#) you can see.

These aren't the only trees, though; due to something you read about once involving arboreal genetics and biome
stability, the same pattern repeats to the right many times:

You start on the open square (.) in the top-left corner and need to reach the bottom (below the bottom-most row on your map).

The toboggan can only follow a few specific slopes (you opted for a cheaper model that prefers rational numbers);
start by counting all the trees you would encounter for the slope right 3, down 1:

From your starting position at the top-left, check the position that is right 3 and down 1.
Then, check the position that is right 3 and down 1 from there, and so on until you go past the bottom of the map.

Starting at the top-left corner of your map and following a slope of right 3 and down 1, how many trees would you encounter?

Time to check the rest of the slopes - you need to minimize the probability of a sudden arboreal stop, after all.

Determine the number of trees you would encounter if, for each of the following slopes, you start at the top-left corner
and traverse the map all the way to the bottom:

Right 1, down 1.
Right 3, down 1. (This is the slope you already checked.)
Right 5, down 1.
Right 7, down 1.
Right 1, down 2.
In the above example, these slopes would find 2, 7, 3, 4, and 2 tree(s) respectively; multiplied together, these produce the answer 336.

What do you get if you multiply together the number of trees encountered on each of the listed slopes?

"""
def main(part: int = 1 ):
    slopes: list[tuple[int,int]] = [(1,1), (3,1), (5,1), (7,1), (1,2)]
    answer = 1
    for slope in slopes:
        file = open('day3_input.txt', 'r')
        num_trees = 0
        col = 0
        dcol, drow = slope

        for line_number, line in enumerate(map(str.rstrip, file)):
            if not line_number%drow: 
                if line[col] == "#":
                    num_trees += 1
                col = (col+dcol) % len(line)

        print ("with slope",slope,"bumped into", num_trees, "trees")
        answer = answer * num_trees
    print ("multiplying slopes is:", answer)

if __name__ == '__main__':
    main(2)

