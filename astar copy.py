import dumper
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
    #   final_node = astar.find_until(final_obj.key)
    #   print(f"Final node id: {final_node.id}")
    #   print(f"Cost to get to final node: {final_node.cost}")
    #   print("Path to get there:")
    #   nodes = astar.get_path(final_node)
    #   for node in nodes:
    #       print(f"id: {node.id} cost: {node.cost}"")

    # -------------------------------------------------------------------------
    # constructor
    # -------------------------------------------------------------------------
    def __init__(self,start_obj):

        # private
        self._visited = set()               # a set of all node id's that were visited
        self._to_be_visited = {}            # a dictionary of node_id:node of nodes to be visited
        self._by_cost = {}                  # {cost_int:[node,node,...]}
        self._max_costs = 0                 # not sure
        self._current_node = None           # what node are we currently looking at?
        self._start_at_node(start_obj)      # where do we start

        # public
        self.progress_sub = lambda i:None   # callback function (user defined)
        self.progress_freq = None           # how often should the callback function be called

    # -------------------------------------------------------------------------
    # find_until
    # -------------------------------------------------------------------------
    def find_until (self, final_obj_key):
        num = 0

        # set the current node to be the lowest cost neighbour
        while current := self._find_lowest_cost_node() :
            
            self._current_node = current
            
            # no idea what this is for
            self._max_costs = max(self._max_costs, current.cost)

            # show user our progress periodically
            num += 1
            if self.progress_freq and not num % self.progress_freq:
                self.progress_sub( current )
                costs = sorted(self._by_cost.keys())
                print (costs[0],"\t",self._max_costs)   

            # are we are done?
            if current.obj.key == final_obj_key: break

            # current node is visited, so remove from to_be_visited
            self._move_node_to_visited(current)

            # get all new neighbours for this node
            for child_obj in current.obj.children():

                child_node = Node( child_obj, current.cost + child_obj.cost, current )

                # skip any node that has already been visited
                if self._already_visited(child_node): continue
                
                # update the node
                self._update_node(current,child_node)

        return self._current_node
 
    # -------------------------------------------------------------------------
    # find the node with the lowest cost
    # -------------------------------------------------------------------------
    def _find_lowest_cost_node (self) :
        
        # a list of costs in descending order
        costs = sorted (self._by_cost.keys())
        input("Press Enter to Continue")

        i = 0
        while True: 

            # if there are no nodes with this cost, remove it
            if not len( self._by_cost[ costs[i] ] ):
                self._by_cost.pop(costs[i])
                i = i + 1
                continue
                

            # we've reached the end of the 'costs' list, so bail out
            if i > len(costs) - 1: break

            # get one of the nodes with this cost
            node = self._by_cost[costs[i]].pop(0)

            # but if this node has already been visited, try the next node
            if not self._to_be_visited[node.id]: continue

            # return node
            return node
        
        return

    # -------------------------------------------------------------------------
    # set the starting node
    # -------------------------------------------------------------------------
    def _start_at_node (self, obj):
        node = Node(obj)
        self._to_be_visited[obj.key] = node
        self._by_cost[0] = [ node ]
        return self

    # -------------------------------------------------------------------------
    # move node to visited
    # -------------------------------------------------------------------------
    def _move_node_to_visited (self, node):
        self._visited.add(node.id)
        return self

    # -------------------------------------------------------------------------
    # already_visited
    # -------------------------------------------------------------------------
    def _already_visited (self,node):
        return node.id in self._visited

    # -------------------------------------------------------------------------
    # already visited?
    # -------------------------------------------------------------------------
    def _already_visited (self,node):
        if node.id in self._visited : return True
        return False

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
    # already in visited nodes?
    # -------------------------------------------------------------------------
    def _get_node_if_already_visited (self, node):
        if node.id in self._to_be_visited.keys() :
            return self._to_be_visited[node.id] 
        return
    
    # -------------------------------------------------------------------------
    # update node if exists, else create it
    # -------------------------------------------------------------------------
    def _update_node (self, current, new_node):
        existing_node = self._get_node_if_already_visited(new_node)

        if  ( existing_node is not None and new_node.cost < existing_node.cost ) \
            or existing_node is None:
        
            self._to_be_visited[ new_node.id ] = new_node
            self._update_cost_array(new_node)
        
    # -------------------------------------------------------------------------
    # update cost array
    # -------------------------------------------------------------------------
    def _update_cost_array (self, node) :
        costs = self._by_cost
        fcost = int (node.cost+node.obj.eta)
        ######### KEY ERROR ########
        if fcost not in costs.keys():
            costs[fcost] = []
        costs[fcost].append(node)
        return self




#########################################################################################
class Node:

    def __init__(self,obj,cost=0,prev=None):
        self.obj = obj
        self.cost = cost
        self.prev = prev
        self.id = obj.key 
