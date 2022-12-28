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
    
    file = open("day16_test_input.txt", 'r')
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

    # for each vent, calculate the distance the next node with a valve with a rate > 0
    # vents.distances_to_nearest_vent()

    # vents and states are not the same thing, set up the states
    states = States(vents)
    initial_state = 0 # all vents closed
    you_vent_state = 'AA'
    elephant_vent_state = 'AA'
    flow,_ = states.flow_and_costs(0)

    initial_state = State(initial_state,you_vent_state,elephant_vent_state,flow,0,states)
    states.all_states[initial_state.key] = initial_state


    # calculate minimum costs via astar
    dijkstra = AStar(initial_state)
    dijkstra.max_depth = MAX_MINS
    all_paths = dijkstra.find_until(lambda x,y: astar_cb(x,y,states)) 
    x = 1
#    for n in (a for a in all_paths if a.time_least_visited == 3):
#        if dijkstra.get_length_path(n):
#            print (n.path_least_visited, n.cost)
#            pass






# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
def astar_cb(astar_obj,node_obj,states):
    global final_max_flow

    path = node_obj.path_least_visited
    time = node_obj.time_least_visited

#    if re.match(r',0-AA-AA,0-DD-BB',astar_obj.get_path_str(node_obj)):
#        pass
#    if re.match(r',0-AA-AA,0-DD-II,2-DD-JJ',astar_obj.get_path_str(node_obj)):
#        pass
     
    states_gen = ( node.obj for node in astar_obj.get_path(node_obj ))
    total = 0
    flow = 0
    for t,state in enumerate(states_gen):
        total +=  flow        
#        print (t,state.key,state.flow)
        flow = state.flow


    #total = sum(node.obj.flow for node in astar_obj.get_path(node_obj))
    total2 = sum(node.obj.flow for node in astar_obj.get_path(node_obj))
#    print (time, total, total2, path)

#    print (total, total2)
    if total > final_max_flow:
        print (time, total, path)
        final_max_flow = total    

    # if all vents are open, stop
    all_open = states.are_all_vents_open (node_obj.obj)

    if all_open:
        print ()
        print (f"\n\nFINAL RESULT: {total}  ",end="")
        total += (MAX_MINS-time-1)*81
        print (f"Adjusted: {total}")
        quit()
    return time == MAX_MINS

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
        self.max_flow = 0
        self.vent_state = 0

        vent_state = 0
        for vent in self.vents:
            if vent.rate != 0:
                vent_state += 2**vent.index
        self.all_vents_open = vent_state

    
    # ----------------------------------------------------------------------------
    # are all vents open
    # ----------------------------------------------------------------------------
    def are_all_vents_open (self,state):
        return state.vent_state == self.all_vents_open


    # ----------------------------------------------------------------------------
    # create the links between states
    # ----------------------------------------------------------------------------
    def update_children (self,state):

        # get info about current state
        you_vent = self.vents.get(state.you_vent_key)
        elephant_vent = self.vents.get(state.elephant_vent_key)
        vent_state = state.vent_state

        # update the vent_state if parent state openned a vent
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
        one,two =  sorted( (you_vent_key,elephant_vent_key) ) 
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
        self.cost = cost
        self.flow = flow
        self.states = states
        self.states.all_states[self.key] = self
        self.visited = False

    
    def eta(self,node):
        # for all vents that are still open, what would be the approximate loss
        time = node.time_least_visited
        fcost = 0
        open_vent_rates = (v.rate for v in self.states.vents if self.states.vents.rate != 0 and self.states.vents.is_closed(self.vent_state))
        for r in sorted(open_vent_rates,reversed=True):
            time += 1/2
            fcost += r
        
        return int((MAX_MINS-time)*fcost)

    def copy (self,state):
        return State(self.vent_state,self.you_vent_key,self.elephant_vent_key,self.flow,self.cost,self.states)

    def children(self,astar_obj,node_obj):
        path = node_obj.path_least_visited
        time = node_obj.time_least_visited
        flow = node_obj.obj.flow
        if (MAX_MINS-time) *(self.states.vents.max_flow()) + node_obj.cost < final_max_flow:
            return []

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
        self.nearest_vents = {}
    def add(self,obj):
        if self.get(obj.key) is None:
            self.vents[obj.key] = obj
    def exists(self,key):
        return self.get(key)
    def get (self,key):
        if key in self.vents.keys(): 
            return self.vents[key]
        return None

    def distances_to_nearest_vent(self):
        for v in self.vents.values():
            self.list_of_nearest_vents(v)


    def list_of_nearest_vents (self,vent):
        if vent.key in self.nearest_vents:
            return self.nearest_vents[vent.key]
        dijkstra = AStar(vent)
        self.nearest_vents[vent.key] = []
        for v in (v for v in self.vents.values() if v.rate > 0) :
            if v.key == vent.key: continue
            dijkstra = AStar(vent)
            shortest_paths = dijkstra.find_until(lambda dijk_obj, node_obj: node_obj.id == v.key)
            shortest_path = shortest_paths[0].time_least_visited
            flow =  shortest_paths[0].obj.rate
            self.nearest_vents[vent.key].append( (shortest_path, flow ) )

    def max_flow (self):
        return sum (v.rate for v in self.vents.values())

# ============================================================================
class Vent:
# ============================================================================
    index = -1
    @classmethod
    def get_new_index(cls):
        cls.index += 1
        return cls.index
    def __eq__(self,other):
        return self.key == other.key

    def __init__(self,id):
        self.cost = 1
        self.rate = 0
        self.key = id
        self.child_ids = {}
        self.index = Vent.get_new_index()
        self.actively_openning = False
    
    def eta(self,node):
        return 1
    def add_child( self, obj):
        self.child_ids[obj.key] = obj

    def children (self):
        return self.child_ids.values()

    def children_and_self (self):
        return itertools.chain(self.child_ids.values(), (self,))
    
    def is_closed (self,vent_state):
        return self.rate != 0 and not (vent_state>>self.index)%2

    def is_open (self,vent_state):
        return self.rate == 0 or (vent_state>>self.index)%2

    def open_vent (self,vent_state):
        return vent_state + 2**self.index










# ===================================================================
# Entry point
# ===================================================================
if __name__ == '__main__':
    start = time.time()
    main()    
    end = time.time()

    total_time = end - start
    print("\n"+ str(total_time))
 
