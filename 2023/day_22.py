from __future__ import annotations
import re

supports: dict[Brick, list[Brick]] = dict()
bricks: list[Brick] = list()
supported_by: dict[Brick, list[Brick]] = dict()

def main():
    file = open("day_22_input.txt", 'r')
    for line in map(str.rstrip, file):
        bricks.append(Brick(line))
    bricks.sort()

    # go through each brick, and make it fall down if necessary
    for brick in bricks:
        if brick.z1 == 0:
            continue
        lower_bricks = [b for b in bricks if b != brick and brick.on_top_of(b)]
        if len(lower_bricks):
            lower_bricks.sort(key=lambda x: x.z2, reverse=True)
            brick.fall(brick.z1 - lower_bricks[0].z2 - 1)
        else:
            brick.fall(brick.z1)

    # which bricks support which bricks?
    bricks.sort()

    for brick in bricks:
        supports[brick] = [b for b in bricks if b != brick and b.z1 == brick.z2 + 1 and b.on_top_of(brick)]

    for brick in bricks:
        supported_by[brick] = [b for b in bricks if b != brick and b.z2 == brick.z1 - 1 and brick.on_top_of(b)]

    ans2 = 0
    zeros = 0
    for brick in bricks:
        ans = who_falls_if(brick)
        print (brick, ans)
        ans2 = ans2 + ans
        if not ans:
            zeros+=1
    print("Answer 1:",zeros,"Answer 2:", ans2)


def who_falls_if(brick: Brick):
    above_layer: set[Brick] = set()
    below_layer: set[Brick] = {brick}
    ans = 0

    fallen = {brick}

    while True:
        for b in below_layer:
            for supported_block in supports[b]:
                s = set(supported_by[supported_block]) - fallen
                if len(s) == 0:
                    above_layer.add(supported_block)
                    fallen.add(supported_block)
        ans = ans + len(above_layer)
        if len(above_layer) == 0:
            break
        below_layer = above_layer
        above_layer = set()

    return len(fallen)-1


class Brick:
    def __init__(self, descr: str):
        x1, y1, z1, x2, y2, z2 = re.search(r"(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)", descr).groups()
        self.x1 = min(int(x1), int(x2))
        self.x2 = max(int(x1), int(x2))
        self.y1 = min(int(y1), int(y2))
        self.y2 = max(int(y1), int(y2))
        self.z1 = min(int(z1), int(z2))
        self.z2 = max(int(z1), int(z2))

    def fall(self, distance: int):
        self.z1 = self.z1 - distance
        self.z2 = self.z2 - distance

    def on_top_of(self, other: Brick) -> bool:
        if self.z2 < other.z1:
            return False
        if self.x2 < other.x1 or other.x2 < self.x1 \
                or self.y2 < other.y1 or other.y2 < self.y1:
            return False
        return True

    def __hash__(self):
        return hash(str(self))

    def __lt__(self, other):
        if self.z1 == other.z1:
            if self.y1 == other.y1:
                return self.x1 < other.x1
            else:
                return self.y1 < other.y1
        else:
            return self.z1 < other.z1

    def __eq__(self, other):
        return str(self) == str(other)

    def __str__(self):
        return f"{self.x1},{self.y1},{self.z1}~{self.x2},{self.y2},{self.z2}"

    def __repr__(self):
        return str(self)


if __name__ == "__main__":
    main()
