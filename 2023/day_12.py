import itertools
import re
from typing import Optional


def main(part: int = 1):
    file = open("day_12_input.txt", 'r')
    ans1 = 0
    for line in map(str.rstrip, file):
        n = parse(line)
        #ans1 += n
        #print(n)
    #print("answer 1:", ans1)


class SpringGroup:
    def __init__(self, s: str):
        self.s: str = s
        self.max_size: int = len(s)
        self.max_grps: Optional[int] = None
        self.min_grp_size: Optional[int] = None

        # if all "?"
        if re.search(r"^\?+$", s):
            self.max_grps = (len(s) + 1) // 2

        # if "?##?"
        m = re.search(r"^\??(#+)\??$", s)
        if m is not None:
            self.min_grp_size = len(m.group(1))

    def __str__(self):
        return self.s

    def __repr__(self):
        return str(self)


def parse(s: str, num: int = 0, part=2) -> int:
    """
    start the process of parsing the string
    1. break into SpringGroup's
    2. find valid SpringGroup for all the max required groups
    """
    num = 0
    springs, unknown_groupings = s.split()
    s_tmp = (SpringGroup(s) for s in re.split(r"\.+", springs))
    s_groups: list[SpringGroup] = [s for s in s_tmp if s.max_size > 0]
    required_groups: list[int] = list(map(int, unknown_groupings.split(",")))

    # how many groups do we have that are of max size, and what are the groups inbetween
    max_grp_size = max(required_groups)
    in_between_groups: list[list[int]] = [[], ]
    num_max_grp = 0
    for g in required_groups:
        if g != max_grp_size:
            in_between_groups[-1].append(g)
        else:
            in_between_groups.append(list())
            num_max_grp += 1

    # where can the max size groups fit?
    max_indices: list[int] = list()
    for i, s in enumerate(s_groups):
        if max_grp_size <= s.max_size:
            max_indices.append(i)

    # what are all the possible locations for the max groups?
    possible_locations = itertools.combinations(max_indices, num_max_grp)
    old = -1
    total = 0
    found:dict[str, int] = dict()
    for loc in possible_locations:
        p = 1
        for i, j in enumerate(loc):
            springs = s_groups[old + 1:j]
            print(springs, in_between_groups[i])
            old = j
            valids = list()
            string_to_match = ".".join(list(map(str, springs)))

            num = found.get(string_to_match, None)
            if num is None:
                num = _parse("", string_to_match, in_between_groups[i], valids)

            found[string_to_match] = num
            if num == 0:
                break
            p = p*num
        total = total + p
    print ("total = ", total)

def _parse(prev: str, tbd: str, groups: list[int], valids, depth=1):

    if "?" not in prev + tbd and valid_str(prev + tbd, groups):
        valids.append(prev + tbd)
        return
    elif "?" not in prev + tbd:
        return
    print("tbd:",tbd)

    # if we have a string of question marks, how many
    # ways can we place the remaining groups?
    m = re.search(r"^([?.]+)(.?|#+.?)$", tbd)
    if m is not None:

        # how many groups still need to be worked on?
        dones = re.split(r"\.+", prev)
        done = sum(1 for d in dones if len(d) > 0)
        remaining = len(groups) - done

        tmp_groups = remaining
        for tmp_groups in range(1, remaining+1):
            n = len(tbd) - (remaining - 1) + sum(groups[done + 1:])
            possible_combos = free_combos(n, tmp_groups)
            if possible_combos:
                s = ".".split(groups[done+1:])
                _parse(prev + "."+s, )





    # brute force it
    a, b = tbd.split("?", maxsplit=1)
    if maybe_valid(prev + a + "#", groups):
        _parse(prev + a + "#", b, groups, valids, depth + 1)
    if maybe_valid(prev + a + ".", groups):
        _parse(prev + a + ".", b, groups, valids, depth + 1)
    return len(valids)


def is_valid_group(s, g) -> bool:
    if len(s) < g:
        return False
    l = re.findall(r"(#+)", s)
    if l:
        if min((len(i) for i in l)) > g:
            return False
    return True


def free_combos(n: int, ng: int) -> int:
    """given 'n' free spaces, and 'ng' number of groups, return the number of possibilities"""
    if n < 1:
        return 0
    if ng < 0:
        return 0
    elif ng == 1:
        return n
    elif ng == 2:
        return n * (n + 1) // 2
    elif ng == 3:
        return ((n * (n + 1) * (2 * n + 1)) // 6 + (n * (n + 1)) // 2) // 2
    else:
        total = 0
        for i in range(n):
            total = total + free_combos(n, ng - 1)
        return total


def maybe_valid(s: str, groups) -> bool:
    s_grps = re.findall(r"([#\?]+)", s)
    if len(s_grps) > len(groups):
        return False
    for i in range(len(s_grps) - 1):
        if len(s_grps[i]) != groups[i]:
            return False
    if s_grps:
        return len(s_grps[-1]) <= groups[len(s_grps) - 1]
    return True


def valid_str(s: str, groups) -> bool:
    s_grps = re.findall(r"([#\?]+)", s)
    if len(s_grps) != len(groups):
        return False
    for i in range(len(s_grps)):
        if len(s_grps[i]) != groups[i]:
            return False
    print("    ", s)
    return True


def group_possibilities(spring_group, group) -> int:
    #  ...gg ..gg. .gg.. gg...      5-2+1
    #  ..ggg .ggg. ggg..            5-3+1
    #  ...ggg ..ggg. .ggg.. ggg...  6-3+1
    return len(group) - len(spring_group) + 1


if __name__ == "__main__":
    main()
