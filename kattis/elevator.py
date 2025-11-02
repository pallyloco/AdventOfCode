import sys

start,stop = list(map(int,input().split()))
n = int(input())
floors = list(map(int,sys.stdin.readlines()))
num_floors = abs(start-stop)
stops = 0


for i in range(1,num_floors):
    floor = min(start,stop) + i
    if floor in floors:
        stops+=1

print(num_floors*4 + stops*10)
