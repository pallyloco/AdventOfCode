def main(part: int = 1):
    file = open('day5_input.txt', 'r')
    bin_dict = {"F":0, "B":1,"L":0, "R":1}

    max_seat_id = 0
    for line in map(str.rstrip, file):
        seat_id = 0
        for c in line:
            seat_id = seat_id << 1
            seat_id += bin_dict[c]

        max_seat_id = max(max_seat_id, seat_id)
    print ("Max seat id is:", max_seat_id)
if __name__ == '__main__':
    main(1)
