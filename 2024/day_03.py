"""xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""
import re

"""
Scan the corrupted memory for uncorrupted mul instructions. 
What do you get if you add up all of the results of the multiplications?
"""
# data = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"

fh = open("day_03.txt", "r")
data = fh.read()
total = sum((int(m) * int(n) for m, n in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", data)))
print(total)

# part 2
"""
There are two new instructions you'll need to handle:
- The do() instruction enables future mul instructions.
- The don't() instruction disables future mul instructions.
"""
# data = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
x = re.findall(r"(mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\))", data)

enabled = True
total = 0
for match in x:
    if match == "do()":
        enabled = True
    elif match == "don't()":
        enabled = False
    elif enabled:
        total += sum((int(m) * int(n) for m, n in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", match)))
print(total)
