"""
You collect the rules for ticket fields, the numbers on your ticket, and the numbers on
other nearby tickets for the same train service (via the airport security cameras) together
into a single document you can reference (your puzzle input).

The rules for ticket fields specify a list of fields that exist somewhere on the ticket and
the valid ranges of values for each field. For example, a rule like class: 1-3 or 5-7 means
that one of the fields in every ticket is named class and can be any value in the
ranges 1-3 or 5-7 (inclusive, such that 3 and 5 are both valid in this field, but 4 is not).

Each ticket is represented by a single line of comma-separated values. The values are the numbers
on the ticket in the order they appear; every ticket has the same format.

Start by determining which tickets are completely invalid; these are tickets that contain
values which aren't valid for any field. Ignore your ticket for now.

Adding together all of the invalid values produces your ticket scanning error rate: 4 + 55 + 12 = 71.

Consider the validity of the nearby tickets you scanned. What is your ticket scanning error rate?

--- Part Two ---
Now that you've identified which tickets contain invalid values, discard those tickets entirely.
Use the remaining valid tickets to determine which field is which.

Using the valid ranges for each field, determine what order the fields appear on the tickets.
The order is consistent between all tickets:

Once you work out which field is which, look for the six fields on your ticket that start with the
word departure. What do you get if you multiply those six values together?

"""


def main(part: int = 1):
    file = open("day16_input.txt", "r")
    parse_type = "rules"
    rules: dict[str, set] = dict()
    yours: list[int] = list()
    others: list[list[int]] = list()
    for line in map(str.rstrip, file):
        if line == "":
            continue
        elif line == "your ticket:":
            parse_type = "yours"
            continue
        elif line == "nearby tickets:":
            parse_type = "nearby"
            continue

        if parse_type == "rules":
            parse_rules(line, rules)
        elif parse_type == "yours":
            parse_yours(line, yours)
        else:
            parse_nearby(line, others)

    # valid tickets and error_rate
    valid_tickets = list()
    error_rate = 0
    for ticket in others:
        valid_ticket = True
        for value in ticket:
            valid_value = False
            for rule in rules:
                if value in rules[rule]:
                    valid_value = True
                    break

            if not valid_value:
                valid_ticket = False
                error_rate += value
        if valid_ticket:
            valid_tickets.append(ticket)

    print("Part 1: error rate:", error_rate)

    # determine the order of the ticket fields


def parse_rules(line, rules):
    descr, rest = line.split(":")
    range1, range2 = rest.split(" or ")
    a1, a2 = map(int, range1.split("-"))
    b1, b2 = map(int, range2.split("-"))
    rules[descr] = {*range(a1, a2 + 1), *range(b1, b2 + 1)}


def parse_yours(line, yours):
    yours.extend(list(map(int, line.split(","))))


def parse_nearby(line, others):
    others.append(list(map(int, line.split(","))))


if __name__ == "__main__":
    main(1)
