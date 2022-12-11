def calories_gen():
    with open('day1_input1.txt', 'r') as file:
        elf_total = 0 
        for lineno, line in enumerate(file, 1):
            data = line.strip()
            if data:
                elf_total = elf_total + int(data)
            else:
                yield elf_total
                elf_total = 0
            
            print (f"{lineno}: {data} {elf_total}")

def main():
    calories = calories_gen()
    print (f"max is {max(calories)}")

if __name__ == '__main__':
    main()