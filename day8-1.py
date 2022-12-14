import re
trees = []
trees_horizontal = []
trees_vertical = []
visible_trees = []
visible_right = []
visible_left = []
visible_top = []
visible_bottom =[]

def main():
    file = open('day8_test_input.txt', 'r')
    while True:
        line = file.readline()
        line = line.rstrip()
        if not line: 
            break
        num_cols = len(line)
        trees.append(line.rstrip())
        visible_trees.append(visible_trees_horizontal(line.rstrip()))
    
    for column in range(num_cols):
        max_height = -1
        for row in range(len(visible_trees)):
            if int(trees[row][column]) > max_height:
                visible_trees[row][column] = 1
                max_height = int(trees[row][column])

    for column in range(num_cols):
        max_height = -1
        for row in range(len(visible_trees)-1,-1,-1):
            if int(trees[row][column]) > max_height:
                visible_trees[row][column] = 1
                max_height = int(trees[row][column])

    #for t in trees:
    #    print(t)
    #for v in visible_trees:
    #    print(v)
    # in C#  a[i][j]  is an array of arrays
    #        a[i,j] is a proper 2d array

    num_visible_trees = 0
    for column in range(num_cols):
        for row in range(len(visible_trees)):
            num_visible_trees += visible_trees[row][column]

    print (f"visible trees: {num_visible_trees}")

def visible_trees_horizontal(line):
    high_tree = -1
    visible_trees = []
    for tree_height in line:
        if int(tree_height) > high_tree:
            visible_trees.append(1)
            high_tree = int(tree_height)
        else:
            visible_trees.append(0)
    
    high_tree = -1
    reversed_trees = []
    for tree_height in reversed(line):
        if int(tree_height) > high_tree:
            reversed_trees.append(1)
            high_tree = int(tree_height)
        else:
            reversed_trees.append(0)

    reversed_trees = reversed(reversed_trees)
    return [i or j for i,j in zip(visible_trees,reversed_trees)]



# ===================================================================
# Entry point
# ===================================================================
if __name__ == '__main__':
    main()