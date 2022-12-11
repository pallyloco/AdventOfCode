from collections import deque
import re
def main():
    file = open('day6_input.txt', 'r')
    line = file.readline()
    #queue_size = 4, for part 1
    queue_size = 14 # for part 2
    queue = deque([],queue_size)
    count = 0
    for char in line:
        queue.append(char)
        print (queue)
        count = count+1
            

        if count >= queue_size:
            flag = True
            for i in range(queue_size):
                if queue.count(queue[i]) > 1:
                    flag=False
            if flag:
                print (count)
                break

    

    

if __name__ == '__main__':
    main()