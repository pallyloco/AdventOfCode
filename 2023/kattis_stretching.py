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


def random_input() -> str:
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
    #print(s_string)
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

        #return all((c in trial_string for c in stats))


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


class State:
    def __init__(self, node: State_Node, index: int):
        self.node = node
        self.p_index = index
        self.s_index = 0
    def __str__(self):
        return f"{self.node} {self.p_index}"
    def __repr__(self):
        return str(self)


from enum import Enum


class State_Node(Enum):
    start = 1
    middle = 2
    end_of_s = 3
    end_of_p = 4
    end_of_both = 5


def get_next_state(p, index_p, s, index_s) -> tuple[State, ...]:
    #print(p[:index_p+2], s[:index_s+2], "... next states ",end="")
    states = list()

    if index_s + 1 == len(s):
        states.append (State(State_Node.end_of_s, -1))
    if index_p + 1 == len(p):
        states.append (State(State_Node.end_of_p, 0))
    if len(states) > 1:
        #print(states)
        return (State(State_Node.end_of_both, 0),)
    if len(states) > 0:
        #print(states)
        return tuple(states,)


    next_s_char = s[index_s + 1]

    if next_s_char == p[0]:
        states.append(State(State_Node.start, 0))

    if p[index_p+1] == s[index_s+1]:
        states.append(State(State_Node.middle, i + 1))

    #print(states)
    return tuple(states)




current_string = None
# def is_valid(s: str, p: str, index_s:int = 0, index_p:int = 0, stack: Optional[list]=None, state:Optional[State] = None, depth = 0) -> bool:
#     global current_string
#     if current_string is None:
#         current_string = s
#     if stack is None:
#         stack: list[State] = list()
#     stack = stack.copy()
#     if state is None:
#         state = State(State_Node.start,0)
#     stack.append(state)
#     #print (depth, index_p, index_s, stack)
#
#     states = get_next_state(p, index_p, s, index_s)
#     if len(states) == 0:
#         return False
#
#     for state_num, state in enumerate(states):
#         #print(state)
#         if state.node == State_Node.end_of_s:
#             print("State_Node.end_of_s: returning False")
#             return False
#         elif state.node == State_Node.end_of_both:
#             print("returning True")
#             return True
#         elif state.node == State_Node.end_of_p:
#             if len(stack) < len(p):
#                 print("State_Node.end_of_p: returning False")
#                 return False
# #            print ("popping", stack)
#             for i in range(len(p)):
#                 stack.pop()
# #            print("after popping", stack)
#             current_string = current_string[:index_s-5] + "------" + current_string[index_s+1:]
#             print(index_s, current_string)
#             last_state = stack[-1]
#             if not is_valid(s,p,index_s,last_state.p_index, stack,last_state):
#                 continue
#             return True
#         elif state.node == State_Node.middle:
#             if not is_valid(s,p,index_s+1,index_p+1, stack,state, depth+1):
#                 continue
#             return True
#         elif state.node == State_Node.start:
#             if not is_valid(s,p,index_s+1,0, stack, state, depth+1):
#                 continue
#             return True
#
# #    print ("Nothing true found")
#     return False
#

#@functools.cache
def is_valid2(s: str, p: str, not_repeating: set[str]) -> bool:

    #print (depth,"---",len(s), len(p), int(len(s)/len(p))*len(p))
    if len(s) == 0:
        return True
    state = False
    g=find_indices_for(s, p)
    for i in find_indices_for(s, p):
        if VERBOSE:
            pass
            #print (f"{len(s)} {i}")
        print(s[:i] + "-"*len(p) + s[i + len(p):])
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
def allowed_repeating(p):
    results = list()

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

def is_valid(s: str, p: str) -> bool:
    len_old = -1

    # simplistic approach
    while True:
        print(s, len(s)/len(p))
        indices = find_indices_for(s, p)

        # time to either bail out or do something new
        if len(s) > 0 and len(indices) == 0:
            return False
        if len(s) == len_old:
            print(s)
            break
        len_old = len(s)

        # adjust indices so that there are no overlapping groups
        new_indices = list()
        prev = -900
        for i in range(len(indices)-1):
            if prev + len(p) >= indices[i]:
                prev = indices[i]
            elif indices[i]+len(p) >= indices[i+1]:
                prev = indices[i]
            else:
                new_indices.append(indices[i])

        indices = new_indices
        substrings = list()
        index_s = 0
        diff = "-"*len(p)
        if len(indices) == 1:
            i = indices[0]
            substrings = [s[:i],s[i+len(p)]]
        else:
            for a in indices:
                substrings.append(s[index_s:a])
                index_s = a + len(p)
                print(s)
                print(diff.join(substrings))
            substrings.append(s[index_s:])
        print(s)
        print(diff.join(substrings))
        s = "".join(substrings)
        if len(s) == 0:
            return True

    print ("is still valid? ", s)

    return is_valid2(s,p)


def main():
    #s: str = input()
    p,s  = random_input()
    # s.rstrip()
    #p="dvuduv"
    #  012345678901234567890123456789
    #s="ddvuduvdvdvuduvdvdvuduvuduvdvudvuduvdvdvuduvuduvdvududdvuduvvuduvdvududvuduvvvdvududvuduvvduvuduvdvuduvvdvddvdvuduvuduvvudvuduvddvuduvdvuduvuvdvdvuddvuduvuvuddvududvuduvvuvdvuduvududvuduvvuddvuduvdvuduvuv"
    p="lzfftzflkktf"
    print(f"\n Answer: {p}")
    s = "lzflzfftlzfftzflkktfzflkktfftzflkktflzlzlzfftzflkktffftzflzfftzflkklzfftzflkktftflkktffftzflkklzfftzflkktftf"
    print(f"{s}")
    #s = "fwknfkfwknfkfkbamffnafkmfwknfkfkbamffnafkmwbwbfkbamfwknfkfwknfkfkbamffnafkmwbfkbamfffwknfkfkbamffnafkmwbnafkmwbffnafkmwb"
    #print("ans is", "wononw")
    #s = "wwwononwononwowonwononwononwwonwononwwnonwwwononwwononwononwwwwononwowononwnowononwnwowononwnowononwnw"
    start = s[0]
    end = s[-1]

    stats = dict(Counter(s))
    numbers = list(stats.values())
    gcd = math.gcd(*numbers)

    possibilities = list()
    original_stats = {k: v // gcd for k, v in stats.items()}
    min_length = len(s) // min(stats.values())

#    for i in range(len(s)):
    for i in range(2):
        stats = {k: v * (i + 1) for k, v, in original_stats.items()}
        min_length = sum((i for i in stats.values()))
        viable_words = get_viable_words(s, min_length, start, end, stats)
        not_allowed = get_non_repeating(p)
        #viable_words = ["dvuduv"]
        #print (len(s), min_length, int(len(s)/min_length)*min_length)
        if len(viable_words) == 0:
            continue
        for word in viable_words:
            #print( word)
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
