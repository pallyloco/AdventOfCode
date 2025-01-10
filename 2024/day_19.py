from reading import read_paragraphs
from collections import deque

input_data = [
    "r, wr, b, g, bwu, rb, gb, br",
    "",
    "gbbr",
    "brwrr",
    "bggr",
    "rrbgbr",
    "ubwu",
    "bwurrg",
    "brgr",
    "bbrgwb",
]

fh = open("day_19.txt", "r")
input_data = list(map(str.rstrip, fh))

matches = dict()


class PatternMatch:
    def __init__(self, towels: list[str], pattern: str):
        self.towels = towels
        self.pattern = pattern

    def parent_children(self):
        kids = []
        for towel in self.towels:
            if len(towel) <= len(self.pattern):
                if towel == self.pattern[:len(towel)]:
                    kids.append((towel, PatternMatch(self.towels, self.pattern[len(towel):])))
        return kids

    def __str__(self):
        return self.pattern

    def __repr__(self):
        return str(self)


def main(data):
    towels_str, patterns = [d for d in read_paragraphs(data)]
    towels = list(map(str.strip, towels_str[0].split(",")))

    workable = 0
    totals = 0
    for pattern in patterns:
        total = reverse_pattern(PatternMatch(towels, pattern))
        print(total, pattern)
        totals = total + totals
        if total > 0:
            workable += 1
    print(workable, totals)
    pass

def reverse_pattern(p: PatternMatch):
    test_pattern = ""
    total = 0
    for c in reversed(p.pattern):
        test_pattern = c + test_pattern
        if test_pattern not in matches:
            paths = find_pattern(PatternMatch(p.towels, test_pattern))
            matches[test_pattern] = paths
        total = matches[test_pattern]
    return total


def find_pattern(p: PatternMatch, path="", paths = None) -> int:
    if path == "":
        paths = dict()
    if len(p.pattern) == 0:
        paths[path] = 1
    for parent, child in p.parent_children():
        new_path = ",".join((path, parent))
        if child.pattern in matches:
            paths[new_path+","+child.pattern] = matches[child.pattern]
        else:
            find_pattern(child, new_path, paths)
    return sum(i for i in paths.values())


main(input_data)
