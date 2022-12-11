import re
import math

def main():
    score = 0
    x = 1
    cycle = 1
    file = open('day10_input.txt', 'r')
    for line in file:
        line = line.rstrip()
        if re.match(r'noop',line):
            score += signal_strength(cycle,x)
            cycle += 1
            continue
        regex = re.match(r'addx (-?\d+)',line)
        if regex:
            score += signal_strength(cycle,int(x))
            cycle += 1
            score += signal_strength(cycle,int(x))
            cycle += 1
            x += int(regex.group(1))
    print(f"score = {score}")

def signal_strength (cycle, x):
    if cycle < 20:
        return 0
    if not (cycle - 20)%40:
        return cycle*x
    return 0
 

# ===================================================================
# Entry point
# ===================================================================
if __name__ == '__main__':
    main()