from dataclasses import dataclass, field
from queue import PriorityQueue


class Node:
    def __init__(self,name,x,y):
        self.name=name
        self.x = x
        self.y = y
        self.f = 0


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: object = field()

q = PriorityQueue()
n = Node('a', 0, 0)
n.f = 1
n2 = Node('b', 0, 0)
n2.f = 0
n3 = Node('c', 0, 0)
n3.f = 1
q.put(PrioritizedItem(n.f, n))
q.put(PrioritizedItem(n2.f, n2))
q.put(PrioritizedItem(n3.f, n3))
