import numpy as np
from typing import List

def calculate_nrci(bit_vector: np.ndarray, reference_vectors: List[np.ndarray]) -> float:
    """
    Calculate Non-Random Coherence Index (NRCI) between a bit vector and multiple reference vectors.
    NRCI is defined as the mean normalized dot-product (cosine similarity) between bit_vector and each reference.
    Returns a float NRCI score (typically close to 1 for high coherence).
    """
    scores = []
    for ref in reference_vectors:
        # Avoid division by zero
        norm_product = (np.linalg.norm(bit_vector) * np.linalg.norm(ref)) + 1e-12
        score = np.dot(bit_vector, ref) / norm_product
        scores.append(score)
    return float(np.mean(scores))

def validate_nrci(nrci: float, threshold: float = 0.999997) -> bool:
    """
    Validate if NRCI exceeds UBP threshold for coherence.
    Returns True if NRCI is above threshold, False otherwise.
    """
    return nrci > threshold

def batch_nrci(vectors: List[np.ndarray], reference_vectors: List[np.ndarray]) -> List[float]:
    """
    Batch NRCI calculation for a list of vectors against references.
    Returns a list of NRCI scores.
    """
    return [calculate_nrci(v, reference_vectors) for v in vectors]
