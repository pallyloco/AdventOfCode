"""
Bus schedules are defined based on a timestamp that measures the number of minutes
since some fixed reference point in the past. At timestamp 0, every bus simultaneously
departed from the sea port.

After that, each bus travels to the airport, then various other locations, and finally
returns to the sea port to repeat its journey forever.

The time this loop takes a particular bus is also its ID number: the bus with ID 5
departs from the sea port at timestamps 0, 5, 10, 15, and so on. The bus with ID 11
departs at 0, 11, 22, 33, and so on. If you are there when the bus departs, you can ride
that bus to the airport!

Your notes (your puzzle input) consist of two lines.
The first line is your estimate of the earliest timestamp you could depart on a bus.
The second line lists the bus IDs that are in service according to the shuttle company;
entries that show x must be out of service, so you decide to ignore them.

To save time once you arrive, your goal is to figure out the earliest bus you can take to
the airport. (There will be exactly one such bus.)

What is the ID of the earliest bus you can take to the airport multiplied by
the number of minutes you'll need to wait for that bus?

# ====== part 2
The shuttle company is running a contest: one gold coin for anyone that can find the
earliest timestamp such that the first bus ID departs at that time and each subsequent
listed bus ID departs at that subsequent minute.
(The first line in your input is no longer relevant.)

The only bus departures that matter are the listed bus IDs at their specific offsets from t.
Those bus IDs can depart at other times, and other bus IDs can depart at those times.

What is the earliest timestamp such that all of the listed bus IDs depart at offsets
matching their positions in the list?

ANS: 552612234243498
"""
from typing import Optional


def main(part: int = 1):
    file = open('day13_input.txt', 'r')
    timestamp = int(file.readline())
    info = file.readline()
    buses: list[tuple[int, int]] = list()
    for offset, bus in enumerate(info.split(",")):
        if bus != "x":
            buses.append([int(bus), -offset])
    buses.sort(reverse=True)

    # =========== part 1 ===================
    best_bus = None
    if part == 1:
        for bus, offset in buses:
            m = timestamp % bus
            wait = bus - m
            if best_bus is None:
                best_bus = (wait, bus)
            if wait < best_bus[0]:
                best_bus = (wait, bus)
        print("Answer =", best_bus[0] * best_bus[1])

    # ========= part 2 =====================
    if part == 2:
        factor: Optional[int] = None
        offset: Optional[int] = None
        for bus, remainder in buses:
            # t = (bus * i + offset)
            if factor is None:
                factor = bus
                offset = remainder
            else:
                # t = (factor * i + offset) % bus = remainder
                # i = bus * j + n
                n = solve_congruency(factor, offset, bus, remainder)
                # t =  (factor (bus * j + n) + offset
                #   = factor*bus*j + factor*n+offset
                offset = factor * n + offset
                factor = factor * bus
        print(f"t = {factor}k + {offset}")


def solve_congruency(multiplier, offset, modulus, remainder) -> int:
    """
        (multiplier * i + offset ) % modulus = remainder
        returns i
    """
    for i in range(modulus):
        if (multiplier * i + offset) % modulus == remainder % modulus:
            return i
    return 0


if __name__ == "__main__":
    main(1)
    main(2)
