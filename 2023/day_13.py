import itertools as it
from typing import TextIO, NewType, Any


def main(part: int = 1):
    file = open("day_13_input.txt", 'r')
    ans1 = 0
    ans2 = 0
    for para in read_paragraph(file):
        h_old, v_old = (-1, -1)
        lines = [l for l in para if len(l) != 0]
        if len(lines) > 0:
            ht, vt = find_mirror(lines)
            for h in ht:
                ans1 += (h + 1) * 100
                h_old = h
            for v in vt:
                ans1 += (v + 1)
                v_old = v

        # have to find a new line of reflection, assuming 1 smudge
        done = False

        for row, line in enumerate(lines):
            if done:
                break
            for col, c in enumerate(line):
                if done:
                    break
                l = lines[row]
                a = l[:col]
                b = toggle(l[col])
                c = l[col + 1:]
                nl = a + b + c
                lines[row] = nl
                hn, vn = find_mirror(lines)

                for h in hn:
                    if h != h_old:
                        ans2 += (h + 1) * 100
                        done = True
                for v in vn:
                    if v != v_old:
                        ans2 += (v + 1)
                        done = True

                l = lines[row]
                nl = l[:col] + toggle(l[col]) + l[col + 1:]
                lines[row] = nl

    print("Answer 1:", ans1)
    print("Answer 2:", ans2)


def toggle(c: str) -> str:
    if c == "#": return "."
    return "#"


def find_mirror(lines: list[str]) -> tuple[tuple, tuple]:
    horizontal: list[bool] = [True] * (len(lines) - 1)
    vertical: list[bool] = [True] * (len(lines[0]) - 1)

    for row, (before, after) in enumerate(it.pairwise(lines)):
        for col, (c, d) in enumerate(it.pairwise(before)):
            if vertical[col] and c != d:
                vertical[col] = False
            if before[col] != after[col]:
                horizontal[row] = False

    for col, (c, d) in enumerate(it.pairwise(lines[-1])):
        if c != d:
            vertical[col] = False

    for col, tf in enumerate(vertical):
        if not tf:
            continue
        for line in lines:
            if vertical[col]:
                for c1, c2 in zip(reversed(line[:col + 1]), line[col + 1:]):
                    if c1 != c2:
                        vertical[col] = False
                        break

    for row, tf in enumerate(horizontal):
        if not tf:
            continue
        for l1, l2 in zip(reversed(lines[:row + 1]), lines[row + 1:]):
            if l1 != l2:
                horizontal[row] = False
                break

    return safe_index(horizontal, True), safe_index(vertical, True)


# part 2 too low: 37718
def safe_index(l: list[Any], value: Any) -> tuple:
    return tuple(ind for ind, ele in enumerate(l) if ele == value)


# ============================================================================
# read lines until a blank line
# ============================================================================
def read_paragraph(file: TextIO) -> list[str]:
    lines: list[str] = list()
    for line in map(str.rstrip, file):
        lines.append(line)
        if not line and len(lines) > 0:
            yield lines
            lines.clear()
    yield lines


if __name__ == "__main__":
    main()
