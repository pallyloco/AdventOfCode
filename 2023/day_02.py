MAX_BALLS: dict[str, int] = {"red": 12, "green": 13, "blue": 14}


class Game:
    def __init__(self, descr: str, turns: str):
        _, number = descr.split(" ")
        self.id: int = int(number)
        self.turns: list[GameTurn] = list()
        for t in turns.split(";"):
            self.turns.append(GameTurn(t))

    def is_game_valid(self) -> bool:
        for turn in self.turns:
            for colour, max_count in MAX_BALLS.items():
                if turn.balls[colour] > max_count:
                    return False
        return True

    def power(self) -> int:
        max_balls: dict[str, int] = {"red": 0, "blue": 0, "green": 0}
        for turn in self.turns:
            for colour, count in turn.balls.items():
                max_balls[colour] = max(max_balls[colour], count)
        return max_balls["red"] * max_balls["blue"] * max_balls["green"]


class GameTurn:
    def __init__(self, descr: str):
        self.balls: dict[str, int] = {"red": 0, "blue": 0, "green": 0}
        for play in descr.split(","):
            num, colour = play.split()
            self.balls[colour] = int(num)


def main(part: int = 1):
    file = open("day_02_input.txt", 'r')
    """
    Determine which games would have been possible if the bag had been loaded with only 
    12 red cubes, 13 green cubes, and 14 blue cubes. What is the sum of the IDs of those games?
    
    The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together. 
    For each game, find the minimum set of cubes that must have been present. 
    What is the sum of the power of these sets?
    """
    ans1 = 0
    ans2 = 0
    for line in map(str.rstrip, file):
        game_descr, rest = line.split(":")
        game: Game = Game(game_descr, rest)
        if game.is_game_valid():
            ans1 += game.id
        ans2 += game.power()

    print("part 1:", ans1)
    print("part 2:", ans2)


if __name__ == "__main__":
    main()
