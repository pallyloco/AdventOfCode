from __future__ import annotations
from dataclasses import dataclass, field
import heapq

@dataclass
class Node:
    row:int
    col:int
    accumulated_cost:int
    visited:bool = False

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Node=field(compare=False)

def cost(row,col):
    c= ((row-1)*max_col + col)%max_num
    return c if c!=0 else max_num

max_row = int(input())
max_col = int(input())
max_num = int(input())
max_col = min(max_col, max_num**max_num)
# if max_col > 10 or max_row > 10:
#     print(max_row,max_col,max_num)
#     exit()
from datetime import datetime
print(datetime.now())

todos:list[PrioritizedItem] = []
all_nodes:dict[int,dict[int,Node]] = {row+1:dict() for row in range(max_row)}
for i in range(max_col):
    column = i+1
    node = Node(1,column,cost(1,column))
    todos.append( PrioritizedItem(cost(1,column), node) )
    all_nodes[1][column] = node
heapq.heapify(todos)

def children(node):
    row,col = node.row,node.col
    nodes = []
    for d_row,d_col in ((1,-1),(1,0),(1,1)):
        new_row,new_col = d_row+row, d_col+col
        if 0 < new_col < max_col+1 and (new_row,new_col):
            nodes.append(Node(new_row,new_col,cost(new_row,new_col)))
    return nodes

while True:
    visit_node = heapq.heappop(todos).item
    # print(visit_node.accumulated_cost, visit_node.row, visit_node.col)
    if visit_node.row == max_row:
        print(visit_node.accumulated_cost)
        break
    visit_node.visited = True
    for child in children(visit_node):
        if child.visited:
            continue
        accumulated_cost = cost(child.row,child.col) + visit_node.accumulated_cost
        # print(f"... {accumulated_cost}, {child.row}, {child.col}")
        if child.col in all_nodes[child.row] and accumulated_cost < all_nodes[child.row][child.col].accumulated_cost:
            child = all_nodes[child.row][child.col]
            child.accumulated_cost = accumulated_cost
            heapq.heappush( todos, PrioritizedItem(child.accumulated_cost+max_row-child.row, child))
        elif child.col not in all_nodes[child.row]:
            all_nodes[child.row][child.col] = child
            child.accumulated_cost = accumulated_cost
            heapq.heappush( todos, PrioritizedItem(child.accumulated_cost+max_row-child.row, child))

print(datetime.now())

"""
from __future__ import annotations
from dataclasses import dataclass
import heapq
all_nodes:dict[tuple[int,int],Node] = dict()

@dataclass
class Node:
    row:int
    col:int
    accumulated_cost:int
    visited:bool = False
    def __lt__(self, other):
        return self.row>other.row

def cost(row,col):
    c= ((row-1)*max_col + col)%max_num
    return c if c!=0 else max_num

max_row = int(input())
max_col = int(input())
max_num = int(input())
todos = []
for i in range(max_col):
    column = i+1
    node = Node(1,column,cost(1,column))
    todos.append( (cost(1,column)+max_row-1, node) )
    all_nodes[(1,column)] = node
heapq.heapify(todos)

def children(node):
    row,col = node.row,node.col
    nodes = []
    for d_row,d_col in ((1,-1),(1,0),(1,1)):
        new_row,new_col = d_row+row, d_col+col
        if new_col > 0 and new_row > 0:
            nodes.append(Node(new_row,new_col,cost(new_row,new_col)))
    return nodes

while True:
    _,visit_node = heapq.heappop(todos)
    if visit_node.row == max_row:
        print(visit_node.accumulated_cost)
        break
    visit_node.visited = True
    for child in children(visit_node):
        if child.visited:
            continue
        accumulated_cost = cost(child.row,child.col) + visit_node.accumulated_cost
        if (child.row,child.col) in all_nodes and accumulated_cost < all_nodes[(child.row,child.col)].accumulated_cost:
            child = all_nodes[(child.row,child.col)]
            child.accumulated_cost = accumulated_cost
            heapq.heappush( todos, (child.accumulated_cost + (max_row-child.row), child))
        elif str(child) not in all_nodes:
            all_nodes[(child.row,child.col)] = child
            child.accumulated_cost = accumulated_cost
            heapq.heappush( todos, (child.accumulated_cost + (max_row-child.row), child))

"""




