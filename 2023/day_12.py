import re
from functools import cache

# answer: (5) 3367542988
# answer: (1) 7007


def main(duplicate: int = 5):
    """read file and process each line"""
    file = open("day_12_input.txt", 'r')
    ans1 = 0
    for line in map(str.rstrip, file):
        spring_str, unknown_groupings = line.split()
        groups: list[int] = list(map(int, unknown_groupings.split(",")))
        spring_str = "?".join([spring_str]*duplicate)
        groups = groups*duplicate

        n = calculate_number_of_matches(spring_str, groups)
        ans1 += n
    print("answer 1:", ans1)

def min_skip2_regex(skip, groups)->str:
    """
    Skips the first characters, and then finds the minimum number of "." or "?" that need to be skipped
    in order to match the specified group numbers to the string
    Args:
        skip: # of characters to ignore at the beginning of the string
        groups: the remaining spring groups to be matched

    Returns: an regex string with one group capture
    """
    regex = rf"^.{{{skip}}}([.?]*?)"
    for g in groups[:-1]:
        regex += rf"[#?]{{{g}}}[.?]+?"
    regex += rf"[#?]{{{groups[-1]}}}(?:[.?]+|$)"
    return regex

def parse(spring_str, groups, indices: dict[int,int]):
    """
    Args:
        spring_str: The string to match
        groups: The current set of integers to match
        indices: The valid indices and frequencies into spring_str from where to start matching the groups

    Returns: A list of numbers of characters that can be ignored before matching all but the first group number

    """
    skips = {}
    for skip, frequency in indices.items():
        max_skip2 = len(spring_str) - skip - sum(groups)
        skip+=1
        regex = min_skip2_regex(skip, groups)

        if match := re.match(regex, spring_str):
            skip2 = len(match.group(1))

            for skip2 in range(skip2,max_skip2+1):
                if matched(spring_str,skip,skip2, groups):
                    index = skip + skip2 + groups[0]
                    current = skips.get(index,0)
                    skips[skip + skip2 + groups[0]] = current + frequency

    return skips

def matched(spring_str, skip, skip2, groups) ->bool:
    """check if string matches with the groups"""
    if "#" in spring_str[skip:skip+skip2]:
        return False
    return does_match(spring_str[skip+skip2:], tuple(groups))

@cache
def does_match(spring_str,group)->bool:
    """check if this matches, starting with the first element in group (no leading "." or "?"
    NOTE: Simulates a regular expression with minimumal grouping
          i.e. [character]*? etc
    """
    for g in group:

        # cannot fit the first element in group
        if "." in spring_str[:g]:
            return False

        # must have enough length
        if len(spring_str) < g:
            return False

        # if this is the last group, then can have no more "#" in the remainder of the string
        if len(group) == 1:
            if "#" in spring_str[g:]:
                return False
            return True

        # if we have more groups to go, then next character cannot be a "#"
        try:
            if spring_str[g] == "#":
                return False
        except IndexError:
            return False

        # can skip over any number of non "#"
        for i in range(len(spring_str)-sum(group)+1):

            if "#" in spring_str[g+1:g+1+i]:
                return False

            # check the rest of the group
            fits = does_match(spring_str[g+1+i:], group[1:])
            if fits:
                return True
        return False
    return False



def calculate_number_of_matches(spring_str, groups):

    skips = {-1:1}
    while len(groups) != 0:
        skips = parse(spring_str,groups,skips)
        groups.pop(0)
    ans = sum(skips.values())
    return ans

main(1)
main(5)

