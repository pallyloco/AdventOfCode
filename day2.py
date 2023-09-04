# Day2-1.py
from enum import Enum


class Me(Enum):
    X = 0
    Y = 1
    Z = 2


class Her(Enum):
    A = 0
    B = 1
    C = 2


def main(day: int):
    score = 0
    with open('day2_input.txt', 'r') as file:
        for line in map(str.rstrip, file):
            hers, mine = line.split(" ")
            her_play = Her[hers].value

            if day == 1:
                my_play = Me[mine].value
            else:
                offset = (Me[mine].value + 2) % 3
                my_play = (her_play + offset) % 3

            score += 3 * ((my_play - her_play + 1) % 3)
            score = score + my_play + 1

        print(f"final score is: {score}")


if __name__ == '__main__':
    main(1)
    main(2)

"""
DAY 1

One Elf gives you an encrypted strategy guide (your puzzle input) that they say will be 
sure to help you win. 

The first column is what your opponent is going to play: 
A for Rock, 
B for Paper, and 
C for Scissors. 

The second column must be what you should play in response: 
X for Rock, 
Y for Paper, and 
Z for Scissors. 

Your total score is the sum of your scores for each round. 
The score for a single round is the score for the shape you selected 
    (1 for Rock, 2 for Paper, and 3 for Scissors) 
plus the score for the outcome of the round 
    (0 if you lost, 3 if the round was a draw, and 6 if you won).

What would your total score be if everything goes exactly according to your strategy guide?

Your puzzle answer was 13268

DAY 2

The Elf says "Anyway, the second column says how the round needs to end: 
    X means you need to lose, 
    Y means you need to end the round in a draw, and 
    Z means you need to win. Good luck!"

The total score is still calculated in the same way, but now you need to figure out what shape to 
choose so the round ends as indicated. 

What would your total score be if everything goes exactly according to your strategy guide?

Your puzzle answer was 15508.

"""
