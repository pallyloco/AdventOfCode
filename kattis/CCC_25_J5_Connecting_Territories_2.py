# Ians
from datetime import datetime
from queue import PriorityQueue
from functools import cache

# https://dmoj.ca/problem/ccc25j5

R = int(input())
C = int(input())
M = int(input())

print (datetime.now())
# Mathematically, it's easier to work with the costs as numbers between [0,M-1]
# This means that each cost calculated below is -1 from the real cost, so at the end
# I add R to the total, 1 for the cost of each row.

@cache  # does this still work with closures?
def next(cost):
    return (cost + C - 1) % M, (cost + C) % M, (cost + C + 1) % M


# track the "in progress" paths, in a queue ordered by their current cost. (Dijkstra's algorithm)
queue = PriorityQueue()

# add the step unto the first row
for i in range(C):
    # format: (cost so far, previous cost, x position, y position)
    queue.put((i % M, i % M, i, 1))

while not queue.empty():
    accum_cost, prev_cost, x, y = queue.get()

    # the first path that comes out of the queue having reached the lower territory
    # has the lowest accumulated cost
    if y == R:
        print(accum_cost + R)  # remember to add R
        break

    down_left, down, down_right = next(prev_cost)

    queue.put((accum_cost + down, down, x, y + 1))

    # check for walls
    if x > 0:
        queue.put((accum_cost + down_left, down_left, x - 1, y + 1))
    if x < C - 1:
        queue.put((accum_cost + down_right, down_right, x + 1, y + 1))
print (datetime.now())

"""
from datetime import datetime

import numpy as np
max_row = int(input())
max_col = int(input())
max_num = int(input())
print(datetime.now())


row = np.array([c%max_num+1 for c in range(max_col)])
cost = max_col%max_num
next_row = np.array([0] * max_col)
for r in range(1,max_row):
    for c in range(max_col):
        if cost == max_num:
            cost=1
        else:
            cost = cost+1
        if 0 < c < max_col-1:
            next_row[c] = np.min(row[c-1:c+2]) + cost
        elif c == max_col - 1:
            next_row[c] = np.min(row[c-1:c+1]) + cost
        else:
            next_row[c] = np.min(row[c:c+2]) + cost
    row,next_row = next_row,row
    print(row)
print(min(row))
print(datetime.now())

"""

"""
max_row = int(input())
max_col = int(input())
max_num = int(input())

row = [c%max_num+1 for c in range(max_col)]
cost = max_col%max_num
for r in range(1,max_row):
    next_row = []
    for c in range(max_col):
        if cost == max_num:
            cost=1
        else:
            cost = cost+1
        if 0 < c < max_col-1:
            next_row.append(min(row[c-1],row[c],row[c+1],) + cost)
        elif c == max_col - 1:
            next_row.append(min(row[c-1],row[c],) + cost)
        else:
            next_row.append(min(row[c+1],row[c],) + cost)
    row = next_row
print(min(row))

"""