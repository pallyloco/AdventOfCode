from typing import Optional
from reading import read_paragraphs
from dictionaries import DictSet

"""
Safety protocols clearly indicate that new pages for the safety manuals must be printed in a 
very specific order. The notation X|Y means that if both page number X and page number Y 
are to be produced as part of an update, page number X must be printed at some point before page number Y.

part 1
To get the printers going as soon as possible, start by identifying which updates are already 
in the right order.
"""
input_data = [
    "47|53",
    "97|13",
    "97|61",
    "97|47",
    "75|29",
    "61|13",
    "75|53",
    "29|13",
    "97|29",
    "53|29",
    "61|53",
    "97|53",
    "61|29",
    "47|13",
    "75|47",
    "97|75",
    "47|61",
    "75|61",
    "47|29",
    "75|13",
    "53|13",
    "",
    "75,47,61,53,29",
    "97,61,53,29,13",
    "75,29,13",
    "75,97,47,61,53",
    "61,13,29",
    "97,13,75,29,47",
]

fh = open("day_05.txt", "r")
input_data = [line.rstrip() for line in fh]


def main(data):
    rules, updates = read_paragraphs(data)
    rule_dict = DictSet()
    for a, b in (r.split("|") for r in rules):
        rule_dict[a].add(b)

    valid_updates = []
    invalid_updates = []

    for pages in (u.split(",") for u in updates):
        valid = True
        for p in (page for page in pages if page in rule_dict):
            valid = valid and all((a not in pages) or pages.index(p) < pages.index(a) for a in rule_dict[p])
        if valid:
            valid_updates.append(pages)
        else:
            invalid_updates.append(pages)

    # part 1
    # What do you get if you add up the middle page number from those correctly-ordered updates
    total = 0
    for valid_update in valid_updates:
        total = total + int(valid_update[len(valid_update) // 2])
    print(total)

    # part 2
    # Find the updates which are not in the correct order. What do you get if you add up the
    # middle page numbers after correctly ordering just those updates?
    updated = []
    for pages in invalid_updates:
        updated.append(re_order(pages, rule_dict))
    total = 0
    for valid_update in updated:
        total = total + int(valid_update[len(valid_update) // 2])
    print(total)


def re_order(pages, rule_dict) -> list:
    """take pages and correct the ordering as defined by rule_dict"""
    result = []
    while len(pages) > 0:
        index = find_page_no_rule(pages, rule_dict)
        page = pages.pop(index)
        result.append(page)
    result.reverse()
    return result


def find_page_no_rule(pages, rule_dict) -> Optional[int]:
    """find a page such that it does not have to be before any other page in pages"""
    for index, page in enumerate(pages):
        if page not in rule_dict:
            return index
        needed = any(a in pages for a in rule_dict[page])
        if not needed:
            return index
    return None


main(input_data)
