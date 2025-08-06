import numpy as np

class NoiseSignal:
    """
    Core class for representing and processing noise signals in UBP framework.
    Includes methods for generating, loading, and analyzing signals.
    """

    def __init__(self, data: np.ndarray, samplerate: float = 1.0, label: str = "unknown"):
        self.data = np.asarray(data)
        self.samplerate = samplerate
        self.label = label

    @classmethod
    def from_csv(cls, path, samplerate=1.0, column=0):
        arr = np.loadtxt(path, delimiter=",", usecols=column)
        return cls(arr, samplerate=samplerate, label=path)

    @classmethod
    def synthetic_thermal(cls, length, resistance=1.0, temperature=300.0, samplerate=1.0, rng=None):
        """
        Simulate Johnson-Nyquist thermal noise (Gaussian, zero mean).
        """
        k = 1.380649e-23  # Boltzmann constant
        if rng is None:
            rng = np.random.default_rng()
        power = 4 * k * temperature * resistance * samplerate
        noise = rng.normal(0, np.sqrt(power), length)
        return cls(noise, samplerate=samplerate, label="Synthetic Thermal")

    @classmethod
    def synthetic_white(cls, length, std=1.0, samplerate=1.0, rng=None):
        """
        Generate white Gaussian noise.
        """
        if rng is None:
            rng = np.random.default_rng()
        noise = rng.normal(0, std, length)
        return cls(noise, samplerate=samplerate, label="Synthetic White")

    @classmethod
    def synthetic_pink(cls, length, samplerate=1.0, rng=None):
        """
        Generate pink (1/f) noise using Voss-McCartney algorithm.
        """
        if rng is None:
            rng = np.random.default_rng()
        n = length
        ncols = int(np.ceil(np.log2(n)))
        array = rng.normal(size=(ncols, n))
        pink = np.sum(array, axis=0)
        pink = (pink - np.mean(pink)) / np.std(pink)
        return cls(pink, samplerate=samplerate, label="Synthetic Pink")

    def to_bitfield(self, threshold=None):
        """
        Discretize signal to binary bitfield using threshold.
        Default: mean of data.
        """
        if threshold is None:
            threshold = np.mean(self.data)
        return (self.data > threshold).astype(int)

    def toggle_rate(self):
        """
        Compute toggle rate (number of state changes per unit time).
        """
        bits = self.to_bitfield()
        changes = np.sum(np.abs(np.diff(bits)))
        duration = len(bits) / self.samplerate
        return changes / duration if duration > 0 else 0

    def window_segments(self, winlen=128, overlap=0.5):
        """
        Segment signal into overlapping windows.
        Returns array of shape (num_windows, winlen).
        """
        step = int(winlen * (1 - overlap))
        win_starts = np.arange(0, len(self.data) - winlen + 1, step)
        return np.array([self.data[s:s+winlen] for s in win_starts])

    def get_segment(self, idx, winlen=128, overlap=0.5):
        segs = self.window_segments(winlen, overlap)
        return segs[idx] if 0 <= idx < len(segs) else None
