from collections import deque
import re
def main():
    stacks = []
    # initialize the stacks
    for i in range(10):
        stacks.append(deque([]))

    with open('day5_input.txt', 'r') as file:  
        # create the stacks
        for line in file:
            if line[1:2] == "1":
                break
            for i in range(len(stacks)):
                index = 1 + 4*i
                c = line[index:index+1]
                if c != " " and c != "":
                    stacks[i].append(c)

        # process the commands
        for line in file:
            cmd = re.match(r'move (\d+) from (\d+) to (\d+)',line)
            if cmd:
                line = line.strip()
                (amt,from_stack,to_stack) = cmd.groups()
                for _ in range(int(amt)):
                    stacks[int(to_stack)-1].appendleft(stacks[int(from_stack)-1].popleft())

        # print results
        for i in range(len(stacks)):
            if len(stacks[i]) > 0:
                print(stacks[i][0],end="")
        print()
#        print (f"Score: {score}")

if __name__ == '__main__':
    main()