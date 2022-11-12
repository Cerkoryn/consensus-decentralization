import numpy as np


def compute_gini(x):
    mad = np.abs(np.subtract.outer(x, x)).mean()
    rmad = mad/np.mean(x)
    return 0.5 * rmad


def compute_nc(blocks_per_pool):
    nc = [0, 0]
    for (name, blocks) in sorted(blocks_per_pool.items(), key=lambda x: x[1], reverse=True):
        if nc[1] < 50:
            nc[0] += 1
            nc[1] += 100 * blocks / sum([i[1] for i in blocks_per_pool.items()])
        else:
            return nc
