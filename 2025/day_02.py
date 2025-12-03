import re

data = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""
fh = open("day_02.txt", "r")
data = tuple(map(str.rstrip,fh.readlines()))[0]

ranges = ((int(x),int(y)) for x,y in (d.split("-") for d in data.split(",")))
ans1 = 0
ans2 = 0















for s,e in ranges:
    for i in range(s,e+1):
        if re.match(r"^(\d+)\1$", str(i)):
            ans1 = ans1 + i
        if re.match(r"(\d+)(\1)+$", str(i)):
            ans2 = ans2 + i
print(f"{ans1=} {ans2=}")