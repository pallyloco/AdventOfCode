"""
Solves day 25 (https://adventofcode.com/2023/day/25) using the following physics
1. Assume all nodes are connected by springs
2. Fix one node's position (cannot move)
3. Until movement becomes minimal
    a. Apply a gravitational pull on each node
    b. Add all forces from springs attached to node
    c. Adjust position accordingly
4. Look for any "y" value that cuts through ONLY three springs
5. Cut those springs and you now have two distinct networks

IMPROVEMENT
* Made it 2d
* Made graphics to go with it
"""

from __future__ import annotations

import itertools
import math
import tkinter as tk
import random

mw = tk.Tk()

# ==========================================================================
# global variables
# ==========================================================================
springs: dict[str, Spring] = {}
all_nodes: dict[str, Node] = {}
k = 2  # spring constant
N = 35  # natural length of the spring
g = -1  # gravitational pull
# these numbers were determined by the above numbers
min_x = -100
max_x = 100
min_y = -600
max_y = 50
scale = 1
ROUNDING = 1  # precision required for x,y coordinate

# ==========================================================================
# set up the canvas
# ==========================================================================
canvas = tk.Canvas(mw, width = max((max_x-min_x)*2, (max_y-min_y)*2),
                   height = max((max_x-min_x)*2, (max_y-min_y)*2))
canvas.pack(expand=1, fill='both')
def coordinate_conversion_to_canvas(x,y) -> tuple[float, float]:
    x_canvas = scale*(x+(max_y-min_y)/2)
    y_canvas = scale*(max_y - y)
    return x_canvas, y_canvas

# ==========================================================================
# Spring
# ==========================================================================
class Spring:
    def __init__(self, n1: Node, n2: Node):
        self.n1: Node = n1
        self.n2: Node = n2
        self.canvas_obj = canvas.create_line(n1.x,n1.y, n2.x, n2.y)

    def crosses_over(self, y):
        y = round(y, ROUNDING)
        ys = sorted([round(self.n1.y, ROUNDING), round(self.n2.y, ROUNDING)])
        return ys[0] <= y < ys[1]

    def move(self):
        obj_id = self.canvas_obj
        x0,y0 = coordinate_conversion_to_canvas(self.n1.x, self.n1.y)
        x1,y1 = coordinate_conversion_to_canvas(self.n2.x, self.n2.y)

        canvas.coords(obj_id, x0, y0, x1, y1)

    def __str__(self):
        return f"{self.n1.name}-{self.n2.name} {str(abs(self.n1.x - self.n2.x))}"

    def __repr__(self):
        return str(self)


# ==========================================================================
# Node
# ==========================================================================
class Node:
    def __lt__(self, other):
        return round(self.y, ROUNDING) < round(other.y, ROUNDING)

    def __eq__(self, other):
        return round(self.y, ROUNDING) == round(other.y, ROUNDING)

    def __str__(self):
        return f"{self.name} {round(self.y, ROUNDING)}"

    def __hash__(self):
        return hash(str(self))

    def __init__(self, name: str):
        self.name = name
        self.y = 0
        self.x = 0
        self.new_x = 0
        self.new_y = 0
        self.connections: set[Node] = set()
        self.fixed = False

    def add_connection(self, node: Node):
        self.connections.add(node)

    def forces(self) -> tuple[float, float]:
        f_y = 0
        f_x = 0
        if self.name == "rkj":
            pass
        for n in self.connections:
            l_y = abs(self.y - n.y)
            l_x = abs(self.x - n.x)
            l = math.sqrt(l_y**2 + l_x**2)
            if l > 1:
                N_x = (N - l) * l_x / l if l > 0 else N
                N_y = (N - l) * l_y / l if l > 0 else N
            else:
                theta = random.uniform(0,2*math.pi)
                N_x = N * math.cos(theta)
                N_y = N * math.sin(theta)
            F_y = k * N_y if self.y > n.y else -k * N_y
            f_y = f_y + F_y
            F_x = k * N_x if self.x > n.x else -k * N_x
            f_x = f_x + F_x
        return f_x/10,(f_y+g)/10

    def adjust_position(self):
        if self.fixed:
            return
        f_x,f_y = self.forces()
        self.new_y = self.y + f_y
        self.new_x = self.x + f_x

    def update_position(self):
        self.x = self.new_x
        self.y = self.new_y

# ==========================================================================
# Get a list of unique y positions of all nodes
# ==========================================================================
def get_all_ys() -> list[int]:
    ys = set()
    for node in all_nodes.values():
        ys.add(round(node.y, ROUNDING))
    return sorted(ys, reverse=True)


# ==========================================================================
# Find a y position and springs, where only 3 springs cross the y value
# ==========================================================================
def find_snip_points() -> tuple[float, list[Spring]]:
    for y in get_all_ys():
        e = [e for e in springs.values() if e.crosses_over(y)]
        if len(e) == 3:
            return y, e
    return 0, []


# ==========================================================================
# read the input
# ==========================================================================
def decipher_inputs(lines: list[str]):
    """Note: first node read will be fixed."""
    springs.clear()
    all_nodes.clear()
    did_fix = False

    for line in lines:
        node_names = line.split(" ")

        # find the anchor
        anchor_name = node_names[0].replace(":", "")
        if anchor_name not in all_nodes:
            all_nodes[anchor_name] = Node(anchor_name)
        anchor = all_nodes[anchor_name]
        all_nodes[anchor_name] = anchor

        if not did_fix:
            anchor.fixed = True
            did_fix = True

        # attach all other nodes to the anchor
        for node_name in node_names[1:]:
            if node_name not in all_nodes:
                all_nodes[node_name] = Node(node_name)
            node = all_nodes[node_name]
            all_nodes[node_name] = node
            anchor.add_connection(node)
            node.add_connection(anchor)

    # once we have all the nodes, define all the springs
    set_springs()


# ==========================================================================
# once we have all the nodes, figure out all the springs
# ==========================================================================
def set_springs():
    for node in all_nodes.values():
        for child in node.connections:
            key = str(sorted([node.name, child.name]))
            springs[key] = Spring(node, child)
    return springs


# ==========================================================================
# adjust all of the nodes based on the forces on each node
# ==========================================================================
def adjust(iteration):
    movement = 0
    for node in all_nodes.values():
        y_old = node.y
        node.adjust_position()
        movement = movement + abs(y_old - node.new_y)
    for node in all_nodes.values():
        node.update_position()
    if iteration%10 == 0:
        for e in springs.values():
            e.move()
    mw.update()
    return movement

# ==========================================================================
# main program
# ==========================================================================
def main():
    with open("day_25_input.txt", "r") as file:
        LINES: list[str] = list(map(str.rstrip, file.readlines()))
    decipher_inputs(LINES)

    a = adjust(0)
    for iteration in itertools.count():
        if a/len(all_nodes) < 0.01:
            break
        a = adjust(iteration)

    y, e = find_snip_points()

    total_nodes = len(all_nodes)
    top_nodes = [n for n in all_nodes.values() if round(n.y, ROUNDING) <= y]
    answer = len(top_nodes) * (total_nodes - len(top_nodes))
    print(answer)


if __name__ == "__main__":
    main()
    input("Press enter to exit program")
