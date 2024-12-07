from __future__ import annotations

import itertools

# ==========================================================================
# global variables
# ==========================================================================
edges: dict[str, Edge] = {}
all_nodes: dict[str, Node] = {}
k = 0.3  # spring constant
N = 0  # natural length of the spring
g = -10  # gravitational pull
ROUNDING = 1  # precision required for y coordinate


# ==========================================================================
# Edge
# ==========================================================================
class Edge:
    def __init__(self, n1: Node, n2: Node):
        self.n1: Node = n1
        self.n2: Node = n2

    def crosses_over(self, y):
        y = round(y, ROUNDING)
        ys = sorted([round(self.n1.y, ROUNDING), round(self.n2.y, ROUNDING)])
        return ys[0] <= y < ys[1]

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
        self.y = 300
        self.connections: set[Node] = set()
        self.fixed = False

    def add_connection(self, node: Node):
        self.connections.add(node)

    def forces(self):
        f = g
        for n in self.connections:
            l = abs(self.y - n.y)
            F = k * (N - l) if self.y > n.y else -k * (N - l)
            f = f + F
        return f

    def adjust_position(self):
        if self.fixed:
            return
        f = self.forces()
        self.y = self.y + f


# ==========================================================================
# Get a list of unique y positions of all nodes
# ==========================================================================
def get_all_ys() -> list[int]:
    ys = set()
    for node in all_nodes.values():
        ys.add(round(node.y, ROUNDING))
    return sorted(ys, reverse=True)


# ==========================================================================
# Find a y position and edges, where only 3 edges cross the y value
# ==========================================================================
def find_snip_points() -> tuple[float, list[Edge]]:
    for y in get_all_ys():
        e = [e for e in edges.values() if e.crosses_over(y)]
        if len(e) == 3:
            return y, e
    return 0, []


# ==========================================================================
# read the input
# ==========================================================================
def decipher_inputs(lines: list[str]):
    """Note: first node read will be fixed."""
    edges.clear()
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

    # once we have all the nodes, define all the edges
    set_edges()


# ==========================================================================
# once we have all the nodes, figure out all the edges
# ==========================================================================
def set_edges():
    for node in all_nodes.values():
        for child in node.connections:
            key = str(sorted([node.name, child.name]))
            edges[key] = Edge(node, child)
    return edges


# ==========================================================================
# adjust all of the nodes based on the forces on each node
# ==========================================================================
def adjust():
    movement = 0
    for node in all_nodes.values():
        y_old = node.y
        node.adjust_position()
        movement = movement + abs(y_old - node.y)
    return movement


# ==========================================================================
# main program
# ==========================================================================
def main():
    with open("day_25_input.txt", "r") as file:
        LINES: list[str] = list(map(str.rstrip, file.readlines()))
    decipher_inputs(LINES)

    while adjust() / len(all_nodes) >= 0.5:
        pass

    y, e = find_snip_points()

    total_nodes = len(all_nodes)
    top_nodes = [n for n in all_nodes.values() if round(n.y, ROUNDING) <= y]
    answer = len(top_nodes) * (total_nodes - len(top_nodes))
    print(answer)


if __name__ == "__main__":
    main()
