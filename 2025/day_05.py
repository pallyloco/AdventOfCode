from reading import read_paragraphs
data="""3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""
data = data.splitlines()
fh = open("day_05.txt", "r")
data = tuple(map(str.rstrip, fh.readlines()))


def fresh(day=1):

    # parse data
    data_generator = read_paragraphs(data)
    ranges_str = next(data_generator)
    ingredient_id_str = next(data_generator)
    ranges = [range(int(x),int(y)+1) for x,y in (r.split("-") for r in ranges_str)]
    ingredient_ids = (int(x) for x in ingredient_id_str)

    # how many ingredients are fresh?
    if day == 1:
        num_fresh = sum(1 for i in ingredient_ids if in_ranges(i,ranges))
        return num_fresh
    else:
        available_fresh = sum(len(r) for r in merging_ranges(ranges))
        return available_fresh

def merging_ranges(data: list[range]):
    data.sort(key=lambda x: x.start)
    one = data[0]
    for two in data[1:]:

        # merge one and two
        if two.start in one:
            one = range(one.start, max(one.stop, two.stop))

        # not mergeable
        else:
            yield one
            one = two

    yield one


def in_ranges(i: int, rs: list[range]) -> bool:
    for r in rs:
        if i in r:
            return True
    return False

if __name__ == "__main__":
    print(f"answer 1: {fresh(1)}")
    print(f"answer 2: {fresh(2)}")
