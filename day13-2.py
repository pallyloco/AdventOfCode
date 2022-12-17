import functools
def main():
    file = open("day13_input.txt", 'r')

    # Now, you just need to put all of the packets in the right order. 
    # Disregard the blank lines in your list of received packets.

    # The distress signal protocol also requires that you include two additional divider packets:
    # [[2]]
    # [[6]]
    pair = [ [[2]], [[6]], ]
 
    for r,line in enumerate(filter(bool,map(str.rstrip,file))):
        pair.append(eval(line))
    
    pair_sorted = sorted(pair,key=functools.cmp_to_key(compare))

    key1 = "[[2]]"
    key2 = "[[6]]"
    keys = [None,None]
    for i,p in enumerate(pair_sorted):
        print (p)
        if f"{p}" == key1: keys[0] = i + 1
        if f"{p}" == key2: keys[1] = i + 1
    print (keys)
    print (keys[0]*keys[1])


def compare(a,b):
    return is_in_order(a,b)
    
def is_in_order(pair1,pair2, depth = 0):

    #print ("\n-------------------------------------")
    #print (depth, pair1, pair2)
    #print ("-------------------------------------")

    for p1,p2 in zip(pair1,pair2):

        # If both values are integers, the lower integer should come first. 
        # If the left integer is lower than the right integer, the inputs are in the right order. 
        # If the left integer is higher than the right integer, the inputs are not in the right order. 
        # Otherwise, the inputs are the same integer; continue checking the next part of the input.
        if isinstance(p1,int) and isinstance(p2,int):
     #       print(depth, f"compare {p1} int to {p2} int")
            if p1 < p2: return -1
            if p1 > p2: return 1

        # If both values are lists, compare the first value of each list, then the second value, and so on. 
        # If the left list runs out of items first, the inputs are in the right order. 
        # If the right list runs out of items first, the inputs are not in the right order. 
        # If the lists are the same length and no comparison makes a decision about the order, 
        # continue checking the next part of the input.
        elif isinstance(p1,list) and isinstance(p2,list):
            result = is_in_order(p1,p2,depth+1)
            if result is not None:
                return result

        # If exactly one value is an integer, convert the integer to a list which contains that integer 
        # as its only value, then retry the comparison. 
        # For example, if comparing [0,0,0] and 2, convert the right value to [2] (a list containing 2); 
        # the result is then found by instead comparing [0,0,0] and [2].
        elif isinstance(p1,int):
            result = is_in_order([p1],p2,depth+1)
            if result is not None: return result
        elif isinstance(p2,int):
            result = is_in_order(p1,[p2],depth+1)
            if result is not None: return result

    if len(pair1) < len(pair2) : return -1
    if len(pair1) > len(pair2) : return 1
    if depth == 0:
        return 0

# ===================================================================
# Entry point
# ===================================================================
if __name__ == '__main__':
    main()