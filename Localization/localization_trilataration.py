import numpy as np
import pickle
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial


def distance_estimate(rssi):
    ### Approach 1: log function ###
    # return 10 ** ((-rssi - 13.5) / 30)

    ### Approach 2: polynomial fit ###
    return Polynomial([-7.63, -0.782, -0.0111, -1.17e-4])(rssi)


def trilateration(dist: np.ndarray, ap: np.ndarray) -> np.ndarray:
    ap_x = ap[:, 0]
    ap_y = ap[:, 1]
    d_x = ap_x - np.mean(ap_x)
    d_xx = ap_x ** 2 - np.mean(ap_x ** 2)
    d_y = ap_y - np.mean(ap_y)
    d_yy = ap_y ** 2 - np.mean(ap_y ** 2)
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
    if len(ap.shape) > 2:
        ap = ap.mean(axis=1)
    labels: np.ndarray = data.get("labels")
    rssi: np.ndarray = data.get("rssi")
    return rssi, labels, ap


def test_localization():
    rssi, labels, ap = load_data("./data/data_env1.pickle")
    results = localization(rssi, ap)
    
    rssi2, labels2, ap2 = load_data("./data/data_env2.pickle")
    results2 = localization(rssi2, ap2)
    
    ax = plt.subplot()
    ax.set_aspect("equal")
    ax.scatter(ap[:, 0], ap[:, 1])
    ax.scatter(labels[:, 0], labels[:, 1])
    ax.scatter(results[:, 0], results[:, 1])
    plt.legend(["AP", "True", "Estimated"])
    plt.show()

    error = np.linalg.norm(results - labels, axis=1)
    error = error[np.isfinite(error)]
    print("mean error of env1", np.mean(error))
    print("median error of env1", np.median(error))

    error2 = np.linalg.norm(results2 - labels2, axis=1)
    error2 = error2[np.isfinite(error2)]
    print("mean error of env2", np.mean(error2))
    print("median error of env2", np.median(error2))

    plt.plot(sorted(error), np.linspace(0, 1, len(error)))
    plt.plot(sorted(error2), np.linspace(0, 1, len(error2)))
    plt.xlabel("Error")
    plt.ylabel("CDF")
    plt.title("CDF of error")
    plt.legend(["env1", "env2"])
    plt.show()


if __name__ == "__main__":
    test_localization()
