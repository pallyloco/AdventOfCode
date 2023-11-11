num_datasets = int(input())
for _ in range(num_datasets):
    size, min_num = map(int, input().split())
    dataset = list(map(int, input().split()))

    last_sum = 0
    this_sum = 0
    m_count = 0
    max_sum = 0
    for n in dataset:
        if n == min_num:
            m_count += 1
        if n < min_num or n == min_num:
            if m_count > 0:
                max_sum = max(max_sum, last_sum + this_sum + min_num)
            if n < min_num:
                last_sum = 0
                this_sum = 0
                m_count = 0
                continue
            else:
                last_sum = this_sum
                this_sum = 0
                continue
        this_sum += n
    if m_count > 0:
        max_sum = max(max_sum, last_sum + this_sum + min_num)

    print (max_sum)

""" NOT FAST ENOUGH

import itertools as it
num_datasets = int(input())
for _ in range(num_datasets):
    size, min_num = map(int, input().split())
    dataset = list(map(int, input().split()))

    # split data set into smaller groups where there are no numbers less than min_num
    subsets = list()
    while dataset:
        subset = [*it.takewhile(lambda x: x >= min_num, dataset)]
        dataset = dataset[len(subset):]
        if dataset:
            dataset = dataset[1:]
        subsets.append(subset)

    sums = list()
    max_sum = 0
    for subset in subsets:
        if min_num not in subset: continue

        # split subset into sequences, separated by minimum number
        while subset:
            part = [*it.takewhile(lambda x: x > min_num, subset)]
            subset = subset[len(part):]
            sums.append(sum(part))

            # pop off the min_num from the subset
            if subset:
                subset = subset[1:]

        # what is the max weight for this subset?
        for i in range(len(sums)-1):
            max_sum = max(max_sum, sums[i] + sums[i+1] + min_num)

    print(max_sum)
"""