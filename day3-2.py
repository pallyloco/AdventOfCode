def main():
#Lowercase item types a through z have priorities 1 through 26.
#Uppercase item types A through Z have priorities 27 through 52.
#Look for common item in all three groups
    score = 0
    count = 0
    with open('day3_input.txt', 'r') as file:  
        rucksacks = [0,0,0]
        for line in file:
            line = line.strip()
            if count != 0 and not count%3:
                score = score + find_badge_score(rucksacks)

            rucksacks[count%3] = line
            count = count + 1

        score = score + find_badge_score(rucksacks)
        print (f"score is {score}")

def find_badge_score (rucksacks):
    for c in rucksacks[0] :
        if c in rucksacks[1] and c in rucksacks[2]:
            print (f"found badge {c}")
            if c == c.upper():
                score = ord(c) - ord("A") + 27
                print (f"add score  {ord(c) - ord('A') + 27}")
            else:
                score = ord(c) - ord("a") + 1
                print (f"add score {ord(c) - ord('a') + 1}")
            return score        


if __name__ == '__main__':
    main()