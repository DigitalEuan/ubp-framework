import numpy as np
from python.monad_config import MonadConfig
from python.bitfield_monad import BitfieldMonad

def test_monad_initialization():
    monad = BitfieldMonad()
    assert monad.offbit.shape == (24,)
    assert monad.get_state_string() == '0'*24

def test_monad_energy():
    config = MonadConfig(freq=3.14159)
    monad = BitfieldMonad(config)
    energy = monad.calculate_energy()
    assert isinstance(energy, float)
    assert abs(energy) > 0

def test_monad_step_and_face_ops():
    monad = BitfieldMonad()
    # Set some bits for nonzero state
    monad.offbit[0:8] = 1
    monad.offbit[8:16] = 0
    monad.offbit[16:24] = 1
    state_before = monad.get_state_string()
    monad.step(time=1e-12)
    state_after = monad.get_state_string()
    assert state_before != state_after  # State changes after TGIC + faces

def test_tgic_interaction_probabilities():
    from python.tgic_engine import TGICEngine
    monad = BitfieldMonad()
    engine = TGICEngine(monad)
    # Run many steps to see distribution
    interactions = [engine.select_interaction() for _ in range(1000)]
    assert set(interactions) <= set(engine.interactions)
