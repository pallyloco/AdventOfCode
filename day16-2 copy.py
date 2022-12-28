import re                           # regular expressions
from astar import AStar             # A* algorithm
import time
MAX_MINS = 26
final_max_flow = 0

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

    # vents and states are not the same thing, set up the states
    states = States(vents)
    initial_state = 0 # all vents closed
    you_vent_state = 'AA'
    elephant_vent_state = 'AA'
    flow,cost = states.flow_and_costs(0)
    initial_state = State(initial_state,you_vent_state,elephant_vent_state,flow,cost,states)
    states.all_states[initial_state.key] = initial_state

    # calculate minimum costs via astar
    dijkstra = AStar(initial_state)
    dijkstra.find_until(astar_cb) 





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
    def update_children (self,state,path_length):

        # exceeds the maximum path length
        if path_length >= 26-1:
            return


        # get info about current state
        you_vent = self.vents.get(state.you_vent_key)
        elephant_vent = self.vents.get(state.elephant_vent_key)
        vent_state = state.vent_state
        
        # possible moves for you
        for you_vc in [vc for vc in you_vent.children()]:

            for elephant_vc in [vc for vc in elephant_vent.children()]:

                if elephant_vent.actively_openning:
                    new_vent_state = vent_state + 2**elephant_vent.index
                    key = State.make_key(new_vent_state,you_vc.key,elephant_vent.key)
                    if key not in self.all_states.keys():
                        flow, cost = self.flow_and_costs(new_vent_state)
                        self.all_states[key] = State(new_vent_state, you_vc.key, elephant_vent.key,flow,cost,self)
                    state_child = self.all_states[key]        
                    state.add_child(state_child)
                    elephant_vent.actively_openning = False

                if you_vent.actively_openning:
                    new_vent_state = vent_state + 2**you_vent.index
                    key = State.make_key(new_vent_state,you_vent.key,elephant_vc.key)
                    if key not in self.all_states.keys():
                        flow, cost = self.flow_and_costs(new_vent_state)
                        self.all_states[key] = State(new_vent_state,you_vent.key,elephant_vc.key,flow,cost,self)
                    state_child = self.all_states[key]        
                    state.add_child(state_child)

                # maybe we want to open a vent if it is not already open? (elephant)
                if elephant_vent.rate != 0 and not (vent_state>>elephant_vent.index)%2:
                    elephant_vent.actively_openning = True
                if you_vent.rate != 0 and not (vent_state>>you_vent.index)%2:
                    you_vent.actively_openning = True

                if you_vent.rate != 0 and not (vent_state>>you_vent.index)%2:
                    new_vent_state = vent_state + 2**you_vent.index
                    key = State.make_key(new_vent_state,you_vent.key,elephant_vc.key)
                    if key not in self.all_states.keys():
                        flow, cost = self.flow_and_costs(new_vent_state)
                        self.all_states[key] = State(new_vent_state,you_vent.key,elephant_vc.key,flow,cost,self)
                    state_child = self.all_states[key]        
                    state.add_child(state_child)

                # just moving to a new vent
                key = State.make_key(vent_state,you_vc.key,elephant_vc.key)
                if key not in self.all_states.keys():
                    flow, cost = self.flow_and_costs(vent_state)
                    self.all_states[key] = State(vent_state, you_vc.key, elephant_vc.key,flow,cost,self)
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
    def make_key (c,vent_state,you_vent_key,elephant_vent_key):
        return f"{vent_state}-{you_vent_key}-{elephant_vent_key}"

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
    
    def copy (self,state):
        return State(self.vent_state,self.you_vent_key,self.elephant_vent_key,self.flow,self.cost,self.states)

    def children(self,path_length):
        self.kids = []
        self.states.update_children(self,path_length)
#        print (f"initial state: {self.key}")
#        for k in self.kids:
#            print(f"   {k.key}, {k.cost}")
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
        self.actively_openning = False
    
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
 
