from __future__ import annotations

import itertools
from collections import Counter
import random
from typing import Optional

import math
import functools

alphabet = "abcdefghijklmnopqrstuvwxyz"

p_string = ""
VERBOSE = True


def random_input() -> tuple[str,str]:
    global p_string
    p_string = ""
    for i in range(random.randint(1, 10)):
        p_string += random.choice(alphabet)

    # duplicate letters and rearrange
    p_list = [c for c in p_string + p_string]
    random.shuffle(p_list)
    p_string = "".join(p_list)
    n = int(100 / len(p_string))
    s_string = p_string
    for _ in range(n):
        i = random.choice(range(len(s_string) + 1))
        s_string = s_string[:i] + p_string + s_string[i:]
    return p_string, s_string


@functools.cache
def find_subsets(string, n) -> tuple[int, str]:
    for i in range(len(string) - n + 1):
        yield i, string[i:i + n]


def get_viable_words(s, min_length, start, end, stats):
    get_words = find_subsets(s, min_length)
    results: dict[str, list[int]] = {}
    for index, trial_string in get_words:
        if not possible(s,trial_string, start, end, stats):
            continue
        if trial_string not in results:
            results[trial_string] = []
        results[trial_string].append(index)
    return results


def possible(s,trial_string, start, end, stats) -> bool:

    if trial_string[0] == start and trial_string[-1] == end:
        short_stats = dict(Counter(trial_string))
        if short_stats == stats:
            for ss in get_non_repeating(trial_string):
                if ss in s:
                    return False
            return True

@functools.cache
def find_indices_for(s: str, p: str) -> list[int]:
    i = 0
    results = list()
    while True:
        i = s.find(p, i)
        if i < 0:
            break
        results.append(i)
        i += 1
    return results

#@functools.cache
def is_valid2(s: str, p: str, not_repeating: set[str], depth = 0) -> bool:

    #print (depth,"---",len(s), len(p), int(len(s)/len(p))*len(p))
    if len(s) == 0:
        return True
    state = False
    for i in find_indices_for(s, p):
        if VERBOSE:
            pass
            #print (f"{len(s)} {i}")
        print(f"{depth: 10}",s[:i] + "-"*len(p) + s[i + len(p):])
        t = s[:i] + s[i + len(p):]
        if len(t) == 0:
            return True
        if t[0] != p[0]:
            return False
        if t[-1] != p[-1]:
            return False
        if i > 0 and i+len(p) < len(s) and s[i-1] + s[i + len(p)] in not_repeating:
            return False
        state = state or is_valid2(t, p, not_repeating,depth+1)
        if state:
            return True
    return False


def is_valid(s: str, p: str, not_repeating: set[str]) -> bool:
    if len(s) == 0:
        return True
    state = False
    for i in find_indices_for(s, p):
        if VERBOSE:
            pass
        t = s[:i] + s[i + len(p):]
        if len(t) == 0:
            return True
        if t[0] != p[0]:
            return False
        if t[-1] != p[-1]:
            return False
        if i > 0 and i+len(p) < len(s) and s[i-1] + s[i + len(p)] in not_repeating:
            return False
        state = state or is_valid2(t, p, not_repeating)
        if state:
            return True
    return False

def get_non_repeating(p):
    not_allowed = set()
    allowed = set()
    first_char = p[0]
    for c1 in p:
        if c1 == p[-1]:
            continue
        for c2 in p:
            substring = c1+c2
            if c2 == first_char:
                allowed.add(substring)
            elif c1+c2 in p:
                allowed.add(substring)
            else:
                not_allowed.add(substring)
    return not_allowed

def main():
    #s: str = input()
    p,s  = random_input()
    s.rstrip()
    print(p)
    print(f"{s}")
    p = "hbbh"
    s = "hhbbhbhbhbbhbhbhhbhbbhhbbhbbhhbhbbhhbhbhbbhbhbbhhbhhhbbhhbbhbhhbbhbbhbbhhbhhbhbbhhbhbbhbhbhbbhhhhhbbhbbh"
    start = s[0]
    end = s[-1]


    stats = dict(Counter(s))
    numbers = list(stats.values())
    gcd = math.gcd(*numbers)

    possibilities = list()
    original_stats = {k: v // gcd for k, v in stats.items()}
    min_length = len(s) // min(stats.values())

    for i in range(len(s)):
#    for i in range(2):
        stats = {k: v * (i + 1) for k, v, in original_stats.items()}
        min_length = sum((i for i in stats.values()))
        viable_words = get_viable_words(s, min_length, start, end, stats)
        not_allowed = get_non_repeating(p)
        if len(viable_words) == 0:
            continue
        print (f"viable words: {viable_words}")
        for word in viable_words:
            print( f"testing {word}")
            if True:
                if is_valid2(s, word, not_allowed):
                    possibilities.append(word)

        if len(possibilities) != 0:
            print("found")
            break
    possibilities.sort()
    print(possibilities)
    return possibilities[0]


for i in range(1):
    x = main()
    print(f"the answer is {x}")
    #if x != p_string:
    #    break

"""
pchhcppchhpcpchhcphhcppchhppchhcppchhcpcpchhcphhpchhcppchhpchhcpcpcppchhcppchhpchhcpcpcpchhcpchhcpppcp
pchhcp
hbbh
hhbbhbhbhbbhbhbhhbhbbhhbbhbbhhbhbbhhbhbhbbhbhbbhhbhhhbbhhbbhbhhbbhbbhbbhhbhhbhbbhhbhbbhbhbhbbhhhhhbbhbbh
hbhbhbbhbhbhhbhbbhhbbhbbhhbhbbhhbhbhbbhbhbbhhbhhhbbhhbbhbhhbbhbbhbbhhbhhbhbbhhbhbbhbhbhbbhhhhhbbhbbh

"""