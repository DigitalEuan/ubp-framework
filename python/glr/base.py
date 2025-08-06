from abc import ABC, abstractmethod
import numpy as np
from typing import List, Tuple

class GLRCorrectorBase(ABC):
    """
    Abstract base class for all Golay-Leech Resonance (GLR) error correction modules.
    Each realm-specific GLR corrector must implement these methods.
    """

    @abstractmethod
    def encode(self, data: np.ndarray) -> np.ndarray:
        """Encode data using the realm-specific GLR code."""
        pass

    @abstractmethod
    def decode(self, received: np.ndarray) -> Tuple[np.ndarray, int]:
        """Decode received codeword and return corrected data and number of errors corrected."""
        pass

    @abstractmethod
    def nrci(self, bit_vector: np.ndarray, reference_vectors: List[np.ndarray]) -> float:
        """Calculate Non-Random Coherence Index for a bit vector against reference vectors."""
        pass

    @abstractmethod
    def correct_frequency(self, frequencies: List[float], nrcis: List[float]) -> dict:
        """Apply frequency correction using NRCI-weighted error minimization."""
        pass
