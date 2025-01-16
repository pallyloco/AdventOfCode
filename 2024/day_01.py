from collections import Counter
left_list = []
right_list = []

fh = open("day_01.txt", "r")
# part a - what is the differences between the smallest, 2nd smallest, etc., comparing
#          two lists side by side
for line in map(str.rstrip, fh):
    a, b = line.split()
    left_list.append(int(a))
    right_list.append(int(b))
total = 0
left_list.sort()
right_list.sort()
for l1, l2 in zip(left_list, right_list):
    total += abs(l2 - l1)

print(total)

# part b
"""
This time, you'll need to figure out exactly how often each number from the left list   
appears in the right list. Calculate a total similarity score by adding up each number 
in the left list after multiplying it by the number of times that number appears in the 
right list."""
total = 0
cl2 = Counter(right_list)
for number, frequency in Counter(left_list).items():
    total = total + frequency * number * cl2[number]
print(total)
