from dataclasses import dataclass
from typing import List

@dataclass
class MonadConfig:
    dims: List[int] = None         # Bitfield dimensions
    bits: int = 24                 # OffBit size
    steps: int = 100               # Simulation steps
    bit_time: float = 1e-12        # Time resolution (seconds)
    freq: float = 3.14159          # Pi Resonance frequency (Hz)
    coherence: float = 0.9999878   # NRCI coherence factor
    layer: str = "all"             # Processing layer

    def __post_init__(self):
        if self.dims is None:
            self.dims = [1, 1, 1, 1, 1, 1]
