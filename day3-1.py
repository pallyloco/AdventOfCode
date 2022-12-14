def main():
#Lowercase item types a through z have priorities 1 through 26.
#Uppercase item types A through Z have priorities 27 through 52.
    score = 0
    with open('day3_input.txt', 'r') as file:  
        for line in file:
            line = line.strip()
            length = len(line)//2
            first = set(line[0:length])
            last =  set(line[length:])
            print (f"\nfirst: {first} last: {last}")

            result = first.intersection(last)

            if result:
                print(result)
                c, *_ = result
                print (f"found duplicate {c}")
                if c.isupper():
                    score = score + ord(c) - ord("A") + 27
                    print (f"add score  {ord(c) - ord('A') + 27}")
                else:
                    score = score + ord(c) - ord("a") + 1
                    print (f"new score is {ord(c) - ord('a') + 1}")

        print (f"score is {score}")


if __name__ == '__main__':
    main()