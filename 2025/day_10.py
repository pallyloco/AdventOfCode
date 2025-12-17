from __future__ import annotations
from sympy import Matrix, symbols, Symbol, Tuple
from sympy.solvers.solveset import linsolve

import re

from astar import DijkstraObject, AStar
# data = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
# [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
# [.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
# """
# data = list(map(str.rstrip,data.splitlines()))
fh = open("day_10.txt", "r")
data = list(map(str.rstrip, fh.readlines()))


def process_light_switches(line):
    match = re.match(r'(\[.*?])\s(.*?)(\{.*?})\s*$', line)
    final_light_str = match.group(1)
    initial_light_str = final_light_str.replace('#','.')

    wiring_str = match.group(2)
    joltage_str = match.group(3)
    final_jolts = list(map(int,(j for j in joltage_str[1:-1].split(","))))

    initial_state_lights = IndicatorState(initial_light_str, wiring_str)

    def is_final_light_state(state: IndicatorState) -> bool:
        return str(state) == final_light_str

    astar_lights = AStar(initial_state_lights)
    final_node_light = astar_lights.find_until(is_final_light_state)

    return final_node_light.cumulative_cost


def process_jolt_switches(line):
    # Parse the line
    match = re.match(r'(\[.*?])\s(.*?)(\{.*?})\s*$', line)
    wiring_str = match.group(2)
    joltage_str = match.group(3)
    final_jolts = list(map(int,(j for j in joltage_str[1:-1].split(","))))
    buttons =  tuple(tuple(int(a) for a in x[1:-1].split(",")) for x in wiring_str.split())


    return solve(final_jolts, buttons)

# ================================================================================================================
# get all possible solutions to reduced gaussian
# ================================================================================================================
def solve(jolts, buttons):
    a = matrix(jolts, buttons)
    max_pushes = tuple(get_max_button_pushes(index, a) for index in range(len(buttons)))

    # create the symbols necessary for this problem
    needed_symbols = {}
    for index in range(len(buttons)):
        needed_symbols[index] = symbols(f"b{index}")

    # solve the problem
    z = linsolve(a,list(needed_symbols.values()))
    eqn = z.args[0]

    # how many free variables do we have, and what are their indices?
    free_indices = [i for i,v in enumerate(eqn) if str(v).strip() == str(needed_symbols[i])]

    if len(free_indices) > 0:
        sums = set()
        loop_over(free_indices[0], free_indices[1:], sums, dict(), needed_symbols, a, eqn, max_pushes)
        return min(sums)
    return sum(list(eqn))


# ================================================================================================================
# loop over the free variables to find possible solutions
# ================================================================================================================
def loop_over(index:int, rest: list[int], sums: set[int], eqn_dict: dict[Symbol, int],
              needed_symbols: dict[int,Symbol], a:Matrix, eqn: Tuple, max_pushes):

    for num_pushes in range(max_pushes[index]+1):
        eqn_dict[needed_symbols[index]] = num_pushes
        if len(rest) != 0:
            loop_over(rest[0], rest[1:], sums, eqn_dict, needed_symbols, a, eqn, max_pushes)
        else:
            button_pushes = eqn.subs(eqn_dict)
            if any(push < 0 or not is_positive_int(push) for push in button_pushes):
                continue
            sums.add(int(sum(button_pushes)))

# ================================================================================================================
# get the maximum number of pushes for specified button
# ================================================================================================================
def get_max_button_pushes(button_index, a):
    min_button_push = 1e10
    for row_index in range(a.rows):
        if a[row_index,button_index] != 0:
            min_button_push = min(a[row_index,-1], min_button_push)
    if min_button_push == 1e10:
        return 0
    return min_button_push

# --------------------------------------------------------------------------------------------------------------------
# is x a positive integer (0->inf)
# --------------------------------------------------------------------------------------------------------------------
def is_positive_int(x:float) -> bool:
    return abs(x-int(x)) < 1e-5 and int(x) >= 0


# ================================================================================================================
# create matrix
# ================================================================================================================
def matrix(jolts, buttons) -> Matrix:
    A = []
    for index in range(len(jolts)):
        eqn = []
        for b_index,b in enumerate(buttons):
            if index in b:
                eqn.append(1)
            else:
                eqn.append(0)
        eqn.append(jolts[index] )
        A.append(eqn)
    return Matrix(A)

# ================================================================================================================
# toggle light switch
# ================================================================================================================
def toggle(light):
    n = "#" if light == "." else "."
    return n

# ================================================================================================================
# light indicator state (for using with part I dijkstra)
# ================================================================================================================
class IndicatorState(DijkstraObject):
    def __init__(self, light_str: str, wiring_str: str):
        self.wiring_str = wiring_str
        self.lights = list(light_str[1:-1])
        self.buttons = [ tuple(int(a) for a in x[1:-1].split(",")) for x in wiring_str.split()]

    def key(self) -> str:
        """string that uniquely defines this object"""
        return str(self)

    def activate_button(self, button) -> IndicatorState:
        lights = self.lights.copy()
        for wire in button:
            lights[wire] = toggle(lights[wire])
        return IndicatorState(f"[{''.join(lights)}]", self.wiring_str)

    def children(self) -> list[IndicatorState]:
        """list of neighbours"""
        next_states = []
        for b in self.buttons:
            next_states.append(self.activate_button(b))
        return next_states

    def edge_cost(self, prev: DijkstraObject):
        """How much does it cost to get from prev to self"""
        return 1

    def __str__(self):
        return f"[{''.join(self.lights)}]"

    def _repr__(self):
        return str(self)

    def eta(self, node=None):
        return 0


# ================================================================================================================
# Entry point
# ================================================================================================================

if __name__ == "__main__":
    ans1 = 0
    ans2 = 0
    for line in data:
        print(line)
        a = process_light_switches(line)
        ans1 += a
        b = process_jolt_switches(line)
        ans2 += b
        print(f"{a=} {ans1=}, {b=}, {ans2}")
    print(f"Answer: {ans1}, {ans2}")
