import math

n = int(input())
for _ in range(n):
    encoded = input()
    size = int(math.sqrt(len(encoded)))
    answer = []
    for c in range(size):
        for row in range(size):
            answer.append(encoded[size-c-1 + row*size] )
    print("".join(answer))
