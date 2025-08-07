import numpy as np
from glr_core import GLRErrorCorrector

class TelecomProcessor:
    def __init__(self):
        self.glr = GLRErrorCorrector()
        # 5G NR parameters
        self.subcarrier_spacing = 15e3  # 15 kHz
        self.max_bw = 400e6  # 400 MHz
        self.max_scs = 3300  # Maximum subcarriers
        
    def process_5g_signal(self, iq_samples):
        """Process 5G NR signal with UBP error correction"""
        # Convert IQ samples to binary format
        binary_data = self._iq_to_binary(iq_samples)
        
        # Step 1: Apply GLR error correction
        corrected_samples = self.glr.process_data({
            'data': binary_data,
            'observed_freqs': self._estimate_frequencies(iq_samples),
            'target_freqs': self._get_target_frequencies(),
            'nrcis': self._calculate_nrcis(iq_samples)
        })
        
        return corrected_samples
        
    def _estimate_frequencies(self, iq_samples):
        """Estimate frequencies from IQ samples"""
        # Convert to numpy array
        iq_array = np.array(iq_samples)
        
        # Perform FFT to get frequency components
        fft_result = np.fft.fft(iq_array)
        freqs = np.fft.fftfreq(len(iq_array), d=1/self.subcarrier_spacing)
        
        # Get dominant frequencies
        dominant_freqs = []
        for i in range(min(3, len(freqs))):  # Get top 3 frequencies
            idx = np.argmax(np.abs(fft_result))
            dominant_freqs.append(freqs[idx])
            fft_result[idx] = 0  # Remove this frequency for next iteration
            
        return dominant_freqs
        
    def _get_target_frequencies(self):
        """Get target frequencies based on 5G NR configuration"""
        # For initial implementation, use center frequency and ±1 subcarrier
        center_freq = 0  # Baseband center
        return [
            center_freq - self.subcarrier_spacing,
            center_freq,
            center_freq + self.subcarrier_spacing
        ]
        
    def _iq_to_binary(self, iq_samples):
        """Convert IQ samples to 12-bit binary format"""
        # Convert to numpy array
        iq_array = np.array(iq_samples)
        
        # Get magnitude and phase
        magnitudes = np.abs(iq_array)
        phases = np.angle(iq_array)
        
        # Normalize and quantize to 12 bits (4 bits magnitude + 8 bits phase)
        mag_bits = np.round(magnitudes/np.max(magnitudes) * 15).astype(int)
        phase_bits = np.round((phases + np.pi)/(2*np.pi) * 255).astype(int)
        
        # Combine into 12-bit chunks (4 + 8)
        binary_data = []
        for m, p in zip(mag_bits[:12], phase_bits[:12]):
            binary_data.extend([int(b) for b in format(m, '04b')])
            binary_data.extend([int(b) for b in format(p, '08b')][:8])
        
        return binary_data[:12]  # Return first 12 bits for Golay encoding

    def _calculate_nrcis(self, iq_samples):
        """Calculate NRCI values for frequency correction"""
        # Calculate signal quality metrics
        iq_array = np.array(iq_samples)
        signal_power = np.mean(np.abs(iq_array)**2)
        noise_power = np.var(iq_array - np.mean(iq_array))
        
        # Simple NRCI calculation (will be enhanced with UBP-specific metrics)
        snr = 10 * np.log10(signal_power/noise_power) if noise_power > 0 else 30
        nrcis = [
            min(1.0, max(0.7, snr/30)),  # Lower frequency
            min(1.0, max(0.9, snr/20)),  # Center frequency
            min(1.0, max(0.7, snr/30))   # Higher frequency
        ]
        
        return nrcis