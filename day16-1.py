import DictionaryGrid as dg
import re
MAX_MINS = 30

def main():
    file = open("day16_test_input.txt", 'r')
    nodes = Pipes_and_vents()

    for line in map(str.rstrip,file):
        # "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB"
        print("line:",line)
        regex = re.match(r".*?Valve ([A-Z]+) .*?rate=(\d+).*?valves? (.*)",line)
        if not regex:
            print (f"line is <{line}>, WTF!")

        valve_key = regex.group(1)
        rate = int(regex.group(2))
        pipes = regex.group(3)
        dest_valve_keys = map(str.strip, pipes.split(","))

        nodes.add(Pipe_or_vent(valve_key))
        nodes.get(valve_key).rate = rate

        for dest_valve_key in dest_valve_keys:
            nodes.add(Pipe_or_vent(dest_valve_key))
            nodes.get(valve_key).add_child(nodes.get(dest_valve_key))

    vents = Vents(nodes.get('AA'))
    print ('AA rate is',nodes.get('AA').rate)
    vents_seen = vents.find_all_paths()
 #   for vent in vents_seen:
 #       print (vent)


class Pipes_and_vents:
    def __init__(self, type="valve"):
        self.pipes_and_vents = {}
        self.type = type
    def add(self,obj,type="valve"):
        if self.get(obj.key) is None:
            self.pipes_and_vents[obj.key] = obj
    def exists (self,key):
        return key in self.pipes_and_vents.keys()
    def get (self,key):
        if self.exists(key): 
            return self.pipes_and_vents[key]
        return None

class Pipe_or_vent:
    def __init__(self,id,type="valve"):
        self.cost = 1
        self.rate = 0
        self.key = id
        self.child_ids = {}
        self.eta = 0
        self.type = type
        self.open_valve_states = []

    
    def add_child( self, obj):
        self.child_ids[obj.key] = obj

    def children (self):
        return self.child_ids.values()

 
    
class Vents:
    # Maximize the additions of rates
    # -------------------------------------------------------------------------
    # constructor
    # -------------------------------------------------------------------------
    def __init__(self,start_obj):

        # private
        self._all_nodes = dict()
        self._current_node = None           # what node are we currently looking at?

        node = Node(start_obj)
        self._all_nodes[start_obj.key] = node
        self.start_node = node

        # public
        self.progress_sub = lambda i:None   # callback function (user defined)
        self.progress_freq = None           # how often should the callback function be called

    # -------------------------------------------------------------------------
    # find_all_paths - without the state repeating itself
    # -------------------------------------------------------------------------
    def find_all_paths (self):

        self.all_paths = list()

        self.current = self.start_node
        self.current.was_visisted = True

        open_valves = ""
        self.append_children(self.current," AA[],",open_valves)

        return self.all_paths

    


    def append_children(self,node,path,open_valves,waterflow=0,total_flow=0):

        if len(path.split(",")) < MAX_MINS+2:
            for child_obj in node.obj.children():

                # if this state for this node already exists, do not repeat
                if f"{child_obj.key}[{open_valves}]" in path:
                    continue

                child_node = Node( child_obj, node)
                self._all_nodes[child_node.id] = child_node
                newpath = path + " " + child_node.id + f"[{open_valves}]-{waterflow}-{total_flow+waterflow}" + ","
                self.append_children(child_node,newpath, open_valves,waterflow,total_flow+waterflow)

                # if valve has not already been opened, another option is to open it
                if child_obj.rate != 0 and child_obj.key not in open_valves:
                    new_open_valves = f"{open_valves}-{child_obj.key}"
                    self.append_children(child_node, newpath + " open,", new_open_valves, waterflow + child_obj.rate,total_flow+2*waterflow)

        if len(path.split(",")) >= MAX_MINS: 
            if total_flow > 1650: print (total_flow,path)

            self.all_paths.append((total_flow,path))

                    

 
    # -------------------------------------------------------------------------
    # get_path
    # -------------------------------------------------------------------------
    def get_path (self,node, max_nodes = 800):
        count = 0
        nodes = [node]
        while ( next_node := node.prev) and count < max_nodes:
            nodes.insert(0,next_node)
            node = next_node
            count += 1
        
        return nodes
    


#########################################################################################
class Node:

    def __init__(self,obj,prev=None):
        self.obj = obj
        self.id = obj.key 
        self.fcost = 0
        self.was_visited = False


# ===================================================================
# Entry point
# ===================================================================
if __name__ == '__main__':
    main()