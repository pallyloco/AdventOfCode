from __future__ import annotations
from typing import Protocol, Optional, Any


class ExploreObject(Protocol):
    def obj(self) -> Any:
        """The original object"""

    def key(self) -> str:
        """string that uniquely defines this object"""

    def children(self) -> list[ExploreObject]:
        """list of neighbours"""


class Explore:

    # -------------------------------------------------------------------------
    # constructor
    # -------------------------------------------------------------------------
    def __init__(self):

        self.heap = list()

        self.all_nodes: dict[str, ExploreObject] = dict()
        self._current_node: Optional[ExploreObject] = None  # where are we?

    # -------------------------------------------------------------------------
    # process
    # -------------------------------------------------------------------------
    def go_explore(self, start_obj: ExploreObject) -> list[ExploreObject]:

        current = start_obj
        self.all_nodes[start_obj.key()] = current

        # current node is visited
        current.was_visited = True
        self._current_node = current

        # get all new neighbours for this node
        for child_obj in current.children():

            # skip any node that has already been visited
            node = self.all_nodes.get(child_obj.key(), None)
            if node is not None:
                continue

            # keep going
            self.go_explore(child_obj)

        return list(self.all_nodes.values())

