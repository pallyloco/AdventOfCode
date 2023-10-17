from collections import deque
key_length = 25
inputs = list()

def main(part: int = 1):
    file = open('day9_input.txt', 'r')
    invalid = 0
    deck = deque()
    for line in map(int, map(str.rstrip, file)):
        inputs.append(line)
        if not invalid:
            if len(deck) < key_length:
                deck.append(line)
                continue

            if len(deck) > key_length:
                deck.popleft()

            if  not is_valid(line, deck):
                print("found invalid", line)
                invalid = line


        deck.append(line)


    # find weakness
    for i in range(len(inputs)-1):
        total = inputs[i]
        lowest = total
        highest = total
        for j in range(i+1,len(inputs)):
            total = total+inputs[j]
            lowest = min(lowest,inputs[j])
            highest = max(highest,inputs[j])
            if total > invalid:
                break
            if total == invalid:
                print (lowest+highest)
                exit

def is_valid(num:int, deck:deque[int]):
    for i in range(0,key_length-1):
        for j in range(i+1,key_length):
            x=deck[i]
            y=deck[j]
            if deck[i] + deck[j] == num:
                return True
    return False




if __name__ == '__main__':
    main(1)
