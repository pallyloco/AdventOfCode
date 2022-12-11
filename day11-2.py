import re
import math

# After each monkey inspects an item but before it tests your worry level, your
#  relief that the monkey's inspection didn't damage the item causes your worry
#  level to be divided by three and rounded down to the nearest integer.

# The monkeys take turns inspecting and throwing items.
#  On a single monkey's turn, it inspects and throws all of the items it is
#  holding one at a time and in the order listed. Monkey 0 goes first, then
#  monkey 1, and so on until each monkey has had one turn. The process of each
#  monkey taking a single turn is called a round.

# When a monkey throws an item to another monkey, the item goes on the end of
#  the recipient monkey's list. A monkey that starts a round with no items could
#  end up inspecting and throwing many items by the time its turn comes
#  around. If a monkey is holding no items at the start of its turn, its turn ends.

# Using test input
# After round 1
# Monkey 0: 20, 23, 27, 26
# Monkey 1: 2080, 25, 167, 207, 401, 1046
# Monkey 2: 
# Monkey 3: 

# After round 20, the monkeys are holding items with these worry levels:
# Monkey 0: 10, 12, 14, 26, 34
# Monkey 1: 245, 93, 53, 199, 115
# Monkey 2: 
# Monkey 3: 


MAX_ROUND = 10000
PRINT_WHEN = 10000
def main():
    file = open('day11_input.txt', 'r')
    lines = []
    monkeys = Monkeys()

    for line in file:
        line = line.rstrip()
 
        if not line and len(lines) > 0:
            monkeys.add(Monkey(lines))
            lines = []
            continue

        lines.append(line)

    if len(lines) > 0:
        monkeys.add(Monkey(lines))

    # print(monkeys)

    lcm = monkeys.get_lcm_of_tests()

    for round in range(MAX_ROUND):
        for monkey in monkeys:
            for throw_to in monkey.process_items() :
                receiver = monkeys.get_monkey_by_id(throw_to['to'])
                receiver.receive(throw_to['item']%lcm)
        if not (round+1)%PRINT_WHEN:
            print(f"\nround: {round+1}")
            print (monkeys)

    highest = monkeys.get_highest_inspections(2)
    answer = 1
    for high in highest:
        answer = answer * high
    print(answer)



class Monkeys:
    def __init__(self):
        self._monkeys = []
        self._monkey_by_id = {}
    def __iter__(self):
        return iter(self._monkeys)

    def add(self, monkey):
        self._monkeys.append(monkey)
        self._monkey_by_id[monkey.id] = monkey
    def get_monkey_by_id(self,id):
        return self._monkey_by_id[id]
    def get_highest_inspections(self,number):
        all = sorted([i.num_inspected_items for i in self._monkeys],reverse=True)
        print("="*10)
        print(all)
        return [all[i] for i in range(number)]
    
    def get_lcm_of_tests(self):
        lcm = 1
        for monkey in self:
            lcm = lcm * monkey.test
        return lcm

    def __str__(self):
        str = ""
        for monkey in self._monkeys:
            str += f"\n{monkey}"
        return str
    def __repr__(self):
        return self.__str__()
        

class Monkey:
    def __init__(self, lines:[str]):
        
        self.num_inspected_items = 0

        for line in lines:
            regex = re.match(r'Monkey\s(\d+)',line)
            if regex: self.id = regex.group(1)
            
            regex = re.match(r'\s*Starting items: (.*)',line)
            if regex: self.items = [int(i) for i in regex.group(1).split(',')]

            regex = re.match(r'\s*Operation: new\s*=\s*(.*)',line)
            if regex: self.operation = regex.group(1)

            regex = re.match(r'\s*Test: divisible by (\d+)',line)
            if regex: self.test = int(regex.group(1))

            regex = re.match(r'\s*If true: throw to monkey (\d+)',line)
            if regex: self.if_true = regex.group(1)

            regex = re.match(f'\s*If false: throw to monkey (\d+)',line)
            if regex: self.if_false = regex.group(1)

    def process_items(self):
        to_throw=[]
        # Monkey inspects an item with a worry level of item
        for old in self.items:
            # Count the total number of times each monkey inspects items 
            self.num_inspected_items += 1
            # Worry level is operated on
            new = eval(self.operation)
            # Monkey gets bored with item. Worry level is divided by 3
            # new = new // 3
            # divisible by test?
            if not new % self.test:
                to_throw.append({'item':new, 'to':self.if_true})
            else:
                to_throw.append({'item':new, 'to':self.if_false})
        self.items = []
        return to_throw
    
    def receive (self, item):
       # item = item % self.test
        self.items.append(item)

    def __str__(self):
        str = f"id:{self.id} num_inspected_items: {self.num_inspected_items} "
        return str
    def __repr__(self):
        return self.__str__()


# ===================================================================
# Entry point
# ===================================================================
if __name__ == '__main__':
    main()