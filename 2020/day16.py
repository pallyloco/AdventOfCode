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
from __future__ import annotations

from typing import Optional


class Ticket:
    def __init__(self, values: list(int)):
        self.values: list(int) = values
        self.num_columns = len(self.values)
        self.columns = range(self.num_columns)
        self._valid_rules_per_column: list[set[str]] = [set() for _ in range(self.num_columns)]
        self._updated_valid_rules_per_column: bool = False

    def _determine_valid_rules_per_column(self, rules: list[Rule]):
        self._updated_valid_rules_per_column = True
        for column in self.columns:
            for rule in rules:
                if self.values[column] in rule.valid_values:
                    self._valid_rules_per_column[column].add(rule.name)

    def value_at_column(self,column):
        return self.values[column]

    def is_value_at_column_valid(self, column, rules) -> bool:
        return len(self.valid_rules_for_column(column, rules)) != 0

    def valid_rules_for_column(self, column, rules) -> set[str]:
        if not self._updated_valid_rules_per_column:
            self._determine_valid_rules_per_column(rules)
        return self._valid_rules_per_column[column]

    def is_valid(self, rules: list[Rule]) -> bool:
        if not self._updated_valid_rules_per_column:
            self._determine_valid_rules_per_column(rules)
        for column in self.columns:
            if len(self.valid_rules_for_column(column, rules)) == 0:
                return False
        return True


class Rule:
    def __init__(self, name: str, valid_values: set[int]):
        self.name: str = name
        self.valid_values = valid_values


def main(part: int = 1):
    file = open("day16_input.txt", "r")
    parse_type = "rules"
    rules: list[Rule] = list()
    yours: Optional[Ticket] = None
    others: list[Ticket] = list()

    # ------------------------------------------------------------------------
    # parse the input
    # ------------------------------------------------------------------------
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
            yours: Ticket = parse_yours(line)
        else:
            parse_nearby(line, others)

    # ------------------------------------------------------------------------
    # error_rate
    # ------------------------------------------------------------------------
    error_rate = 0

    for ticket in others:
        for column in ticket.columns:
            if not ticket.is_value_at_column_valid(column, rules):
                error_rate += ticket.value_at_column(column)

    print("Part 1: error rate:", error_rate)

    # ------------------------------------------------------------------------
    # determine the order of the ticket fields
    # ------------------------------------------------------------------------
    valid_tickets: list[Ticket] = [ticket for ticket in others if ticket.is_valid(rules)]
    fields_by_column: list[set[str]] = [set([rule.name for rule in rules]) for _ in yours.columns]
    for column in yours.columns:
        for ticket in valid_tickets:
            fields_by_column[column].intersection_update(ticket.valid_rules_for_column(column, rules))

    # valid column to field is true if only one rule applies
    done = False
    found_fields = set()
    while not done:
        done = True
        for column in yours.columns:
            if len(fields_by_column[column]) <= 1:
                found_fields.update(fields_by_column[column])
            else:
                done = False
                fields_by_column[column] -= found_fields

    ans = 1
    for i, (field,) in enumerate(fields_by_column):
        if field[0:9] == "departure":
            ans = ans * yours.value_at_column(i)
    print("part 2:", ans)


def parse_rules(line:str, rules: list[Rule]):
    descr, rest = line.split(":")
    range1, range2 = rest.split(" or ")
    a1, a2 = map(int, range1.split("-"))
    b1, b2 = map(int, range2.split("-"))
    rules.append(Rule(descr, {*range(a1, a2 + 1), *range(b1, b2 + 1)}))


def parse_yours(line: str) -> Ticket:
    return Ticket(list(map(int, line.split(","))))


def parse_nearby(line: str, others: list[Ticket]):
    ticket = Ticket(list(map(int, line.split(","))))
    others.append(ticket)


if __name__ == "__main__":
    main(1)
