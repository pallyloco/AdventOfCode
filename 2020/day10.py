"""
Its battery is dead.

You'll need to plug it in. There's only one problem: the charging outlet near your seat
produces the wrong number of jolts. Always prepared, you make a list of all of the
joltage adapters in your bag.

Each of your joltage adapters is rated for a specific output joltage (your puzzle input).
Any given adapter can take an input 1, 2, or 3 jolts lower than its rating and still produce
its rated output joltage.

In addition, your device has a built-in joltage adapter rated for 3 jolts higher than the
highest-rated adapter in your bag.
(If your adapter list were 3, 9, and 6, your device's built-in adapter would be rated for 12 jolts.)

Treat the charging outlet near your seat as having an effective joltage rating of 0.

Since you have some time to kill, you might as well test all of your adapters.
Wouldn't want to get to your resort and realize you can't even charge your device!

If you use every adapter in your bag at once, what is the distribution of joltage differences
between the charging outlet, the adapters, and your device?

"""


def main(part: int = 1):
    file = open('day10_input.txt', 'r')
    one_jolt = 0
    three_jolt = 0
    adapters: list[int] = list()
    adapters.append(0)
    for line in map(int, map(str.rstrip, file)):
        adapters.append(line)

    """
    Find a chain that uses all of your adapters to connect the charging outlet to your
    device's built-in adapter and count the joltage differences between the charging outlet,
    the adapters, and your device.

    What is the number of 1-jolt differences multiplied by the number of 3-jolt differences?
    
    What is the total number of distinct ways you can arrange the adapters to connect 
    the charging outlet to your device?
    """

    adapters.sort()
    adapters.append(adapters[-1] + 3)

    arrangements = 1
    """this dictionary defines the total number of combinations for a given number
    of integers, with 1 'joltage' between each integer
    """
    d = {1: 1, 2: 2, 3: 4, 4: 7, 5: 13, 6: 24, 7: 44, 8: 81, 9: 149, 10: 274}

    """
    This list 'series' keeps track of all series of integers with incremented
    by 1 'joltage'
    """
    series: list[int] = list()
    for index in range(len(adapters) - 1):
        diff = adapters[index + 1] - adapters[index]

        if diff == 1:
            one_jolt += 1
            series.append(adapters[index + 1])

        elif diff == 3:
            if series:
                arrangements = arrangements*d[len(series)]
                series.clear()
            three_jolt += 1

    print("number of 1j * 3j is:", one_jolt * (three_jolt + 1))
    print("number of different ways to arrange the adapters is: ",arrangements)


if __name__ == '__main__':
    main(1)
