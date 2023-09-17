def main(day):
    score = 0
    with open('day4_input.txt', 'r') as file:
        for line in map(str.rstrip, file):
            (elf1, elf2) = line.split(",")
            (elf1_start, elf1_end) = elf1.split("-")
            (elf2_start, elf2_end) = elf2.split("-")

            if day == 1:
                if int(elf1_start) <= int(elf2_start) and int(elf1_end) >= int(elf2_end):
                    score = score + 1
                elif int(elf1_start) >= int(elf2_start) and int(elf1_end) <= int(elf2_end):
                    score = score + 1

            else:
                flag = 0
                if int(elf2_start) <= int(elf1_start) <= int(elf2_end):
                    flag = 1
                if int(elf2_start) <= int(elf1_end) <= int(elf2_end):
                    flag = 1
                if int(elf1_start) <= int(elf2_start) <= int(elf1_end):
                    flag = 1
                if int(elf1_start) <= int(elf2_end) <= int(elf1_end):
                    flag = 1
                score = score + flag

        print(f"Score: {score}")


if __name__ == '__main__':
    main(1)
    main(2)

"""
Every section has a unique ID number, and each Elf is assigned a range of section IDs.

As some of the Elves compare their section assignments with each other, they've noticed that 
many of the assignments overlap. To try to quickly find overlaps and reduce duplicated effort, 
the Elves pair up and make a big list of the section assignments for each pair (your puzzle input).

For example, 

2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8

In how many assignment pairs does one range fully contain the other?

Your puzzle answer was 475.

--- Part Two ---
It seems like there is still quite a bit of duplicate work planned. 
Instead, the Elves would like to know the number of pairs that overlap at all.

In how many assignment pairs do the ranges overlap?

Your puzzle answer was 825.
"""
