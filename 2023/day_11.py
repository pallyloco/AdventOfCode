import itertools as it


def main(part: int = 1):
    if part == 1:
        expand = 2 - 1
    else:
        expand = 1_000_000 - 1

    galaxies: list[tuple[int, int]] = list()
    file = open("day_11_input.txt", 'r')
    expanding_horizontal = list()
    expanding_vertical = list()
    lines: list[str] = list()

    # parse the input
    for row, line in enumerate(map(str.rstrip, file)):
        lines.append(line)
        if len(expanding_vertical) == 0:
            expanding_vertical = [True] * len(line)
        expanding_vertical = [a and b == "." for b, a in zip(line, expanding_vertical)]
        expanding_horizontal.append(all(a == "." for a in line))

    # find and save the galaxy locations
    expansion_row = 0
    for row, line in enumerate(lines):
        if expanding_horizontal[row]:
            expansion_row += expand
        expansion_col = 0
        for col, c in enumerate(line):
            if expanding_vertical[col]:
                expansion_col += expand
            if c == "#":
                galaxies.append((row + expansion_row, col + expansion_col))

    # calculate all distances between pairs
    ans1 = 0
    for pair in it.combinations(galaxies, 2):
        d = abs(pair[0][0] - pair[1][0]) + abs(pair[0][1] - pair[1][1])
        ans1 += d
    print("Answer 1:", ans1)


if __name__ == "__main__":
    main(1)
    main(2)
