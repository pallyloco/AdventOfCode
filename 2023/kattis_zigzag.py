import math

# ----------------------------------------------------------------------------
# globals
# ----------------------------------------------------------------------------
letters = list()
for i in range(26):
    letters.append(chr(ord('a') + i))


def main(n):

    num_digits = math.ceil(n / 25) + 1

    if num_digits == 2:
        return f"a{letters[n]}"

    s = "az" * int(num_digits / 2) + "a" * (num_digits % 2)

    p = n // 25
    remainder = n - 25*(p-1)
    if remainder == 25:
        return s
    index = (remainder + 1)//2
    s = "a"+letters[index]+"a"
    l1 = "z"
    l2 = "a"
    l3 = "b"
    l4 = "y"
    total = index*2
    for i in range(p-1):
        s += l1
        l2,l1 = l1,l2
        l3,l4 = l4,l3
        total = total + 25
    if total - n == 1:
        s = s[:-1]+l3

    return s

def code(s):
    n = 0
    for i,j in zip(s[:-1],s[1:]):
        n = abs(ord(i)-ord(j)) + n
    return n

n = int(input())
print(main(n))
# for n in range(0,1000):
#     s=main(n+1)
#     x = code(s)
#     if x != n+1:
#         print (n+1, s, x)



