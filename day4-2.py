def main():
    score = 0
    with open('day4_input.txt', 'r') as file:  
        print ("Hello")
        for line in file:
            line = line.strip()
            (elf1,elf2) = line.split(",")
            (elf1_start,elf1_end) = elf1.split("-")            
            (elf2_start,elf2_end) = elf2.split("-")  
            flag = 0  
            if int(elf2_start) <= int(elf1_start) <= int(elf2_end):
                flag =1
            if int(elf2_start) <= int(elf1_end) <= int(elf2_end):
                flag =1
            if int(elf1_start) <= int(elf2_start) <= int(elf1_end):
                flag =1
            if int(elf1_start) <= int(elf2_end) <= int(elf1_end):
                flag =1
            score = score  + flag                
        print (f"Score: {score}")

if __name__ == '__main__':
    main()