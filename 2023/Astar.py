from __future__ import annotations
from dataclasses import dataclass, field
import heapq
import itertools as it
from typing import Protocol, TypeVar, Optional, Callable, Any


# =====================================================================================
# AStar/Dijkstra usage:
#
#   astar = Astar(dijkstra_obj: DijkstraObject)
#   cb_function: Callable[ [DijkstraObject], bool]
#
# --- find costs from one node to all the rest
#     astar.find_all()
#     for node in astar.all_nodes.values():
#         dijkstra_obj = node.obj
#         print("Cost to ", dijkstra_obj, "is", node.cumulative_cost)
#
# --- stop when you get to a desired location
#   final_node: Node = astar.find_until(cb_function)
#           cb function returns true if final state is reached
#
#   print(f"Final node id: {final_node.id}")
#   print(f"Cost to get to final node: {final_node.cumulative_cost}")
#
#   print("Path to get there:")
#   nodes = astar.get_path(final_node)
#   for node in nodes:
#       print(f"id: {node.id} cost: {node.cost}")
#       print(f"obj is: {node.obj}")
# =====================================================================================


# =====================================================================================
# Requirements for using AStar or Dijkstra
# =====================================================================================

# ----------------------------------------------------------------------------------
# The Cost type must have '__add__' and '__lt__'.
#
# If you are using integers, you don't
# have to do anything, but if you are using an object as a cost, make sure you
# implement this protocol
# ----------------------------------------------------------------------------------
class CostProtocol(Protocol):
    """What we need for 'costing' ASTAR compatible objects"""

    def __lt__(self: Cost, other: Cost) -> bool: pass

    def __add__(self: Cost, other: Cost) -> Cost: pass


Cost = TypeVar("Cost", bound=CostProtocol)


class DijkstraObject(Protocol):
    def key(self) -> str:
        """string that uniquely defines this object"""

    def children(self) -> list[DijkstraObject]:
        """list of neighbours"""

    def edge_cost(self, prev: DijkstraObject) -> Cost:
        """How much does it cost to get from prev to self"""

    def eta(self, node=None) -> Cost:
        """
        estimated time of arrival to the final node.

        Note that if this returns zero, then this
        algorithm will behave like a simple dijkstra's algorithm

        * if eta ever gives an estimate that is higher than the actual costs,
        then finding the shortest possible path is not guaranteed
        """


# =====================================================================================
# Dijkstra/AStar
# =====================================================================================
# -------------------------------------------------------------------------
# print info to the screen
# -------------------------------------------------------------------------
def print_info(current: Node, iteration: int):
    prev: str = str(current.prev.obj) if current.prev is not None else "None"
    print(iteration, current.cumulative_cost, current.forecasted_cost,
          current.obj.eta(), prev, "=>", current.obj.key())


class AStar:

    # -------------------------------------------------------------------------
    # constructor
    # -------------------------------------------------------------------------
    def __init__(self,
                 start_obj: DijkstraObject,
                 zero: Cost = 0):

        self.print_intervals: int = 0
        self.heap = list()

        self.all_nodes: dict[str, Node] = dict()
        self._current_node: Optional[Node] = None  # what node are we currently looking at?

        node = Node(start_obj, zero)
        self.all_nodes[start_obj.key()] = node
        heapq.heappush(self.heap, PrioritizedItem(node.forecasted_cost, node))
        self.max_depth = None

    # -------------------------------------------------------------------------
    # process
    # -------------------------------------------------------------------------
    def find_all(self, print_every_nth_iteration: int = 0,
                 what_to_print: Callable[[Node], None] = print_info):
        return self.find_until(lambda _: False, print_every_nth_iteration, what_to_print)

    def find_until(self,
                   reached_desired_end: Callable[[DijkstraObject], bool],
                   print_every_nth_iteration: int = 0,
                   what_to_print: Callable[[Node], None] = print_info) \
            -> Optional[Node]:

        for iteration in it.count():

            # set the current node to be the lowest cost neighbour, if no neighbours
            # left, we are finished this process
            try:
                current = self._find_lowest_cost_node()
            except NodeNotFoundError:
                break

            # print stuff to screen if requested
            if print_every_nth_iteration and not iteration % print_every_nth_iteration:
                self.print_intervals and what_to_print(current)

            # current node is visited
            current.was_visited = True
            self._current_node = current

            # are we are done?
            if reached_desired_end(current.obj):
                return self._current_node

            # get all new neighbours for this node
            if self.max_depth is None or current.time_least_visited < self.max_depth:
                for child_obj in current.obj.children():

                    # skip any node that has already been visited
                    if child_obj.key() in self.all_nodes:
                        if self.all_nodes[child_obj.key()].was_visited:
                            continue

                    cost = current.cumulative_cost + child_obj.edge_cost(current)
                    child_node = Node(child_obj, cost, current)

                    self._update_node(child_node, current)

        # never reached the end goal
        return None

    # -------------------------------------------------------------------------
    # find the node with the lowest cost
    # -------------------------------------------------------------------------
    def _find_lowest_cost_node(self) -> Optional[Node]:

        try:
            while True:
                pi = heapq.heappop(self.heap)
                if not pi.item.was_visited:
                    return pi.item
        except IndexError:
            raise NodeNotFoundError

    # -------------------------------------------------------------------------
    # get_path
    # -------------------------------------------------------------------------
    def get_path(self, node, max_nodes=20000):
        count = 0
        nodes = [node]
        while (next_node := node.prev) and count < max_nodes:
            nodes.insert(0, next_node)
            node = next_node
            count += 1

        return nodes

    # -------------------------------------------------------------------------
    # update node if exists, else create it
    # -------------------------------------------------------------------------
    def _update_node(self, new_node: Node, prev_node: Node):

        updated_cost: Cost = new_node.cumulative_cost

        # if node does not exist:
        if new_node.id not in self.all_nodes:
            self.all_nodes[new_node.id] = new_node
            new_node.forecasted_cost = new_node.cumulative_cost + new_node.obj.eta(new_node)

        else:
            new_node = self.all_nodes[new_node.id]
            if updated_cost < new_node.cumulative_cost:
                new_node.cumulative_cost = updated_cost
                new_node.forecasted_cost = new_node.cumulative_cost + new_node.obj.eta(new_node)
                new_node.prev = prev_node

        x = PrioritizedItem(new_node.forecasted_cost, new_node)
        heapq.heappush(self.heap, x)


class NodeNotFoundError(Exception):
    pass


# =====================================================================================
# Node
# =====================================================================================
class Node:
    __slots__ = ('obj', 'cumulative_cost', 'prev', 'id', 'forecasted_cost', 'was_visited',
                 'time_least_visited')

    def __init__(self, obj, cumulative_cost=0, prev=None):
        self.obj: Any = obj
        self.cumulative_cost = cumulative_cost
        self.prev: Optional[Node] = prev
        self.id: str = obj.key()
        self.forecasted_cost: Cost = self.cumulative_cost
        self.was_visited: bool = False
        self.time_least_visited = 0

    def __gt__(self, other):
        return self.forecasted_cost > other.forecasted_cost

    def __lt__(self, other):
        return self.forecasted_cost < other.forecasted_cost

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id


@dataclass(order=True)
class PrioritizedItem:
    priority: Cost
    item: object = field()
