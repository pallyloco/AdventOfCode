from __future__ import annotations
import itertools as it
import math

data="""162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""
data = list(map(str.rstrip,data.splitlines()))
fh = open("day_08.txt", "r")
data = list(map(str.rstrip, fh.readlines()))
num_shortest_connections = 1000

def playground():
    boxes = list(map(JunctionBox, data))
    connections = []
    for b1,b2 in it.combinations(boxes,2):
        connections.append(Connection(b1,b2))
    connections.sort()
    pass

    circuits = []
    for i,c in enumerate(connections):
        if i == num_shortest_connections:
            answer1(circuits)
        circuits.append(Circuit(c))
        circuits = merge_circuits(circuits)
        if len(circuits) == 1 and len(circuits[0]) == len(boxes):
            answer2(c)
            break

    # part 2
    # while True:
    #     circuits = [c for c in circuits if len(c) > 0]

def merge_circuits(circuits):
    for index in range(1,len(circuits)):
        new_circuit = circuits[index-1]
        for c in circuits[index:]:
            if new_circuit in c:
                c+= new_circuit
                new_circuit.clear()
                break
    return  [c for c in circuits if len(c) > 0]

def answer2(c:Connection):
    print(f"Anser 2: {c.box1.x * c.box2.x}")
def answer1(circuits):
    ans1 = 1
    for i,c in enumerate(sorted(circuits, reverse=True)):
        ans1 *= len(c)
        if i == 2:
            break
    print(ans1)

class Connection:
    def __init__(self, box1: JunctionBox, box2: JunctionBox):
        # always sort boxes, makes it easier for comparisons, etc
        boxes = [box1,box2]
        boxes.sort()
        self.box1, self.box2 = boxes
        self.distance = box1.distance(box2)

    def __eq__(self, other):
        return str(self) == str(other)

    def __lt__(self, other):
        return self.distance < other.distance

    def __str__(self):
        return f"{self.box1}:{self.box2} - {self.distance}"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(str(self))

class JunctionBox:

    def __init__(self, line:str):
        x,y,z = map(int,line.split(","))
        self.x: int = x
        self.y: int = y
        self.z: int = z
        self.connected_to = []

    def distance(self, other):
        t = (self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2
        #return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)
        return math.sqrt(t)

    def __str__(self):
        return f"({self.x},{self.y},{self.z})"

    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        return (self.x, self.y, self.z) < (other.x, other.y, other.z)


class Circuit:
    def __init__(self, connection: Connection = None):
        if connection is None:
            self.boxes = set()
            self.connections = set()
        else:
            self.boxes = {connection.box1, connection.box2}
            self.connections = {connection}

    def clear(self):
        self.boxes = set()
        self.connections = set()

    def add(self, connection: Connection):
        self.boxes.add(connection.box1)
        self.boxes.add(connection.box2)
        self.connections.add(connection)
        return self

    def __add__(self, other):
        new_circuit = Circuit()
        for c in self.connections:
            new_circuit.add(c)
        for c in other.connections:
            new_circuit.add(c)
        return other

    def __iadd__(self, other):
        self.boxes.update(other.boxes)
        self.connections.update(other.connections)
        return self

    def __contains__(self, item):
        return not self.boxes.isdisjoint(item.boxes)

    def __len__(self):
        return len(self.boxes)

    def __repr__(self):
        return f"Circuit: size ({len(self)})"

    def __str__(self):
        return f"size ({len(self)}){" ".join(sorted(map(str, self.boxes)))}"

    def __lt__(self, other):
        return len(self) < len(other)




if __name__ == "__main__":
    playground()
