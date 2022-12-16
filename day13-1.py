def main():
    file = open("day13_input.txt", 'r')
    pair = []
    pair_num = 1
    score = 0

    for r,line in enumerate(map(str.rstrip,file)):
        if not line:
            is_good = is_in_order(pair)
            if is_good: score += pair_num
            print (pair_num, is_good)
            pair = []
            pair_num += 1
            continue
        pair.append(eval(line))

    is_good = is_in_order(pair)
    print (pair_num, is_good)

    print (f"score: {score}")


def is_in_order(pair, depth = 0):

    pair1 = pair[0]
    pair2 = pair[1]
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
            if p1 < p2: return True
            if p1 > p2: return False

        # If both values are lists, compare the first value of each list, then the second value, and so on. 
        # If the left list runs out of items first, the inputs are in the right order. 
        # If the right list runs out of items first, the inputs are not in the right order. 
        # If the lists are the same length and no comparison makes a decision about the order, 
        # continue checking the next part of the input.
        elif isinstance(p1,list) and isinstance(p2,list):
      #      print(depth, f"comparing {p1},{p2}, ")
            result = is_in_order([p1,p2],depth+1)
            if result is not None:
                return result

        # If exactly one value is an integer, convert the integer to a list which contains that integer 
        # as its only value, then retry the comparison. 
        # For example, if comparing [0,0,0] and 2, convert the right value to [2] (a list containing 2); 
        # the result is then found by instead comparing [0,0,0] and [2].
        elif isinstance(p1,int):
       #     print(depth, f"comparing {p1},{p2}, ")
            result = is_in_order([[p1],p2],depth+1)
            if result is not None: return result
        elif isinstance(p2,int):
        #    print(depth, f"comparing {p1},{p2}, ")
            result = is_in_order([p1,[p2]],depth+1)
            if result is not None: return result

    if len(pair1) < len(pair2) : return True
    if len(pair1) > len(pair2) : return False
    if depth == 0:
        return True

# ===================================================================
# Entry point
# ===================================================================
if __name__ == '__main__':
    main()