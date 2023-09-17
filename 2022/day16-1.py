import re                           # regular expressions
from astar import AStar             # A* algorithm
import time
MAX_MINS = 30

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

        if not vents.exists(regex.group('valve_key')):
            vents.add(Vent(regex.group('valve_key')))
        vents.get(regex.group('valve_key')).rate = int(regex.group('rate'))
        dest_valve_keys = map(str.strip, regex.group('neighbours').split(","))

        for dest_valve_key in dest_valve_keys:
            vents.add(Vent(dest_valve_key))
            vents.get(regex.group('valve_key')).add_child(vents.get(dest_valve_key))

    # create all the valid states for these vents, based on open/closed, etc
    states = States(vents)
    states.all_states["0AA"] = State(0,'AA',0,0,states)

    # calculate minimum costs via astar
    dijkstra = AStar(states.all_states["0AA"])
    final_node = dijkstra.find_until(lambda astar_obj, node_obj : astar_obj.get_length_path(node_obj) == MAX_MINS-1) 
    total = sum(node.obj.flow for node in dijkstra.get_path(final_node))
    print(total)

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
        
    # ----------------------------------------------------------------------------
    # create the links between states
    # ----------------------------------------------------------------------------
    def update_children (self,state):

        vent = self.vents.get(state.vent_key)
        vent_state = state.vent_state
        
        # maybe we want to open a vent?
        if vent.rate != 0 and not (vent_state>>vent.index)%2:
            new_vent_state = vent_state + 2**vent.index
            key = State.make_key(new_vent_state,vent.key)
            if key not in self.all_states.keys():
                flow, cost = self.flow_and_costs(new_vent_state)
                self.all_states[key] = State(new_vent_state, vent.key, flow,cost,self)
            state_child = self.all_states[State.make_key(new_vent_state,vent.key)]        
            state.add_child(state_child)

        # just moving to a new vent
        for vent_child in vent.children():
            key = State.make_key(vent_state,vent_child.key)
            if key not in self.all_states.keys():
                flow, cost = self.flow_and_costs(vent_state)
                self.all_states[key] = State(vent_state, vent_child.key, flow,cost,self)
            state_child = self.all_states[key]        
            state.add_child(state_child)

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
    def make_key (c,vent_state,vent_key):
        return f"{vent_state}{vent_key}"

    # ----------------------------------------------------------------------------
    # constructor
    # ----------------------------------------------------------------------------
    def __init__(self,vent_state,vent_key,flow,cost,states):
        self.vent_state = vent_state
        self.vent_key = vent_key
        self.key = State.make_key(vent_state,vent_key)
        self.kids = None
        self.eta = 0
        self.cost = cost
        self.flow = flow
        self.states = states
    
    def children(self,dummy):
        if self.kids is None:
            self.kids = []
            self.states.update_children(self)
        return self.kids

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

# ===================================================================
# Entry point
# ===================================================================
if __name__ == '__main__':
    start = time.time()
    main()    
    end = time.time()

    total_time = end - start
    print("\n"+ str(total_time))
 