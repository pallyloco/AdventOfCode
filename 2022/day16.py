from __future__ import annotations
import re  # regular expressions
from functools import partial

from Astar import AStar, Node  # A* algorithm
import time
import itertools
from typing import Iterable, Iterator, Optional, Dict

MAX_MINS: int = 18
final_max_flow_rate: int = 0
final_max_flow: int = 0
final_paths = dict()
vents_all_open = None
max_flow_cost: Optional[int] = None
max_minute = 0


# ============================================================================
# main code
# ============================================================================
def main():
    global max_flow_cost

    file = open("day16_input.txt", 'r')
    vents = Vents()

    # read the input and create "Vent" objects
    for line in map(str.rstrip, file):
        regex = re.match(r".*?Valve (?P<valve_key>[A-Z]+) .*?rate=(?P<rate>\d+).*?valves? (?P<neighbours>.*)", line)

        vent: Vent = Vent(regex.group('valve_key'), vents)
        vent.rate = int(regex.group('rate'))
        vent.child_id_keys = str.rstrip(regex.group('neighbours'))
        vents.add(vent)

    # go through all the events, and link the child_id_keys to the actual children
    for vent in vents:
        if vent.child_id_keys is not None:
            for dest_valve_key in vent.child_id_keys.split(","):
                vent.add_child(vents.get(str.strip(dest_valve_key)))
    vents.update_valve_info()

    # ----------------------------------------------------------------------------
    # set up initial state
    # ----------------------------------------------------------------------------
    initial_state_of_all_vents = StateOfAllVents(str(vents))
    you_are_here = 'AA'
    elephant_is_there = 'AA'
    initial_state = State(initial_state_of_all_vents, you_are_here, elephant_is_there, vents, 0)
    max_flow_cost = vents.max_flow()

    # calculate minimum costs via astar
    dijkstra = AStar(initial_state, zero=0, print_at_n_intervals=0)
    final_node: Optional[Node] = dijkstra.find_until(partial(have_we_reached_the_end, vents))
    print("Path to get there:")
    total_flow = 0
    ccost = -210
    if final_node:
        nodes = dijkstra.get_path(final_node)
        for minute, node in enumerate(nodes):
            state = node.obj
            total_flow += state.flow_rate()
            ccost = ccost + (210 - state.flow_rate())
            print(f"x{ccost}\tcosts: {node.cumulative_cost},{node.forecasted_cost}\tstate: {node.id}, flow_rate: {state.flow_rate()}, total: {total_flow}")

        node = nodes[-1]
        for _ in range(minute, MAX_MINS):
            state = node.obj
            ccost = ccost + (210 - state.flow_rate())
            total_flow += state.flow_rate()
            print(f"x{ccost}\tcosts: {node.cumulative_cost},{node.forecasted_cost}\tstate: {node.id}, flow_rate: {state.flow_rate()}, total: {total_flow}")


# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
def have_we_reached_the_end(vents, state: State) -> bool:
    global max_minute
    if state.vent_state.all_vents_open(vents):
        return True
    if state.minutes > max_minute:
        max_minute = state.minutes
        print(state.key())

    return state.minutes == MAX_MINS


# ============================================================================
# State (dijkstra object needed for AStar algorithm)
# ============================================================================
class State:

    @staticmethod
    def make_key(vent_state: str, you_vent_key: str, elephant_vent_key: str) -> str:
        one, two = sorted((you_vent_key, elephant_vent_key))
        return f"{vent_state}-{one}-{two}"

    # ----------------------------------------------------------------------------
    # constructor
    # ----------------------------------------------------------------------------
    def __init__(self, vent_state: StateOfAllVents, you_are_here: str, elephant_is_there: str,
                 vents: Vents, minutes: int):
        self.vent_state: StateOfAllVents = vent_state
        self.you_are_here: str = you_are_here
        self.elephant_is_there: str = elephant_is_there
        self._key: str = State.make_key(vent_state, you_are_here, elephant_is_there)+f"__{minutes}"
        self.unique_kids: Dict[str, State] = dict()
        self.vents = vents
        self.minutes = minutes

    def key(self) -> str:
        return self._key

    def flow_rate(self):
        return sum(v.rate for v in self.vents.valves if self.vent_state.is_open(v))

    def edge_cost(self, *_) -> int:
        return sum(v.rate for v in self.vents.valves if not self.vent_state.is_open(v))

    # ----------------------------------------------------------------------------
    # estimated cost to get to the finish line
    # ----------------------------------------------------------------------------
    def eta(self, node=None) -> int:
        #return 0

        time_left = MAX_MINS - self.minutes

        # maximum lost flow if no valves opened
        potential_flow = sum(v.rate for v in self.vents.valves if not self.vent_state.is_open(v))
        max_flow_lost = potential_flow * time_left

        # assume best case scenario, you and elephant open valves every second minute,
        # in order of the largest rate valves first
        open_valve_rates: list[int] = sorted(
            (v.rate for v in self.vents.valves if not self.vent_state.is_open(v)))
        opened_flow: int = 0
        best_outflow: int = 0
        for minute in range(time_left):
            if open_valve_rates and (minute+1)%2:
                opened_flow += open_valve_rates.pop(-1)
                if open_valve_rates:
                    opened_flow += open_valve_rates.pop(-1)
            best_outflow = best_outflow + opened_flow
        return max_flow_lost - best_outflow

    # ----------------------------------------------------------------------------
    # get the next possible states
    # ----------------------------------------------------------------------------
    def children(self, *_) -> list[State]:
        self.unique_kids.clear()

        # get info about current state
        you_vent = self.vents.get(self.you_are_here)
        ele_vent = self.vents.get(self.elephant_is_there)
        vent_state = self.vent_state

        # open appropriate vents (will only work if it has already been turned)
        new_vent_state = vent_state.open_any_turned_valves()

        # find all possible children - can stay at the same spot only if rate and
        # is not already opened
        you_kids = [v for v in you_vent.children_and_self() if
                    v != you_vent or (v == you_vent and v.rate and vent_state.is_closed(v))]
        ele_kids = [v for v in ele_vent.children_and_self() if
                    v != ele_vent or (v == ele_vent and v.rate and vent_state.is_closed(v))]

        # loop through all possible kids between you and elephant
        for you_vc in you_kids:
            for elephant_vc in ele_kids:

                # turning a vent

                # both you and the elephant can turn the vent
                if you_vc.key == you_vent.key and elephant_vc.key == ele_vent.key:
                    tmp_vent_state = new_vent_state.turn(you_vc)
                    tmp_vent_state = tmp_vent_state.turn(elephant_vc)
                    self._add_child(State(tmp_vent_state, you_vc.key, elephant_vc.key, self.vents, self.minutes + 1))

                # you can turn a vent
                elif you_vc.key == you_vent.key:
                    tmp_vent_state = new_vent_state.turn(you_vc)
                    self._add_child(State(tmp_vent_state, you_vc.key, elephant_vc.key, self.vents, self.minutes + 1))

                # the elephant can turn a vent
                elif elephant_vc.key == ele_vent.key:
                    tmp_vent_state = new_vent_state.turn(elephant_vc)
                    self._add_child(State(tmp_vent_state, you_vc.key, elephant_vc.key, self.vents, self.minutes + 1))

                # add the new state to the children
                self._add_child(State(new_vent_state, you_vc.key, elephant_vc.key, self.vents, self.minutes + 1))

        return list(self.unique_kids.values())

    # ----------------------------------------------------------------------------
    # add child
    # ----------------------------------------------------------------------------
    def _add_child(self, state: State):
        self.unique_kids[state._key] = state


# ============================================================================
# ============================================================================
class Vents:
    __slots__ = ('vents', 'nearest_vents_lookup', 'closest_vents', 'valves')

    def __iter__(self) -> Iterator[Vent]:
        return iter(self.vents.values())

    def __contains__(self, key: str) -> bool:
        return key in self.vents

    def __init__(self):
        self.vents: dict[str, Vent] = dict()
        self.nearest_vents_lookup: dict[str, Vent] = dict()
        self.closest_vents: dict[str, Vent] = dict()
        self.valves = list()

    def __str__(self):
        return "-" * (len(self.valves))

    def update_valve_info(self):
        self.valves = [v for v in self if v.rate]
        for index, v in enumerate(self.valves):
            v.valve_index = index

    def add(self, obj: Vent):
        if obj.key not in self:
            self.vents[obj.key] = obj
        if obj.rate:
            self.valves.append(obj)

    def get(self, key: str) -> Optional[Vent]:
        if key in self.vents:
            return self.vents[key]
        return

    def max_flow(self) -> int:
        return sum(v.rate for v in self.valves)


# ============================================================================
# Vent
# ============================================================================
class Vent:
    __slots__ = ('rate', 'key', 'cost', 'child_ids', 'valve_index', 'child_id_keys', 'vents')

    def __eq__(self, other: Vent) -> bool:
        return self.key == other.key

    def __init__(self, identifier: str, vents: Vents):
        self.rate = 0
        self.key = identifier
        self.cost = 1
        self.child_ids = dict()
        self.valve_index = None
        self.child_id_keys: Optional[str] = None
        self.vents = vents

    def add_child(self, obj: Vent) -> None:
        self.child_ids[obj.key] = obj

    def children(self, *_) -> Iterable[Vent]:
        return self.child_ids.values()

    def children_and_self(self) -> Iterable[Vent]:
        return itertools.chain(self.child_ids.values(), (self,))


# ============================================================================
# State Of All Vents
# ============================================================================
class StateOfAllVents(str):
    """
    A string with the following info:
    -   untouched
    *   valve is opened
    +   valve is being turned
    """

    def open_a_vent(self, vent: Vent) -> StateOfAllVents:
        if self.is_turning(vent):
            return StateOfAllVents(self[:vent.valve_index] + '*' + self[vent.valve_index + 1:])
        return self

    def turn(self, vent: Vent) -> StateOfAllVents:
        if self.is_closed(vent):
            return StateOfAllVents(self[:vent.valve_index] + '+' + self[vent.valve_index + 1:])
        return self

    def is_open(self, vent: Vent) -> bool:
        return vent.valve_index is not None and self[vent.valve_index] == '*'

    def is_closed(self, vent: Vent) -> bool:
        return vent.valve_index is not None and self[vent.valve_index] == '-'

    def is_turning(self, vent: Vent) -> bool:
        return vent.valve_index is not None and self[vent.valve_index] == '+'

    def open_any_turned_valves(self) -> StateOfAllVents:
        return StateOfAllVents(re.sub(r'\+', "*", self))

    def all_vents_open(self, vents) -> bool:
        global vents_all_open
        if vents_all_open is None:
            vent_state = StateOfAllVents(vents)
            for vent in vents.valves:
                if vent.rate:
                    vent_state = vent_state.turn(vent)
                    vent_state = vent_state.open_a_vent(vent)
            vents_all_open = vent_state
        return vents_all_open == self

    def current_flow_rate(self, vents) -> int:
        return sum((v.rate for v in vents.valves if self.is_open(v)))


# ===================================================================
# Entry point
# ===================================================================
if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()

    total_time = end - start
    print("\n" + str(total_time))

"""

15 days

Path to get there:
state: ----------------AA-AA__0, flow_rate: 0, total: 0
state: ----------------BZ-TL__1, flow_rate: 0, total: 0
state: ----------------AI-KY__2, flow_rate: 0, total: 0
state: --+-------------AI-CJ__3, flow_rate: 0, total: 0
state: --*----+--------CJ-MM__4, flow_rate: 11, total: 11
state: --*----*--------JW-RG__5, flow_rate: 21, total: 32
state: --*----*--------KB-KS__6, flow_rate: 21, total: 53
state: --*----*-+----+-KB-KS__7, flow_rate: 21, total: 74
state: --*----*-*----*-GD-OY__8, flow_rate: 55, total: 129
state: --*----*-*----*-AO-QK__9, flow_rate: 55, total: 184
state: --*--+-*-*----*-CU-QK__10, flow_rate: 55, total: 239
state: --*--*-*-*+---*-CU-EJ__11, flow_rate: 70, total: 309
state: --*--*-*-**---*-DP-LY__12, flow_rate: 89, total: 398
state: --*--*-*-**---*-IZ-YE__13, flow_rate: 89, total: 487
state: -+*-+*-*-**---*-IZ-YE__14, flow_rate: 89, total: 576
state: -**-**-*-**---*-DP-LY__15, flow_rate: 133, total: 709

50.802855253219604
"""


"""
18 minutes

Path to get there:
x0	costs: 0,0	state: ----------------AA-AA__0, flow_rate: 0, total: 0
x210	costs: 210,1172	state: ----------------BZ-TL__1, flow_rate: 0, total: 0
x420	costs: 420,1382	state: ----------------AI-KY__2, flow_rate: 0, total: 0
x630	costs: 630,1592	state: --+-------------AI-CJ__3, flow_rate: 0, total: 0
x829	costs: 829,1663	state: --*----+--------CJ-MM__4, flow_rate: 11, total: 11
x1018	costs: 1018,1746	state: --*----*--------JW-RG__5, flow_rate: 21, total: 32
x1207	costs: 1207,1935	state: --*----*--------KB-KS__6, flow_rate: 21, total: 53
x1396	costs: 1396,2121	state: --*----*-+----+-KB-KS__7, flow_rate: 21, total: 74
x1551	costs: 1551,2019	state: --*----*-*----*-GD-OY__8, flow_rate: 55, total: 129
x1706	costs: 1706,2171	state: --*----*-*----*-AO-QK__9, flow_rate: 55, total: 184
x1861	costs: 1861,2323	state: --*--+-*-*----*-CU-QK__10, flow_rate: 55, total: 239
x2001	costs: 2001,2353	state: --*--*-*-*+---*-CU-EJ__11, flow_rate: 70, total: 309
x2122	costs: 2122,2376	state: --*--*-*-**---*-DP-LY__12, flow_rate: 89, total: 398
x2243	costs: 2243,2482	state: --*--*-*-**---*-IZ-YE__13, flow_rate: 89, total: 487
x2364	costs: 2364,2588	state: -+*-+*-*-**---*-IZ-YE__14, flow_rate: 89, total: 576
x2441	costs: 2441,2530	state: -**-**-*-**---*-DP-LY__15, flow_rate: 133, total: 709
x2518	costs: 2518,2592	state: -**-**-*-**---*-CU-EJ__16, flow_rate: 133, total: 842
x2595	costs: 2595,2632	state: -**-**-*-**---*-AO-QK__17, flow_rate: 133, total: 975
x2672	costs: 2672,2672	state: -**-**-*-**---*-OY-UK__18, flow_rate: 133, total: 1108


26 minutes

Path to get there:
costs:    0,   0	state: ----------------AA-AA__0,  flow_rate:   0, total:    0
costs:  210,1172	state: ----------------BZ-TL__1,  flow_rate:   0, total:    0
costs:  420,1382	state: ----------------AI-KY__2,  flow_rate:   0, total:    0
costs:  630,1592	state: --+-------------AI-CJ__3,  flow_rate:   0, total:    0
costs:  829,1663	state: --*----+--------CJ-MM__4,  flow_rate:  11, total:   11
costs: 1018,1746	state: --*----*--------JW-RG__5,  flow_rate:  21, total:   32
costs: 1207,1935	state: --*----*--------KB-KS__6,  flow_rate:  21, total:   53
costs: 1396,2124	state: --*----*-+----+-KB-KS__7,  flow_rate:  21, total:   74
costs: 1551,2019	state: --*----*-*----*-OY-RA__8,  flow_rate:  55, total:  129
costs: 1706,2174	state: --*----*-*----*-AO-XC__9,  flow_rate:  55, total:  184
costs: 1861,2329	state: --*----*-*----*-CU-IZ__10, flow_rate:  55, total:  239
costs: 2016,2484	state: -+*----*-*+---*-CU-IZ__11, flow_rate:  55, total:  294
costs: 2132,2382	state: -**----*-**---*-DP-LY__12, flow_rate:  94, total:  388
costs: 2248,2498	state: -**----*-**---*-EJ-YE__13, flow_rate:  94, total:  482
costs: 2364,2614	state: -**-+--*-**---*-QK-YE__14, flow_rate:  94, total:  576
costs: 2456,2622	state: -**-*+-*-**---*-DP-QK__15, flow_rate: 118, total:  694
costs: 2533,2643	state: -**-**-*-**---*-CU-UK__16, flow_rate: 133, total:  827
costs: 2610,2720	state: -**-**-*-**---*-AO-PB__17, flow_rate: 133, total:  960
costs: 2687,2797	state: -**-**-*-**+--*-OY-PB__18, flow_rate: 133, total: 1093
costs: 2759,2843	state: -**-**-*-***--*-GG-KS__19, flow_rate: 138, total: 1231
costs: 2831,2915	state: -**-**-*-***--*-AI-OF__20, flow_rate: 138, total: 1369
costs: 2903,2987	state: -**-**-*-***--*-CL-ZK__21, flow_rate: 138, total: 1507
costs: 2975,3059	state: -**-**-*-***--*-GU-JN__22, flow_rate: 138, total: 1645
costs: 3047,3121	state: -**+**-*-***--*-EK-GU__23, flow_rate: 138, total: 1783
costs: 3105,3141	state: -*****+*-***--*-EK-VP__24, flow_rate: 152, total: 1935
costs: 3141,3151	state: -*******-***--*-JN-MB__25, flow_rate: 174, total: 2109
costs: 3177,3177	state: -*******+***--*-CL-MB__26, flow_rate: 174, total: 2283

32251.475764274597

"""