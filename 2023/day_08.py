import itertools as it
import re


def main(part: int = 1):
    file = open("day_08_input.txt", 'r')
    line_map = map(str.rstrip, file)
    right_left: list[str] = list()
    tree_info: dict[str, tuple[str, str]] = dict()
    for line in line_map:
        if line == "":
            break
        right_left += [*line]
    for line in line_map:
        if line == "":
            continue
        key, value = map(str.strip,line.split("="))
        v1, v2 = re.findall(r"[A-Z]+", value)
        tree_info[key] = (v1, v2)

    location = "AAA"
    dmap: dict[str, int] = {"R": 1, "L": 0}
    for i, direction in enumerate(it.cycle(right_left)):
        location = tree_info[location][dmap[direction]]
        print(i, location)
        if location == "ZZZ":
            break
    print("part 1:", i+1)


if __name__ == "__main__":
    main()
