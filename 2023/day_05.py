def main(part: int = 1):
    file = open("day_05_input.txt", 'r')

    # seeds
    _, seed_str = next(file).split(":")
    seeds = list(map(int, seed_str.split()))
    conversion: dict[str, dict[int, int]] = dict()

    valid_source_numbers: list[int] = seeds

    conversion_type = None
    for line in map(str.rstrip, file):
        if len(line) == 0:
            continue

        # line for conversion tmap
        if line.find(":") != -1:

            # update any conversion numbers that were not listed
            valid_source_numbers = update_conversion_numbers(conversion, conversion_type, valid_source_numbers)

            # setup for new conversion type
            conversion_type, _ = line.split()
            conversion[conversion_type] = dict()

        else:
            destination_start, source_start, number_range = list(map(int, line.split()))
            for v in valid_source_numbers:
                if v in range(source_start, source_start + number_range):
                    conversion[conversion_type][v] = destination_start + (v - source_start)

    update_conversion_numbers(conversion, conversion_type, valid_source_numbers)
    print(conversion)
    locations = [get_location_from_seed(seed, conversion) for seed in seeds]
    print("part 1:", min(locations))


def update_conversion_numbers(conversion, conversion_type, valid_source_numbers):
    if conversion_type in conversion:
        for v in valid_source_numbers:
            if v not in conversion[conversion_type].keys():
                conversion[conversion_type][v] = v
        return list(conversion[conversion_type].values())
    return valid_source_numbers


def get_location_from_seed(seed: int, conversion: dict[str, dict[int, int]]) -> int:
    soil: int = conversion["seed-to-soil"][seed]
    fertilizer: int = conversion["soil-to-fertilizer"][soil]
    water: int = conversion["fertilizer-to-water"][fertilizer]
    light: int = conversion["water-to-light"][water]
    temperature: int = conversion["light-to-temperature"][light]
    humidity: int = conversion["temperature-to-humidity"][temperature]
    location: int = conversion["humidity-to-location"][humidity]
    print(seed, soil, fertilizer, water, light, temperature, humidity, location)
    return location


if __name__ == "__main__":
    main()
