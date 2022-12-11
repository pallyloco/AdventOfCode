import re
import math

def main():
    x = 1
    cycle = 0
    print()
    file = open('day10_input.txt', 'r')
    for line in file:
        line = line.rstrip()
        if re.match(r'noop',line):
            draw_pixel(cycle,x)
            cycle += 1
            continue
        regex = re.match(r'addx (-?\d+)',line)
        if regex:
            draw_pixel(cycle,x)
            cycle += 1
            draw_pixel(cycle,x)
            cycle += 1
            x += int(regex.group(1))
    print()

def draw_pixel (cycle, x):
    pos = cycle%40
    if not pos:
        print()
    if x-1 <= pos <= x+1:
        print("#",end="")
    else:
        print(".",end="")

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