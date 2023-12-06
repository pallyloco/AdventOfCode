import math

# input_str: list[str] = ["Time:      7  15   30", "Distance:  9  40  200"]
input_str: list[str] = ["Time:        50     74     86     85", "Distance:   242   1017   1691   1252"]


def main():
    _, times = input_str[0].split(":")
    _, distances = input_str[1].split(":")

    time: list[int] = list(map(int, times.split()))
    distance: list[int] = list(map(int, distances.split()))

    ans1 = 1
    for t, d in zip(time, distance):
        ans1 *= num_puzzle_solutions(t, d)
    print("Part 1:", ans1)

    t = int(times.replace(" ", ""))
    d = int(distances.replace(" ", ""))
    print("Part 2:", num_puzzle_solutions(t, d))


def num_puzzle_solutions(t: int, d: int) -> int:
    xl = (t - math.sqrt(t * t - 4 * d)) / 2
    xh = (t + math.sqrt(t * t - 4 * d)) / 2
    xh = math.floor(xh) if math.floor(xh) != xh else xh - 1
    xl = math.ceil(xl) if math.ceil(xl) != xl else xl + 1
    return int(xh - xl + 1)


if __name__ == "__main__":
    main()
