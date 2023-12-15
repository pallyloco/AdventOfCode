import re
def main(part: int = 1):
    file = open("day_12_input.txt", 'r')
    ans1 = 0
    for line in map(str.rstrip, file):
        print()
        print(line)
        n = parse(line)
        ans1 += n
    print("answer 1:", ans1)



def parse(s: str, num: int = 0) -> int:
    num = 0
    springs, unknown_groupings = s.split()
    groups: list[int] = list(map(int, unknown_groupings.split(",")))
    valids = list()
    return _parse("", springs, groups, valids)


def _parse(prev: str, tbd: str, groups: list[int], valids, depth = 1) -> int:
    if "?" not in prev+tbd and valid_str(prev + tbd, groups):
        valids.append(prev + tbd)
        return 0
    elif "?" not in prev+tbd:
        return 0

    a, b = tbd.split("?", maxsplit=1)
    if maybe_valid(prev + a + "#", groups):
        _parse(prev + a + "#", b, groups, valids, depth+1)
    if maybe_valid(prev + a + ".", groups):
        _parse(prev + a + ".", b, groups, valids, depth+1)
    return len(valids)


def maybe_valid(s: str, groups) -> bool:
    s_grps = re.findall(r"([#\?]+)", s)
    if len(s_grps) > len(groups):
        return False
    for i in range(len(s_grps) - 1):
        if len(s_grps[i]) != groups[i]:
            return False
    if s_grps:

        return len(s_grps[-1]) <= groups[len(s_grps)-1]
    return True


def valid_str(s: str, groups) -> bool:
    s_grps = re.findall(r"([#\?]+)",s)
    if len(s_grps) != len(groups):
        return False
    for i in range(len(s_grps)):
        if len(s_grps[i]) != groups[i]:
            return False
    print("    ",s)
    return True


def group_possibilities(spring_group, group) -> int:
    #  ...gg ..gg. .gg.. gg...      5-2+1
    #  ..ggg .ggg. ggg..            5-3+1
    #  ...ggg ..ggg. .ggg.. ggg...  6-3+1
    return len(group) - len(spring_group) + 1


if __name__ == "__main__":
    main()
