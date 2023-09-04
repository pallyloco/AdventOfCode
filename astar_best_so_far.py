from __future__ import annotations
import functools
from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import Protocol, TypeVar


class CostProtocol(Protocol):
    """What we need for 'costing' ASTAR compatible objects"""

    def __lt__(self: Cost, other: Cost) -> bool: pass

    def __add__(self: Cost, other: Cost) -> Self: pass

    def __sub__(self: Cost, other: Cost): pass


Cost = TypeVar("Cost", bound=CostProtocol)


class DijkstraObject(Protocol):
    key: str
    cost: Cost

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
    def __init__(self, start_obj: DijkstraObject):

        # private
        self._all_nodes: Dict[str, Node] = dict()
        self._current_node: Optional[Node] = None  # what node are we currently looking at?
        self._prioritized_queue = PriorityQueue()

        node = Node(start_obj)
        self._all_nodes[start_obj.key] = node
        self._prioritized_queue.put(PrioritizedItem(node.fcost, node))
        self.max_depth = None

    # -------------------------------------------------------------------------
    # find_until
    # -------------------------------------------------------------------------
    def find_until(self, cb_routine: Callable[[DijkstraObject], bool]) -> list[Node]:
        iterations = 0
        # set the current node to be the lowest cost neighbour
        while current := self._find_lowest_cost_node():
            iterations += 1
            self.get_path_str(current)
            if not iterations % 1000:
                print(iterations, current.cost, current.fcost, current.obj.eta(), current.obj.key)

            # current node is visited
            current.was_visited = True
            self._current_node = current

            # are we are done?
            if cb_routine(current.obj):
                print("All Done!")
                return [self._current_node]

            # get all new neighbours for this node
            if self.max_depth is None or current.time_least_visited < self.max_depth:
                for child_obj in current.obj.children(self, current):

                    # skip any node that has already been visited
                    if child_obj.key in self._all_nodes:
                        if self._all_nodes[child_obj.key].was_visited:
                            continue

                    cost = current.cost + child_obj.cost
                    child_node = Node(child_obj, cost, current)

                    self._update_node(current, child_node)
            else:
                print("No children")

        # all nodes have been visited
        return [n for n in self._all_nodes.values()]

    # -------------------------------------------------------------------------
    # find the node with the lowest cost
    # -------------------------------------------------------------------------
    def _find_lowest_cost_node(self):

        try:
            while node := self._prioritized_queue.get(block=False):
                if not node.item.was_visited: return node.item
        except Exception:
            return
        return

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

    def get_path_str(self, node):
        return node.path_least_visited

    # -------------------------------------------------------------------------
    # get_length_of path
    # -------------------------------------------------------------------------
    def get_length_path(self, node):
        return node.path_least_visited

    # -------------------------------------------------------------------------
    # update node if exists, else create it
    # -------------------------------------------------------------------------
    def _update_node(self, current, new_node):

        updated_cost = new_node.cost

        # if node does not exist:
        if new_node.id not in self._all_nodes:
            self._all_nodes[new_node.id] = new_node

            new_node.cost = updated_cost
            new_node.time_least_visited = current.time_least_visited + 1
            new_node.path_least_visited = f"{current.path_least_visited}\n{new_node.id}"
            new_node.fcost = new_node.cost + new_node.obj.eta(new_node)

            x = PrioritizedItem(new_node.fcost, new_node)

            self._prioritized_queue.put(x)

        new_node = self._all_nodes[new_node.id]

        # compare old costs to new costs
        if updated_cost < self._all_nodes[new_node.id].cost:
            new_node.fcost = new_node.fcost - new_node.cost - updated_cost
            new_node.cost = updated_cost
            new_node.time_least_visited = current.time_least_visited + 1
            new_node.path_least_visited = current.path_least_visited + f"\n{new_node.id}"
            new_node.fcost = new_node.cost + new_node.obj.eta(new_node)
            x = PrioritizedItem(new_node.fcost, new_node)

            self._prioritized_queue.put(x)


#########################################################################################
class Node:
    __slots__ = ('obj', 'cost', 'prev', 'id', 'fcost', 'was_visited', 'path_least_visited', 'time_least_visited')

    def __init__(self, obj, cost=None, prev=None):
        self.obj: Any = obj
        if cost is None:
            self.cost: Cost = obj.cost
        else:
            self.cost = cost
        self.prev: Optional[Node] = prev
        self.id: str = obj.key
        self.fcost: Cost = 0
        self.was_visited: bool = False
        self.path_least_visited = ""
        self.time_least_visited = 0

    def __gt__(self, other):
        return self.fcost > other.fcost

    def __lt__(self, other):
        return self.fcost < other.fcost


@dataclass(order=True)
class PrioritizedItem:
    priority: Cost
    item: object = field()
