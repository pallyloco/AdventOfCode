# Ch 1 No Side Cars

total = 0
for x in range(100):
  total += x

total = sum(range(100))

res = []
for x in range(100):
    res.append(x)

res = list(range(100))

index = 0
x = list('abc','def')
for name in x:
    boo[index] = "gotcha"
    index += 1

for index,name in enumerate(x):
    ...

'''
zip
enumerate
map
filter
'''

# Chapter 2
# Don't loop by index/key

# For Lists loop, looping
# Looping by index limits what is being iterated to be
# lists (or other which has .__getitem__(x: int))

for i in range(len(x)):
    y = x[i]
    ...

for k in x.keys():
    v = x[k]
    ...

for y in x:
    ...

for k, v in x.items():
    ...

# Chapter 3
# Generators and lazy evalutation

def getChildren(self):
    queue = deque((self,))
    while queue:
        curr = queue.popleft()
        yield curr
        queue.extend(immediate_children(curr))


# Idea 4
# What are iterable

# Part 1
# Here are things that you didn't realize you can loop over
# Files, loop over their line
# dict loop over their keys
# database cursors loop over the rows of a query

# Part 2
# __iter__ and __next__
# Elaborating on what exactly is `range` and `map`
# Python2, these returned lists


# Idea 5
# Comprehensions
# list:
    [mapping_expression for element in iterable if filter_expression]
# set:
    {mapping_expression for element in iterable if filter_expression}
# dict:
    {key_expression: value_expression for element in iterable if filter_expression}
# generators:
    (mapping_expression for element in iterable if filter_expression)

sum(a**2 for a in range(10))

# Idea 6
# Everthing takes an iterable

csv.writerows([[2, 3],[3, 4]])
# SHOW MY CSV SERERIALIZER EXAMPLE

#container constructors
list, dict, set, tuple

# Idea 7
# DON'T USE LISTS

bad: list(map(lambda a: a*a for a in range(10)))