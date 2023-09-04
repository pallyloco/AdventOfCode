import functools
###############################################################################
class AStar:

    # USAGE:
    #
    #   pass in an object that has the following properties/methods
    #       key - a unique identifier for any object that we might encounter
    #       children - must return a list of children for this object
    #       cost - the cost of moving to this object
    #       eta - estimated time of arrival to the final node.  
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
    def __init__(self,start_obj):

        # private
        self._all_nodes = dict()
        self._current_node = None           # what node are we currently looking at?

        node = Node(start_obj)
       # self.cost_calculation = lambda current_cost, obj, parent_node,path:  
        self._all_nodes[start_obj.key] = node
        

    # -------------------------------------------------------------------------
    # find_until
    # -------------------------------------------------------------------------
    def find_until (self, cb_routine):

        # set the current node to be the lowest cost neighbour
        while current := self._find_lowest_cost_node() :

            # current node is visited
            current.was_visited = True
            self._current_node = current
            
            # are we are done?
            if cb_routine(self,current): 
                return [self._current_node]
 
            # get all new neighbours for this node
            for child_obj in current.obj.children(self.get_length_path(current)):

                cost = current.obj.cost+child_obj.cost 
                child_node = Node( child_obj, cost )

                # skip any node that has already been visited
                if child_obj.key in self._all_nodes:
                    if self._all_nodes[child_obj.key].was_visited:
                        continue
                
                # update the node
                self._update_node(current,child_node)

        
        # all nodes have been visited
        return 
 
    # -------------------------------------------------------------------------
    # find the node with the lowest cost
    # -------------------------------------------------------------------------
    def _find_lowest_cost_node (self) :
        
        # a list of nodes in ordering of descending costs 
        unvisited_nodes = [n for n in self._all_nodes.values() if not n.was_visited]
        for node in sorted(unvisited_nodes, key=lambda x:x.forecasted_cost):
            return node        
        return

    # -------------------------------------------------------------------------
    # get_path
    # -------------------------------------------------------------------------
    def get_path (self,node, max_nodes = 800):
        count = 0
        nodes = [node]
        while ( next_node := node.prev) and count < max_nodes:
            nodes.insert(0,next_node)
            node = next_node
            count += 1
        
        return nodes
    

    # -------------------------------------------------------------------------
    # get_length_ofpath
    # -------------------------------------------------------------------------
    def get_length_path (self,node, max_nodes = 800):
        count = 0
        while ( next_node := node.prev) :
            node = next_node
            count += 1
        return count

    # -------------------------------------------------------------------------
    # update node if exists, else create it
    # -------------------------------------------------------------------------
    def _update_node (self, current, new_node):

        updated_cost = new_node.cost

        # if node does not exists:
        if new_node.id not in self._all_nodes:
            self._all_nodes[new_node.id] = new_node
        
        # compare old costs to new costs
        if updated_cost < self._all_nodes[new_node.id].cost:
            self._all_nodes[new_node.id].cost = updated_cost
        
        self._all_nodes[new_node.id].fcost = self._all_nodes[new_node.id].cost + self._all_nodes[new_node.id].obj.eta
        

#########################################################################################
class Node:

    def __init__(self,obj,cost=0,prev=None):
        self.obj = obj
        self.cost = cost
        self.prev = prev
        self.id = obj.key 
        self.fcost = 0
        self.was_visited = False
