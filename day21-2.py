import re                           # regular expressions
from astar import AStar             # A* algorithm
import time
import itertools
import math

# ----------------------------------------------------------------------------
# main code
# ----------------------------------------------------------------------------
monkeys = {}
def main():
    file = open("day21_input.txt", 'r')
    for line in map(str.rstrip,file):
        if regex:=re.match(r'([a-z]*): ([a-z]*) (.) ([a-z]*)',line):
            name,monkey1,op,monkey2 = regex.groups()
            monkeys[name] = Monkey(name,monkey1,op,monkey2)
        elif regex:=re.match(r'([a-z]*): (\d+)',line):
            name,value = regex.groups()
            monkeys[name] = Monkey(name,None,None,None)
            monkeys[name].value = int(value)

    # which value is reliant on humn
    root = monkeys["root"] 
    
    
    for monkey in monkeys.values():
        monkey.value = evaluate(monkey)

    if monkeys[root.monkey1].value is not None:
        other_value = monkeys[root.monkey1].value
        other_monkey = monkeys[root.monkey2]
    else:
        other_value = monkeys[root.monkey2].value
        other_monkey = monkeys[root.monkey1]
    
    other_monkey.value = other_value

    ans = reverse_evaluate(other_monkey)
    print(f"{ans=}")

def evaluate(monkey):
    if monkey.name == "humn": return None
    if monkey.value is not None: return monkey.value

    monkey1 = monkeys[monkey.monkey1]
    value1 = evaluate(monkey1)

    monkey2 = monkeys[monkey.monkey2]
    value2 = evaluate(monkey2)

    if value1 is None or value2 is None: return None

    value1 = int(value1)
    value2 = int(value2)

    if monkey.operation == "*":
        monkey.value = value1 * value2
    elif monkey.operation == "/":
        monkey.value = value1 / value2
    elif monkey.operation == "+":
        monkey.value = value1 + value2
    elif monkey.operation == "-":
        monkey.value = value1 - value2
    return monkey.value
    
def reverse_evaluate(monkey):

    
    if monkeys[monkey.monkey1].value is not None:
        other_value = monkeys[monkey.monkey1].value
        other_monkey = monkeys[monkey.monkey2]
        other_monkey_num = 2
    else:
        other_value = monkeys[monkey.monkey2].value
        other_monkey = monkeys[monkey.monkey1]
        other_monkey_num = 1

    if monkey.operation == "*":  
        other_monkey.value = monkey.value / other_value
    elif monkey.operation == "/":
        other_monkey.value = monkey.value * other_value
    elif monkey.operation == "+":
        other_monkey.value = monkey.value - other_value
    elif monkey.operation == "-" and other_monkey_num == 1:
        other_monkey.value = monkey.value + other_value
    elif monkey.operation == "-" and other_monkey_num == 2:
        other_monkey.value = other_value - monkey.value

    if other_monkey.name == "humn": return other_monkey.value
    return reverse_evaluate(other_monkey)


class Monkey:
    def __init__(self,name,monkey1,operation,monkey2):
        self.name = name
        self.monkey1 = monkey1
        self.monkey2 = monkey2
        self.operation = operation
        self.parent = None
        self.value = None


# ===================================================================
# Entry point
# ===================================================================
if __name__ == '__main__':
    global start
    start = time.time()
    main()    
    end = time.time()

    total_time = end - start
    print("\n"+ str(total_time))
 
