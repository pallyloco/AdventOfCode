import re
import math


def main():
    file = open('day10_input.txt', 'r')

    """
    The CPU has a single register, X, which starts with the value 1. It supports only two instructions:

    addx V takes two cycles to complete. After two cycles, the X register is increased by the value V. 
    (V can be negative.)
    
    noop takes one cycle to complete. It has no other effect.
    
    The CPU uses these instructions in a program (your puzzle input) to, somehow, tell the screen what 
    to draw.
    """
    x = 1
    score = 0
    cycle = 0

    for line in map(str.rstrip, file):
        if re.match(r'noop', line):
            draw_pixel(cycle, x)
            score += signal_strength(cycle, x)
            cycle += 1
            continue
        regex = re.match(r'addx (-?\d+)', line)
        if regex:
            draw_pixel(cycle, x)
            score += signal_strength(cycle,int(x))
            cycle += 1
            draw_pixel(cycle, x)
            score += signal_strength(cycle,int(x))
            cycle += 1
            x += int(regex.group(1))
    print()

    print(f"signal strength is: {score}")


def draw_pixel(cycle, x):
    """
    It seems like the X register controls the horizontal position of a sprite. Specifically, the sprite is 3 pixels
    wide, and the X register sets the horizontal position of the middle of that sprite. (In this system, there is
    no such thing as "vertical position": if the sprite's horizontal position puts its pixels where the CRT is
    currently drawing, then those pixels will be drawn.)

    You count the pixels on the CRT: 40 wide and 6 high.
    This CRT screen draws the top row of pixels left-to-right, then the row below that, and so on.
    The left-most pixel in each row is in position 0, and the right-most pixel in each row is in position 39.

    The CRT draws a single pixel during each cycle.

    So, by carefully timing the CPU instructions and the CRT drawing operations,
    you should be able to determine whether the sprite is visible the instant each pixel is drawn.
    If the sprite is positioned such that one of its three pixels is the pixel currently being drawn,
    the screen produces a lit pixel (#); otherwise, the screen leaves the pixel dark (.).

    Render the image given by your program. What eight capital letters appear on your CRT?

    Your puzzle answer was RGZEHURK.
    """
    pos = cycle % 40
    if not pos:
        print()
    if x - 1 <= pos <= x + 1:
        print("\033[41m \033[0m", end="")
    else:
        print(" ", end="")


def signal_strength(cycle, x):
    """
    Maybe you can learn something by looking at the value of the X register throughout execution.
    For now, consider the signal strength (the cycle number multiplied by the value of the X register)
    during the 20th cycle and every 40 cycles after that
    (that is, during the 20th, 60th, 100th, 140th, 180th, and 220th cycles).

    Find the signal strength during the 20th, 60th, 100th, 140th, 180th, and 220th cycles.
    What is the sum of these six signal strengths?

    Your puzzle answer was 14860.
    """
    if cycle < 20:
        return 0
    if not (cycle - 20) % 40:
        return cycle * x
    return 0


# ===================================================================
# Entry point
# ===================================================================
if __name__ == '__main__':
    main()
