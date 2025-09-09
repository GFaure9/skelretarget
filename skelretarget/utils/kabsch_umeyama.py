import numpy as np


# The following code is an adapted version of https://github.com/clementinboittiaux/umeyama-python to
# allow for applying it on a batch to take advantage of numpy matrix computation parallelism.
# The formalism of Kabsch-Umeyama algorithm can be found at: https://en.wikipedia.org/wiki/Kabsch_algorithm.
# See an example of usage at: tests/

def batch_kabsch_umeyama(x: np.ndarray, y: np.ndarray) -> tuple:
    # x shape=(B, Npts, 3) [source]
    # y shape=(B, Npts, 3) [target]
    #
    # returns (c, R, t) with c of shape (B, 1, 1), R of shape (B, 3, 3) and t of shape (c, 3, 1), such that:
    #
    #                                   y[i] ~ (c[i] * (R[i] @ x[i].T) + t[i]).T
    mu_x = x.mean(axis=1, keepdims=True)  # shape=(B, 1, 3)
    mu_y = y.mean(axis=1, keepdims=True)  # shape=(B, 1, 3)
    var_x = np.square(x - mu_x).sum(axis=-1, keepdims=True).mean(axis=1, keepdims=True)  # shape=(B, 1, 1)
    cov_xy = ((y - mu_y).transpose(0, 2, 1) @ (x - mu_x)) / x.shape[1]  # shape=(B, 3, 3)
    U, D, VH = np.linalg.svd(cov_xy)  # U shape=(B, 3, 3) | D shape=(B, 3) | VH shape=(B, 3, 3)
    S = np.tile(np.eye(3), (cov_xy.shape[0], 1, 1))  # shape=(B, 3, 3)
    detU = np.linalg.det(U)  # (B,)
    detVH = np.linalg.det(VH)  # (B,)
    mask = (detU * detVH) < 0  # (B,)
    S[mask, -1, -1] = -1
    Dmat = np.zeros_like(S)
    Dmat[:, np.arange(3), np.arange(3)] = D  # shape=(B, 3, 3)
    c = np.trace(Dmat @ S, axis1=1, axis2=2)[:, None, None] / var_x  # shape=(B, 1, 1)
    R = U @ S @ VH  # shape=(B, 3, 3)
    t = mu_y.transpose(0, 2, 1) - c * R @ mu_x.transpose(0, 2, 1)  # shape=(B, 3, 1)
    return c, R, t
