import numpy as np
from python.nrci import compute_nrci  # NRCI from your repo
from python.glr.base import glr_error  # GLR base error metric

class NoiseSignal:
    """
    UBP NoiseSignal: Handles generation, loading, and analysis of noise signals.
    Integrates NRCI and GLR metrics via your repo modules.
    """

    def __init__(self, data: np.ndarray, samplerate: float = 1.0, label: str = "unknown"):
        self.data = np.asarray(data)
        self.samplerate = samplerate
        self.label = label

    @classmethod
    def synthetic_thermal(cls, length, resistance=1.0, temperature=300.0, samplerate=1.0, rng=None):
        k = 1.380649e-23  # Boltzmann constant
        if rng is None:
            rng = np.random.default_rng()
        power = 4 * k * temperature * resistance * samplerate
        noise = rng.normal(0, np.sqrt(power), length)
        return cls(noise, samplerate=samplerate, label="Synthetic Thermal")

    def to_bitfield(self, threshold=None):
        if threshold is None:
            threshold = np.mean(self.data)
        return (self.data > threshold).astype(int)

    def toggle_rate(self):
        bits = self.to_bitfield()
        changes = np.sum(np.abs(np.diff(bits)))
        duration = len(bits) / self.samplerate
        return changes / duration if duration > 0 else 0

    def nrci(self, winlen=128, overlap=0.5):
        """Compute NRCI using your repo's NRCI module."""
        return compute_nrci(self.data, winlen=winlen, overlap=overlap)

    def glr(self):
        """Compute GLR error using your repo's GLR base module."""
        return glr_error(self.to_bitfield())
