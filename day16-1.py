import re                           # regular expressions
from astar import AStar             # A* algorithm
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

        vents.add(Vent(regex.group('valve_key')))
        vents.get(regex.group('valve_key')).rate = int(regex.group('rate'))
        dest_valve_keys = map(str.strip, regex.group('neighbours').split(","))

        for dest_valve_key in dest_valve_keys:
            vents.add(Vent(dest_valve_key))
            vents.get(regex.group('valve_key')).add_child(vents.get(dest_valve_key))

    # create all the valid states for these vents, based on open/closed, etc
    states = States(vents)

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
        num = len([v for v  in vents if v.rate !=0])
        self.max_vent_states = 2**num        
        
        # give each vent an index, so we can use it to create flags for open/
        # closed vents
        for index,v in enumerate ([v for v  in vents if v.rate !=0]):
            v.index = index

        # get a list of all possible vent open/close states
        self.all_states = {}

        for vent_state in range(self.max_vent_states):
            flow = sum([v.rate for v in vents if v.rate!=0 and  (vent_state>>v.index)%2])
            cost = sum([v.rate for v in vents if v.rate!=0 and  not (vent_state>>v.index)%2])

            for v in vents:
                state = State(vent_state,v.key,flow,cost)
                self.all_states[state.key] = state         
        
        # once we have all possible states, calculate children
        for state in self.all_states.values():
            self.update_children(state)

    # ----------------------------------------------------------------------------
    # create the links between states
    # ----------------------------------------------------------------------------
    def update_children (self,state):

        vent = self.vents.get(state.vent_key)
        vent_state = state.vent_state
        
        # maybe we want to open a vent?
        if vent.index is not None and not (vent_state>>vent.index)%2:
            new_vent_state = vent_state + 2**vent.index
            state_child = self.all_states[State.make_key(new_vent_state,vent.key)]        
            state.add_child(state_child)
        
        for vent_child in vent.children():
            state_child = self.all_states[State.make_key(vent_state,vent_child.key)]        
            state.add_child(state_child)


# ============================================================================
class State:
# ============================================================================

    @classmethod
    def make_key (c,vent_state,vent_key):
        return f"{vent_state}{vent_key}"

    # ----------------------------------------------------------------------------
    # constructor
    # ----------------------------------------------------------------------------
    def __init__(self,vent_state,vent_key,flow,cost):
        self.vent_state = vent_state
        self.vent_key = vent_key
        self.key = State.make_key(vent_state,vent_key)
        self.kids = []
        self.eta = 0
        self.cost = cost
        self.flow = flow
    
    def children(self):
        return self.kids

    # ----------------------------------------------------------------------------
    # add child
    # ----------------------------------------------------------------------------
    def add_child(self, state):
        self.kids.append(state)

# ============================================================================
class Vents:
# ============================================================================
    def __iter__(self):
        return iter(self.vents.values())
    def __init__(self):
        self.vents = {}
    def add(self,obj,type="valve"):
        if self.get(obj.key) is None:
            self.vents[obj.key] = obj
    def get (self,key):
        if key in self.vents.keys(): 
            return self.vents[key]
        return None

# ============================================================================
class Vent:
# ============================================================================
    def __init__(self,id):
        self.cost = 1
        self.rate = 0
        self.key = id
        self.child_ids = {}
        self.eta = 0
        self.index = None
    
    def add_child( self, obj):
        self.child_ids[obj.key] = obj

    def children (self):
        return self.child_ids.values()

# ===================================================================
# Entry point
# ===================================================================
if __name__ == '__main__':
    main()    
 