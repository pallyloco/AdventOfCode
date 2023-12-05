import re

conversion: dict[str, int] = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                              "six": 6, "seven": 7, "eight": 8, "nine": 9, "zero": 0,
                              "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "0": 0}


# too low: part 2 54978

def main(part: int = 1):
    file = open("day_01_input.txt", 'r')
    ans: int = 0
    ans2: int = 0
    for line in map(str.rstrip, file):
        b = list(map(int, filter(str.isdigit, line)))
        ans += b[0] * 10 + b[-1]
        d1 = re.search(r"(one|two|three|four|five|six|seven|eight|nine|zero|[0-9])", line).group(1)
        d2 = re.search(r".*(one|two|three|four|five|six|seven|eight|nine|zero|[0-9])", line).group(1)
        ans2 += myint(d1) * 10 + myint(d2)

    print(ans)
    print(ans2)


def myint(s: str) -> int:
    return conversion[s]


if __name__ == "__main__":
    # main(1)
    main(2)
