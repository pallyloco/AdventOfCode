# Day2-1.py
def main():
    # x is lose
    # y is draw
    # z is win
    opponent={"A":"rock","B":'paper',"C":'scissors'}
    #you={"X":"rock","Y":"paper","Z":"scissors"}
    we_lose={"paper":"rock","rock":"scissors","scissors":"paper"}
    we_win={"rock":"paper","scissors":"rock","paper":"scissors"}
    points={"rock":1,"paper":2,"scissors":3}
    score = 0
    with open('day2_input.txt', 'r') as file:  
        for line in file:
            line = line.strip()
            (other, you_play) = line.split(" ")
            other_play=opponent[other]
            if you_play == "X":
                you_play = we_lose[other_play]
                score = score + points[you_play]
            elif you_play == "Z":
                you_play = we_win[other_play]
                score = score + points[you_play] + 6
            else:
                you_play = other_play
                score = score + points[you_play] + 3
            

        print (f"final score is: {score}")   






if __name__ == '__main__':
    main()