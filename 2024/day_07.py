import itertools as it

data = [
    "190: 10 19",
    "3267: 81 40 27",
    "83: 17 5",
    "156: 15 6",
    "7290: 6 8 6 15",
    "161011: 16 10 13",
    "192: 17 8 14",
    "21037: 9 7 18 13",
    "292: 11 6 16 20",
]


def main():
    # part 1
    fh = open("day_07.txt", "r")
    data = list(map(str.rstrip,fh))
    num_valid = 0
    for line in data:
        num_valid = num_valid + is_valid(line)
    print(num_valid)


def is_valid(line: str) -> int:
    result, rest = line.split(":")
    nums = rest.split()
    return int(result) if recursive_calc(int(result),list(map(int,nums))) else 0


def recursive_calc(wanted, nums) -> bool:
    if len(nums) >= 2:
        a, b, *rest = nums
        new_num = int(str(a)+str(b))
        if a * b > wanted and a + b > wanted and new_num > wanted:
            return False
        valid1 = recursive_calc(wanted, [a * b, *rest])
        valid2 = recursive_calc(wanted, [a + b, *rest])
        valid3 = recursive_calc(wanted, [new_num, *rest])
        if valid1 or valid2 or valid3:
            return True
    else:
        return nums[0] == wanted




main()