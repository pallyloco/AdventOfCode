import re                           # regular expressions
from astar import AStar             # A* algorithm
import time
import itertools
import math


MAX_MINS=32
# Answer (11,79,43) = 37367 

# ----------------------------------------------------------------------------
# main code
# ----------------------------------------------------------------------------
def main():
    answer = 0
    file = open("day19_input.txt", 'r')
    blueprint=((4,0,0), (2,0,0),(3,14,0),(2,0,7))
#    number_of_geodes = run_blueprint(blueprint)
#    print (number_of_geodes)
#    exit()
    for num,line in enumerate(map(str.rstrip,file)):
        blueprint_num, blueprint = parse_blueprint(line)
        print()
        print(f"Blue print {blueprint_num}")
        number_of_geodes = run_blueprint(blueprint)
        answer += number_of_geodes*blueprint_num
        if num==2:
            break
    print (f"{answer=}")

def parse_blueprint(line):
    regex = re.match(r'.*?(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+)',line)
    blueprint_num = int(regex.group(1))
    ore_robot_cost = (int(regex.group(2)),0,0)
    clay_robot_cost = (int(regex.group(3)),0,0)
    obsidian_robot_cost= (int(regex.group(4)),int(regex.group(5)),0)
    geode_robot_cost=(int(regex.group(6)),0,int(regex.group(7)))
    return (blueprint_num, ( ore_robot_cost, clay_robot_cost, obsidian_robot_cost, geode_robot_cost))

def assets(factory):
        p_ore,p_clay,p_obsidian = factory.ore_robot_cost

        payment_clay,p_clay,p_obsidian = factory.clay_robot_cost

        p_ore,p_clay,p_obsidian = factory.obsidian_robot_cost
        payment_obs = p_ore + p_clay*payment_clay

        p_ore,p_clay,p_obsidian = factory.geode_robot_cost
        payment_geo = p_ore + p_clay*payment_clay + payment_obs*p_obsidian

        return factory.ore + (factory.num_ore_robot-1) + \
            payment_clay*(factory.clay+factory.num_clay_robot) + \
                payment_obs*(factory.num_obsidian_robot+factory.obsidian) + \
                    payment_geo*(factory.num_geode_robot+factory.geode)



def run_blueprint(blueprint):
    ore_robot_cost, clay_robot_cost, obsidian_robot_cost, geode_robot_cost = blueprint

    factory = Factory(ore_robot_cost, clay_robot_cost, obsidian_robot_cost, geode_robot_cost)

    children = [None]*(MAX_MINS+1)
    children[0] = {factory.key: factory}
    for minute in range(MAX_MINS):
        children[minute+1] = {}

#        half_max = assets(max(children[minute].values(), key=assets))//2        
#        if minute > 20: half_max = ( half_max * 4)//3
        

#        for child in (child for child in children[minute].values() if assets(child) >= half_max):

        max_assets_dict = {assets(child):1 for child in children[minute].values()}
        min_asset_for_this_generation = sorted(max_assets_dict.keys(),reverse=True)[min(len(max_assets_dict)-1,2*MAX_MINS)]
        for num,child in enumerate(child for child in children[minute].values() if assets(child) >= min_asset_for_this_generation ):            
            for grand_child in child.children():
                children[minute+1][grand_child.key] = grand_child
        print ("processed",num)
        print (minute, len(children[minute+1]), len(max_assets_dict),min_asset_for_this_generation,end=" ")
        children[minute].clear()


        maxg = 0
        maxf = None
        for f in children[minute+1].values():
            if f.geode >= maxg:
                maxf = f
                maxg = max(maxg,f.geode)
        print (f"num geodes is {maxf.geode}")
    return maxf.geode


# To collect the obsidian from the bottom of the pond, you'll need waterproof 
# obsidian-collecting robots. 
# Fortunately, there is an abundant amount of clay nearby that you can use to make them waterproof.    

# In order to harvest the clay, you'll need special-purpose clay-collecting robots. 
# To make any type of robot, you'll need ore, which is also plentiful but in the 
# opposite direction from the clay.

# Collecting ore requires ore-collecting robots with big drills. 
# Fortunately, you have exactly one ore-collecting robot in your pack that you 
# can use to kickstart the whole operation.

# Each robot can collect 1 of its resource type per minute. 
# It also takes one minute for the robot factory (also conveniently from your pack) 
# to construct any type of robot, although it consumes the necessary resources 
# available when construction begins.


#  Each ore robot costs 4 ore.
#  Each clay robot costs 2 ore.
#  Each obsidian robot costs 3 ore and 14 clay.
#  Each geode robot costs 2 ore and 7 obsidian.
# ===================================================================
# Factory
# ===================================================================
class Factory:
    def __init__(self,ore_robot_cost = (2,0,0), clay_robot_cost = (3,0,0), obsidian_robot_cost= (3,8,0), geode_robot_cost=(3,0,12)):
        self.ore_robot_cost = ore_robot_cost
        self.clay_robot_cost = clay_robot_cost
        self.obsidian_robot_cost = obsidian_robot_cost
        self.geode_robot_cost = geode_robot_cost
        self.num_ore_robot = 1
        self.num_clay_robot = 0
        self.num_obsidian_robot = 0
        self.num_geode_robot = 0
        self.ore = 0
        self.clay = 0
        self.obsidian = 0
        self.geode = 0
        self.cost = 0

        #self.update_cost()
        self.key = self.readable(self.get_state())
        # 0 (ore=2,clay=17,obsidian=3,geode=0) Robots:(ore=1,clay=4,obsidian=2,geode=1)

    def update_cost(self):
        self.key = self.readable(self.get_state())
        return 0


    def get_state(self):
        return ( self.ore,self.clay,self.obsidian,self.geode,self.num_ore_robot,self.num_clay_robot,self.num_obsidian_robot, self.num_geode_robot)
    def set_state(self,state):
        self.ore,self.clay,self.obsidian,self.geode,self.num_ore_robot,self.num_clay_robot,self.num_obsidian_robot, self.num_geode_robot = state
    def readable(self,state):
        ore,clay,obsidian,geode,num_ore_robot,num_clay_robot,num_obsidian_robot, num_geode_robot = state
        return f"(ore={ore},clay={clay},obsidian={obsidian},geode={geode})" + \
            f" Robots:(ore={num_ore_robot},clay={num_clay_robot},obsidian={num_obsidian_robot},geode={num_geode_robot})"
    def buy_ore_robot(self):
        payment_ore,payment_clay,payment_obsidian = self.ore_robot_cost
        if self.ore >= payment_ore and self.clay >= payment_clay and self.obsidian >= payment_obsidian:
            self.ore -= payment_ore
            self.clay -= payment_clay
            self.obsidian -= payment_obsidian
            self.num_ore_robot += 1
            return True
        return False
    def buy_clay_robot(self):
        payment_ore,payment_clay,payment_obsidian = self.clay_robot_cost
        if self.ore >= payment_ore and self.clay >= payment_clay and self.obsidian >= payment_obsidian:
            self.ore -= payment_ore
            self.clay -= payment_clay
            self.obsidian -= payment_obsidian
            self.num_clay_robot += 1
            return True
        return False
    def buy_obsidian_robot(self):
        payment_ore,payment_clay,payment_obsidian = self.obsidian_robot_cost
        if self.ore >= payment_ore and self.clay >= payment_clay and self.obsidian >= payment_obsidian:
            self.ore -= payment_ore
            self.clay -= payment_clay
            self.obsidian -= payment_obsidian
            self.num_obsidian_robot += 1
            return True
        return False
    def buy_geode_robot(self):
        payment_ore,payment_clay,payment_obsidian = self.geode_robot_cost
        if self.ore >= payment_ore and self.clay >= payment_clay and self.obsidian >= payment_obsidian:
            self.ore -= payment_ore
            self.clay -= payment_clay
            self.obsidian -= payment_obsidian
            self.num_geode_robot += 1
            return True
        return False

    def children(self, *_):
        children = []
        child = Factory(self.ore_robot_cost,self.clay_robot_cost,self.obsidian_robot_cost,self.geode_robot_cost)
        child.set_state(self.get_state())
        child.ore += self.num_ore_robot
        child.clay += self.num_clay_robot
        child.obsidian += self.num_obsidian_robot
        child.geode += self.num_geode_robot
        child.update_cost()
        child.parent = self
        children.append(child)    
        
        child = Factory(self.ore_robot_cost,self.clay_robot_cost,self.obsidian_robot_cost,self.geode_robot_cost)
        child.set_state(self.get_state())
        if child.buy_ore_robot():
            child.ore += self.num_ore_robot
            child.clay += self.num_clay_robot
            child.obsidian += self.num_obsidian_robot
            child.geode += self.num_geode_robot
            child.parent = self
            child.update_cost()
            children.append(child)
        child = Factory(self.ore_robot_cost,self.clay_robot_cost,self.obsidian_robot_cost,self.geode_robot_cost)
        child.set_state(self.get_state())
        if child.buy_clay_robot():
            child.ore += self.num_ore_robot
            child.clay += self.num_clay_robot
            child.obsidian += self.num_obsidian_robot
            child.geode += self.num_geode_robot
            child.parent = self
            child.update_cost()
            children.append(child)
        child = Factory(self.ore_robot_cost,self.clay_robot_cost,self.obsidian_robot_cost,self.geode_robot_cost)
        child.set_state(self.get_state())
        if child.buy_obsidian_robot():
            child.ore += self.num_ore_robot
            child.clay += self.num_clay_robot
            child.obsidian += self.num_obsidian_robot
            child.geode += self.num_geode_robot
            child.parent = self
            child.update_cost()
            children.append(child)
        child = Factory(self.ore_robot_cost,self.clay_robot_cost,self.obsidian_robot_cost,self.geode_robot_cost)
        child.set_state(self.get_state())
        if child.buy_geode_robot():
            child.ore += self.num_ore_robot
            child.clay += self.num_clay_robot
            child.obsidian += self.num_obsidian_robot
            child.geode += self.num_geode_robot
            child.update_cost()
            child.parent = self
            children.append(child)
        return children

    # ----------------------------------------------------------------------------
    # estimated cost to get to the finish line
    # ----------------------------------------------------------------------------
    def eta(self,node):
        return 0 
        
    

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
 
