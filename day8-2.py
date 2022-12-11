import re
trees = []

def main():
    file = open('day8_input.txt', 'r')
    while True:
        line = file.readline()
        line = line.rstrip()
        if not line: 
            break
        num_cols = len(line)
        trees.append(line.rstrip())

    num_rows = len(trees)
    distance_left = [None]*num_rows
    distance_right = [None]*num_rows

    # side to side
    for row in range(num_rows):
        distance_left[row] = [0]*num_cols
        distance_right[row] = [0]*num_cols
        for col in range (num_cols):
            countr = 0
            countl = 0
            for col2 in range(col+1,num_cols):
                countl += 1
                if int(trees[row][col2]) >= int(trees[row][col]) :
                    break
            for col2 in range(col-1,-1,-1):
                countr += 1
                if int(trees[row][col2]) >= int(trees[row][col]) :
                    break
            distance_left[row][col]=countl
            distance_right[row][col]=countr


    distance_up = []
    distance_down = []
    for row in range(num_rows):
        distance_up.append([])
        distance_down.append([])
        for col in range (num_cols):
            distance_up[row].append(None)
            distance_down[row].append(None)

    # up down
    for col in range(num_cols):
        
        for row in range (num_rows):
            countu = 0
            countd = 0
            for row2 in range(row+1,num_rows):
                countu += 1
                if int(trees[row2][col]) >= int(trees[row][col]) :
                    break
            for row2 in range(row-1,-1,-1):
                countd += 1
                if int(trees[row2][col]) >= int(trees[row][col]) :
                    break
            distance_up[row][col]=countu
            distance_down[row][col]=countd

#    for dl in distance_left:
#        print(dl)
#    for dr in distance_right:
#        print(dr)
#    for t in trees:
#        print(t)
#    for du in distance_up:
#        print(du)

    max = 0
    for row in range(num_rows):
        for col in range (num_cols):
            diru = distance_up[row][col]
            dird = distance_down[row][col]
            dirl = distance_left[row][col]
            dirr = distance_right[row][col]
            if diru*dird*dirl*dirr > max:
                print (f"({row},{col})  {diru*dird*dirl*dirr}")
                max = diru*dird*dirl*dirr


# ===================================================================
# Entry point
# ===================================================================
if __name__ == '__main__':
    main()