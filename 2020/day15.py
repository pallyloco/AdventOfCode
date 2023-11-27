"""
In this game, the players take turns saying numbers. They begin by taking turns reading from a list of
starting numbers (your puzzle input).

Then, each turn consists of considering the most recently spoken number:

If that was the first time the number has been spoken, the current player says 0.

Otherwise, the number had been spoken before; the current player announces how many turns apart
the number is from when it was previously spoken.

So, after the starting numbers, each turn results in that player speaking aloud either 0
(if the last number is new) or an age (if the last number is a repeat).

Their question for you is: what will be the 2020th number spoken? In the example above,
the 2020th number spoken will be 436.

"""

input = "19,0,5,1,10,13"


def main(part: int = 1):
    last_play = 30000000
    if part == 1:
        last_play = 2020
    numbers = list(map(int, input.split(",")))
    spoken_numbers = dict()
    repeat_pattern = list()
    for i in range(1, last_play + 1):
        if numbers:
            number = numbers.pop(0)
        born = spoken_numbers.get(number, i)
        spoken_numbers[number] = i
        if i == last_play:
            print(i, number)
        number = i - born


if __name__ == '__main__':
    main(1)
    main(2)
