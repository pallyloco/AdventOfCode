# https://open.kattis.com/problems/set
cards = list()
cards.extend(input().split(" "))
cards.extend(input().split(" "))
cards.extend(input().split(" "))
cards.extend(input().split(" "))
sets = set()
for i in range(12):
    for j in range(12):
        if i == j: continue
        for k in range(12):
            if i == k or j == k: continue
            A = set((cards[i][0], cards[j][0], cards[k][0]))
            if len(A) == 2: continue
            B = set((cards[i][1], cards[j][1], cards[k][1]))
            if len(B) == 2: continue
            C = set((cards[i][2], cards[j][2], cards[k][2]))
            if len(C) == 2: continue
            D = set((cards[i][3], cards[j][3], cards[k][3]))
            if len(D) == 2: continue

            this = sorted([i+1, j+1, k+1])
            sets.add(tuple(this))

if sets:
    for s in sorted(sets):
        print(s[0], s[1], s[2])
else:
    print ("no sets")