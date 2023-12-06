from __future__ import annotations
from typing import Optional

Range = tuple[int, int]  # start and end numbers


def main():
    file = open("day_05_input.txt", 'r')

    # seeds
    _, seed_str = next(file).split(":")
    seed_info = list(map(int, seed_str.split()))
    conversion: dict[str, dict[Range, Range]] = dict()

    valid_source_ranges: list[Range] = list()
    seed_source_ranges: list[Range] = list()
    for s, l in zip(seed_info[::2], seed_info[1::2]):
        valid_source_ranges.append(make_range(s, l))
        seed_source_ranges.append(make_range(s, l))

    conversion_type = None
    for line in map(str.rstrip, file):
        if len(line) == 0:
            continue

        # line for conversion tmap
        if line.find(":") != -1:

            # update any conversion numbers that were not listed
            if conversion_type in conversion:
                conversion[conversion_type] = update_conversion_numbers(conversion[conversion_type],
                                                                        valid_source_ranges)
                valid_source_ranges = list(conversion[conversion_type].values())

            # setup for new conversion type
            conversion_type, _ = line.split()
            conversion[conversion_type] = dict()

        else:
            destination_start, source_start, number_range = list(map(int, line.split()))
            conversion[conversion_type][make_range(source_start, number_range)] = make_range(destination_start,
                                                                                             number_range)

    conversion[conversion_type] = update_conversion_numbers(conversion[conversion_type], valid_source_ranges)

    locations: list[Range] = list(conversion["humidity-to-location"].values())
    locations.sort()
    print("ans part 2:", start(locations[0]))


def update_conversion_numbers(decoder: dict[Range, Range], source_ranges: list[Range]) -> dict[Range, Range]:
    decoder_sorted_keys: list[Range] = sorted(decoder.keys())
    source_ranges.sort()
    new_decoder: dict[Range:Range] = dict()

    decoder_src: Optional[Range] = None
    if len(decoder_sorted_keys):
        decoder_src = decoder_sorted_keys.pop(0)

    while len(source_ranges):
        src: Range = source_ranges.pop(0)
        done = False
        while not done:

            # ++++++++
            #           ***********
            if decoder_src is None or end(src) < start(decoder_src):
                new_decoder[src] = src
                done = True
                break

            #        +++++++++
            # ****
            if start(src) > end(decoder_src):
                decoder_src = None
                if len(decoder_sorted_keys):
                    decoder_src = decoder_sorted_keys.pop(0)
                continue

            # +++++++++++
            #           ********
            if start(src) < start(decoder_src) <= end(src):
                new_decoder[(start(src), start(decoder_src) - 1)] = (start(src), start(decoder_src) - 1)
                src = (start(decoder_src), end(src))
                continue

            #    ++++++++++
            #   ************
            if start(src) >= start(decoder_src) and end(src) <= end(decoder_src):
                decoder_dest = decoder[decoder_src]
                dest_start = start(src) - start(decoder_src) + start(decoder_dest)
                new_decoder[src] = make_range(dest_start, length(r=src))
                done = True
                break

            #         +++++++++
            # ************
            if start(src) <= end(decoder_src) < end(src):
                decoder_dest = decoder[decoder_src]
                dest_start = start(src) - start(decoder_src) + start(decoder_dest)
                l = end(decoder_src) - start(src) + 1
                new_decoder[make_range(start(src), l)] = make_range(dest_start, l)
                src = (end(decoder_src) + 1, end(src))
                continue

            print("wtf", )
    return new_decoder


def length(start_number: Optional[int] = None, end_number: Optional[int] = None, r: Optional[Range] = None) -> int:
    if r is not None:
        return end(r) - start(r) + 1
    return end_number - start_number + 1


def make_range(start_number: int, length_number: int) -> Range:
    return start_number, start_number + length_number - 1


def start(r: Range) -> int:
    return r[0]


def end(n: Range) -> int:
    return n[1]


if __name__ == "__main__":
    main()
