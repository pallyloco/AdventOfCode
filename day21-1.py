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
            monkeys[name].value = value

    root = monkeys["root"] 
    
    value = evaluate(root)
    print (root.value)

def evaluate(monkey):
    if monkey.value is not None: return monkey.value

    monkey1 = monkeys[monkey.monkey1]
    value1 = int(evaluate(monkey1))

    monkey2 = monkeys[monkey.monkey2]
    value2 = int(evaluate(monkey2))

    if monkey.operation == "*":
        monkey.value = value1 * value2
    elif monkey.operation == "/":
        monkey.value = value1 / value2
    elif monkey.operation == "+":
        monkey.value = value1 + value2
    elif monkey.operation == "-":
        monkey.value = value1 - value2
    return monkey.value
    




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
 
