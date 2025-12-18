from __future__ import annotations

from functools import lru_cache

data = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""
data = list(map(str.rstrip, data.splitlines()))
fh = open("day_11.txt", "r")
data = list(map(str.rstrip, fh.readlines()))


class Device:
    def __init__(self, name: str):
        self.connected_to: set[Device] = set()
        self.name = name
        self.num_total = None
        self.num_fft_paths = None
        self.num_dac_paths = None
        self.num_both = None
        self.has_fft = True if name == "fft" else False
        self.has_dac = True if name == "dac" else False


    def __str__(self):
        return f"{self.name} paths: {self.num_total} (fft:{self.num_fft_paths}) (dac:{self.num_dac_paths}) (both:{self.num_both})"

    def __repr__(self):
        return str(self)


def parse_server_rack_connections(d):
    all_devices: dict[str, Device] = {}
    for line in d:
        source_device, other_devices = line.split(":")
        if source_device not in all_devices:
            all_devices[source_device] = Device(source_device)
        all_devices[source_device] = all_devices[source_device]
        for device in other_devices.split():
            if device not in all_devices:
                all_devices[device] = Device(device)
            all_devices[source_device].connected_to.add(all_devices[device])
    return all_devices


def walk_through_connections(start_device: Device, end_device: Device, debug=""):
    if start_device.name == end_device.name:
        end_device.num_total = 1
        end_device.num_dac_paths = 1 if end_device.has_dac else 0
        end_device.num_both = 0
        end_device.num_fft_paths = 1 if end_device.has_fft else 0
        return

    start_device.num_total = 0
    start_device.num_dac_paths = 0
    start_device.num_fft_paths = 0
    start_device.num_both = 0

    for next_device in start_device.connected_to:
        if next_device.num_total is None:
            walk_through_connections(next_device, end_device, debug + " " + next_device.name)
        else:
            debug += f"... {next_device.name}"

        start_device.num_total += next_device.num_total
        if start_device.has_dac:
            start_device.num_dac_paths += next_device.num_total
            start_device.num_both += next_device.num_fft_paths
            start_device.num_fft_paths += next_device.num_fft_paths
        elif start_device.has_fft:
            start_device.num_dac_paths += next_device.num_dac_paths
            start_device.num_both += next_device.num_dac_paths
            start_device.num_fft_paths += next_device.num_total
        else:
            start_device.num_dac_paths += next_device.num_dac_paths
            start_device.num_both += next_device.num_both
            start_device.num_fft_paths += next_device.num_fft_paths



    return


if __name__ == "__main__":
    devices = parse_server_rack_connections(data)
    paths = set()

    # part 1
    walk_through_connections(devices["you"], devices["out"], "you")
    print(devices["you"].num_total)

    #part 2
    walk_through_connections(devices["svr"], devices["out"], "svr")
    print(devices["svr"].num_both)
