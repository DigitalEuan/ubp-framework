import numpy as np

def coherence_analysis(signal, winlen=128, overlap=0.5):
    """Returns NRCI and mean coherence using NRCI module."""
    from python.nrci import compute_nrci
    nrci_val, coherence_matrix = compute_nrci(signal, winlen=winlen, overlap=overlap)
    mean_coherence = np.mean(coherence_matrix)
    return nrci_val, mean_coherence

def glr_analysis(bitfield):
    """Returns GLR error using GLR module."""
    from python.glr.base import glr_error
    return glr_error(bitfield)
