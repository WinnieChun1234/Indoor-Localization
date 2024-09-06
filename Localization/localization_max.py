import numpy as np
import pickle
import matplotlib.pyplot as plt


def localization(rssi: np.ndarray, ap: np.ndarray):
    return ap[np.argmax(rssi, axis=1)]

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