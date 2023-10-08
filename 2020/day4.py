"""
It seems like you're not the only one having problems, though; a very long line has formed for the automatic 
passport scanners, and the delay could upset your travel itinerary.

Due to some questionable network security, you realize you might be able to solve both of these problems at 
the same time.

The automatic passport scanners are slow because they're having trouble detecting which passports have all 
required fields. The expected fields are as follows:

byr (Birth Year)
iyr (Issue Year)
eyr (Expiration Year)
hgt (Height)
hcl (Hair Color)
ecl (Eye Color)
pid (Passport ID)
cid (Country ID)

Passport data is validated in batch files (your puzzle input). Each passport is represented as a sequence of 
key:value pairs separated by spaces or newlines. Passports are separated by blank lines.

Count the number of valid passports - those that have all required fields. Treat cid as optional. 
In your batch file, how many passports are valid?

"""
from typing import Optional

# 212 is too low
delme = 0

REQUIRED_KEYS = sorted(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])


def main(part: int = 1):
    file = open('day4_input.txt', 'r')
    required_keys_passports = 0
    passport_lines: list[str] = list()
    passports: list[dict[str,str]] = list()

    for line in map(str.rstrip, file):

        # passports are separated by lines
        if not line:
            passports.append(convert_to_passport(passport_lines))
            passport_lines.clear()
            continue

        passport_lines.append(line)

    # last passport
    passports.append(convert_to_passport(passport_lines))

    # part 1, number of passports with all the appropriate keys
    num_with_keys = sum((1 for passport in passports if passport is not None))
    print("passports with all required keys:", num_with_keys)

    # part 2
    num_valid_passports = sum((1 for passport in passports if passport is not None and valid_passport(passport)))
    print("valid passports:", num_valid_passports)


def convert_to_passport(lines: list[str]) -> Optional[dict[str, str]]:
    passport: dict[str, str] = dict()
    for line in lines:
        key_values = line.split(" ")
        for key_value in key_values:
            key, value = key_value.split(":")
            passport[key] = value

    keys: list[str] = [k for k in passport.keys() if k in REQUIRED_KEYS]

    if len(keys) == len(REQUIRED_KEYS):
        return passport
    return None


def valid_passport(passport: dict[str, str]) -> bool:
    """
    You can continue to ignore the cid field, but each other field has strict rules about
    what values are valid for automatic validation:

    cid (Country ID) - ignored, missing or not.

    Your job is to count the passports where all required fields are both present and valid
    according to the above rules.
    """

    # going to try this without regex :)

    try:
        """byr (Birth Year) - four digits; at least 1920 and at most 2002."""
        if not between(int(passport["byr"]), 1920, 2020): return False

        """iyr (Issue Year) - four digits; at least 2010 and at most 2020."""
        if not between(int(passport["iyr"]), 2010, 2020): return False

        """eyr (Expiration Year) - four digits; at least 2020 and at most 2030."""
        if not between(int(passport["eyr"]), 2020, 2030): return False

        """hgt (Height) - a number followed by either cm or in:
                If cm, the number must be at least 150 and at most 193.
                If in, the number must be at least 59 and at most 76.
        """
        if passport["hgt"][-2:] != "cm" and passport["hgt"][-2:] != "in": return False
        hgt = int(passport["hgt"][0:-2])
        if passport["hgt"][-2:] == "in" and not between(hgt, 59, 76): return False
        if passport["hgt"][-2:] == "cm" and not between(hgt, 150, 193): return False

        """hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f."""
        if passport["hcl"][0] != "#": return False
        if len(passport["hcl"]) != 7: return False
        _ = int(passport["hcl"][1:], 16)

        """ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth."""
        if passport["ecl"] not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]: return False

        """pid (Passport ID) - a nine-digit number, including leading zeroes."""
        if len(passport["pid"]) !=9: return False
        _ = int(passport["pid"])

    except ValueError:
        return False

    return True


def between(value: int, min_value: int, max_value: int) -> bool:
    return min_value <= value <= max_value


if __name__ == '__main__':
    main(1)
