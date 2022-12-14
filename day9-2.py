import re
import math
head = [6,10]
knots = [[6,10],[6,10],[6,10],[6,10],[6,10],[6,10],[6,10],[6,10],[6,10],]
row = 0
col = 1
score = {"6,10":1}

# sets and pairwise

def main():
    file = open('day9_input.txt', 'r')
    for line in file:
        line = line.rstrip()
        regex = re.match(r"(.)\s(\d+)",line)
        print(line)

        if regex.group(1) == "L":
            move(head,int(regex.group(2)),0,-1)
        elif regex.group(1) == "R":
            move(head,int(regex.group(2)),0,1)
        elif regex.group(1) == "U":
            move(head,int(regex.group(2)),1,0)
        elif regex.group(1) == "D":
            move(head,int(regex.group(2)),-1,0)

    answer = len(score)
    output()
    print(f"answer: {answer}")

def print_snake():
    return
    print()
    for row in range(25,-1,-1):
        for col in range(-5,30):
            str = "."
            if row == 6 and col == 10:
                str = "s"
            for knot in range(8,-1,-1):
                if knots[knot][0] == row and knots[knot][1] == col:
                    str = knot+1
            if head[0] == row and head[1] == col:
                str = "H"
            print (str,end="")
        print()
    #input("press enter to continue")

def output():
    return
    print()
    for row in range(25,-1,-1):
        for col in range(-5,30):
            if f"{row},{col}" in score.keys():
                print("#",end="")
            else:
                print (".",end="")
        print()
    input("Press Enter to continue")

def move(head,amount,row_amt,col_amt):
    for i in range(amount):
        lead = head
        lead[row] = lead[row] + row_amt
        lead[col] = lead[col] + col_amt

        for knot in knots:
    
            # If the head is ever two steps directly up, down, left, or right 
            # from the tail, the tail must also move one step in that 
            # direction so it remains close enough:
            if abs(knot[row]-lead[row]) == 2 and knot[col] == lead[col]:
                knot[row] += math.copysign(1,lead[row]-knot[row])
            elif abs(knot[col]-lead[col]) == 2 and knot[row] == lead[row]:
                knot[col] += math.copysign(1,lead[col]-knot[col])

            # Otherwise, if the head and tail aren't touching and aren't 
            # in the same row or column, the tail always moves one step 
            # diagonally to keep up:
            elif abs(knot[row]-lead[row]) > 1 or abs(knot[col]-lead[col]) > 1:
                knot[row] += math.copysign(1,lead[row]-knot[row])
                knot[col] += math.copysign(1,lead[col]-knot[col])
            
            else:
                break

            lead = knot
        score[f"{int(knots[-1][row])},{int(knots[-1][col])}"] = 1
    print_snake() 



 

# ===================================================================
# Entry point
# ===================================================================
if __name__ == '__main__':
    main()