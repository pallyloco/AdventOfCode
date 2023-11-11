# https://open.kattis.com/problems/ornaments
import math

while True:
    r, h, s = map(int, input().split(" "))
    if r == 0 and h == 0 and s == 0:
        exit()
    l = math.sqrt(h*h - r*r)
    theta = math.asin(l/h)
    p = 2*math.pi*r - 2*r*theta
    t = (p + 2*l)*(1+s/100.)
    print(f"{t:.2f}")

