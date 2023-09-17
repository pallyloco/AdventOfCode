import DictionaryGrid as dg
import re

# Sensor at x=2, y=18: closest beacon is at x=-2, y=15
parse = re.compile(r'.*?x=(-?\d+).*?y=(-?\d+).*?x=(-?\d+).*?y=(-?\d+)')

real_max = 4000000
max_row = real_max
max_col = real_max

def main():
    file = open("day15_input.txt", 'r')
    sensors = list()

    all_ranges = [[(0,max_col)] for _ in range(max_row+1)]
    for line in map(str.rstrip,file):
        print(line)
        sc,sr,bc,br = map(int,parse.match(line).groups())
        distance = abs(sc - bc) + abs(sr - br)
        sensors.append((sr,sc,distance))

        row_start = max(0,sr-distance)
        row_end = min(max_row,sr+distance)
        for r in range(row_start,row_end+1):
            col_start = max (0, sc-(distance-abs(r-sr)))
            col_end = min (max_col, sc + (distance-abs(r-sr)))
            
            remove_ranges(all_ranges,r,col_start,col_end)
    
    for r,ranges in enumerate(all_ranges):
        if len(ranges) != 0:
            print (r, ranges)
            print (r + ranges[0][0]*real_max)
#    print_map(all_ranges)
#    input("wait")
            
def print_map (all_ranges):
    print()
    for r in range(max_row+1):
        for c in range (max_col+1):
            ranges = all_ranges[r]
            str = "#"
            for start,end in ranges:
                if start <= c <= end:
                    str = "."
            print (str,end="")
        print()

def remove_ranges(all_ranges,r,cl,ch):
    ranges = all_ranges[r]
    new_ranges = []
    for cs,ce in ranges:
        
        # [cs .. (cl,ch) .. ce]
        if cs <= cl <= ce and cs <= ch <= ce:
            if cl-cs != 0 : new_ranges.append( (cs,cl-1) )
            if ch-ce != 0 : new_ranges.append( (ch+1,ce) )
            continue

        #  if [cs .. (cl .. ce] .. ch)
        if cs <= cl <= ce: 
            if cs-cl !=0 : new_ranges.append( (cs,cl-1) )
            continue

        # if (cl .. [cs .. ch) .. ce]
        if cs <= ch <= ce:
            if ch-ce !=0 : new_ranges.append( (ch+1,ce) )
            continue

        # if (cl .. [cs,ce] .. ch)
        if cl <=cs and ce <= ch:
            continue

        new_ranges.append( (cs,ce) )
    all_ranges[r] = new_ranges
        






# ===================================================================
# Entry point
# ===================================================================
if __name__ == '__main__':
    main()