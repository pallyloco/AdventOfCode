from __future__ import annotations
import re
from math import gcd
from typing import TextIO, NewType
from dataclasses import dataclass

PRINT_WHEN = 20000
NUM_MOST_ACTIVE_MONKEYS = 2

MonkeyID = NewType('MonkeyID', str)
MathOperation = NewType('MathOperation', str)
WorryLevel = NewType('WorryLevel', int)
DivisibleBy = NewType('DivisibleBy', int)


# ============================================================================
# main
# ============================================================================
def main(max_round: int, worry_level_decrease: WorryLevel):
    file = open('day11_input.txt', 'r')
    monkeys = Monkeys()

    for lines in read_paragraph(file):
        if len(lines) > 0:
            monkeys.add(Monkey(lines))

    # need the lcm to keep the worry level within reasonable integer bounds
    lcm = monkeys.get_lcm_of_tests()

    # start of monkey business :)
    for round_num in range(max_round):
        for monkey in monkeys:
            for throw_to in monkey.process_items(worry_level_decrease):
                receiver = monkeys.get_monkey_by_id(throw_to.to)
                if worry_level_decrease == 1:
                    throw_to.item = throw_to.item % lcm
                receiver.receive(throw_to.item)

        if not (round_num + 1) % PRINT_WHEN:
            print(f"\nround_num: {round_num + 1}")
            print(monkeys)

    """
    Chasing all of the monkeys at once is impossible; you're going to have to focus on the two 
    most active monkeys if you want any hope of getting your stuff back. 
    Count the total number of times each monkey inspects items over MAX_ROUND rounds:
    
    The level of monkey business in this situation can be found by multiplying these together
    """

    highest = monkeys.get_highest_inspections(NUM_MOST_ACTIVE_MONKEYS)
    answer = 1
    for high in highest:
        answer = answer * high
    print(answer)


# ============================================================================
# read lines until a blank line
# ============================================================================
def read_paragraph(file: TextIO) -> list[str]:
    lines: list[str] = list()
    for line in map(str.rstrip, file):
        lines.append(line)
        if not line and len(lines) > 0:
            yield lines
            lines.clear()
    yield lines


# ============================================================================
# Monkey class
# ============================================================================
class Monkeys:
    def __init__(self):
        self._monkeys: dict[MonkeyID, Monkey] = dict()

    def __iter__(self):
        return iter(sorted(self._monkeys.values(), key=lambda x: x.id))

    def add(self, monkey: Monkey):
        self._monkeys[monkey.id] = monkey

    def get_monkey_by_id(self, monkey_id: MonkeyID):
        return self._monkeys[monkey_id]

    def get_highest_inspections(self, number):
        all_monkeys = sorted([i.num_inspected_items for i in self._monkeys.values()], reverse=True)
        print("=" * 10)
        print(all_monkeys)
        return [all_monkeys[i] for i in range(number)]

    def get_lcm_of_tests(self) -> int:
        lcm = 1
        for monkey in self:
            lcm = lcm * monkey.test // gcd(lcm, monkey.test)
        return lcm

    def __str__(self):
        output = ""
        for monkey in self:
            output += f"\n{monkey}"
        return output

    def __repr__(self):
        return self.__str__()


# ============================================================================
# class Monkey
# ============================================================================
class Monkey:
    """
    You take some notes (your puzzle input) on the items each monkey currently has, how worried you
    are about those items, and how the monkey makes decisions based on your worry level. For example:

    Monkey 0:
      Starting items: 79, 98
      Operation: new = old * 19
      Test: divisible by 23
        If true: throw to monkey 2
        If false: throw to monkey 3

    """

    def __init__(self, lines: [str]):

        self.num_inspected_items = 0

        for line in lines:
            regex = re.match(r'Monkey\s(\d+)', line)
            if regex:
                self.id: MonkeyID = regex.group(1)

            regex = re.match(r'\s*Starting items: (.*)', line)
            if regex:
                self.items: list[WorryLevel | int] = [int(i) for i in regex.group(1).split(',')]

            regex = re.match(r'\s*Operation: new\s*=\s*(.*)', line)
            if regex:
                self.operation: MathOperation = regex.group(1)

            regex = re.match(r'\s*Test: divisible by (\d+)', line)
            if regex:
                self.test: int = int(regex.group(1))

            regex = re.match(r'\s*If true: throw to monkey (\d+)', line)
            if regex:
                self.throw_to_if_passed_test: MonkeyID = regex.group(1)

            regex = re.match(r'\s*If false: throw to monkey (\d+)', line)
            if regex:
                self.throw_to_if_failed_test: MonkeyID = regex.group(1)

    def process_items(self, worry_level_decrease: WorryLevel):
        """
        On a single monkey's turn, it inspects and
        throws all of the items it is holding one at a time and in the order listed.

        Starting items lists your worry level for each item the monkey is currently holding in the order
        they will be inspected.

        Operation shows how your worry level changes as that monkey inspects an item.
        (An operation like new = old * 5 means that your worry level after the monkey inspected the item
        is five times whatever your worry level was before inspection.)

        Test shows how the monkey uses your worry level to decide where to throw an item next.
        If true shows what happens with an item if the Test was true.
        If false shows what happens with an item if the Test was false.
        """
        to_throw: list[ThrowTo] = list()
        # Monkey inspects an item with a worry level of item
        for old in self.items:
            # Count the total number of times each monkey inspects items 
            self.num_inspected_items += 1
            # Worry level is operated on
            new: WorryLevel = eval(self.operation)
            # Monkey gets bored with item. Worry level is divided by WorryLevel
            new = new // worry_level_decrease
            # divisible by test?
            if not new % self.test:
                to_throw.append(ThrowTo(self.throw_to_if_passed_test, new))
            else:
                to_throw.append(ThrowTo(self.throw_to_if_failed_test, new))
        self.items.clear()
        return to_throw

    def receive(self, item):
        self.items.append(item)

    def __str__(self):
        return f"id:{self.id} num_inspected_items: {self.num_inspected_items} " + \
              f"items:{self.items} operation:`{self.operation}` test:{self.test} " + \
              f"if_true:{self.throw_to_if_passed_test} if_false:{self.throw_to_if_failed_test}"

    def __repr__(self):
        return self.__str__()


@dataclass
class ThrowTo:
    to: MonkeyID
    item: WorryLevel


# ===================================================================
# Entry point
# ===================================================================
if __name__ == '__main__':
    main(20, 3)
    main(10000, 1)

"""
Monkeys are playing Keep Away with your missing things!

To get your stuff back, you need to be able to predict where the monkeys will throw your items. 
After some careful observation, you realize the monkeys operate based on how worried you are about 
each item.

You take some notes (your puzzle input) on the items each monkey currently has, how worried you 
are about those items, and how the monkey makes decisions based on your worry level. For example:

Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Starting items lists your worry level for each item the monkey is currently holding in the order 
they will be inspected.

Operation shows how your worry level changes as that monkey inspects an item. 
(An operation like new = old * 5 means that your worry level after the monkey inspected the item 
is five times whatever your worry level was before inspection.)

Test shows how the monkey uses your worry level to decide where to throw an item next.
If true shows what happens with an item if the Test was true.
If false shows what happens with an item if the Test was false.

After each monkey inspects an item but before it tests your worry level, your relief that the 
monkey's inspection didn't damage the item causes your worry level to be divided by three and 
rounded down to the nearest integer.

The monkeys take turns inspecting and throwing items. On a single monkey's turn, it inspects and 
throws all of the items it is holding one at a time and in the order listed. 
Monkey 0 goes first, then monkey 1, and so on until each monkey has had one turn. 
The process of each monkey taking a single turn is called a round.

When a monkey throws an item to another monkey, the item goes on the end of the recipient monkey's list. 
A monkey that starts a round with no items could end up inspecting and throwing many items by the time 
its turn comes around. If a monkey is holding no items at the start of its turn, its turn ends.

Chasing all of the monkeys at once is impossible; you're going to have to focus on the two 
most active monkeys if you want any hope of getting your stuff back. 
Count the total number of times each monkey inspects items over 20 rounds:

Figure out which monkeys to chase by counting how many items they inspect over 20 rounds. 
What is the level of monkey business after 20 rounds of stuff-slinging simian shenanigans?

Your puzzle answer was 120756.

--- Part Two ---

Worry levels are no longer divided by three after each item is inspected; 
you'll need to find another way to keep your worry levels manageable. 
Starting again from the initial state in your puzzle input, what is the 
level of monkey business after 10000 rounds?

Your puzzle answer was 39109444654.

"""