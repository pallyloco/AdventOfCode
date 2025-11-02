import itertools

while True:
    n = int(input())
    if n == 0:
        break
    sum1 = sum(int(i) for i in str(n))
    for answer in itertools.count(start=11):
        big_n = answer * n
        if sum1 == sum(int(i) for i in str(big_n)):
            print(answer)
            break

