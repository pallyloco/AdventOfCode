from __future__ import annotations

import re
from typing import Optional

tree: dict[str, Optional[dict | int]] = {"up": None, "/": dict()}
current_directory: dict[str, Optional[dict | int]] = tree["/"]
dir_sizes: dict[str:int] = dict()
MAX_SIZE = 70000000
REQUIRED_SIZE = 30000000
MIN_SIZE = 100000


def main(day):
    file = open('day7_input.txt', 'r')
    for line in map(str.rstrip, file):

        # commands
        if line[0:1] == '$':
            process_cmd(line)

        # directory information
        else:

            # new directory
            regex = re.match(r'dir (.*)', line)
            if regex:
                new_dir = regex.group(1)
                current_directory[new_dir] = {'up': current_directory}
                continue

            # size_of_file, file
            regex = re.match(r'(\d+)\s+(.*)', line)
            if regex:
                current_directory[regex.group(2)] = regex.group(1)

    # process directory structure
    get_dir_sizes("", tree)

    if day == 1:
        """
        To begin, find all of the directories with a total size of at most MIN_SIZE, 
        then calculate the sum of their total sizes. """
        total = sum((size for size in map(int, dir_sizes.values()) if size <= MIN_SIZE))
        print(f"Total size of directories whose size is less than {MIN_SIZE} = {total}")

    else:
        """
        The total disk space available to the filesystem is MAX_SIZE. 
        To run the update, you need unused space of at least REQUIRED_SIZE. 
        You need to find a directory you can delete that will free up enough space to run the update.
        Choose the smallest directory that satisfies the need
        """
        total_used = dir_sizes['//']
        min_delete = total_used - (MAX_SIZE - REQUIRED_SIZE)
        dir_size_to_delete = min((size for size in map(int, dir_sizes.values()) if size >= min_delete))

        print("Minimize size of directory to free up enough space:", dir_size_to_delete)


# ====================================================================
# get dir sizes
# ====================================================================
def get_dir_sizes(name, node, indent=0):
    if isinstance(node, dict):
        size = calculate_dir_size(name, node)
        dir_sizes[name] = size
        for new_name, value in node.items():
            if new_name != 'up':
                get_dir_sizes(name + "/" + new_name, value, indent + 3)


# ====================================================================
# calculate dir sizes
# ====================================================================
def calculate_dir_size(name, node):
    size = 0
    for new_name, value in node.items():
        if new_name != 'up':
            if isinstance(value, dict):
                new_size = calculate_dir_size(name + '/' + new_name, value)
                size += new_size
            else:
                size += int(value)
    return size


# ====================================================================
# process command
# ====================================================================
def process_cmd(cmd):
    global current_directory
    regex = re.match(r'.*cd (.*)', cmd)
    if regex:
        if regex.group(1) == "..":
            current_directory = current_directory['up']
        elif regex.group(1) == "/":
            current_directory = tree['/']
        else:
            current_directory = current_directory[regex.group(1)]
        return


if __name__ == '__main__':
    main(1)
    main(2)


"""
You try to run a system update:

$ system-update --please --pretty-please-with-sugar-on-top
Error: No space left on device
Perhaps you can delete some files to make space for the update?

You browse around the filesystem to assess the situation and save the resulting terminal output 
(your puzzle input). 

Within the terminal output, lines that begin with $ are commands you executed, 
very much like some modern computers:

123 abc means that the current directory contains a file named abc with size 123.
dir xyz means that the current directory contains a directory named xyz.

Since the disk is full, your first step should probably be to find directories that are good 
candidates for deletion. To do this, you need to determine the total size of each directory. 

Find all of the directories with a total size of at most 100000. 
What is the sum of the total sizes of those directories?

Your puzzle answer was 1306611.

--- Part Two ---
Now, you're ready to choose a directory to delete.

The total disk space available to the filesystem is 70000000. 
To run the update, you need unused space of at least 30000000. 
You need to find a directory you can delete that will free up enough space to run the update.

Find the smallest directory that, if deleted, would free up enough space on the filesystem 
to run the update. What is the total size of that directory?

Your puzzle answer was 13210366.

"""