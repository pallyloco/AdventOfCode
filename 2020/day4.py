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

def main(part: int = 1 ):
    file = open('day4_input.txt', 'r')
    good_passports = 0
    for line in map(str.rstrip, file):
        
        pass

if __name__ == '__main__':
    main(1)

