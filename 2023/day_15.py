import re

class Lens:
    def __init__(self, label: str, focal: int):
        self.focal: int = focal
        self.label: str = label

    def __eq__(self, other):
        return self.label == other.label

    def __str__(self):
        return f"[{self.label} {self.focal}]"

    def __repr__(self):
        return str(self)


def main(part: int = 1):
    file = open("day_15_input.txt", 'r')
    ans1 = 0
    hashmap: list[list[Lens]] = [[] for i in range(256)]

    for line in map(str.rstrip, file):
        for s in re.split("[,]", line):

            # part 1
            ans1 = ans1 + my_hash(s)

            # part 2
            m = re.search(r"(.*)([-=])(.*)", s)
            label = m.group(1)
            action = m.group(2)
            value = m.group(3)

            if action == "-":
                remove_lens(Lens(label, 0), hashmap)
            else:
                insert_lens(Lens(label, int(value)), hashmap)

    print("answer 1:", ans1)

    ans2 = 0
    for box in range(256):
        for slot, lens in enumerate(hashmap[box]):
            ans2 += (box + 1) * (slot + 1) * lens.focal
    print("answer 2:", ans2)


def remove_lens(lens: Lens, hashmap: list[list[Lens]]):
    box = my_hash(lens.label)
    hashmap[box] = [l for l in hashmap[box] if l != lens]


def insert_lens(lens: Lens, hashmap: list[list[Lens]]):
    box = my_hash(lens.label)
    if lens in hashmap[box]:
        hashmap[box] = [l if l != lens else lens for l in hashmap[box]]
    else:
        hashmap[box].append(lens)


def my_hash(s: str) -> int:
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h = h & 255
    return h


if __name__ == "__main__":
    main()
