"""
To try to debug the problem, they have created a list (your puzzle input) of passwords
(according to the corrupted database) and the corporate policy when that password was set.

For example, suppose you have the following list:

1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
Each line gives the password policy and then the password.
The password policy indicates the lowest and highest number of times a given letter must
appear for the password to be valid. For example, 1-3 a means that the password must contain a
at least 1 time and at most 3 times.

The Official Toboggan Corporate Policy actually works a little differently.

Each policy actually describes two positions in the password, where 1 means the first character,
2 means the second character, and so on. (Be careful; Toboggan Corporate Policies have no concept of "index zero"!)
Exactly one of these positions must contain the given letter.
Other occurrences of the letter are irrelevant for the purposes of policy enforcement.

"""

def main(part: int = 1 ):
    file = open('day2_input.txt', 'r')
    good_passwords = 0
    for line in map(str.rstrip, file):
        frequency, letter, password = line.split(" ")
        low_freq, hi_freq = map(int,frequency.split("-"))
        letter = letter[0]

        if part == 1:
            # without using regex
            num_chars = len([c for c in password if c == letter])
            if low_freq <= num_chars <= hi_freq:
                good_passwords += 1

        if part == 2:
            if (password[low_freq-1] == letter or password[hi_freq-1] == letter) and \
                   not (password[low_freq-1] == letter and password[hi_freq-1] == letter):
                good_passwords += 1

    print ("Number of good passwords is:", good_passwords)


if __name__ == '__main__':
    main(1)
    main(2)
