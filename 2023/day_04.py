def main():
    file = open("day_04_input.txt", "r")
    ans1 = 0
    num_winning_numbers: dict[int, int] = dict()
    num_cards: dict[int,int] = dict()
    for line in map(str.rstrip, file):
        card, numbers = line.split(":")
        _,card_num = card.split()
        card_num = int(card_num)
        num_cards[card_num] = 1
        winning, yours = numbers.split("|")
        winning = winning.split()
        yours = yours.split()
        your_win = set(winning).intersection(set(yours))
        num_winning_numbers[card_num] = len(your_win)
        if len(your_win) > 0:
            ans1 = ans1 + 2**(len(your_win)-1)
    print("part 1:", ans1)

    # part 2
    for card_number in num_cards:
        for i in range(num_winning_numbers[card_number]):
            num_cards[card_number+i+1] += num_cards[card_number]
    print("part 2:", sum(num_cards.values()))

if __name__ == "__main__":
    main()