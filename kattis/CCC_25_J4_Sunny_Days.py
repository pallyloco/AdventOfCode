import itertools
import sys

def go(data):
    iter_data = iter(data)
    n = int(next(iter_data))

    summary = []
    prev = None
    count = 0
    c=None

    for _,c in zip(range(n), iter_data):
        if (c[0] == "S" and c[0] != prev) or (c[0] == "P" and c[0] != prev):
            if prev is not None:
                summary.append((count,prev))
            prev = c[0]
            count = 1
        else:
            count += 1
    summary.append((count,c[0]))


    if len(summary) == 1:
        if summary[0][1] == "S":
            return summary[0][0] - 1
        else:
            return 1

    most = 0

    for s1,p,s2 in itertools.zip_longest(summary, summary[1:], summary[2:]):
        if s1[1] != "S":
            most = max(most,1)
        elif p is not None and s2 is not None:
            if p[0] == 1:
                most = max(most, s1[0] + s2[0] + 1)
            else:
                most = max(most, s1[0]+1, s2[0]+1)
        else:
            most = max(most, s1[0]+1)
    return most

print(go(sys.stdin))
