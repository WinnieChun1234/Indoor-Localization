import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


def get_ml_data(env_n, labels, test_only=False):
    env = pd.read_csv(f"data/env{env_n}.csv")

    env = env.replace([np.inf, -np.inf], np.nan)
    env = env.dropna()

    X = env[
        [
            "AP_1_RSSI",
            "AP_2_RSSI",
            "AP_3_RSSI",
            "AP_4_RSSI",
            "AP_5_RSSI",
            "AP_6_RSSI",
            "AP_1_LOC_X",
            "AP_1_LOC_Y",
            "AP_2_LOC_X",
            "AP_2_LOC_Y",
            "AP_3_LOC_X",
            "AP_3_LOC_Y",
            "AP_4_LOC_X",
            "AP_4_LOC_Y",
            "AP_5_LOC_X",
            "AP_5_LOC_Y",
            "AP_6_LOC_X",
            "AP_6_LOC_Y",
        ]
    ]
    y = env[labels]

    if test_only:
        return X, y
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    if len(labels) == 1:
        y_train = y_train.values.ravel()
        y_test = y_test.values.ravel()
    return X_train, X_test, y_train, y_test


def get_ml_data_all_env(labels, test_only=False):
    X_train_1, X_test_1, y_train_1, y_test_1 = get_ml_data(1, labels, test_only)
    X_train_2, X_test_2, y_train_2, y_test_2 = get_ml_data(2, labels, test_only)

    X_train = pd.concat([X_train_1, X_train_2])
    X_test = pd.concat([X_test_1, X_test_2])
    y_train = np.concatenate([y_train_1, y_train_2])
    y_test = np.concatenate([y_test_1, y_test_2])

    return X_train, X_test, y_train, y_test
