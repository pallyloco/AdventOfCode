def main(part: int = 1):
    file = open("day_09_input.txt", 'r')
    ans1 = 0
    ans2 = 0
    for line in map(str.rstrip, file):
        data = list(map(int, line.split()))
        result = find_diff(data)

        # add up all the end bits to get the last number
        for i in range(len(result) - 2, -1, -1):
            minus = result[i + 1][0]
            add = result[i + 1][-1]
            result[i].append(add + result[i][-1])
            result[i].insert(0, result[i][0] - minus)
        ans1 = ans1 + result[0][-1]
        ans2 = ans2 + result[0][0]
    print("Part 1:", ans1)
    print("Part 2:", ans2)


def find_diff(data: list[int, int], diffs=None):
    if diffs is None:
        diffs = list()
    diffs.append(data)
    if all((a == 0 for a in diffs[-1])):
        return diffs
    return find_diff([b - a for a, b in zip(data, data[1:])], diffs)


if __name__ == "__main__":
    main()
