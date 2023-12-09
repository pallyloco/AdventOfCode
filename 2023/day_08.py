import itertools as it
import re
import math

right_left: list[str] = list()
tree_info: dict[str, tuple[str, str]] = dict()
dmap: dict[str, int] = {"R": 1, "L": 0}


def main(part: int = 1):
    global right_left
    global tree_info

    file = open("day_08_input.txt", 'r')
    line_map = map(str.rstrip, file)
    for line in line_map:
        if line == "":
            break
        right_left += [*line]
    for line in line_map:
        if line == "":
            continue
        key, value = map(str.strip, line.split("="))
        v1, v2 = re.findall(r"((?:[A-Z]|[0-9])+)", value)
        tree_info[key] = (v1, v2)

    """
    IMPORTANT INFORMATION ABOUT THE DATA: 
    ====================================================
    
    IT IS CYCLICAL
    xyA -> ijZ -> ijZ for all xy and ij
    
    ijZ -> ijZ takes exactly one cycle of the directions, for all ij
    
    xyA -> ijZ takes exactly n*(length of directions), for all xy
    
    ====================================================
    """
    cycle = len(right_left)

    locations = [x for x in tree_info.keys() if x[-1] == 'A']
    state: list[list] = list()

    # steps to get from xyA -> ijZ -> ijZ
    for location in locations:
        aaa = location == "AAA"
        z_found = False
        for i in it.count():
            direction = right_left[i % cycle]
            location = tree_info[location][dmap[direction]]
            if location[-1] == "Z" and z_found:
                state[-1].append(i - state[-1][0])
                break
            if location[-1] == "Z":
                state.append([i])
                z_found = 3
        if aaa:
            print("Answer 1:", state[-1][0] + 1)
    multiples = [s[1] // cycle for s in state]
    lcm = math.lcm(*multiples)
    print("answer 2: ", lcm * cycle)


if __name__ == "__main__":
    main()
