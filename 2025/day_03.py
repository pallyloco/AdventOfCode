data = """987654321111111
811111111111119
234234234234278
818181911112111
"""
data = tuple(map(str.rstrip, data.splitlines()))
fh = open("day_03.txt", "r")
data = tuple(map(str.rstrip, fh.readlines()))

def max_joltage(max_batteries):
    total = 0
    for battery_bank in data:
        battery_joltage = []
        joltages = [int(b) for b in battery_bank]
        for n in range(max_batteries,0,-1):
            if n == 1:
                battery_joltage.append(max(joltages))
            else:
                battery_joltage.append(max(joltages[:-(n-1)]))
            index = joltages.index(battery_joltage[-1])
            joltages = joltages[index+1:]

        max_joltage = 0
        for joltage in battery_joltage:
            max_joltage = max_joltage*10 +  joltage

        total += max_joltage
    return total

if __name__ == "__main__":
    for max_batteries in (2,12):
        print(max_joltage(max_batteries))

