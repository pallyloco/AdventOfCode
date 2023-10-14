from __future__ import annotations
import re
import itertools

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

You have a shiny gold bag. 
"""


def main(part: int = 1):
    file = open('day7_input.txt', 'r')
    bags: dict[str, Bag] = dict()
    for line in map(str.rstrip, file):
        matches = re.match(r'(\w+ \w+) bags contain', line)
        contains = re.findall(r'(\d+) (\w+ \w+)',line)

        container_bag_name = matches.group(1).replace(" ", "_")
        container_bag = get_bag(bags, container_bag_name)

        for num_bags, insert_bag_name in contains:
            insert_bag_name = insert_bag_name.replace(" ", "_")
            insert_bag = get_bag(bags, insert_bag_name)
            container_bag.add_bag(num_bags, insert_bag)
            insert_bag.contained_by.append(container_bag)
        pass

    print("number of unique color bags is:",len(how_many_bag_colour_containers(bags, "shiny_gold")))
    print("number of bags to buy is:",carry_on_bags(bags, "shiny_gold"))
    pass


def get_bag(db: dict[str, Bag], name: str) -> Bag:
    if name not in db:
        db[name] = Bag(name)
    return db[name]


def how_many_bag_colour_containers(db: dict[str, Bag], name: str) -> int:
    """If you wanted to carry it in at least one other bag, how many different bag colors would be
    valid for the outermost bag? (In other words: how many colors can, eventually, contain at least one shiny gold bag?)
    """
    bag = get_bag(db, name)
    unique_colour_bags: set[Bag] = set()
    for contained_bag in bag.contained_by:
        unique_colour_bags.update( how_many_bag_colour_containers(db, contained_bag.name))
        unique_colour_bags.update([contained_bag])
    return unique_colour_bags


def carry_on_bags(db: dict[str, Bag], name: str) -> int:
    """How many individual bags are required inside your single shiny gold bag?"""

    # Note: I am going to assume that there is no infinite loop (eek)
    bag = get_bag(db, name)
    total_bags = bag.number_of_bags_contained()
    for number, contained_bag in bag.contains:
        this_total = carry_on_bags(db, contained_bag.name)
        total_bags = total_bags + number*this_total
    return total_bags





class Bag:
    def __init__(self, name: str):
        self.name = name
        self.contains: list[tuple[Bag, int]] = list()
        self.contained_by: list[Bag] = list()

    def add_bag(self, number, bag):
        self.contains.append((int(number), bag))

    def number_of_bags_contained(self)->int:
        return sum(n[0] for n in self.contains)

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


if __name__ == '__main__':
    main(1)
