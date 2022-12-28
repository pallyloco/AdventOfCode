import re                           # regular expressions
from astar import AStar             # A* algorithm
import time
import itertools
MAX_MINS = 26
final_max_flow = 0
final_paths = {}
vents_all_open = None
max_flow_cost = None

# ----------------------------------------------------------------------------
# main code
# ----------------------------------------------------------------------------
def main():
    global max_flow_cost
    
    file = open("day16_input.txt", 'r')
    vents = Vents()

    # read the input and create "Vent" objeccts
    for line in map(str.rstrip,file):

        #print("line:",line)
        regex = re.match(r".*?Valve (?P<valve_key>[A-Z]+) .*?rate=(?P<rate>\d+).*?valves? (?P<neighbours>.*)",line)

        #valve_key,rate,neighbours = regex.group()

        if vents.get(regex.group('valve_key')) is None:
            vents.add(Vent(regex.group('valve_key')))
        vents.get(regex.group('valve_key')).rate = int(regex.group('rate'))
        dest_valve_keys = map(str.strip, regex.group('neighbours').split(","))

        for dest_valve_key in dest_valve_keys:
            if vents.get(dest_valve_key) is None:
                vents.add(Vent(dest_valve_key))
            vents.get(regex.group('valve_key')).add_child(vents.get(dest_valve_key))

    # for each vent, calculate the distance the next node with a valve with a rate > 0
    vents.distances_to_nearest_vent()
    vents.update_valve_info()


    # vents and states are not the same thing, set up the states
    states = States(vents)
    initial_state = VentState.new(vents)
    you_vent_state = 'AA'
    elephant_vent_state = 'AA'
    flow = vents.flow(initial_state)
    cost = vents.cost(initial_state)
    initial_state = State(initial_state,you_vent_state,elephant_vent_state,flow,cost,states)
    max_flow_cost = vents.max_flow()

    # calculate minimum costs via astar
    dijkstra = AStar(initial_state)
    dijkstra.max_depth = MAX_MINS
    dijkstra.find_until(lambda x,y: astar_cb(x,y,states)) 

#    x = 1
#    for n in (a for a in all_paths if a.time_least_visited == 3):
#        if dijkstra.get_length_path(n):
#            print (n.path_least_visited, n.cost)
#            pass






# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
def astar_cb(astar_obj,node_obj,states):
    global final_max_flow



    path = node_obj.path_least_visited
    time_step = node_obj.time_least_visited

#    if re.match(r',0-AA-AA,0-DD-BB',astar_obj.get_path_str(node_obj)):
#        pass
#    if re.match(r',0-AA-AA,0-DD-II,2-DD-JJ',astar_obj.get_path_str(node_obj)):
#        pass
     
    #total = sum(node.obj.flow for node in astar_obj.get_path(node_obj))
    #states_gen = ( node.obj for node in astar_obj.get_path(node_obj ))
    #total = sum(node.obj.flow for node in astar_obj.get_path(node_obj))
    #for state in states_gen:
    #    flow = state.flow
    #    total +=  flow        
#        print (t,state.key,state.flow)
    total = max_flow_cost*time_step - node_obj.cost
    #print (time_step, node_obj.obj.cost,node_obj.cost, node_obj.id)
#    print (time_step, total, path)
    if total > final_max_flow:
        end = time.time()
        total_time = end - start
        print (time_step, node_obj.cost, node_obj.fcost-node_obj.cost, total, total_time, path)
        final_max_flow = total

    if time_step == 1 and re.search(r'TL-TM',node_obj.id) :
        end = time.time()
        total_time = end - start
       # print (time_step, node_obj.cost, node_obj.fcost-node_obj.cost, total, total_time, path)
    if time_step == 2  :
        end = time.time()
        total_time = end - start
       # print (time_step, node_obj.cost, node_obj.fcost-node_obj.cost, total, total_time, path)
    if time_step == 3  and False:
        end = time.time()
        total_time = end - start
       # print (time_step, node_obj.cost, node_obj.fcost-node_obj.cost, total, total_time, path)
    if time_step == 4  and False:
        end = time.time()
        total_time = end - start
       # print (time_step, node_obj.cost, node_obj.fcost-node_obj.cost, total, total_time, path)

#        print (time_step, node_obj.cost, node_obj.fcost-node_obj.cost, total, total_time, path)
#        final_max_flow = total    

    # if all vents are open, stop

#    if VentState.all_vents_open (node_obj.obj.states.vents,node_obj.obj.vent_state):
#        print ()
#        print (f"\n\nFINAL RESULT: {total}  ",end="")
#        total += (MAX_MINS-time)*(flow)
#        print (f"Adjusted: {total}")
#        return True

    return time_step >= MAX_MINS

class vent_state:
    def __init__(self,vents):
        self.vents = vents
        
# ============================================================================
class States:
# ============================================================================

    # ----------------------------------------------------------------------------
    # constructor
    # ----------------------------------------------------------------------------
    def __init__(self,vents):
        self.vents = vents
        self.max_flow = 0
    
    # ----------------------------------------------------------------------------
    # are all vents open
    # ----------------------------------------------------------------------------
    def are_all_vents_open (self,state):
        return state.vent_state == VentState.all_vents_open(state.vents,state.vent_state)

    # ----------------------------------------------------------------------------
    # get the next possible states
    # ----------------------------------------------------------------------------
    def update_children (self,state):

        # get info about current state
        if re.search(r"AI-KF",state.key):
            pass
        you_vent = self.vents.get(state.you_vent_key)
        ele_vent = self.vents.get(state.elephant_vent_key)
        vent_state = state.vent_state        
        
        # open the vent (will only work if it has already been turned)
        new_vent_state = VentState.open_any_turned_valves(vent_state)

        # find all possible children
        you_kids = [v for v in you_vent.children_and_self() if v!=you_vent or (v==you_vent and v.rate and VentState.is_closed(v,vent_state))]
        ele_kids = [v for v in ele_vent.children_and_self() if v!=ele_vent or (v==ele_vent and v.rate and VentState.is_closed(v,vent_state))]
        
        # no diff between you_v and elephant_v
        done_before = []
        for you_vc in you_kids:
            for elephant_vc in ele_kids:
                key = State.make_key(new_vent_state,you_vc.key,elephant_vc.key)
                if key in done_before: continue
                #done_before.append(key)

                # turning a vent
                if you_vc.key == you_vent.key and elephant_vc.key == ele_vent.key: 
                    tmp_vent_state = VentState.turn(you_vc,new_vent_state)
                    tmp_vent_state = VentState.turn(elephant_vc,tmp_vent_state)
                    flow, cost = self.flow_and_costs(tmp_vent_state)
                    state.add_child( State(tmp_vent_state, you_vc.key, elephant_vc.key,flow,cost,self))
                elif you_vc.key == you_vent.key: 
                    tmp_vent_state = VentState.turn(you_vc,new_vent_state)
                    flow, cost = self.flow_and_costs(tmp_vent_state)
                    state.add_child( State(tmp_vent_state, you_vc.key, elephant_vc.key,flow,cost,self))
                elif elephant_vc.key == ele_vent.key: 
                    tmp_vent_state = VentState.turn(elephant_vc,new_vent_state)
                    flow, cost = self.flow_and_costs(tmp_vent_state)
                    state.add_child( State(tmp_vent_state, you_vc.key, elephant_vc.key,flow,cost,self))
        
                # add the new state to the children
                #key = State.make_key(new_vent_state,you_vc.key,elephant_vc.key)
                flow, cost = self.flow_and_costs(new_vent_state)
                state.add_child( State(new_vent_state, you_vc.key, elephant_vc.key,flow,cost,self))
        #        print (f"Child: {key}")

        return

    # ----------------------------------------------------------------------------
    # calculate the cost to move to this state, and the flow rate associated with it
    # ----------------------------------------------------------------------------
    #@lru_cache()
    def flow_and_costs(self,vent_state):
        #if vent_state not in self.flow_and_cost_lookup.keys(): 
            flow = self.vents.flow(vent_state)
            cost = self.vents.cost(vent_state)
            #self.flow_and_cost_lookup[vent_state] = (flow,cost)
            return flow,cost
        #flow,cost = self.flow_and_cost_lookup[vent_state] 
        #return self.flow_and_cost_lookup[vent_state]


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
        self.cost = cost
        self.flow = flow
        self.states = states
        self.unique_kids = {}

    
    def eta(self,node):
        return 0
        # for all vents that are still open, what would be the approximate loss

        # if we don't open a vent, then that's wasted potential
        # how far is it to each valve, and know that we lose that much 

        you_vent = self.states.vents.get(self.you_vent_key)
        ele_vent = self.states.vents.get(self.elephant_vent_key)
        this_state = node.obj

        # what is the maximum wasted potential? 
        # how much can we release in the time left?
        time_left=MAX_MINS - node.time_least_visited        
        
        nearest_valves = \
            [c for c in self.states.vents.closest_vents[you_vent.key] if c[0]<time_left and VentState.is_closed(c[1],this_state.vent_state)] \
            + [c for c in self.states.vents.closest_vents[ele_vent.key] if c[0]<time_left and VentState.is_closed(c[1],this_state.vent_state)] 
        
        unique_valves_open = {}
        for v in nearest_valves:
            unique_valves_open[v[1].key]=v
        
        # min flow first 
        cost = 0
        step =0
        for uvo in sorted(unique_valves_open.values(), key=lambda v: v[1].rate):
            step = step + uvo[0]
            if step < time_left:
                cost += uvo[1].rate



                

        # but if we are turning valves on, wasted potential is much less
        if VentState.is_turning(ele_vent,this_state.vent_state):
            cost -= ele_vent.rate
        if VentState.is_turning(you_vent,this_state.vent_state):
            cost -= you_vent.rate
        
        wasted_potential = cost*time_left

        sorted_unique_valves_open = sorted(list(unique_valves_open.values()),key=lambda x: x[0])

        if len(nearest_valves):
            min_time,vent = sorted_unique_valves_open[0]
            wasted_potential = min_time*cost

        return max(wasted_potential,0)


    def copy (self,state):
        return State(self.vent_state,self.you_vent_key,self.elephant_vent_key,self.flow,self.cost,self.states)

    def children(self,astar_obj,node_obj):
        self.unique_kids.clear()
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
        self.nearest_vents_lookup = {}
        self.closest_vents = {}
        self.valves = list()

    def update_valve_info(self):
        self.valves = [v for v in self.vents.values() if v.rate]
        for index,v in enumerate(self.valves):
            v.valve_index = index

    def add(self,obj):
        if self.get(obj.key) is None:
            self.vents[obj.key] = obj
        if obj.rate:
            self.valves.append(obj)
    def exists(self,key):
        return self.get(key)
    def get (self,key):
        if key in self.vents.keys(): 
            return self.vents[key]
        return 
    def get_all(self):
        return self.vents.values()
    
    def distances_to_nearest_vent(self):
        for v in self.vents.values():
            self._list_of_nearest_vents(v)


    def _list_of_nearest_vents (self,vent):
        if vent.key in self.nearest_vents_lookup:
            return self.nearest_vents_lookup[vent.key]
        
        dijkstra = AStar(vent)
        shortest_paths = dijkstra.find_until(lambda x,y: False)
        self.nearest_vents_lookup[vent.key] = {}
        self.closest_vents[vent.key] = list()
        
        for node in shortest_paths :
            if node.obj.rate != 0:               
                #self.nearest_vents_lookup[vent.key][node.id] = (node.time_least_visited, [n.id for n in dijkstra._get_path(node)] ) 
                self.closest_vents[vent.key].append((node.time_least_visited,node.obj))
    def flow(self,vent_state):
        flow = 0
        for v in self.valves:
            if VentState.is_open(v,vent_state):
                flow+= v.rate
        return flow

    def cost(self,vent_state):
        cost = 0
        for v in self.valves:
            if not VentState.is_open(v,vent_state):
                cost += v.rate
        return cost

    def max_flow (self):
        return sum (v.rate for v in self.valves)



# ============================================================================
class Vent:
# ============================================================================
    def __eq__(self,other):
        return self.key == other.key

    def __init__(self,id):
        self.rate = 0
        self.key = id
        self.cost = 1
        self.child_ids = {}
        self.valve_index = None
    
    def eta(self,node):
        return 0

    def add_child( self, obj):
        self.child_ids[obj.key] = obj

    def children (self,x=None,y=None):
        return self.child_ids.values()

    def children_and_self (self):
        return itertools.chain(self.child_ids.values(), (self,))
    

class VentState:
    @classmethod
    def new (self,vents):
        return "-"*(len(vents.valves))
    @classmethod
    def open(self,vent,vent_str):
        if VentState.is_turning(vent,vent_str):
            return vent_str[:vent.valve_index] + '*' + vent_str[vent.valve_index+1:]
        return vent_str
    @classmethod
    def turn(self,vent,vent_str):
        if VentState.is_closed(vent,vent_str):
            return vent_str[:vent.valve_index] + '+' + vent_str[vent.valve_index+1:]
        return vent_str
    @classmethod
    def is_open(self,vent,vent_str):
        return vent.valve_index is not None and vent_str[vent.valve_index] == '*'
    @classmethod
    def is_closed(self,vent,vent_str):
        return vent.valve_index is not None and vent_str[vent.valve_index] == '-'
    @classmethod
    def is_turning(self,vent,vent_str):
        return vent.valve_index is not None and vent_str[vent.valve_index] == '+'
    @classmethod
    def open_any_turned_valves(self,vent_str):
        return re.sub(r'\+', "*", vent_str)
    @classmethod
    def all_vents_open(self,vents,vent_str):
        global     vents_all_open
        if vents_all_open is None:
            vent_state = self.new(vents)
            for vent in vents.valves:
                if vent.rate:
                    vent_state = self.turn(vent,vent_state)
                    vent_state = self.open(vent,vent_state)
            vents_all_open = vent_state
        return vents_all_open == vent_str









# ===================================================================
# Entry point
# ===================================================================
if __name__ == '__main__':
    global start
    start = time.time()
    main()    
    end = time.time()

    total_time = end - start
    print("\n"+ str(total_time))
 
