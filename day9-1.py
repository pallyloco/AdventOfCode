import re
head = [0,0]
tail = [0,0]
row = 0
col = 1
score = {"0,0":1}

def main():
    file = open('day9_input.txt', 'r')
    for line in file:
        line = line.rstrip()
        regex = re.match(r"(.)\s(\d+)",line)

        if regex.group(1) == "U":
            sideways(int(regex.group(2)),1)
        elif regex.group(1) == "D":
            sideways(int(regex.group(2)),-1)
        elif regex.group(1) == "R":
            vertical(int(regex.group(2)),1)
        elif regex.group(1) == "L":
            vertical(int(regex.group(2)),-1)

    answer = sum(score.values())
    print(f"answer: {answer}")

def sideways(amount,dir):
    for _ in range(amount):
        head[row] = head[row] + dir
        if abs(tail[row]-head[row]) > 1 :
            tail[row] = tail[row] + dir
            tail[col] = head[col]
            score[f"{tail[row]},{tail[col]}"] = 1


def vertical(amount,dir):
    for _ in range(amount):
        head[col] = head[col] + dir
        if abs(tail[col]-head[col]) > 1 :
            tail[col] = tail[col] + dir
            tail[row] = head[row]
            score[f"{tail[row]},{tail[col]}"] = 1

# ===================================================================
# Entry point
# ===================================================================
if __name__ == '__main__':
    main()