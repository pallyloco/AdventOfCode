# Day2-1.py
def main():
    opponent={"A":"rock","B":'paper',"C":'scissors'}
    you={"X":"rock","Y":"paper","Z":"scissors"}
    wins=("paper rock","rock scissors","scissors paper")
    points={"rock":1,"paper":2,"scissors":3}
    score = 0
    with open('day2_input.txt', 'r') as file:  
        for line in file:
            line = line.strip()
            hers, mine = line.split(" ")
            if f"{you[mine]} {opponent[hers]}" in wins:
                score = score + 6
            elif opponent[hers] == you[mine]:
                score = score +3
            score = score + points[you[mine]]
        print (f"final score is: {score}")   






if __name__ == '__main__':
    main()