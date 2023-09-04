from __future__ import annotations
import heapq
from dataclasses import dataclass, field
from typing import Protocol, TypeVar, Optional, Callable, Any, TypeAlias
key: TypeAlias = str


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
    def __init__(self, start_obj: DijkstraObject, max_heap_size: int = 0,
                 print_at_n_intervals: int = 1000):

        self.max_nodes = max_heap_size
        self._all_nodes: dict[key, Node] = dict()
        self._current_node: Optional[Node] = None  # what node are we currently looking at?
        self._heap: list[Cost] = list()
        self._cost_nodes: dict[Cost, list[key]] = dict()
        self.max_heap_size: int = max_heap_size
        self.print_intervals:int = print_at_n_intervals

        node = Node(start_obj)
        self._all_nodes[start_obj.key()] = node
        self._add_to_heap(node)

    # -------------------------------------------------------------------------
    # find_until
    # -------------------------------------------------------------------------
    def find_until(self, cb_routine: Callable[[DijkstraObject], bool]) -> list[Node]:
        iterations = 1
        while True:

            # set the current node to be the lowest cost neighbour
            current: Node = self._find_lowest_cost_node()
            if current is None:
                break

            # keep user up to date with what is going on
            if not iterations % self.print_intervals:
                print(iterations, current.cumulative_cost, current.forecasted_cost, current.obj.eta(),
                      current.obj.key())
            iterations += 1

            # current node is visited
            current.was_visited = True
            self._current_node = current

            # are we are done?
            if cb_routine(current.obj):
                print("All Done!")
                print("heap size is: ", len(self._heap))
                return [self._current_node]

            # get all new neighbours for this node
            for child_obj in current.obj.children(self, current):

                # skip any node that has already been visited
                if child_obj.key() in self._all_nodes:
                    if self._all_nodes[child_obj.key()].was_visited:
                        continue

                cumulative_cost = current.cumulative_cost + child_obj.edge_cost()
                child_node = Node(child_obj, cumulative_cost, current)

                self._update_node(current, child_node)

        # all nodes have been visited
        print("heap size is: ", len(self._heap))
        return [n for n in self._all_nodes.values()]

    # -------------------------------------------------------------------------
    # get_path
    # -------------------------------------------------------------------------
    def get_path(self, node):
        count = 0
        nodes = [node]
        while self.max_nodes == 0 or count < self.max_nodes:
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
    def _update_node(self, current, new_node):

        updated_cost = new_node.cumulative_cost

        # if node does not exist:
        if new_node.id not in self._all_nodes:
            self._all_nodes[new_node.id] = new_node

            new_node.cumulative_cost = updated_cost
            new_node.forecasted_cost = new_node.cumulative_cost + new_node.obj.eta(new_node)
            self._add_to_heap(new_node)

        else:
            new_node = self._all_nodes[new_node.id]
            if updated_cost < self._all_nodes[new_node.id].cumulative_cost:
                new_node.forecasted_cost = new_node.forecasted_cost - new_node.cumulative_cost - updated_cost
                new_node.cumulative_cost = updated_cost
                new_node.forecasted_cost = new_node.cumulative_cost + new_node.obj.eta(new_node)
                self._add_to_heap(new_node)

    # -------------------------------------------------------------------------
    # keep track of sorted costs in heap, with associated nodes
    # -------------------------------------------------------------------------
    def _add_to_heap(self, node):
        if node.forecasted_cost not in self._cost_nodes:
            self._cost_nodes[node.forecasted_cost] = list()
        if node.id not in self._cost_nodes[node.forecasted_cost]:
            self._cost_nodes[node.forecasted_cost].append(node.id)
        if node.forecasted_cost not in self._heap:
            heapq.heappush(self._heap, node.forecasted_cost)

    # -------------------------------------------------------------------------
    # find the node with the lowest cumulative_cost
    # -------------------------------------------------------------------------
    def _find_lowest_cost_node(self) -> Optional[Optional]:

        try:
            while True:
                lowest_cost = self._heap[0]

                # get any node with this cost, as long as it has not already
                # been visited.
                if self._cost_nodes[lowest_cost]:
                    node_id = self._cost_nodes[lowest_cost].pop()
                    node = self._all_nodes[node_id]
                    if not node.was_visited:
                        return node

                else:
                    heapq.heappop(self._heap)

        except IndexError:
            return None


#########################################################################################
class Node:
    __slots__ = ('obj', 'cumulative_cost', 'prev', 'id', 'forecasted_cost', 'was_visited', 'path_least_visited', 'time_least_visited')

    def __init__(self, obj, cumulative_cost=None, prev=None):
        self.obj: Any = obj
        if cumulative_cost is None:
            self.cumulative_cost: Cost = obj.edge_cost()
        else:
            self.cumulative_cost = cumulative_cost
        self.prev: Optional[Node] = prev
        self.id: str = obj.key()
        self.forecasted_cost: Cost = 0
        self.was_visited: bool = False
        self.path_least_visited = ""
        self.time_least_visited = 0

    def __gt__(self, other):
        return self.forecasted_cost > other.forecasted_cost

    def __lt__(self, other):
        return self.forecasted_cost < other.forecasted_cost


@dataclass(order=True)
class PrioritizedItem:
    priority: Cost
    item: object = field()
