list1 = []
list2 = []
from collections import Counter

fh = open("day_01.txt", "r")
for line in map(str.rstrip,fh):
    print(line)
    a,b = line.split()
    list1.append(int(a))
    list2.append(int(b))
total = 0
list1.sort()
list2.sort()
for l1,l2 in zip(list1,list2):
    total += abs(l2-l1)

print(total)

# part b
total = 0
cl2 = Counter(list2)
for n,i in Counter(list1).items():
    total = total+i*n*cl2[n]
print(total)
