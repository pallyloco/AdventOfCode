# too low 5907
# too high 5967
data = """L68
L30
R48
L5
R160
L55
L1
L99
R14
L82
"""
data = tuple(map(str.rstrip, data.splitlines()))
fh = open("day_01.txt", "r")
data = tuple(map(str.rstrip,fh.readlines()))
pointer = 50

password_number1 = 0
password_number2 = 0

for d in data:
    direction, value = d[0], int(d[1:])

    # pointer passes 0 for every value of '100'
    password_number2 += int(value/100)
    value = value%100

    if direction == "R":
        new = (pointer+value)%100
        if new < pointer:
            password_number2 += 1
    else:
        new = (pointer-value)%100
        if (new > pointer or new == 0) and pointer !=0:
            password_number2 += 1
    pointer = new
    if pointer == 0:
        password_number1 += 1
print (password_number1, password_number2)