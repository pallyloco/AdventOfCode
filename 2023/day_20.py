from __future__ import annotations
from collections import deque
from typing import Any
import re
from io import StringIO
import pyperclip as pc

"""
Flip-flop modules (prefix %) are either on or off; they are initially off.
If a flip-flop module receives a high pulse, it is ignored and nothing happens.
However, if a flip-flop module receives a low pulse, it flips between on and off.
If it was off, it turns on and sends a high pulse.
If it was on, it turns off and sends a low pulse.

Conjunction modules (prefix &) remember the type of the most recent pulse received
from each of their connected input modules;
they initially default to remembering a low pulse for each input.
When a pulse is received, the conjunction module first updates its memory for that input.
Then, if it remembers high pulses for all inputs,
    it sends a low pulse; otherwise, it sends a high pulse.

There is a single broadcast module (named broadcaster). When it receives a pulse,
it sends the same pulse to all of its destination modules.

Here at Desert Machine Headquarters, there is a module with a single button on it called,
aptly, the button module. When you push the button, a single low pulse is sent directly
to the broadcaster module.
"""

all_machines: dict[str, tuple[Machine, str]] = dict()

# answer too low: 707778288

def main():
    file = open("day_20_input.txt", 'r')
    all_machines["output"] = (Output("output"), "")
    machine_list = list()
    for line in map(str.rstrip, file):
        name, to = re.split(r"\s*->\s*", line)
        if name == "broadcaster":
            name = "-broadcaster"
            all_machines["broadcaster"] = (Broadcaster("broad"), to)
        if name[0:1] == "%":
            all_machines[name[1:]] = (FlipFlop(name[1:]), to)
        if name[0:1] == "&":
            all_machines[name[1:]] = (Conjunction(name[1:]), to)
        machine_list.append(all_machines[name[1:]][0])

    for m, to in all_machines.values():
        if to:
            for t in re.split(r"\s*,\s*", to):
                if t not in all_machines:
                    t = "output"
                m.add_listener(all_machines[t][0])
                if all_machines[t][0] != "output":
                    all_machines[t][0].add_input_machine(m)

    button = Button("button")
    button.add_listener(all_machines["broadcaster"][0])

    machines = [m for m,_ in all_machines.values()]
    print(sum(1 for m in machines if isinstance(m,FlipFlop))/4)
    i = 1
    # 4096 is too low
    machines.sort()
    digits = dict()
    for i in range(5000):
        state1 = 0
        state2 = 0
        state3 = 0
        state4 = 0
        for name in "kx pn hl hm zm cz zf xf ch ht sv dl".split():
            m = all_machines[name][0]
            state1 = (state1 << 1) + int(m.state)
        if state1 == 0:
            pass
            print(f"State 1 is zero after {i} button presses")

        for name in "bf hh sm vv pv bh lc xb fc nx dr fb".split():
            m = all_machines[name][0]
            state2 = (state2 << 1) + int(m.state)
        if state2 == 0:
            pass
            print(f"State 2 is zero after {i} button presses")

        for name in "lq gv zv sr gd lg tb zc st mt mb xg".split():
            m = all_machines[name][0]
            state3 = (state3 << 1) + int(m.state)
        if state3 == 0:
            pass
            print(f"State 3 is zero after {i} button presses")

        for name in "rs nh rv pb mh sg ts qq gb dc vd gh".split():
            m = all_machines[name][0]
            state4 = (state4 << 1) + int(m.state)
        if state4 == 0:
            pass
            print(f"State 4 is zero after {i} button presses")

        #print (state1, state2, state3, state4)
        if i>100000:
            g = Graphiz(machines)
            g.draw_graph()
            input(f"Button has been pressed {i} times")
            print()
            print()
        button.send(0, 1)
        while len(bus.queue):
            bus.process()
        if machines_at_initial_values(machines):
            break

    bl = bus.low_signals
    bh = bus.high_signals

    num_times = 1000//(i+1)
    bus.low_signals = bl * num_times
    bus.high_signals = bh * num_times

    print ("part 1: num signals is: ",bus.low_signals, bus.high_signals, bus.low_signals*bus.high_signals)

    # ---------------- part 2
    #print (gcm(3917,3931,3943,4057))


def machines_at_initial_values(machines: list[Machine])->bool:
    return all(not m.state for m in machines)
class Signal:
    def __init__(self, from_machine: Machine, to_machine: Machine, pulse: int, priority: int):
        self.from_machine: Machine = from_machine
        self.to_machine: Machine = to_machine
        self.pulse: int = pulse
        self.priority: int = priority

    def __lt__(self, other):
        return self.priority < other.priority

    def __str__(self):
        return f"p:{self.priority}:\t{self.from_machine} \t-> {int(self.pulse)} ->\t {self.to_machine}"

    def __repr__(self):
        return str(self)


class Bus:
    def __init__(self):
        self.queue: list[Signal] = []
        self.low_signals = 0
        self.high_signals = 0
        self.signals = 0

    def process(self):
        if not self.queue:
            return []

        self.queue.sort()
        lowest_priority = self.queue[0].priority
        for signal in self.queue:
            if signal.priority != lowest_priority:
                continue
            self.signals = (self.signals << 1) + int(signal.pulse)
            if signal.pulse:
                self.low_signals += 1
            else:
                self.high_signals += 1
            signal.to_machine.receive(signal)

        self.queue = [s for s in self.queue if s.priority != lowest_priority]

    def push(self, what: Signal):
        self.queue.append(what)
        # print ("queue-up",what, self.queue)


bus: Bus = Bus()


class Machine:
    def __init__(self, name: str):
        self.name = name
        self.state = 0
        self.listeners: list[Machine] = list()

    def add_listener(self, m: Machine):
        m.state = 0
        self.listeners.append(m)

    def receive(self, signal: Signal): pass

    def send(self, pulse: int, priority: int):
        for listener in self.listeners:
            bus.push(Signal(self, listener, pulse, priority))

    def add_input_machine(self, m: Machine): pass

    def button_push(self): pass

    def __str__(self):
        s = str(type(self))
        _, name = s.split(".")
        return f"{self.name}:{int(self.state)}"

    def __repr__(self):
        return str(self)

    def __lt__(self,other):
        return self.name < other.name


class Output(Machine):

    def receive(self, signal: Signal):
        self.state = signal.pulse
        if not signal.pulse:
            input("rx received low button press: ")


class FlipFlop(Machine):
    def receive(self, signal: Signal):
        if not signal.pulse:
            self.state = not self.state
            self.send(self.state, signal.priority + 1)


class Conjunction(Machine):

    def __init__(self, name):
        super().__init__(name)
        self.last_pulse: dict[str, int] = dict()

    def receive(self, signal: Signal):
        self.last_pulse[signal.from_machine.name] = signal.pulse
        if all(m for m in self.last_pulse.values()):
            self.state = 0
            self.send(0, signal.priority + 1)
        else:
            self.state = 1
            self.send(1, signal.priority + 1)

    def add_input_machine(self, m: Machine):
        self.last_pulse[m.name] = 0


class Broadcaster(Machine):
    def receive(self, signal: Signal):
        self.send(signal.pulse, signal.priority + 1)


class Button(Machine):
    def receive(self, signal: Signal):
        self.send(0, 1)

    def button_push(self):
        self.send(0, 1)





class Graphiz:
    def __init__(self, machines: list[Machine]):
        self.machines: list[Machine] = machines
        self.file = StringIO()

    def draw_graph(self):
        print("digraph G {", file=self.file)
        print("node [style=filled]", file=self.file)
        for m in self.machines:
            if m.name =="output":
                print("rx [fillcolor=white, color=black]", file=self.file)
            elif m.name == "broad":
                print("broad [fillcolor=white, color=black]", file=self.file)
                for l in m.listeners:
                    print(m.name,"->",l.name, "[color=black]", file=self.file)
            elif isinstance(m,FlipFlop):
                if m.state:
                    print(m.name,"[fillcolor=pink, color=red]", file=self.file)
                else:
                    print(m.name,"[fillcolor=white, color=red]", file=self.file)
                for l in m.listeners:
                    print(m.name,"->",l.name, "[color=red]", file=self.file)
            elif isinstance(m,Conjunction):
                if all(mm for mm in m.last_pulse.values()):
                    print(m.name,"[fillcolor=grey, color=black]", file=self.file)
                else:
                    print(m.name,"[fillcolor=white, color=black]", file=self.file)
                for l in m.listeners:
                    print(m.name,"->",l.name, "[color=black]", file=self.file)

        print("}", file=self.file)
        self.file.seek(0)
        s=self.file.read()
        pc.copy(s)


if __name__ == "__main__":
    main()

# x=sum(int(m.state) for m in (mm for mm in machines if isinstance(mm,FlipFlop)))
# if x == 4:
#     print(i,":",end="")
#     for m in (mm for mm in machines if isinstance(mm,FlipFlop)):
#         if m.state:
#             print(m.name,end="  ")
#     print ()
# state1 = 0
# for name in ('hl','hm','gd','bh','lc','qq','ch','dc','dr','dl'):
#     m = all_machines[name][0]
#     state1 = (state1 << 1) + int(m.state)
# state2 = 0
# for name in ('rv','pb','mh','cz','tb','xb','fc','ht','mb','fb'):
#     m = all_machines[name][0]
#     state2 = (state2 << 1) + int(m.state)
# state3 = 0
# for name in ( 'sm',"sr","pv","lg","ts","xf","gb","mt","sv","gh"):
#     m = all_machines[name][0]
#     state3 = (state3 << 1) + int(m.state)
# state4 = 0
# for name in ("zv","vv","zm","sg","zf", "zc", "st", "nx", "vd", "xg"):
#     m = all_machines[name][0]
#     state4 = (state4 << 1) + int(m.state)
#
# print(
#      i,
#      bin(state1)[2:].zfill(10),
#      bin(state2)[2:].zfill(10)
#         )
#
