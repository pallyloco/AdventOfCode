import re                           # regular expressions
from astar import AStar             # A* algorithm
import time
import itertools
MAX_MINS = 26
final_max_flow = 0
final_paths = {}

# ----------------------------------------------------------------------------
# main code
# ----------------------------------------------------------------------------
def main():
    file = open("day16_input.txt", 'r')
    vents = Vents()

    # read the input and create "Vent" objeccts
    for line in map(str.rstrip,file):

        print("line:",line)
        regex = re.match(r".*?Valve (?P<valve_key>[A-Z]+) .*?rate=(?P<rate>\d+).*?valves? (?P<neighbours>.*)",line)

        #valve_key,rate,neighbours = regex.group()

        if not vents.exists(regex.group('valve_key')):
            vents.add(Vent(regex.group('valve_key')))
        vents.get(regex.group('valve_key')).rate = int(regex.group('rate'))
        dest_valve_keys = map(str.strip, regex.group('neighbours').split(","))

        for dest_valve_key in dest_valve_keys:
            vents.add(Vent(dest_valve_key))
            vents.get(regex.group('valve_key')).add_child(vents.get(dest_valve_key))

    # vents and states are not the same thing, set up the states
    states = States(vents)
    initial_state = 0 # all vents closed
    you_vent_state = 'AA'
    elephant_vent_state = 'AA'
    flow,cost = states.flow_and_costs(0)

    initial_state = State(initial_state,you_vent_state,elephant_vent_state,flow,0,states)
    states.all_states[initial_state.key] = initial_state


    # calculate minimum costs via astar
    dijkstra = AStar(initial_state)
    dijkstra.max_depth = MAX_MINS
    all_paths = dijkstra.find_until(astar_cb) 
    for n in (a for a in all_paths if dijkstra.get_length_path(a) == MAX_MINS):
        if dijkstra.get_length_path(n):
            #print (n.id, n.cost)
            pass






# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
def astar_cb(astar_obj,node_obj):
    global final_max_flow
    n = astar_obj.get_length_path(node_obj)

    name= astar_obj.get_path_str(node_obj)
#    print (name)
    if re.match(r',0-AA-AA,0-DD-BB',astar_obj.get_path_str(node_obj)):
        pass
    if re.match(r',0-AA-AA,0-DD-II,2-DD-JJ',astar_obj.get_path_str(node_obj)):
        pass
     
    total = sum(node.obj.flow for node in astar_obj.get_path(node_obj))

    if total > final_max_flow:
        nodes = astar_obj.get_path(node_obj)
#        for nn in nodes:
#            print(nn.obj.key, nn.obj.flow)
#        print (f"turn:{n} total_flow:{total} node_cost:{node_obj.cost} key:{node_obj.obj.key}")
        final_max_flow = total

        nodes = astar_obj.get_path(node_obj)
        i =0
        for tmpnode in nodes:
            i+=1
            total = sum(node.obj.flow for node in astar_obj.get_path(tmpnode))
#            print(f"{i})\tnode cost:{tmpnode.cost}\ttotal:{total}\tflow:{tmpnode.obj.flow} id: {tmpnode.id}")

        total = sum(node.obj.flow for node in astar_obj.get_path(node_obj))
        print(total)
    

    return n >= MAX_MINS-1

# ============================================================================
class States:
# ============================================================================

    # ----------------------------------------------------------------------------
    # constructor
    # ----------------------------------------------------------------------------
    def __init__(self,vents):
        self.vents = vents
        self.flow_and_cost_lookup = {}
        self.all_states = {}
        self.all_vents_number = None
        self.max_flow = 0

    
    def all_vents_open (self,state):
        if self.all_vents_number is None:
            vent_state = 0
            for vent in self.vents:
                if vent.rate != 0:
                    vent_state += 2**vent.index
            self.all_vents_number = vent_state
        return state.vent_state == self.all_vents_number

    # ----------------------------------------------------------------------------
    # create the links between states
    # ----------------------------------------------------------------------------
    def update_children (self,state):

        # get info about current state
        you_vent = self.vents.get(state.you_vent_key)
        elephant_vent = self.vents.get(state.elephant_vent_key)
        vent_state = state.vent_state

        # stay put if all vents open
        if self.all_vents_open(state):
            new_state = state.copy(state)
            num = 1
            while f"{state.key}-{num}" in self.all_states.keys():
                num += 1
            new_state.key =  f"{state.key}-{num}"
            self.all_states[new_state.key] = new_state
            state.add_child(new_state)
            return

        for you_vc in you_vent.children_and_self():
            if you_vc.key == you_vent.key and you_vent.is_open(vent_state): continue

            for elephant_vc in elephant_vent.children_and_self():
                if elephant_vc.key == elephant_vent.key and elephant_vent.is_open(vent_state): continue 

                new_vent_state = vent_state
        
                # openning a vent
                if you_vc.key == you_vent.key: 
                    new_vent_state = you_vc.open_vent(new_vent_state)
                if elephant_vc.key == elephant_vent.key: 
                    new_vent_state = elephant_vent.open_vent(new_vent_state)

                key = State.make_key(new_vent_state,you_vc.key,elephant_vc.key)
                if key not in self.all_states.keys():
                    flow, cost = self.flow_and_costs(new_vent_state)
                    state.add_child( State(new_vent_state, you_vc.key, elephant_vc.key,flow,cost,self))
                else:
                    state_child = self.all_states[key] 
                    state.add_child(state_child)

        return
    # ----------------------------------------------------------------------------
    # calculate the cost to move to this state, and the flow rate associated with it
    # ----------------------------------------------------------------------------
    #@lru_cache()
    def flow_and_costs(self,vent_state):
        if vent_state not in self.flow_and_cost_lookup.keys(): 
            flow = sum(v.rate for v in self.vents if v.rate and  (vent_state>>v.index)%2)
            cost = sum(v.rate for v in self.vents if v.rate and  not (vent_state>>v.index)%2)
            self.flow_and_cost_lookup[vent_state] = (flow,cost)
        return self.flow_and_cost_lookup[vent_state]

# ============================================================================
class State:
# ============================================================================

    @classmethod
    def make_key (c,vent_state,you_vent_key,elephant_vent_key):
        one,two =  (you_vent_key,elephant_vent_key) 
        return f"{vent_state}-{one}-{two}"

    # ----------------------------------------------------------------------------
    # constructor
    # ----------------------------------------------------------------------------
    def __init__(self,vent_state,you_vent_key,elephant_vent_key,flow,cost,states):
        self.vent_state = vent_state
        self.you_vent_key = you_vent_key
        self.elephant_vent_key = elephant_vent_key
        self.key = State.make_key(vent_state,you_vent_key,elephant_vent_key)
        self.unique_kids = None
        self.eta = 0
        self.cost = cost
        self.flow = flow
        self.states = states
        self.states.all_states[self.key] = self
        self.visited = False

    
    def copy (self,state):
        return State(self.vent_state,self.you_vent_key,self.elephant_vent_key,self.flow,self.cost,self.states)

    def children(self):
        self.unique_kids = {}
        self.states.update_children(self)
        return self.unique_kids.values()
        

    # ----------------------------------------------------------------------------
    # add child
    # ----------------------------------------------------------------------------
    def add_child(self, state):
        if self.unique_kids is None:
            self.unique_kids = {}
        self.unique_kids[state.key] = state

# ============================================================================
class Vents:
# ============================================================================
    def __iter__(self):
        return iter(self.vents.values())
    def __init__(self):
        self.vents = {}
    def add(self,obj):
        if self.get(obj.key) is None:
            self.vents[obj.key] = obj
    def exists(self,key):
        return self.get(key)
    def get (self,key):
        if key in self.vents.keys(): 
            return self.vents[key]
        return None

# ============================================================================
class Vent:
# ============================================================================
    index = -1
    @classmethod
    def get_new_index(cls):
        cls.index += 1
        return cls.index

    def __init__(self,id):
        self.cost = 1
        self.rate = 0
        self.key = id
        self.child_ids = {}
        self.eta = 0
        self.index = Vent.get_new_index()
    
    def add_child( self, obj):
        self.child_ids[obj.key] = obj

    def children (self):
        return self.child_ids.values()

    def children_and_self (self):
        l = list(itertools.chain(self.child_ids.values(), (self,)))
        for i in itertools.chain(self.child_ids.values(), (self,)):
            x = 1
        return itertools.chain(self.child_ids.values(), (self,))
    
    def is_closed (self,vent_state):
        return self.rate != 0 and not (vent_state>>self.index)%2

    def is_open (self,vent_state):
        return self.rate == 0 or (vent_state>>self.index)%2

    def open_vent (self,vent_state):
        return vent_state + 2**self.index









class AStar2:


    # -------------------------------------------------------------------------
    # constructor
    # -------------------------------------------------------------------------
    def __init__(self,start_obj):

        # private
        self._all_nodes = dict()
        self._current_node = None           # what node are we currently looking at?

        node = Node(start_obj)
        node.cost = start_obj.cost
        self.cost_calculation = lambda parent_node, obj, path : parent_node.cost + obj.cost
        self._all_nodes[start_obj.key] = node
        self._current_node = node
        

    # -------------------------------------------------------------------------
    # find_until
    # -------------------------------------------------------------------------
    def find_until (self, cb_routine):


        # set the current node to be the the one with the highest flow rate
        while current := self._find_lowest_cost_node(self.get_length_path(self._current_node)) :

            # current node is visited
            current.was_visited = True
            self._current_node = current
            
            # are we are done?
            if cb_routine(self,current): 
                return [self._current_node]
 
            # get all new neighbours for this node
            for child_obj in current.obj.children(self.get_length_path(current)):

                cost = current.cost+child_obj.cost 
                child_node = Node( child_obj, cost, current )

                # skip any node that has already been visited
                if child_obj.key in self._all_nodes:
                    if self._all_nodes[child_obj.key].was_visited:
                        continue
                
                # update the node
                self._update_node(current,child_node)

        
        # all nodes have been visited
        return [n for n in self._all_nodes]
 
    # -------------------------------------------------------------------------
    # find the node with the lowest cost
    # -------------------------------------------------------------------------
    def _find_lowest_cost_node (self,path_length) :
        
        # a list of nodes in ordering of descending costs 
        unvisited_nodes = [n for n in self._all_nodes.values() if not n.was_visited]
        for node in sorted(unvisited_nodes,key=lambda x:x.fcost):
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
        self.len_of_path = 0
        self.was_visited = False





# ===================================================================
# Entry point
# ===================================================================
if __name__ == '__main__':
    start = time.time()
    main()    
    end = time.time()

    total_time = end - start
    print("\n"+ str(total_time))
 
