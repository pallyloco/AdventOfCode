from __future__ import annotations

from typing import Optional

from MyRange import MyRange
import re

accepted = list()
rejected = list()


def main(part: int = 1):
    workflows: dict[str, list[str]] = dict()
    parts: list[Part] = list()
    file = open("day_19_input.txt", 'r')

    parts_flag = False
    for line in map(str.rstrip, file):
        if not parts_flag:
            if not line:
                parts_flag = True
                continue
            name, workflow = line.split("{")
            workflow = workflow.replace("}", "")
            workflows[name] = workflow.split(",")
            workflows[name][-1] = "True:" + workflows[name][-1]
        else:
            parts.append(eval(f"Part({line[1:-1]})"))

    for part in parts:
        process_workflow(part, workflows)

    print("answer 1:", sum((p.rating() for p in accepted)))

    # --------- Part 2
    n = XMASRange()
    r = find_combinations(workflows, n)
    print("answer 2:", r)
    pass


def find_combinations(workflows, xmas: XMASRange, workflow: str = "in", path: str = "") -> int:
    path = path + " -> " + workflow
    result = 0
    r=0
    xmasT = xmas.copy()
    xmasF = xmas.copy()
    for cond, next_node in (w.split(":") for w in workflows[workflow]):
        xmasT = xmasF.copy()
        xmasT.add_constraint(cond)

        if next_node == "A":
            print(path, xmasT, len(xmasT))
            result += len(xmasT)
        elif next_node == "R":
            pass
        else:
            result += find_combinations(workflows, xmasT, next_node, path)
            pass

        xmasF.add_not_constraint(cond)

    return result


def process_workflow(part: Part, workflows, workflow="in"):
    x = part.x
    m = part.m
    a = part.a
    s = part.s
    for cond, result in (w.split(":") for w in workflows[workflow]):
        if eval(cond):
            if result == "A":
                accepted.append(part)
            elif result == "R":
                rejected.append(part)
            else:
                process_workflow(part, workflows, result)
            break


class XMASRange:
    def __init__(self,
                 x:Optional[MyRange] = None,
                 m:Optional[MyRange] = None,
                 a:Optional[MyRange] = None,
                 s:Optional[MyRange] = None):
        self.x: MyRange[int] = x if x is not None else MyRange(1,4000)
        self.m: MyRange[int] = m if m is not None else MyRange(1,4000)
        self.a: MyRange[int] = a if a is not None else MyRange(1,4000)
        self.s: MyRange[int] = s if s is not None else MyRange(1,4000)
        self.easy_access: dict[str, MyRange[int]] = {
            'x': self.x,
            'm': self.m,
            'a': self.a,
            's': self.s
        }

    def testing(self):
        self.x.low = 13
        self.easy_access['m'].high = 59
        self.easy_access['a'].set_high(60)

    def copy(self) -> XMASRange:
        other: XMASRange = XMASRange(
            MyRange(self.x.low, self.x.high),
            MyRange(self.m.low, self.m.high),
            MyRange(self.a.low, self.a.high),
            MyRange(self.s.low, self.s.high)
        )
        return other

    def add_constraint(self, constraint: str, anti = False):
        m = re.match(r"([xmas])([><])(\d+)", constraint)
        if m is None:
            return
        xmas, condition, value = m.group(1, 2, 3)
        if not anti:
            if condition == ">":
                if not self.easy_access[xmas].set_low(int(value) + 1):
                    self.easy_access[xmas].set_to_zero()
            else:
                if not self.easy_access[xmas].set_high(int(value) - 1):
                    self.easy_access[xmas].set_to_zero()
        else:
            if condition == ">":
                if not self.easy_access[xmas].set_high(int(value)):
                    self.easy_access[xmas].set_to_zero()
            else:
                if not self.easy_access[xmas].set_low(int(value)):
                    self.easy_access[xmas].set_to_zero()

    def add_not_constraint(self, constraint: str):
        self.add_constraint(constraint,True)
        # m = re.match(r"([xmas])([><])(\d+)", constraint)
        # if m is None:
        #     return
        # xmas, condition, value = m.group(1, 2, 3)
        # if condition == ">":
        #     self.easy_access[xmas].set_high(int(value))
        # else:
        #     self.easy_access[xmas].set_low(int(value))

    def __len__(self):
        return len(self.x) * len(self.m) * len(self.a) * len(self.s)

    def __str__(self):
        return f"{self.x} {self.m} {self.a} {self.s}"

    def __repr__(self):
        return str(self)


class Part:
    def __init__(self, x, m, a, s):
        self.x: int = x
        self.m: int = m
        self.a: int = a
        self.s: int = s

    def rating(self) -> int:
        return self.x + self.m + self.a + self.s

    def __str__(self):
        return f"{self.x},{self.m},{self.a},{self.s}"

    def __repr__(self):
        return str(self)


if __name__ == "__main__":
    main()
