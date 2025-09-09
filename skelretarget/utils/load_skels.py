import numpy as np


def load_csv_skels(fpath):
    data = np.loadtxt(fpath, delimiter=",", skiprows=1)
    n_cols = data.shape[1]
    assert n_cols % 3 == 0, "Number of columns must be divisible by 3"
    n_joints = n_cols // 3
    return data.reshape(-1, n_joints, 3)
