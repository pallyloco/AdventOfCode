data = [
    "MMMSXXMASM",
    "MSAMXMSMSA",
    "AMXSXMAAMM",
    "MSAMASMSMX",
    "XMASAMXAMM",
    "XXAMMXXAMA",
    "SMSMSASXSS",
    "SAXAMASAAA",
    "MAMMMXMMMM",
    "MXMXAXMASX",
]

fh = open("day_04.txt", "r")
lines = [line.rstrip() for line in fh]
this_data = lines


HEIGHT = len(this_data)
WIDTH = len(this_data[0])
print (WIDTH,HEIGHT)


def main():
    total = 0
    for row, col in x_coordinates(HEIGHT, WIDTH, "X", this_data):
        for s in get_string(row, col):
            if s == "XMAS":
                total = total + 1
    print(total)

    # part 2
    total = 0
    for row, col in x_coordinates(HEIGHT, WIDTH, "A", this_data):
        if row == 0 or row == HEIGHT - 1:
            continue
        if col == 0 or col == WIDTH - 1:
            continue
        pass
        total += xmases(row, col, this_data)
    print(total)


def x_coordinates(height, width, symbol, data):
    for col in range(width):
        for row in range(height):
            if data[row][col] == symbol:
                yield row, col


def xmases(row, col, data):
    # four strings
    s3 = data[row - 1][col - 1] + "A" + data[row + 1][col + 1]
    s4 = data[row - 1][col + 1] + "A" + data[row + 1][col - 1]
    if (s3 == "MAS" or s3 == "SAM") and (s4 == "SAM" or s4 == "MAS"):
        return 1
    return 0


def neighbours(row, col, size, width, height):
    down = [row + i for i in range(size)]
    up = [row - i for i in range(size)]
    right = [col + i for i in range(size)]
    left = [col - i for i in range(size)]
    result = []
    if all(a < height for a in down):
        result.append((down, [col for _ in down]))
    if all(a >= 0 for a in up):
        result.append((up, [col for _ in down]))
    if all(a < width for a in right):
        result.append(([row for _ in right], right))
    if all(a >= 0 for a in left):
        result.append(([row for _ in right], left))
    if all(a >= 0 for a in left) and all(a >= 0 for a in up):
        result.append((up, left))
    if all(a < width for a in right) and all(a >= 0 for a in up):
        result.append((up, right))
    if all(a >= 0 for a in left) and all(a < height for a in down):
        result.append((down, left))
    if all(a < width for a in right) and all(a < height for a in down):
        result.append((down, right))
    for r in result:
        yield r


def get_string(i_row: int, i_col: int):
    for rows, cols in neighbours(i_row, i_col, size=4, height=HEIGHT, width=WIDTH):
        s = ""
        for row, col in zip(rows, cols):
            s += this_data[row][col]
        yield s


main()
