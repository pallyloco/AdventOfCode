from __future__ import annotations
from typing import Optional

# define a type for better clarity
Range = tuple[int, int]  # start and end numbers


def main(part: int = 1):
    file = open("day_05_input.txt", 'r')

    # parsing
    _, seed_str = next(file).split(":")
    seed_info = list(map(int, seed_str.split()))
    conversion: dict[str, dict[Range, Range]] = dict()

    # ------------------------------------------------------------------
    # read the seed ranges, and set valid source range
    # ------------------------------------------------------------------
    valid_source_ranges: list[Range] = list()
    seed_source_ranges: list[Range] = list()
    if part == 1:
        for s in seed_info:
            valid_source_ranges.append(make_range(s, 1))
            seed_source_ranges.append(make_range(s, 1))

    else:
        for s, l in zip(seed_info[::2], seed_info[1::2]):
            valid_source_ranges.append(make_range(s, l))
            seed_source_ranges.append(make_range(s, l))

    # ------------------------------------------------------------------
    # loop through all the various maps
    # ------------------------------------------------------------------
    conversion_type = None
    for line in map(str.rstrip, file):

        # ------------------------------------------------------------------
        # ignore blank lines
        # ------------------------------------------------------------------
        if len(line) == 0:
            continue

        if line.find(":") != -1:
            # ------------------------------------------------------------------
            # starting a new conversion map
            # ------------------------------------------------------------------

            # process previous conversion map so that it only maps valid
            # source ranges, adds any missing source ranges, and ignores everything else
            if conversion_type in conversion:
                conversion[conversion_type] = update_conversion_numbers(conversion[conversion_type],
                                                                        valid_source_ranges)

                # reset the valid source range to the previous destination ranges
                valid_source_ranges = list(conversion[conversion_type].values())

            # setup for new conversion type
            conversion_type, _ = line.split()
            conversion[conversion_type] = dict()

        else:
            # ------------------------------------------------------------------
            # just read in the current mapping ranges
            # ------------------------------------------------------------------
            destination_start, source_start, number_range = list(map(int, line.split()))
            conversion[conversion_type][make_range(source_start, number_range)] = make_range(destination_start,
                                                                                             number_range)

    # ------------------------------------------------------------------
    # process the last map
    # ------------------------------------------------------------------
    conversion[conversion_type] = update_conversion_numbers(conversion[conversion_type], valid_source_ranges)

    # ------------------------------------------------------------------
    # sort locations Ranges
    # ------------------------------------------------------------------
    locations: list[Range] = list(conversion["humidity-to-location"].values())
    locations.sort()
    print(f"ans part {part}:", start(locations[0]))


# =======================================================================
# process the valid source ranges against the decoder source range, and adjust as necessary
# =======================================================================
def update_conversion_numbers(decoder: dict[Range, Range], source_ranges: list[Range]) -> dict[Range, Range]:
    decoder_sorted_keys: list[Range] = sorted(decoder.keys())
    source_ranges.sort()
    new_decoder: dict[Range:Range] = dict()

    decoder_src: Optional[Range] = None
    if len(decoder_sorted_keys):
        decoder_src = decoder_sorted_keys.pop(0)

    # ------------------------------------------------------------------
    # loop over the valid source ranges, adjusting the decoder info as necessary
    # ------------------------------------------------------------------
    while len(source_ranges):
        src: Range = source_ranges.pop(0)
        while True:

            # ------------------------------------------------------------------
            # ++++++++                  src
            #           ***********     decoder_src
            # ------------------------------------------------------------------
            # ++++++++                  new range
            # ------------------------------------------------------------------
            #              ?            next src
            #           ***********     decoder_src unchanged
            # ------------------------------------------------------------------
            if decoder_src is None or end(src) < start(decoder_src):
                new_decoder[src] = src
                break

            # ------------------------------------------------------------------
            #        +++++++++          src
            # ****                      decoder_src
            # ------------------------------------------------------------------
            #        +++++++++          new range
            # ------------------------------------------------------------------
            #              ?            next src
            #              ?            next decoder_src
            # ------------------------------------------------------------------            #
            if start(src) > end(decoder_src):
                decoder_src = None
                if len(decoder_sorted_keys):
                    decoder_src = decoder_sorted_keys.pop(0)
                continue

            # ------------------------------------------------------------------
            # +++++++++++++             src
            #           ********        decoder_src
            # ------------------------------------------------------------------
            # ++++++++++                new range
            # ------------------------------------------------------------------
            #           +++             new src
            #           ********        decoder src unchanged
            # ------------------------------------------------------------------
            if start(src) < start(decoder_src) <= end(src):
                new_decoder[(start(src), start(decoder_src) - 1)] = (start(src), start(decoder_src) - 1)
                src = (start(decoder_src), end(src))
                continue

            # ------------------------------------------------------------------
            #    ++++++++++             src
            #   ****************        decoder_src
            # ------------------------------------------------------------------
            #    ++++++++++             new range
            # ------------------------------------------------------------------
            #              ?            next src
            #   ****************        decoder src unchanged
            # ------------------------------------------------------------------
            if start(src) >= start(decoder_src) and end(src) <= end(decoder_src):
                decoder_dest = decoder[decoder_src]
                dest_start = start(src) - start(decoder_src) + start(decoder_dest)
                new_decoder[src] = make_range(dest_start, length(r=src))
                break

            # ------------------------------------------------------------------
            #         +++++++++         src
            # ************              decoder_src
            # ------------------------------------------------------------------
            #         ++++              new range
            # ------------------------------------------------------------------
            #             +++++         new src
            #                 ?         next decoder_src
            # ------------------------------------------------------------------
            if start(src) <= end(decoder_src) < end(src):
                decoder_dest = decoder[decoder_src]
                dest_start = start(src) - start(decoder_src) + start(decoder_dest)
                l = end(decoder_src) - start(src) + 1
                new_decoder[make_range(start(src), l)] = make_range(dest_start, l)
                src = (end(decoder_src) + 1, end(src))

                if len(decoder_sorted_keys):
                    decoder_src = decoder_sorted_keys.pop(0)
                continue

            print("wtf", )              # should never print!
    return new_decoder


# =======================================================================
# operations on Range (again, just for clarity)
# =======================================================================
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
    main(1)
    main(2)
