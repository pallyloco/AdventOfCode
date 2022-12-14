import itertools
import functools

def chunks(iter, size):
    x = [0 for i in range(size)]
    for element, index in zip(iter, itertools.cycle(range(size))):
        element = element.rstrip()
        x[index] = element
        if (index == size-1):
            yield x

def main():
#Lowercase item types a through z have priorities 1 through 26.
#Uppercase item types A through Z have priorities 27 through 52.
#Look for common item in all three groups
    chunk_size = 3
    score = 0
    with open('day3_input.txt', 'r') as file:
        for rucksacks_line in chunks(map(str.rstrip, file), chunk_size):
            rucksacks = map(set, rucksacks_line)
            score = score + find_badge_score(rucksacks)

        print (f"score is {score}")

def find_badge_score (rucksacks):
    result = functools.reduce(set.intersection,rucksacks)
    c, *_ = result

    if c.isupper():
        return ord(c) - ord("A") + 27
        # print (f"add score  {ord(c) - ord('A') + 27}")
    else:
        return ord(c) - ord("a") + 1
        # print (f"add score {ord(c) - ord('a') + 1}")
    # return score        


if __name__ == '__main__':
    main()