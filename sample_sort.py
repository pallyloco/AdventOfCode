dictionary = {3:"three",1:"one",4:"four",2:"two"}

mynums = [dictionary[i] for i in sorted(dictionary.keys())]
print(mynums)

#my @numbers_in_order = sort {$a <=> $b} keys %dictionary;
#print("@numbers_in_order");