from collections import deque

"""
Upon connection, the port outputs a series of numbers (your puzzle input).

The data appears to be encrypted with the eXchange-Masking Addition System (XMAS) which, 
conveniently for you, is an old cypher with an important weakness.

XMAS starts by transmitting a preamble of 25 numbers. 
After that, each number you receive should be the sum of any two of the 25 immediately previous numbers. 
The two numbers will have different values, and there might be more than one such pair.

The first step of attacking the weakness in the XMAS data is to find the first number in the list 
(after the preamble) which is not the sum of two of the 25 numbers before it. 

What is the first number that does not have this property?

Your puzzle answer was 1038347917.

--- Part Two ---
The final step in breaking the XMAS encryption relies on the invalid number you just found: 
you must find a contiguous set of at least two numbers in your list which sum to the 
invalid number from step 1.

To find the encryption weakness, add together the smallest and largest number in this 
contiguous range

What is the encryption weakness in your XMAS-encrypted list of numbers?

Your puzzle answer was 137394018.

"""
key_length = 25
inputs = list()


def main(part: int = 1):
    file = open('day9_input.txt', 'r')
    invalid = 0
    deck = deque()
    for line in map(int, map(str.rstrip, file)):
        inputs.append(line)
        if not invalid:
            if len(deck) < key_length:
                deck.append(line)
                continue

            if len(deck) > key_length:
                deck.popleft()

            if not is_valid(line, deck):
                print("found invalid", line)
                invalid = line

        deck.append(line)

    # find weakness
    for i in range(len(inputs) - 1):
        total = inputs[i]
        lowest = total
        highest = total
        for j in range(i + 1, len(inputs)):
            total = total + inputs[j]
            lowest = min(lowest, inputs[j])
            highest = max(highest, inputs[j])
            if total > invalid:
                break
            if total == invalid:
                print(lowest + highest)
                exit


def is_valid(num: int, deck: deque[int]):
    for i in range(0, key_length - 1):
        for j in range(i + 1, key_length):
            x = deck[i]
            y = deck[j]
            if deck[i] + deck[j] == num:
                return True
    return False


if __name__ == '__main__':
    main(1)
