import itertools as it
from ranges import Ranges, Range

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
    checksum = 0
    ranges = Ranges()
    frame = 0
    inode_max = 0
    for inode, tmp in enumerate(it.batched(data, 2)):
        size, *empty = map(int, tmp)
        ranges.append(Range(frame, size, inode))
        if len(empty) != 0:
            frame = frame + size + empty[0]
        inode_max = max(inode, inode_max)

    for last_moved in range(inode_max,-1,-1):
        move(ranges,last_moved)

    total = 0
    for r in ranges:
        if r.value is not None:
            for i in range(r.start,r.end+1):
                total += r.value * i
    print(total)


def move(ranges, last_moved):
    empties = ranges.find_empty_ranges().order_by_location()
    files = ranges.find_with_value(last_moved)
    file = files[0]
    for empty in empties:
        if file.end < empty.start:
            break
        if file.size <= empty.size:
            file.start = empty.start
            break



main(input_data)
main2(input_data)
