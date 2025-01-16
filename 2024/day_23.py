from __future__ import annotations
import itertools as it

input_data = [
    "kh-tc",
    "qp-kh",
    "de-cg",
    "ka-co",
    "yn-aq",
    "qp-ub",
    "cg-tb",
    "vc-aq",
    "tb-ka",
    "wh-tc",
    "yn-cg",
    "kh-ub",
    "ta-co",
    "de-co",
    "tc-td",
    "tb-wq",
    "wh-td",
    "ta-ka",
    "td-qp",
    "aq-cg",
    "wq-ub",
    "ub-vc",
    "de-ta",
    "wq-aq",
    "wq-vc",
    "wh-yn",
    "ka-de",
    "kh-ta",
    "co-tc",
    "wh-qp",
    "tb-vc",
    "td-yn",
]

fh = open("day_23.txt", "r")
input_data = list(map(str.rstrip, fh))


class Node:
    def __init__(self, name):
        self.name = name
        self.links: set[Node] = set()

    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(str(self))

    def __lt__(self, other):
        return self.name < other.name


def main(data):
    all_nodes: dict[str, Node] = {}
    sets_of_three: set[tuple[Node, Node, Node]] = set()
    any_set: set[tuple[Node,...]] = set()
    max_size_set = 3

    for link in data:
        n1, n2 = link.split("-")
        for node_name in (n1, n2):
            if node_name not in all_nodes:
                all_nodes[node_name] = Node(node_name)
        all_nodes[n1].links.add(all_nodes[n2])
        all_nodes[n2].links.add(all_nodes[n1])

    for node in all_nodes.values():
        if len(node.links) > 1:
            for n1, n2, n3 in it.combinations(sorted([node, *node.links]), 3):
                if n1 in n2.links and n1 in n3.links and n2 in n3.links:
                    sets_of_three.add((n1, n2, n3))

            for set_size in range(max_size_set, len(node.links)+2):
                for ns in it.combinations(sorted([node, *node.links]), set_size):
                    valid_network = True
                    for n1,n2 in it.combinations(ns,2):
                        if n1 not in n2.links:
                            valid_network = False
                            break
                    if valid_network:
                        any_set.add(ns)
                        max_size_set = len(ns)

    ans = 0
    for threesome in sets_of_three:
        if any((n.name[0]=='t' for n in threesome)):
            ans += 1
    print(ans)
    ans2 = [s for s in any_set if len(s)==max_size_set]
    print(ans2)


main(input_data)
