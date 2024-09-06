import numpy as np
from collections import defaultdict
import pickle


def esp32_log_to_rssi_data(in_filename, out_filename):
    with open(in_filename, "r") as f:
        log = f.read()

    # tally signals
    lines = log.split("\n")
    samples = []
    round_numbers = [0]
    macs = set()
    mac_to_name = {}
    signals = defaultdict(list)
    for line in lines[2:]:
        line = line.strip()
        if not line:
            continue
        if line.startswith("Round"):
            samples.append(signals)
            round_numbers.append(int(line.removeprefix("Round")))
            signals = defaultdict(list)
            continue
        name, signal, mac = line.rsplit(maxsplit=2)
        macs.add(mac)
        mac_to_name[mac] = name
        signals[mac].append(float(signal))
    if signals:
        samples.append(signals)

    # Convert rssi in array format
    macs = np.array(list(macs))
    rssi = np.zeros([len(samples), len(macs)])
    for i, r in enumerate(samples):
        for j, mac in enumerate(macs):
            if len(r[mac]) != 0:
                rssi[i, j] = sum(r[mac]) / len(r[mac])
            else:
                rssi[i, j] = -np.inf

    # Filter out uncommon AP
    valid_signal_count = np.sum(np.isfinite(rssi), axis=0)
    chosen_ap_count = sum(valid_signal_count > len(samples) * 0.4)
    chosen_aps = np.argsort(valid_signal_count)[-2:-chosen_ap_count:-1]
    rssi = rssi[..., chosen_aps]
    macs = macs[chosen_aps]

    # Mapping between round numbers and measurement locations
    location_data = {
        range(0, 3): (46.5625, 60.9375),
        range(7, 11): (23.75, 63.125),
        range(14, 21): (7.1875, 28.75),
        range(23, 32): (31.25, 32.1875),
        range(38, 43): (40.3125, 45.9375),
        range(46, 52): (65.9375, 26.875),
        range(54, 62): (79.375, 33.75),
        range(62, 73): (75.9375, 54.0625),
        range(78, 85): (53.125, 23.4375),
        range(90, 95): (53.125, 28.125),
        range(103, 111): (10.3125, 46.25),
    }

    # Average measurements from same location
    result = np.zeros([rssi.shape[1], len(location_data)])
    for loc_index, r in enumerate(location_data):
        rssi_rows = []
        for i in r:
            if i in round_numbers:
                row = rssi[round_numbers.index(i)]
                row[np.isinf(row)] = np.nan
                rssi_rows.append(row)
        avg_rssi = np.nanmean(rssi_rows, axis=0)
        avg_rssi[np.isnan(avg_rssi)] = -np.inf
        result[:, loc_index] = avg_rssi

    # Save result in pickle
    data = {
        "rssi": result,
        "ap": np.array([*location_data.values()]),
        "macs": macs,
        "names": [mac_to_name[m] for m in macs],
    }
    if out_filename:
        with open(out_filename, "wb") as g:
            pickle.dump(data, g)

    return data


if __name__ == "__main__":
    esp32_log_to_rssi_data("./output.txt", "./data/esp32_data.pickle")