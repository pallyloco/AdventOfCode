from collections import deque
import re
def main():
    file = open('day6_input.txt', 'r')
    line = file.readline()
    #queue_size = 4, for part 1
    queue_size = 14 # for part 2

    # create a queue which has a maximum size of queu_size which slides
    queue = deque([],queue_size)

    for count, char in enumerate(line, 1):
        queue.append(char)
        print (queue)

        if count >= queue_size:
            for i in range(queue_size):
                if queue.count(queue[i]) > 1:
                    break
            else:
                print(count)
                break

    

    

if __name__ == '__main__':
    main()