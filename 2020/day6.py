import re

"""
Due to recent aviation regulations, many rules (your puzzle input) are being enforced about bags and their contents;
bags must be color-coded and must contain specific quantities of other color-coded bags.

For example, consider the following rules:

light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.

These rules specify the required contents for 9 bag types. In this example, every faded blue bag is empty,
every vibrant plum bag contains 11 bags (5 faded blue and 6 dotted black), and so on.

You have a shiny gold bag. If you wanted to carry it in at least one other bag, how many different bag colors would be
valid for the outermost bag? (In other words: how many colors can, eventually, contain at least one shiny gold bag?)
"""


def main(part: int = 1):
    file = open('day6_input.txt', 'r')
    bags: dict[str, list[tuple[str, int]]] = dict()
    for line in map(str.rstrip, file):
        matches = re.match(r'(\w+ \w+) bags contain (\d+) (\w+ \w+) ' +
                           r'bags?(?:, (\d+) (\w+ \w+) bags?)?', line)

        if matches:
            container_bag = matches.group(1).replace(" ","_")
            bags[container_bag] = list()
            for i in (2, 4):
                if matches.group(i) is not None:
                    num_bags = int(matches.groups(i))
                    insert_bag = matches.group(i+1).replace(" ","_")
                    bags[container_bag].append((insert_bag, num_bags))

        else:
            matches = re.match(r'(\w+ \w+) bags contain no other bags', line)


if __name__ == '__main__':
    main(1)
