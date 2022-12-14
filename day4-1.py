def main():
    score = 0
    with open('day4_input.txt', 'r') as file:  
        # sum(1 for line in file if overlap(line))
        for line in file:
            line = line.strip()
            (elf1,elf2) = line.split(",")
            (elf1_start,elf1_end) = elf1.split("-")            
            (elf2_start,elf2_end) = elf2.split("-")  
            flag = 0
            if int(elf1_start) <= int(elf2_start) and int(elf1_end) >= int(elf2_end):
                score = score+1
                flag = 1
            elif int(elf1_start) >= int(elf2_start) and int(elf1_end) <= int(elf2_end):
                score = score+1
                flag = 1
            print (f"{line.strip()}:  {elf1_start}:{elf1_end}, {elf2_start}:{elf2_end},  {flag}")
        print (f"Score: {score}")

if __name__ == '__main__':
    main()