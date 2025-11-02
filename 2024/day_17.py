from reading import read_paragraphs
import re
import itertools as it

input_data = [
    "Register A: 729",
    "Register B: 0",
    "Register C: 0",
    "",
    "Program: 0,1,5,4,3,0",
]

input_data = [
    "Register A: 33024962",
    "Register B: 0",
    "Register C: 0",
    "",
    "Program: 2,4,1,3,7,5,1,5,0,3,4,2,5,5,3,0",
]

input_data = [
    "Register A: 216584205979245",
    "Register B: 0",
    "Register C: 0",
    "",
    "Program: 2,4,1,3,7,5,1,5,0,3,4,2,5,5,3,0",
]
"""
start:
    bst 4  # B = A % 8       (2,4)
    bxl 3  # B = B ^ 3       (1,3)
    cdv 5  # C = A // (2^B)  (7,5)
    bxl 5  # B = B ^ 5       (1,5)
    adv 3  # A = A // (2^3)  (0,3)
    bxc 2  # B = C ^ B       (4,2)
    out 5  # print(B%8)      (5,5)
    jnz 0  # jump start if A != 0 (3,0) 
"""


def main(data):
    outputs = run_program(216584205979245)
    print(",".join(map(str, outputs)))


def run_program(a):
    outputs = []
    while a != 0:
        b1 = (a & 7)
        b1 = b1 ^ 3
        c = a >> b1
        b2 = (b1 ^ 5 ^ c) & 7
        outputs.append(b2)
        a = a >> 3
    return outputs


def find_sequenced_output():
    output = [2, 4, 1, 3, 7, 5, 1, 5, 0, 3, 4, 2, 5, 5, 3, 0]
    output.reverse()
    a_try = {0}

    for k in output:
        new_a_list = set()
        for a in a_try:
            a_list = produces(k, a)
            new_a_list.update(a_list)
        a_try = new_a_list.copy()
    return sorted(list(a_try))[0]


def produces(k, start_a):
    possibilities = []
    start_a = start_a << 3
    for i in range(8):
        a = start_a + i
        output = run_program(a)
        if len(output) > 0 and output[0] == k:
            possibilities.append(a)
    return possibilities


def foo2(k, a):
    a = a << 3
    n3 = a // 64
    n2 = a // 8

    possible_as = []
    for n1 in range(8):
        b2 = (n1 ^ 3) ^ 5 ^ ((8 * n2 + n1) >> (n1 ^ 3))

        if k == b2 & 7:
            a = 64 * n3 + 8 * n2 + n1
            b1 = n1 ^ 3
            c = a >> (n1 ^ 3)
            possible_as.append(a)
    return possible_as


main(input_data)
print(find_sequenced_output())
