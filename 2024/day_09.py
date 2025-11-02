import itertools as it
import time

from ranges import Ranges, Range

"""
The disk map uses a dense format to represent the layout of files and free space on the disk. 
The digits alternate between indicating the length of a file and the length of free space.

Each file on disk also has an ID number based on the order of the files as they appear before 
they are rearranged, starting with ID 0. So, the disk map 12345 has three files: a one-block 
file with ID 0, a three-block file with ID 1, and a five-block file with ID 2. 

Using one character for each block where digits are the file ID and . is free space, the 
disk map 12345 represents these individual blocks:

0..111....22222

PART 1:
The amphipod would like to move file blocks one at a time from the end of the disk to the leftmost 
free space block (until there are no gaps remaining between file blocks).

PART 2:
The eager amphipod already has a new plan: rather than move individual blocks, he'd like to try compacting 
the files on his disk by moving whole files instead.

This time, attempt to move whole files to the leftmost span of free space blocks that could fit the file. 
Attempt to move each file exactly ONCE in order of decreasing file ID number starting with the file with 
the highest file ID number. If there is no span of free space to the left of a file that is large 
enough to fit the file, the file does not move.

CHECKSUM
To calculate the checksum, add up the result of multiplying each of these blocks' position with the file ID 
number it contains. The leftmost block is in position 0.

"""

input_data = "2333133121414131402"
fh = open("day_09.txt", "r")
input_data = list(map(str.rstrip, fh))[0]


def sum_ints(i=5, n=10):
    total = (n * (n + 1)) // 2
    total = total - (i - 1) * i // 2
    return total


def main(data):
    checksum = 0
    frame = 0
    # NB: data is two numbers [inode/free space ... inode], inode starts at 0
    last_inode = len(data) // 2
    for inode in it.count():
        if len(data) > 2:

            # checksum for non-moved file
            size, space, *data = data
            size, space = map(int, (size, space))
            checksum += inode * sum_ints(frame, frame + size - 1)
            frame = frame + size

            # move file from end into empty space
            while space != 0:
                last_file_size = int(data[-1])
                if last_file_size <= space:
                    checksum += last_inode * sum_ints(frame, frame + last_file_size - 1)
                    data = data[:-2]
                    frame = frame + last_file_size
                    space = space - last_file_size
                    last_inode -= 1
                else:
                    checksum += last_inode * sum_ints(frame, frame + space - 1)
                    data[-1] = str(last_file_size - space)
                    frame = frame + space
                    space = 0
        else:
            checksum += last_inode * sum_ints(frame, frame + int(data[0]) - 1)
            break
    print(checksum)


def main2(data):
    ranges = Ranges()
    frame = 0
    inode = 0
    file_dictionary: dict[int, Range] = {}

    # read in the input
    for inode, tmp in enumerate(it.batched(data, 2)):
        size, *empty = map(int, tmp)
        file = Range(frame, size, inode)
        ranges.append(file)
        file_dictionary[inode] = file
        if len(empty) != 0:
            frame = frame + size + empty[0]

    # starting at the end of the disk space and moving toward the beginning
    for file_inode in range(inode, -1, -1):
        move(ranges, file_dictionary[file_inode])

    total = 0
    for r in ranges:
        if r.value is not None:
            for i in range(r.start, r.end + 1):
                total += r.value * i
    print(total)


def move(ranges, file):
    empties = ranges.find_empty_ranges()
    for empty in empties:
        if file.end < empty.start:
            break
        if file.size <= empty.size:
            file.start = empty.start
            break


t = time.time()
main(input_data)
main2(input_data)
print(f"total time taken: {int(time.time() - t)} secs")
