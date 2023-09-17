from __future__ import annotations 
import re                           # regular expressions
from astar import AStar,Node             # A* algorithm
import time
import itertools
from typing import Iterable,Iterator,Optional,Dict


MAX_MINS = 15
final_max_flow = 0
final_paths = {}
vents_all_open = None
max_flow_cost = None
vents: Vents = None

# ----------------------------------------------------------------------------
# main code
# ----------------------------------------------------------------------------
def main():
    global max_flow_cost
    global vents
    
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


    initial_vent_state = VentState(vents)
    you_vent_state = 'AA'
    elephant_vent_state = 'AA'
    flow = vents.flow(initial_vent_state)
    cost = vents.cost(initial_vent_state)
    initial_state = State(initial_vent_state,you_vent_state,elephant_vent_state,flow,cost)
    max_flow_cost = vents.max_flow()

    # calculate minimum costs via astar
    dijkstra = AStar(initial_state)
    dijkstra.max_depth = MAX_MINS
    dijkstra.find_until(lambda x,y: astar_cb(x,y)) 







# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
def astar_cb(astar_obj,node_obj):
    global final_max_flow

    path = node_obj.path_least_visited
    time_step = node_obj.time_least_visited

    total_flow = max_flow_cost*time_step - node_obj.cost
    if total_flow > final_max_flow:
        end = time.time()
        total_time = end - start
        print (time_step, node_obj.cost, node_obj.forecasted_cost - node_obj.cost, total_flow, total_time, path)
        final_max_flow = total_flow


    return time_step == MAX_MINS

# ============================================================================
class State:
# ============================================================================

    __slots__ = ('vent_state','you_vent_key','elephant_vent_key','key','cost','flow','unique_kids')
    @staticmethod
    def make_key (vent_state : str, you_vent_key: str ,elephant_vent_key :str) -> str:
        one,two =  sorted( (you_vent_key,elephant_vent_key) ) 
        return f"{vent_state}-{one}-{two}"

    # ----------------------------------------------------------------------------
    # constructor
    # ----------------------------------------------------------------------------
    def __init__(self,vent_state: VentState ,you_vent_key: str ,elephant_vent_key: str, 
                            flow: int, cost: int):
        self.vent_state: VentState = vent_state
        self.you_vent_key: str = you_vent_key
        self.elephant_vent_key: str = elephant_vent_key
        self.key: str = State.make_key(vent_state,you_vent_key,elephant_vent_key)
        self.cost: int = cost
        self.flow: int = flow
        self.unique_kids: Dict[str, State] = {}

    
    # ----------------------------------------------------------------------------
    # estimated cost to get to the finish line
    # ----------------------------------------------------------------------------
    def eta(self,node):

        return 0
        # THIS DOES NOT IMPROVE SPEED OR MEMORY!

        you_vent = vents.get(self.you_vent_key)
        ele_vent = vents.get(self.elephant_vent_key)
        this_state = node.obj

        time_left=MAX_MINS - node.time_least_visited        
        
        nearest_valves_to_me = (c for c in vents.closest_vents[you_vent.key] if c[0]<time_left and this_state.vent_state.is_closed(c[1]))
        nearest_valves_to_ele = (c for c in vents.closest_vents[ele_vent.key] if c[0]<time_left and this_state.vent_state.is_closed(c[1]))
        nearest_valves = [*nearest_valves_to_me, *nearest_valves_to_ele]
        
        unique_valves_open = {v[1].key: v for v in nearest_valves}.values()
        min_time = sorted(unique_valves_open,key=lambda x: x[0])
        if min_time:
            min_time = min_time[0][0]
        else:
            min_time = time_left

        # what is the flow rate of all the valves within reach?
        flow_rate = sum(v[1].rate for v in unique_valves_open)

        # but if we are turning valves on, wasted potential is much less
        if this_state.vent_state.is_turning(ele_vent):
            flow_rate -= ele_vent.rate
        if this_state.vent_state.is_turning(you_vent):
            flow_rate -= you_vent.rate
        
        wasted_potential = flow_rate*min_time
        return max(wasted_potential,0)

    # ----------------------------------------------------------------------------
    # get the next possible states
    # ----------------------------------------------------------------------------
    def children(self,*_) -> Iterable[State]:
        self.unique_kids.clear()

        # get info about current state
        you_vent = vents.get(self.you_vent_key)
        ele_vent = vents.get(self.elephant_vent_key)
        vent_state = self.vent_state        
        
        # open the vent (will only work if it has already been turned)
        new_vent_state = vent_state.open_any_turned_valves()

        # find all possible children - can stay at the same spot only if rate and is not already openned
        you_kids = [v for v in you_vent.children_and_self() if v!=you_vent or (v==you_vent and v.rate and vent_state.is_closed(v))]
        ele_kids = [v for v in ele_vent.children_and_self() if v!=ele_vent or (v==ele_vent and v.rate and vent_state.is_closed(v))]
        
        # loop thru all possible kids between you and elephant
        for you_vc in you_kids:
            for elephant_vc in ele_kids:
                key = State.make_key(new_vent_state,you_vc.key,elephant_vc.key)

                # turning a vent
                if you_vc.key == you_vent.key and elephant_vc.key == ele_vent.key: 
                    tmp_vent_state = new_vent_state.turn(you_vc)
                    tmp_vent_state = tmp_vent_state.turn(elephant_vc)
                    flow = vents.flow(tmp_vent_state)
                    cost = vents.cost(tmp_vent_state)
                    self.add_child( State(tmp_vent_state, you_vc.key, elephant_vc.key,flow,cost))
                elif you_vc.key == you_vent.key: 
                    tmp_vent_state = new_vent_state.turn(you_vc)
                    flow = vents.flow(tmp_vent_state)
                    cost = vents.cost(tmp_vent_state)
                    self.add_child( State(tmp_vent_state, you_vc.key, elephant_vc.key,flow,cost))
                elif elephant_vc.key == ele_vent.key: 
                    tmp_vent_state = new_vent_state.turn(elephant_vc)
                    flow = vents.flow(tmp_vent_state)
                    cost = vents.cost(tmp_vent_state)
                    self.add_child( State(tmp_vent_state, you_vc.key, elephant_vc.key,flow,cost))
        
                # add the new state to the children
                flow = vents.flow(new_vent_state)
                cost = vents.cost(new_vent_state)
                self.add_child( State(new_vent_state, you_vc.key, elephant_vc.key,flow,cost))

        return self.unique_kids.values()

    # ----------------------------------------------------------------------------
    # add child
    # ----------------------------------------------------------------------------
    def add_child(self, state: State) -> Dict[str,State]:
        if self.unique_kids is None:
            self.unique_kids = {}
        self.unique_kids[state.key] = state

# ============================================================================
class Vents:
# ============================================================================
    __slots__ = ('vents','nearest_vents_lookup','closest_vents','valves')
    def __iter__(self) -> Iterator[Vent]:
        return iter(self.vents.values())
    
    def __contains__(self, key: str) -> bool:
        return key in self.vents
        
    def __init__(self):
        self.vents = {}
        self.nearest_vents_lookup = {}
        self.closest_vents = {}
        self.valves = list()
    
    def __str__(self):
        return "-"*(len(self.valves))

    def update_valve_info(self):
        self.valves = [v for v in self if v.rate]
        for index,v in enumerate(self.valves):
            v.valve_index = index

    def add(self,obj: Vent):
        if obj.key not in self:
            self.vents[obj.key] = obj
        if obj.rate:
            self.valves.append(obj)

    def get (self,key:str) -> Optional[Vent]:
        if key in self.vents: 
            return self.vents[key]
        return 

    def distances_to_nearest_vent(self):
        for v in self.vents.values():
            self._list_of_nearest_vents(v)


    def _list_of_nearest_vents (self,vent: Vent):
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

    def flow(self,vent_state: VentState)-> int:
        return sum(v.rate for v in self.valves if vent_state.is_open(v))

    def cost(self,vent_state: VentState) -> int:
        return sum(v.rate for v in self.valves if not vent_state.is_open(v))

    def max_flow (self) -> int:
        return sum (v.rate for v in self.valves)



# ============================================================================
class Vent:
# ============================================================================
    __slots__ = ('rate','key','cost','child_ids','valve_index')
    def __eq__(self,other: Vent) -> bool:
        return self.key == other.key

    def __init__(self, id: int):
        self.rate = 0
        self.key = id
        self.cost = 1
        self.child_ids = {}
        self.valve_index = None
    
    def eta(self,node: AStar) -> int:
        return 0

    def add_child( self, obj: Vent) -> None:
        self.child_ids[obj.key] = obj

    def children (self,*_) -> Iterable[Vent]:
        return self.child_ids.values()

    def children_and_self (self) -> Iterable[Vent]:
        return itertools.chain(self.child_ids.values(), (self,))
    

class VentState (str):

    def open(self,vent: Vent) -> VentState:
        if self.is_turning(vent):
            return VentState(self[:vent.valve_index] + '*' + self[vent.valve_index+1:])
        return self

    def turn(self,vent: Vent) -> VentState:
        if self.is_closed(vent):
            return VentState(self[:vent.valve_index] + '+' + self[vent.valve_index+1:])
        return self

    def is_open(self,vent: Vent) -> bool:
        return vent.valve_index is not None and self[vent.valve_index] == '*'

    def is_closed(self,vent: Vent) -> bool:
        return vent.valve_index is not None and self[vent.valve_index] == '-'

    def is_turning(self,vent: Vent) -> bool:
        return vent.valve_index is not None and self[vent.valve_index] == '+'
    
    def open_any_turned_valves(self) -> VentState:
        return VentState(re.sub(r'\+', "*", self))

    def all_vents_open(self,vents) -> bool:
        global vents_all_open
        if vents_all_open is None:
            vent_state = VentState(vents)
            for vent in vents.valves:
                if vent.rate:
                    vent_state.turn(vent)
                    vent_state .open(vent)
            vents_all_open = vent_state
        return vents_all_open == self









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
 
