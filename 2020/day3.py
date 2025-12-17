def main(part: int, slopes: list[tuple[int,int]] ):
    answer = 1
    for slope in slopes:
        file = open('day3_input.txt', 'r')
        num_trees = 0
        col = 0
        dcol, drow = slope

        for line_number, line in enumerate(map(str.rstrip, file)):
            if not line_number%drow: 
                if line[col] == "#":
                    num_trees += 1
                col = (col+dcol) % len(line)

        print ("with slope",slope,"bumped into", num_trees, "trees")
        answer = answer * num_trees
    print ("multiplying slopes is:", answer)

if __name__ == '__main__':
    main(1,[(3,1)])
    main(2, [(1,1), (3,1), (5,1), (7,1), (1,2)])


