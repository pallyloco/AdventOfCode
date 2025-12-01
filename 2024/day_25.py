from reading import read_paragraphs
import itertools as it

input_data = [
    "#####",
    ".####",
    ".####",
    ".####",
    ".#.#.",
    ".#...",
    ".....",
    "",
    "#####",
    "##.##",
    ".#.##",
    "...##",
    "...#.",
    "...#.",
    ".....",
    "",
    ".....",
    "#....",
    "#....",
    "#...#",
    "#.#.#",
    "#.###",
    "#####",
    "",
    ".....",
    ".....",
    "#.#..",
    "###..",
    "###.#",
    "###.#",
    "#####",
    "",
    ".....",
    ".....",
    ".....",
    "#....",
    "#.#..",
    "#.#.#",
    "#####",
]


fh = open("day_25.txt", "r")
input_data = list(map(str.rstrip, fh))

def main(data):
    templates = read_paragraphs(data)
    keys = []
    locks = []
    for template in templates:
        if template[0] == ".....":
            read_key(template, keys)
        else:
            read_lock(template, locks)

    ans = 0
    for key,lock in it.product(keys, locks):
        trial = [a+b for a, b in zip(key, lock)]
        if all((a < 6 for a in trial)):
            ans += 1
    print(ans)
    pass



def read_key(template: list[str], keys):
    pins = [0, 0, 0, 0, 0]
    for i,pin_template in enumerate(template):
        for j, pin in enumerate(pin_template):
            if pin == "#":
                pins[j] = max(pins[j], 6-i)
    keys.append(pins)
    pass


def read_lock(template: list[str], locks):
    pins = [0, 0, 0, 0, 0]
    for i, pin_template in enumerate(template):
        for j, pin in enumerate(pin_template):
            if pin == "#":
                pins[j] = max(pins[j], i)
    locks.append(pins)
    pass



main(input_data)
