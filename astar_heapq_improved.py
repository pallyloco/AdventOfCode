from __future__ import annotations
import heapq
from dataclasses import dataclass, field
from typing import Protocol, TypeVar, Optional, Callable, Any, TypeAlias

NodeId: TypeAlias = str


class CostProtocol(Protocol):
    """What we need for 'costing' ASTAR compatible objects"""

    def __lt__(self: Cost, other: Cost) -> bool: pass

    def __add__(self: Cost, other: Cost) -> Cost: pass

    def __sub__(self: Cost, other: Cost) -> Cost: pass


Cost = TypeVar("Cost", bound=CostProtocol)


class DijkstraObject(Protocol):

    def key(self) -> str: pass

    def edge_cost(self) -> Cost: pass

    def children(self): pass

    def eta(self, node=None) -> Cost: pass


# ##############################################################################
class AStar:

    # USAGE:
    #
    #   pass in an object that has the following properties/methods
    #       key - a unique identifier for any object that we might encounter
    #       children - (function) must return a list of children for this object
    #       cost - the cost of moving to this object
    #       eta - (function) estimated time of arrival to the final node.  
    #             Note that if this returns zero, then this
    #             algorithm will behave like a simple dijkstra's algorithm
    #               * if eta ever gives an estimate that is higher than the actual costs,
    #                 then finding the shortest possible path is not guarenteeed
    #
    #   astar = Astar(some_obj)
    #   final_node = astar.find_until(cb_function) # cb function returns true if final state is reached
    #   print(f"Final node id: {final_node.id}")
    #   print(f"Cost to get to final node: {final_node.cost}")
    #   print("Path to get there:")
    #   nodes = astar.get_path(final_node)
    #   for node in nodes:
    #       print(f"id: {node.id} cost: {node.cost}")

    # -------------------------------------------------------------------------
    # constructor
    # -------------------------------------------------------------------------
    def __init__(self, start_obj: DijkstraObject,zero = 0,
                 print_at_n_intervals: int = 5000):

        self._current_node: Optional[Node] = None  # what node are we currently looking at?
        self._heap: dict[Cost, list[Node]] = dict()
        self._unvisited_nodes: dict[NodeId, Node] = dict()
        self._visited_nodes: dict[NodeId, Node] = dict()
        self._current_low_cost: Optional[Cost] = None

        self.print_intervals: int = print_at_n_intervals

        node = Node(start_obj, cumulative_cost=zero)
        self._unvisited_nodes[node.id] = node
        self.heap: Heap = Heap()
        self.heap.insert(node.forecasted_cost, node)

    # -------------------------------------------------------------------------
    # find_until
    # -------------------------------------------------------------------------
    def find_until(self, cb_routine: Callable[[DijkstraObject], bool]) -> list[Node]:
        iterations = 1
        while True:

            # set the current node to be the lowest cost neighbour
            current: Node = self.heap.get_lowest()
            if current is None:
                break

            # keep user up to date with what is going on
            if not iterations % self.print_intervals:
                print(iterations, current.cumulative_cost, current.forecasted_cost, current.obj.eta(),
                      current.obj.key())
            iterations += 1

            # current node is visited
            current.was_visited = True
            self._visited_nodes[current.id] = current
            self._current_node = current

            # are we are done?
            if cb_routine(current.obj):
                print("All Done!")
                return [self._current_node]

            # get all new neighbours for this node
            for child_obj in current.obj.children(self, current):

                if self._visited_nodes.get(child_obj.key()):
                    break

                cumulative_cost = current.cumulative_cost + child_obj.edge_cost()
                child_node = Node(child_obj, cumulative_cost, current)

                self._update_node(child_node)

        # all nodes have been visited
        return [n for n in self._visited_nodes.values()]

    # -------------------------------------------------------------------------
    # get_path
    # -------------------------------------------------------------------------
    def get_path(self, node):
        count = 0
        nodes = [node]
        while True:
            next_node = node.prev
            if not next_node:
                break
            nodes.insert(0, next_node)
            node = next_node
            count += 1

        return nodes

    # -------------------------------------------------------------------------
    # update node if exists, else create it
    # -------------------------------------------------------------------------
    def _update_node(self, new_node):

        updated_cost: Cost = new_node.cumulative_cost

        # if node does not exist:
        if new_node.id not in self._unvisited_nodes:
            self._unvisited_nodes[new_node.id] = new_node
            new_node.cumulative_cost = updated_cost
            new_node.forecasted_cost = new_node.cumulative_cost + new_node.obj.eta(new_node)
            self.heap.insert(new_node.forecasted_cost, new_node)

        else:
            new_node = self._unvisited_nodes[new_node.id]
            if not new_node.was_visited and updated_cost < new_node.cumulative_cost:
                new_node.forecasted_cost = new_node.forecasted_cost - new_node.cumulative_cost - updated_cost
                new_node.cumulative_cost = updated_cost
                new_node.forecasted_cost = new_node.cumulative_cost + new_node.obj.eta(new_node)
                self.heap.insert(new_node.forecasted_cost, new_node)


#########################################################################################
class Node:
    __slots__ = ('obj', 'cumulative_cost', 'prev', 'id', 'forecasted_cost', 'was_visited', 'path_least_visited',
                 'time_least_visited')

    def __init__(self, obj, cumulative_cost=0, prev=None):
        self.obj: Any = obj
        self.cumulative_cost: Cost = cumulative_cost
        self.prev: Optional[Node] = prev
        self.id: str = obj.key()
#        self.forecasted_cost = self.cumulative_cost + self.obj.eta(self)
        self.forecasted_cost = self.cumulative_cost
        self.was_visited: bool = False
        self.path_least_visited = ""
        self.time_least_visited = 0

    def __gt__(self, other):
        return self.forecasted_cost > other.forecasted_cost

    def __lt__(self, other):
        return self.forecasted_cost < other.forecasted_cost


@dataclass()
class HeapNode:
    cost: Cost
    data: list[Any] = field(default_factory=list)
    parent: Optional[HeapNode] = None
    right: Optional[HeapNode] = None
    left: Optional[HeapNode] = None


class Heap:
    def __init__(self):
        self.root: Optional[HeapNode] = None
        self.start_node: Optional[HeapNode] = None

    def print(self):
        print("\ntree")
        self._print(self.root)

    def _print(self, node):
        if node is None:
            print(node)
            return
        rstring = node.right
        if node.right is not None:
            rstring = str(node.right.cost)
        lstring = node.left
        if node.left is not None:
            lstring = str(node.left.cost)

        print(node.cost, len(node.data), "l", lstring, "r", rstring)

        if node.left is not None:
            self._print(node.left)
        if node.right is not None:
            self._print(node.right)

    def insert(self, cost: Cost, datum: Any):
        if self.root is None:
            self.root = HeapNode(cost)
            self.root.data.append(datum)
            self.start_node = self.root
            return

        self._insert(self.root, cost, datum)

    def get_lowest(self) -> Any:
        #self.print()
        node = self.root
        if node is None:
            return node

        while node.left is not None:
            node = node.left
        lowest = node.data.pop()

        if not node.data:
            if node.parent is not None:
                node.parent.left = node.right
                if node.right is not None:
                    node.right.parent = node.parent
                self.start_node = node.parent.right
            else:
                self.root = node.right
                if self.root is not None:
                    self.root.parent = None
                self.start_node = self.root

        #self.print()
        return lowest

    def _insert(self, node: HeapNode, cost, datum):
        while True:
            if node is None:
                break

            if cost < node.cost:
                if node.left is None:
                    node.left = HeapNode(cost)
                    node.left.data.append(datum)
                    node.left.parent = node
                    break
                else:
                    node = node.left

            elif node.cost < cost:
                if node.right is None:
                    node.right = HeapNode(cost)
                    node.right.data.append(datum)
                    node.right.parent = node
                    break
                else:
                    node = node.right
                    self._insert(node.right, cost, datum)

            else:
                node.data.append(datum)
                break
