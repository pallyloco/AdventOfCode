# https://open.kattis.com/problems/closingtheloop
num_cases = int(input())
for case_number in range(1,num_cases+1):
    num_segments = int(input())
    segments = input().split(" ")

    # sort segments by colours
    red = [seg for seg in segments if seg[-1] == "R"]
    blue = [seg for seg in segments if seg[-1] == "B"]
    red.sort(key=lambda x: int(x[0:-1]))
    blue.sort(key=lambda x: int(x[0:-1]))

    # make longest chain
    chain = 0
    segs = 0
    while len(red) and len(blue):
        segs += 2
        red_seg = red.pop(-1)
        blue_seg = blue.pop(-1)
        chain = chain + int(red_seg[0:-1]) + int(blue_seg[0:-1])
    print(f"Case #{case_number}: {chain - segs}")

