def main(part: int = 1):
    file = open('day5_input.txt', 'r')
    bin_dict = {"F":0, "B":1,"L":0, "R":1}
    all_seat_ids = list()

    max_seat_id = 0
    for line in map(str.rstrip, file):
        seat_id = 0
        for c in line:
            seat_id = seat_id << 1
            seat_id += bin_dict[c]

        all_seat_ids.append(seat_id)
        max_seat_id = max(max_seat_id, seat_id)

    print ("Max seat id is:", max_seat_id)
    all_seat_ids.sort()
    for i in range(1,len(all_seat_ids)-1):
        if all_seat_ids[i+1]-all_seat_ids[i] == 2:
            print ("My seat number is:", all_seat_ids[i]+1)


if __name__ == '__main__':
    main(1)
