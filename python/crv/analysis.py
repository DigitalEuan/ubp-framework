import numpy as np

def realm_distribution(catalog):
    """
    Returns a count of nodes per realm.
    """
    from collections import Counter
    realms = [node.realm for node in catalog]
    return Counter(realms)

def known_vs_new_constants(catalog):
    """
    Returns the counts and lists of known vs new constants.
    """
    known = [node for node in catalog if node.known_constant]
    new = [node for node in catalog if not node.known_constant]
    return {
        "known_count": len(known),
        "new_count": len(new),
        "known_constants": [node.crv_name for node in known],
        "new_constants": [node.crv_name for node in new]
    }

def frequency_stats(catalog):
    """
    Returns min, max, mean frequency stats for catalog.
    """
    freqs = np.array([node.frequency for node in catalog])
    return {
        "min_frequency": float(np.min(freqs)),
        "max_frequency": float(np.max(freqs)),
        "mean_frequency": float(np.mean(freqs))
    }

def crv_statistics(catalog):
    """
    Returns min, max, mean CRV value stats.
    """
    crvs = np.array([node.crv_value for node in catalog])
    return {
        "min_crv": float(np.min(crvs)),
        "max_crv": float(np.max(crvs)),
        "mean_crv": float(np.mean(crvs))
    }
