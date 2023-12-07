from __future__ import annotations
from itertools import combinations
from typing import Optional

card_values: dict[str, int] = {"A": 13, "K": 12, "Q": 11, "J": 10, "T": 9, "9": 8, "8": 7, "7": 6, "6": 5, "5": 4,
                               "4": 3,
                               "3": 2, "2": 1}


class Hand:

    def __init__(self, cards: str, wildcard: Optional[str] = None):
        self.cards: str = cards
        self.wildcard = wildcard

    def __str__(self):
        return self.cards

    def __repr__(self):
        return str(self)

    def wildcard_hands(self, result: list[Hand]):
        if self.wildcard is None:
            result.append(self)
            return

        if self.wildcard not in self.cards:
            result.append(self)
            return

        for c in "AKQJT98765432".replace(self.wildcard, ""):
            new = Hand(self.cards.replace(self.wildcard, c), self.wildcard)
            new.wildcard_hands(result)

    def is_num_of_a_kind(self, num: int) -> bool:
        for combo in combinations(str(self), num):
            if all(c == combo[0] for c in combo):
                return True
        return False

    def is_two_pair(self) -> bool:
        return sum([1 for combo in combinations(str(self), 2) if combo[0] == combo[1]]) == 2

    def is_full_house(self) -> bool:
        c = sorted(self.cards)
        return c[0] == c[1] == c[2] and c[3] == c[4] or c[0] == c[1] and c[2] == c[3] == c[4]

    def is_high_card(self) -> bool:
        cards: str = self.cards
        return cards[0] != cards[1] != cards[2] != cards[3] != cards[4] != cards[5]

    def __lt__(self, other: Hand) -> bool:
        rank1 = self._get_rank()
        rank2 = other._get_rank()
        if rank1 == rank2:
            card1 = self.cards
            card2 = other.cards

            for c1, c2 in zip(card1, card2):
                if c1 == c2:
                    continue
                return card_values[c1] < card_values[c2]
            return True

        return rank1 < rank2

    def _get_rank(self) -> int:
        hands: list[Hand] = list()
        max_rank: int = 0
        self.wildcard_hands(hands)
        for hand in hands:
            if hand.is_num_of_a_kind(5):
                max_rank = max(max_rank, 7)
            if hand.is_num_of_a_kind(4):
                max_rank = max(max_rank, 6)
            if hand.is_full_house():
                max_rank = max(max_rank, 5)
            if hand.is_num_of_a_kind(3):
                max_rank = max(max_rank, 4)
            if hand.is_two_pair():
                max_rank = max(max_rank, 3)
            if hand.is_num_of_a_kind(2):
                max_rank = max(max_rank, 2)
            max_rank = max(max_rank, 1)
        return max_rank

    def _who_is_lower(self, other: Hand) -> Hand:
        card1 = self.cards
        card2 = other.cards
        for c1, c2 in zip(card1, card2):
            if c1 == c2:
                continue
            if card_values[c1] < card_values[c2]:
                return self
            else:
                return other
        return self


def main(part: int = 1):
    global card_values
    wildcard = None
    if part != 1:
        card_values["J"] = 0
        wildcard = "J"

    file = open("day_07_input.txt", 'r')
    plays: list[tuple[Hand, int]] = list()
    for line in map(str.rstrip, file):
        hand, bet = line.split()
        plays.append((Hand(hand, wildcard), int(bet)))

    plays.sort()
    ans = 0
    for i, p in enumerate(plays):
        ans += (i + 1) * p[1]
    print("Answer", ans)


if __name__ == "__main__":
    main()
    main(2)
