import re
tree={'/':{},'up':None}
current_location = tree['/']
print (current_location)
dir_sizes={}

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
    print_dirs("",tree)
 
    total = 0
    # sum(size for size in dir_sizes.values() if size <= 10000)
    for dir,size in dir_sizes.items():
        size = int(size)
        if size <= 100000:
            print(f"{dir}\t{size}") 
            total += size
    print (f"total = {total}")

def print_tree(name, node, indent=0):
    print (" "*indent,name,end="")
    if isinstance(node,dict):
        (size,_) = calculate_dir_size(name,node)
        print("/\t\t\t",size)
        for name, value in node.items():
            if name != 'up':
                print_tree(name,value,indent+3)
    else:
        print ("\t",node)

def print_dirs(name, node, indent=0):
    if isinstance(node,dict):
        size = calculate_dir_size(name,node)
        dir_sizes[name] = size
        if size <= 100000:
            print (name,end="")
            print("/\t\t\t",size)
        for nname, value in node.items():
            if nname != 'up':
                print_dirs(name+"/"+nname,value,indent+3)
    
def calculate_dir_size(name, node):
    size = 0
    for new_name,value in node.items():
        if new_name != 'up':
            if isinstance(value,dict):
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