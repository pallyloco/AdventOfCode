# https://open.kattis.com/problems/risdomare
num_of_samples = int(input())
decision = input()
saved_index = 0
max_size = 0
max_num_grains = 0
max_total = 0
for index in range(num_of_samples):
    num, size = map(int, input().split(" "))
    if num+size > max_total:
        max_total = num+size
        saved_index = index
        max_num_grains = num
        max_size = size
    elif num+size == max_total:
        if decision == "antal":
            if num > max_num_grains:
                max_size = size
                max_num_grains = num
                saved_index = index
        else:
            if size > max_size:
                max_size = size
                max_num_grains = num
                saved_index = index
print (saved_index + 1)

