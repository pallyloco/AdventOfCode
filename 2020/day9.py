import itertools

key_length = 25
inputs = list()


def main():
    file = open('day9_input.txt', 'r')
    invalid = 0
    deck = []
    for line in map(int, map(str.rstrip, file)):
        inputs.append(line)
        if not invalid:
            if len(deck) < key_length:
                deck.append(line)
                continue

            if not is_valid(line, deck):
                print("found invalid", line)
                invalid = line
                break

        deck.append(line)

    # find weakness
    for i in range(len(inputs) - 1):
        total = inputs[i]
        lowest = total
        highest = total
        for j in range(i + 1, len(inputs)):
            total = total + inputs[j]
            lowest = min(lowest, inputs[j])
            highest = max(highest, inputs[j])
            if total > invalid:
                break
            if total == invalid:
                print("Encryption weakness ", lowest + highest)
                return


def is_valid(num: int, deck: list[int]):
    s = deck[-key_length:]
    for a,b in itertools.combinations(deck[-key_length:],2):
        if a + b == num:
            return True
    return False

if __name__ == '__main__':
    main()
