from typing import Optional

test_data = [
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


def main():
    fh = open("day_05.txt", "r")
    rules, updates = get_rules_and_updates(map(str.rstrip, fh))
    #rules, updates = get_rules_and_updates(test_data)
    rule_dict = {}
    for a, _ in (r.split("|") for r in rules):
        rule_dict[a] = set()
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
    total = 0
    for vu in valid_updates:
        total = total + int(vu[len(vu) // 2])
    print(total)

    # part 2
    updated = []
    for pages in invalid_updates:
        updated.append(re_order(pages,rule_dict))
    total = 0
    for vu in updated:
        total = total + int(vu[len(vu) // 2])
    print(total)

def re_order(pages, rule_dict)->list:
    result = []
    while len(pages) > 0:
        # find page that does not have any rule associated with it
        i = find_page_no_rule(pages,rule_dict)
        p = pages.pop(i)
        result.append(p)
    result.reverse()
    return result


def find_page_no_rule(pages,rule_dict)->Optional[int]:
    for i,page in enumerate(pages):
        if page not in rule_dict:
            return i
        needed = any(a in pages for a in rule_dict[page])
        if not needed:
            return i
    return None




def get_rules_and_updates(data) -> tuple[list[str], list[str]]:
    rules = []
    updates = []
    update_flag = False
    for rule in data:
        if rule == "":
            update_flag = True
            continue
        if update_flag:
            updates.append(rule)
        else:
            rules.append(rule)
    return rules, updates


main()
