from __future__ import annotations
import re  # regular expressions

from astar_best_so_far2 import AStar, Node  # A* algorithm
import time
from enum import Enum
from dataclasses import dataclass

part = 1
if part == 1:
    MAX: int = 24
else:
    MAX: int = 32

# Answer part 1: (2:15, 3:5, 5:9, 6:4, 11:2, 12:10, 13:1, 14:1, 16:2, 19:1, 20:5, 22:7, 23:8, 24:5, 25:1, 29:7, 30:1
#                = 1150
# Answer part 2: (11,79,43) = 37367
Blueprint = None


# ----------------------------------------------------------------------------
# main code
# ----------------------------------------------------------------------------
def main():
    global Blueprint
    if part == 1:
        answer = 0
    else:
        answer = 1
    file = open("day19_input.txt", 'r')
    for num, line in enumerate(map(str.rstrip, file)):
        Blueprint = BluePrint(line)
        if num != 22:
            continue
        astar = AStar(State(), zero=Cost(), print_at_n_intervals=50000)

        # cb function returns true if final state is reached
        final_nodes: list[Node] = astar.find_until(is_final_state)
        print("Number: ", Blueprint.number)
        print("Path to get there:")
        if final_nodes:
            nodes = astar.get_path(final_nodes[0])
            for node in nodes:
                print(f"id: {node.id} cost: {node.cumulative_cost}")

        if part == 1:
            answer += final_nodes[0].obj.geode * Blueprint.number
        else:
            answer = answer * final_nodes[0].obj.geode
            if num == 2:
                break
    print(f"answer = {answer}")


def is_final_state(state: State) -> bool:
    return state.final_state()


# ----------------------------------------------------------------------------
# Robot & Mining Factory
# ----------------------------------------------------------------------------
class RobotType(Enum):
    ore = 1
    clay = 2
    obsidian = 3
    geode = 4


def build_robot_and_mine(state: State, robot: RobotType) -> bool:
    # Note: pay for robot before mining!
    # Note: mine minerals before updating the number of robots!
    prices: list[BuildRobotPrice] = [
        None,
        Blueprint.ore_robot_cost,
        Blueprint.clay_robot_cost,
        Blueprint.obsidian_robot_cost,
        Blueprint.geode_robot_cost
    ]
    price = prices[robot.value]
    if state.ore >= price.ore and state.clay >= price.clay and state.obsidian >= price.obsidian:
        state.ore -= price.ore
        state.clay -= price.clay
        state.obsidian -= price.obsidian
        mine_minerals(state)
        current_num_robots = getattr(state, robot.name + "_robot", 0)
        setattr(state, robot.name + "_robot", current_num_robots + 1)
        return True

    return False


def mine_minerals(state: State):
    state.ore += state.ore_robot
    state.clay += state.clay_robot
    state.obsidian += state.obsidian_robot
    state.geode += state.geode_robot
    state.day += 1


# ----------------------------------------------------------------------------
# how much it costs to build a robot
# ----------------------------------------------------------------------------
@dataclass
class BuildRobotPrice:
    ore: int
    clay: int
    obsidian: int

    # def __str__(self):
    #     return f"({self.ore},{self.clay},{self.obsidian})"
    #
    # def __repr__(self):
    #     return str(self)


# ----------------------------------------------------------------------------
# blue print class
# ----------------------------------------------------------------------------
class BluePrint:

    def __init__(self, line):
        regex = re.match(r'.*?(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+)', line)
        self.number: int = int(regex.group(1))
        self.ore_robot_cost = BuildRobotPrice(ore=int(regex.group(2)), clay=0, obsidian=0)
        self.clay_robot_cost = BuildRobotPrice(ore=int(regex.group(3)), clay=0, obsidian=0)
        self.obsidian_robot_cost = BuildRobotPrice(ore=int(regex.group(4)), clay=int(regex.group(5)), obsidian=0)
        self.geode_robot_cost = BuildRobotPrice(ore=int(regex.group(6)), clay=0, obsidian=int(regex.group(7)))

    def __str__(self):
        return f"{self.number}: {self.ore_robot_cost}, {self.clay_robot_cost}, " \
            + f"{self.obsidian_robot_cost}, {self.geode_robot_cost})"


# ----------------------------------------------------------------------------
# Cost object
# ----------------------------------------------------------------------------
class Cost:
    def __init__(self, rore: int = 0, rclay: int = 0, robsidian: int = 0, rgeode: int = 0,
                 ore: int = 0, clay: int = 0, obsidian: int = 0, geode: int = 0):
        self.rore: int = rore
        self.rclay: int = rclay
        self.robsidian: int = robsidian
        self.rgeode: int = rgeode
        self.ore: int = ore
        self.clay: int = clay
        self.obsidian: int = obsidian
        self.geode: int = geode

    def __lt__(self, other) -> bool:
        if self.rgeode != other.rgeode:
            return self.rgeode < other.rgeode
        # if self.geode != other.geode:
        #    return self.geode > other.geode
        if self.robsidian != other.robsidian:
            return self.robsidian < other.robsidian
        # if self.obsidian != other.obsidian:
        #    return self.obsidian > other.obsidian
        if self.rclay != other.rclay:
            return self.rclay < other.rclay
        # if self.clay != other.clay:
        #    return self.clay > other.clay
        if self.rore != other.rore:
            return self.rore < other.rore
        return self.ore > other.ore

    def __add__(self, other) -> Cost:
        return Cost(
            self.rore + other.rore,
            self.rclay + other.rclay,
            self.robsidian + other.robsidian,
            self.rgeode + other.rgeode,
            self.ore + other.ore,
            self.clay + other.clay,
            self.obsidian + other.obsidian,
            self.geode + other.geode
        )

    def __sub__(self, other) -> Cost:
        return Cost(
            self.rore - other.rore,
            self.rclay - other.rclay,
            self.robsidian - other.robsidian,
            self.rgeode - other.rgeode,
            self.ore - other.ore,
            self.clay - other.clay,
            self.obsidian - other.obsidian,
            self.geode - other.geode
        )

    def __str__(self):
        return f"({self.rore},{self.rclay},{self.robsidian},{self.rgeode})"

    def __repr__(self):
        return str(self)


# ----------------------------------------------------------------------------
# what do we currently have
# ----------------------------------------------------------------------------
class State:

    def key(self) -> str:
        return self.readable()

    def edge_cost(self) -> Cost:
        return Cost(
            MAX - self.ore_robot,
            MAX - self.clay_robot,
            MAX - self.obsidian_robot,
            MAX - self.geode_robot,
            self.ore,
            self.clay,
            self.obsidian,
            self.geode

        )

    def __init__(self, other: State = None):
        self.kids = None
        self.was_visited: bool = False
        if other is None:
            self.ore = 0
            self.clay = 0
            self.obsidian = 0
            self.geode = 0
            self.ore_robot = 1
            self.clay_robot = 0
            self.obsidian_robot = 0
            self.geode_robot = 0
            self.day = 0
        else:
            self.ore = other.ore
            self.clay = other.clay
            self.obsidian = other.obsidian
            self.geode = other.geode
            self.ore_robot = other.ore_robot
            self.clay_robot = other.clay_robot
            self.obsidian_robot = other.obsidian_robot
            self.geode_robot = other.geode_robot
            self.day = other.day

    def eta(self, *_) -> Cost:
        t = ((MAX-self.day)*(MAX-self.day+1))//2
        ore = t + (MAX-self.day)*(self.day - self.ore_robot)
        clay = t + (MAX-self.day)*(self.day - self.clay_robot)
        obsidian = t + (MAX-self.day)*(self.day - self.obsidian_robot)
        geode = t + (MAX-self.day)*(self.day - self.geode_robot)
        if (ore < 0 or clay < 0 or obsidian < 0 or geode < 0):
            pass

        return Cost(ore, clay, obsidian, geode)

    def children(self, *_):
        if self.kids is not None:
            return self.kids

        children: list[State] = list()

        # do nothing
        child = State(self)
        mine_minerals(child)
        children.append(child)

        # make robots if you can
        for robot_type in RobotType:
            other_child = State(self)
            if build_robot_and_mine(other_child, robot_type):
                children.append(other_child)

        self.kids = children
        return children

    def final_state(self):
        return self.day == MAX

    def readable(self):
        return f"{self.day}: " + \
            f"Robots:({self.ore_robot},{self.clay_robot},{self.obsidian_robot},{self.geode_robot})" + \
            f" Ore:({self.ore},{self.clay},{self.obsidian},{self.geode})"


# ===================================================================
# Entry point
# ===================================================================
if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()

    total_time = end - start
    print("\n" + str(total_time))
