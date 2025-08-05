import numpy as np
from typing import Optional, List
from .monad_config import MonadConfig
from .tgic_engine import TGICEngine

class BitfieldMonad:
    """
    UBP Bitfield Monad: 24-bit computational unit supporting TGIC operations.
    """
    def __init__(self, config: Optional[MonadConfig] = None):
        self.config = config or MonadConfig()
        self.offbit = np.zeros(self.config.bits, dtype=int)
        self.axes = {
            'x': slice(0, 8),
            'y': slice(8, 16),
            'z': slice(16, 24)
        }
        self.faces = {
            'px': 'AND', 'nx': 'AND',
            'py': 'XOR', 'ny': 'XOR',
            'pz': 'OR',  'nz': 'OR'
        }
        self.tgic_engine = TGICEngine(self)

    def calculate_energy(self) -> float:
        """E = M × C × R × P_GCI"""
        M = 1
        C = self.config.freq
        R = 0.9
        P_GCI = np.cos(2 * np.pi * self.config.freq * 0.318309886)
        return M * C * R * P_GCI

    def calculate_resonance(self, time: float) -> float:
        """Resonance operation across axes"""
        exp_decay = np.exp(-0.0002 * (time * self.config.freq) ** 2)
        return self.offbit.sum() * exp_decay

    def apply_face_operations(self):
        """Apply 6-face logical operations: AND, XOR, OR."""
        x_bits = self.offbit[self.axes['x']]
        y_bits = self.offbit[self.axes['y']]
        z_bits = self.offbit[self.axes['z']]
        # AND for ±X faces
        self.offbit[self.axes['x']] = np.bitwise_and(x_bits, y_bits)
        # XOR for ±Y faces
        self.offbit[self.axes['y']] = np.bitwise_xor(y_bits, z_bits)
        # OR for ±Z faces
        self.offbit[self.axes['z']] = np.bitwise_or(z_bits, x_bits)

    def get_state_vector(self) -> np.ndarray:
        return self.offbit.copy()

    def get_state_string(self) -> str:
        return ''.join(str(b) for b in self.offbit)

    def step(self, time: float):
        """Single simulation step combining TGIC + face operations."""
        self.tgic_engine.execute_step(time)
        self.apply_face_operations()
