from telecom_core import TelecomProcessor
import numpy as np

def test_telecom():
    # Initialize processor
    processor = TelecomProcessor()
    
    # Create test signal (complex IQ samples)
    t = np.linspace(0, 1, 1000)
    carrier_freq = 15e3  # 15 kHz
    iq_samples = np.exp(1j * 2 * np.pi * carrier_freq * t)
    
    # Add some noise
    noise = 0.1 * (np.random.randn(1000) + 1j * np.random.randn(1000))
    noisy_samples = iq_samples + noise
    
    # Process signal
    corrected_samples = processor.process_5g_signal(noisy_samples)
    
    # Print results
    print("Original Signal Power:", np.mean(np.abs(noisy_samples)**2))
    print("Corrected Signal Power:", np.mean(np.abs(corrected_samples)**2))

if __name__ == "__main__":
    test_telecom()