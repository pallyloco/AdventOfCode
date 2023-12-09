def main(part: int = 1):
    file = open("day_09_input.txt", 'r')
    ans1 = 0
    ans2 = 0
    for line in map(str.rstrip, file):
        result = [list(map(int, line.split()))]
        find_diff_last(result)
        fr = find_diff_beginning(result)

        # add up all the end bits to get the last number
        for i in range(len(result) - 2, -1, -1):
            add = result[i + 1][-1]
            result[i].append(add + result[i][-1])
        ans1 = ans1 + result[0][-1]

        # add up all the beginning bits to get the first number
        for i in range(len(result) - 2, -1, -1):
            add = fr[i + 1][0]
            fr[i].insert(0, -add + fr[i][0])

        ans2 = ans2 + fr[0][0]
    print("Part 1:", ans1)
    print("Part 2:", ans2)


def find_diff_beginning(result: list[list[int]]) -> list[list[int]]:
    len_r = len(result)
    a = result[0][:len_r]
    b = a[1:]
    r: list[list[int]] = [a]
    while len(b):
        r.append([x - y for x, y in zip(b, a)])
        a = r[-1]
        b = a[1:]
    return r


def find_diff_last(result: list[list[int, int]]):
    # get the difference of the last two numbers
    diff = result[-1][-1] - result[-1][-2]
    result.append([diff])
    if result[-1][-1] == 0:
        return

    # cascade down the next set of differences from top to bottom of result list
    len_r = len(result)
    for i in range(1, len_r):
        result[i].insert(0, result[i - 1][-(1 + len_r - i)] - result[i - 1][-(2 + len_r - i)])
    find_diff_last(result)


if __name__ == "__main__":
    main()
