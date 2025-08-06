import numpy as np

def make_golay_matrix():
    """
    Generate a stub Golay (23,12) generator matrix.
    Replace with the true Golay matrix for production use.
    """
    return np.eye(23, 12, dtype=int)

def syndrome_decode(received: np.ndarray, parity_matrix: np.ndarray) -> np.ndarray:
    """
    Syndrome decoding for error correction.
    Currently a stub. Replace with production syndrome decoding.
    """
    syndrome = np.dot(parity_matrix, received) % 2
    # TODO: Real pattern matching for syndrome
    return syndrome

def validate_nrcis(vectors, threshold=0.999997):
    """
    Check that NRCI scores meet threshold.
    Returns list of vectors passing threshold.
    """
    valid = []
    for v in vectors:
        nrci = np.mean(v)
        if nrci > threshold:
            valid.append(v)
    return valid
