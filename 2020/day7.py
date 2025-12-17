from __future__ import annotations
import re


def main(part: int = 1):
    file = open('day7_input.txt', 'r')
    bags: dict[str, Bag] = dict()
    for line in map(str.rstrip, file):
        container_bag_name, contains_str = (x.rstrip(".").strip() for x in line.split("bags contain"))
        container_bag = get_bag(bags, container_bag_name)

        contains = re.findall(r'(\d+) (\w+ \w+)',contains_str)

        for num_bags, insert_bag_name in contains:
            insert_bag = get_bag(bags, insert_bag_name)
            container_bag.add_bag(num_bags, insert_bag)
            insert_bag.contained_by.append(container_bag)
        pass

    print("number of unique color bags is:",len(how_many_bag_colour_containers(bags, "shiny gold")))
    print("number of bags to buy is:",carry_on_bags(bags, "shiny gold"))
    pass


def get_bag(db: dict[str, Bag], name: str) -> Bag:
    if name not in db:
        db[name] = Bag(name)
    return db[name]


def how_many_bag_colour_containers(db: dict[str, Bag], name: str) -> set:
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
        self.contains: list[tuple[int, Bag]] = list()
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
