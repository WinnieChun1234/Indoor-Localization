import numpy as np
import pickle
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial


def distance_estimate(rssi):
    # return 10 ** ((-rssi - 13.5) / 30)
    return Polynomial([-7.63, -0.782, -0.0111, -1.17e-4])(rssi)


def trilateration(dist: np.ndarray, ap: np.ndarray) -> np.ndarray:
    ap_x = ap[:, 0]
    ap_y = ap[:, 1]
    d_x = ap_x - np.mean(ap_x)
    d_xx = ap_x**2 - np.mean(ap_x**2)
    d_y = ap_y - np.mean(ap_y)
    d_yy = ap_y**2 - np.mean(ap_y**2)
    dd = dist**2
    dd[~np.isfinite(dd)] = np.nan
    d_dd = dist**2 - np.nanmean(dd, axis=-1, keepdims=True)

    A = np.array([d_x, d_y]).T
    b = 0.5 * (d_xx + d_yy - d_dd).T
    A_inv = np.linalg.pinv(A)
    result = (A_inv @ b).T
    return result


def localization(rssi: np.ndarray, ap: np.ndarray):
    dist = distance_estimate(rssi)
    locations = np.zeros([rssi.shape[0], 2])
    for i in range(rssi.shape[0]):
        d = dist[i]
        valid_index = np.isfinite(d)
        locations[i] = trilateration(d[valid_index], ap[valid_index])
    return locations


def load_data(input_filename):
    with open(input_filename, "rb") as f:
        data: dict = pickle.load(f)
    ap: np.ndarray = data.get("ap")
    rssi: np.ndarray = data.get("rssi")
    macs: np.ndarray = data.get("macs")
    names: np.ndarray = data.get("names")
    return rssi, ap, macs, names


def test_localization():
    rssi, ap, macs, names = load_data("./data/esp32_data.pickle")
    results = localization(rssi, ap)

    ax = plt.subplot()
    ax.set_aspect("equal")
    img = plt.imread("./chi_wah_map.jpg")
    ax.imshow(img, extent=[0, 90, 81.25, 0])
    ax.scatter(ap[:, 0], ap[:, 1])
    ax.scatter(results[:, 0], results[:, 1])
    for i, t in enumerate(macs):
        ax.text(results[i, 0], results[i, 1], t)
    ax.legend(["esp32 locations", "estimated AP locations"])

    # print MAC, SSID, estimated location
    print([*zip(macs, names, results[:, 0], results[:, 1])])

    plt.show()


if __name__ == "__main__":
    test_localization()
