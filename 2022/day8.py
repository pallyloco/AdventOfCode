import itertools
from collections.abc import Iterable

trees: list[list[int]] = list()


def main():
    """
    The expedition comes across a peculiar patch of tall trees all planted carefully in a grid.

    You need to count the number of trees that are visible from outside the grid when looking
    directly along a row or column.

    The Elves have already launched a quadcopter to generate a map with the height of each tree
    (your puzzle input). For example:

    30373
    25512
    65332
    33549
    35390

    Each tree is represented as a single digit whose value is its height, where 0 is the shortest
    and 9 is the tallest.

    """

    file = open('day8_input.txt', 'r')

    # create a 2d map (lists of lists
    for line in map(str.rstrip, file):
        numbers: list[int] = [n for n in map(int, (line[i] for i in range(len(line))))]
        trees.append(numbers)

    num_rows = len(trees)
    num_cols = len(trees[0])

    """
    A tree is visible if all of the other trees between it and an edge of the grid are shorter than it.
    Only consider trees in the same row or column; that is, only look up, down, left, or right from any
    given tree.

    All of the trees around the edge of the grid are visible - since they are already on the edge, 
    there are no trees to block the view. 

    Consider your map; how many trees are visible from outside the grid?

    Your puzzle answer was 1676.

    --- Part Two ---
    Content with the amount of tree cover available, the Elves just need to know the best spot to 
    build their tree house: they would like to be able to see a lot of trees.

    To measure the viewing distance from a given tree, look up, down, left, and right from that tree; 
    stop if you reach an edge or at the first tree that is the same height or taller than the tree 
    under consideration. (If a tree is right on the edge, at least one of its viewing distances will be zero.)

    The Elves don't care about distant trees taller than those found by the rules above; 

    A tree's scenic score is found by multiplying together its viewing distance in each of the four directions. 

    Consider each tree on your map. What is the highest scenic score possible for any tree?

    Your puzzle answer was 313200.
    """

    max_visible_trees = 0
    max_view = 0
    for row in range(num_rows):
        for col in range(num_cols):
            tree_height = trees[row][col]
            data_right = [trees[row][c] for c in range(col + 1, num_cols)]
            data_left = [trees[row][c] for c in range(col - 1, -1, -1)]
            data_up = [trees[r][col] for r in range(row + 1, num_rows)]
            data_down = [trees[r][col] for r in range(row - 1, -1, -1)]

            # part 1
            if see_from_outside(tree_height, data_right) or \
                    see_from_outside(tree_height, data_left) or \
                    see_from_outside(tree_height, data_up) or \
                    see_from_outside(tree_height, data_down):
                max_visible_trees += 1

            # part 2
            dr = tree_top_view_distance(tree_height, data_right)
            dl = tree_top_view_distance(tree_height, data_left)
            dd = tree_top_view_distance(tree_height, data_down)
            du = tree_top_view_distance(tree_height, data_up)
            max_view = max(dr * dl * du * dd, max_view)

    print(f"Max trees visible from outside: {max_visible_trees}")
    print(f"Max view is: {max_view}")


def see_from_outside(tree_height: int, data: list[int]) -> bool:
    blocking_tree = next(
        (height for height in data if tree_height <= height), -1
    )
    return blocking_tree == -1


def tree_top_view_distance(treehouse_height: int, data: list[int]) -> int:
    if not data:
        return 0
    number = 0
    for number, tree_height in enumerate(data):
        if tree_height >= treehouse_height:
            return number + 1
    return number + 1


# ===================================================================
# Entry point
# ===================================================================
if __name__ == '__main__':
    main()
