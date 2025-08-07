# GLR Telecom SDK Usage Examples

## Basic Usage

```python
from telecom_core import TelecomProcessor
import numpy as np

# Create test signal
t = np.linspace(0, 1, 1000)
carrier_freq = 15e3  # 15 kHz
iq_samples = np.exp(1j * 2 * np.pi * carrier_freq * t)

# Add noise
noise = 0.1 * (np.random.randn(1000) + 1j * np.random.randn(1000))
noisy_samples = iq_samples + noise

# Process signal
processor = TelecomProcessor()
result = processor.process_5g_signal(noisy_samples)

print("Processed signal:", result)
```

## Error Correction Example

```python
from glr_core import GLRErrorCorrector

# Initialize corrector
glr = GLRErrorCorrector()

# Encode data
data = [1,0,1,0,1,0,1,0,1,0,1,0]
encoded = glr.golay_encode(data)

# Introduce errors
encoded[2] = 1 - encoded[2]  # Flip one bit

# Decode with error correction
decoded = glr.golay_decode(encoded)

print("Original data:", data)
print("Decoded data:", decoded)
```