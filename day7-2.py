import re
tree={'/':{},'up':None}
current_location = tree['/']
print (current_location)
dir_sizes={}
MAX_SIZE=70000000
REQUIRED_SIZE=30000000

def main():
    file = open('day7_input.txt', 'r')
    while True:
        line = file.readline()
        if not line: 
            break
        if line[0:1] == '$': 
            process_cmd(line)
        else:
            regex = re.match(r'dir (.*)',line)
            if regex:
                new_dir = regex.group(1)
                current_location[new_dir] = {'up':current_location}
            regex = re.match(r'(\d+)\s+(.*)',line)
            if regex:
                current_location[regex.group(2)] = regex.group(1)
    
    get_dir_sizes("",tree)
    total_used = dir_sizes['//']
    min_delete = total_used - (MAX_SIZE - REQUIRED_SIZE)
    print ("minimum to delete",min_delete)

    dir_size_to_delete = MAX_SIZE
    for size in dir_sizes.values():
        size = int(size)
        if size >= min_delete:
            dir_size_to_delete = min(size,dir_size_to_delete)
    
    print ("Delete with size:",dir_size_to_delete)
# ====================================================================
# get dir sizes
# ====================================================================
def get_dir_sizes(name, node, indent=0):
    if isinstance(node,dict):
        print (name)
        size = calculate_dir_size(name,node)
        dir_sizes[name] = size
        for nname, value in node.items():
            if nname != 'up':
                get_dir_sizes(name+"/"+nname,value,indent+3)
    
# ====================================================================
# calculate dir sizes
# ====================================================================
def calculate_dir_size(name, node):
    size = 0
    for new_name,value in node.items():
        if new_name != 'up':
            if isinstance(value,dict):
                new_size = calculate_dir_size(name+'/'+new_name,value)
                size += new_size
            else:
                size += int(value)
    return size

    
def process_cmd (cmd):
    global current_location
    regex = re.match(r'.*cd (.*)',cmd)
    if regex:
        if regex.group(1) == "..":
            current_location = current_location['up']
        elif regex.group(1) == "/":
            current_location=tree['/']
        else:
            current_location = current_location[regex.group(1)]
        return
    

    

if __name__ == '__main__':
    main()