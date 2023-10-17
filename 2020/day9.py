from collections import deque
key_length = 25

def main(part: int = 1):
    file = open('day9_input.txt', 'r')
    deck = deque()
    for line in map(int, map(str.rstrip, file)):
        if len(deck) < key_length:
            deck.append(line)
            continue

        if len(deck) > key_length:
            deck.popleft()

        if not is_valid(line, deck):
            print("found invalid", line)
            break

        deck.append(line)

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
