# utils.py

import numpy as np

def filter_levels(levels, price_series, threshold=2, tolerance=1.0):
    filtered = []
    for level in levels:
        touches = np.sum(np.abs(price_series - level) <= tolerance)
        if touches >= threshold:
            filtered.append(round(float(level), 2))
    return sorted(filtered)
