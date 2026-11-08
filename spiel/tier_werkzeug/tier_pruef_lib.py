import numpy as np


def skin(M, off, V):
    h = np.c_[V[:, :3], np.ones(len(V))]
    out = np.zeros((len(V), 3))
    for k in range(4):
        w = V[:, 3 + k]
        b = V[:, 7 + k].astype(int)
        S = np.einsum("nij,njk->nik", M[b], off[b])
        out += w[:, None] * np.einsum("nij,nj->ni", S, h)[:, :3]
    return out


def kanten(el):
    T = el.reshape(-1, 3)
    E = np.concatenate((T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]), 0)
    E.sort(1)
    return np.unique(E, axis=0)


