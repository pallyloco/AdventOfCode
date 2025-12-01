# For your imports look at the rulebook to see what is allowed
# Pour les import permis allez vous référer au livre des règlements
"""part_2.py
This is the template file for the part 2 of the Prelim 2.
Ceci est le fichier template pour la partie 2 du Prelim 2.
"""

def part_2(grid: list[list[str]], word: str):
    """
    Place the world on the Scrabble grid

    Parameters:
        grid [str]: The 10X10 scrabble's grid
        word str: The word to place on the grid

    Returns:
        [str]: The new scrabble's grid with the world place in it
    """
    new_grid = []
    ### You code goes here ###
    ### Votre code va ici ###


    # dictionary of characters to position
    chr_to_location: dict[str: list[tuple[int,int]]] = {}
    for row,line in enumerate(grid):
        for col, char in enumerate(line):
            if char !="" :
                chr_to_location[char] = [] if char not in chr_to_location else chr_to_location[char]
                chr_to_location[char].append(row,col)

    # go though letters in word
    for index,c in enumerate(word):
        if c in chr_to_location.keys():
            n = check(c, index, word, chr_to_location)

    return new_grid

def does_fit(start_index, direction, word, chr_to_location):
    pass

def check(c, index, word, chr_to_location):

    maxs = 0
    for matched_row, matched_col in chr_to_location[c]:

        # up
        first_row = matched_row - index


        # down
        # right
        # left
