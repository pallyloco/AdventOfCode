import re                           # regular expressions
from astar import AStar             # A* algorithm
import time
MAX_MINS = 26
final_max_flow = 0
final_paths = {}

# ----------------------------------------------------------------------------
# main code
# ----------------------------------------------------------------------------
def main():
    file = open("day16_test_input.txt", 'r')
    vents = Vents()

    # read the input and create "Vent" objeccts
    for line in map(str.rstrip,file):

        print("line:",line)
        regex = re.match(r".*?Valve (?P<valve_key>[A-Z]+) .*?rate=(?P<rate>\d+).*?valves? (?P<neighbours>.*)",line)

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
    initial_state = State(initial_state,you_vent_state,elephant_vent_state,flow,cost,states)
    states.all_states[initial_state.key] = initial_state

    # cover all paths and calculate the maximum flow (sigh)

    traverse(initial_state, states,f"{initial_state.key}")

    for path in final_paths.keys():
        print (path)

def traverse(state,states,path=""):
    global final_max_flow

    keys = path.split(",")
    num_nodes = len(keys)
    state.visited = True
    #print (num_nodes)

    # where are we now with the calculated flow?
    total_flow = 0
    flow_rate = 0
    for key in map(str.strip,keys):
        flow_rate = states.all_states[key].flow
        total_flow = total_flow + flow_rate
    total_flow += flow_rate * (26-num_nodes-1)


    # we have reached the maximum flow we can for this path
    if num_nodes >= 13 or state.vent_state == 590874:

        final_paths[path] = total_flow
        final_max_flow = min (total_flow,final_max_flow)
        if total_flow > 1300:
            print(f"total: {total_flow} \t {num_nodes}\t {state.key}")
        return final_paths
                    
    kids = state.children()
    for kid in state.children():
        if f" {kid.key}" in path:
           continue
#        print ("parent",state.key,"child",kid.key)
#        print (path)
        #print (kid.key)
        if len(path.split(",")) == 1:
            pass
        if path == '0-AA-AA, 0-DD-II ':
            pass
        if path == '0-AA-AA, 0-DD-II , 2-DD-JJ ':
            pass
        if path == '0-AA-AA, 0-DD-II , 2-DD-JJ , 524290-EE-JJ ':
            pass
        if path == '0-AA-AA, 0-DD-II , 2-DD-JJ , 524290-EE-JJ , 524920-FF-II ':
            pass
        new_path = f"{path}, {kid.key} "
        traverse(kid,states,new_path)

    x=1















def astar_cb(astar_obj,node_obj):
    global final_max_flow
    n = astar_obj.get_length_path(node_obj)
    # print(n)
    total = sum(node.obj.flow for node in astar_obj.get_path(node_obj))
    if total > final_max_flow:
        print (f"turn:{n} total_flow:{total} node_cost:{node_obj.cost} key:{node_obj.obj.key}")
        final_max_flow = total

        nodes = astar_obj.get_path(node_obj)
        i =0
        for tmpnode in nodes:
            i+=1
            total = sum(node.obj.flow for node in astar_obj.get_path(tmpnode))
            print(f"{i})\tcost:{tmpnode.cost}\ttotal:{total}\tflow:{tmpnode.obj.flow} id: {tmpnode.id}")

        total = sum(node.obj.flow for node in astar_obj.get_path(node_obj))
        print(total)

    return False

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
            print (self.all_vents_number)
        return state.vent_state == self.all_vents_number

    # ----------------------------------------------------------------------------
    # create the links between states
    # ----------------------------------------------------------------------------
    def update_children (self,state):

        # get info about current state
        you_vent = self.vents.get(state.you_vent_key)
        elephant_vent = self.vents.get(state.elephant_vent_key)
        vent_state = state.vent_state
        
        for you_vc in [vc for vc in you_vent.children()]:
                if elephant_vent.rate != 0 and not (vent_state>>elephant_vent.index)%2:
                    new_vent_state = vent_state + 2**elephant_vent.index
                    key = State.make_key(new_vent_state,you_vc.key,elephant_vent.key)
                    if key not in self.all_states.keys():
                        flow, cost = self.flow_and_costs(new_vent_state)
                        state.add_child(State(new_vent_state, you_vc.key, elephant_vent.key,flow,cost,self))
                    else:
                        state_child = self.all_states[key] 
                        state.add_child(state_child)

        for elephant_vc in [vc for vc in elephant_vent.children()]:
                if you_vent.rate != 0 and not (vent_state>>you_vent.index)%2:
                    new_vent_state = vent_state + 2**you_vent.index
                    key = State.make_key(new_vent_state,you_vent.key,elephant_vc.key)
                    if key not in self.all_states.keys():
                        flow, cost = self.flow_and_costs(new_vent_state)
                        state.add_child(State(new_vent_state,you_vent.key,elephant_vc.key,flow,cost,self))
                    else:
                        state_child = self.all_states[key] 
                        state.add_child(state_child)

        
        # possible moves for you
        for you_vc in (vc for vc in you_vent.children()):
            for elephant_vc in [vc for vc in elephant_vent.children()]:

                # just moving to a new vent
                key = State.make_key(vent_state,you_vc.key,elephant_vc.key)
                if key not in self.all_states.keys():
                    flow, cost = self.flow_and_costs(vent_state)
                    state.add_child( State(vent_state, you_vc.key, elephant_vc.key,flow,cost,self))
                else:
                    state_child = self.all_states[key] 
                    state.add_child(state_child)

    def order_by_closest_open_vent(self,kids):
        return kids
        
    # ----------------------------------------------------------------------------
    # calculate the cost to move to this state, and the flow rate associated with it
    # ----------------------------------------------------------------------------
    def flow_and_costs(self,vent_state):
        if vent_state not in self.flow_and_cost_lookup.keys(): 
            flow = sum([v.rate for v in self.vents if v.rate!=0 and  (vent_state>>v.index)%2])
            cost = sum([v.rate for v in self.vents if v.rate!=0 and  not (vent_state>>v.index)%2])
            self.flow_and_cost_lookup[vent_state] = (flow,cost)
        return self.flow_and_cost_lookup[vent_state]

# ============================================================================
class State:
# ============================================================================

    @classmethod
    def make_key (c,vent_state,you_vent_key,elephant_vent_key):
        one,two = sorted( (you_vent_key,elephant_vent_key) )
        return f"{vent_state}-{one}-{two}"

    # ----------------------------------------------------------------------------
    # constructor
    # ----------------------------------------------------------------------------
    def __init__(self,vent_state,you_vent_key,elephant_vent_key,flow,cost,states):
        self.vent_state = vent_state
        self.you_vent_key = you_vent_key
        self.elephant_vent_key = elephant_vent_key
        self.key = State.make_key(vent_state,you_vent_key,elephant_vent_key)
        self.kids = None
        self.eta = 0
        self.cost = cost
        self.flow = flow
        self.states = states
        self.states.all_states[self.key] = self
        self.visited = False

    
    def copy (self,state):
        return State(self.vent_state,self.you_vent_key,self.elephant_vent_key,self.flow,self.cost,self.states)

    def children(self):
        self.kids = []
        self.states.update_children(self)
#        print (f"initial state: {self.key}")
#        for k in self.kids:
#            print(f"   {k.key}, {k.cost}")
        ordered_kids = self.states.order_by_closest_open_vent(self.kids)
        return ordered_kids

    # ----------------------------------------------------------------------------
    # add child
    # ----------------------------------------------------------------------------
    def add_child(self, state):
        if self.kids is None:
            self.kids = []
        self.kids.append(state)

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
 
