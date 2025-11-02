line = input()
cups = [1,0,0]
for move in line:
    if move == 'A':
        cups[0],cups[1] = cups[1],cups[0]
    elif move == 'B':
        cups[2],cups[1] = cups[1],cups[2]
    else:
        cups[2],cups[0] = cups[0],cups[2]
print( cups.index(1)+1)
