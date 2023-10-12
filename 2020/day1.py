file = open("day1_input.txt")
entries: list[int] = [number for number in map(int, map(str.rstrip, file))]
entries.sort()
j = len(entries) - 1
i = 0

# part 1
# you to find the two entries that sum to 2020 and then multiply those two numbers together.
while entries[i] + entries[j] != 2020:
    if entries[i] + entries[j] > 2020:
        j = j - 1
        continue
    if entries[i] + entries[j] < 2020:
        i = i + 1
        continue
    if j < i:
        break
print("Part 1: two numbers that add to 2020:", entries[i], entries[j], "Product", entries[i] * entries[j])

# part 2
# In your expense report, what is the product of the three entries that sum to 2020?
for i in range(0, len(entries)):
    for j in range(i+1, len(entries)):
        for k in range(j+1, len(entries)):
            if entries[i]+entries[j]+entries[k] == 2020:
                print("Part 1: two numbers that add to 2020:", entries[i], entries[j], entries[k],
                      "Product", entries[i] * entries[j] * entries[k])
                break

"""
--- Day 1: Report Repair ---

Before you leave, the Elves in accounting just need you to fix your expense report (your puzzle input);
apparently, something isn't quite adding up.

Specifically, they need you to find the two entries that sum to 2020 and then multiply those two numbers together.

Of course, your expense report is much larger. Find the two entries that sum to 2020;
what do you get if you multiply them together?

Your puzzle answer was 1003971.

--- Part Two ---
... you can find three numbers in your expense report that meet the same criteria.

In your expense report, what is the product of the three entries that sum to 2020?

Your puzzle answer was 84035952.

"""
