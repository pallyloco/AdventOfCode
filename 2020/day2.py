
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
