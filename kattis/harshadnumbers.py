# https://open.kattis.com/problems/harshadnumbers
number_str = input()
digits_add = sum(map(int, number_str))
number = int(number_str)
count = 0
while number % digits_add:
    number += 1
    digits_add = sum(map(int, str(number)))
print (number-1)