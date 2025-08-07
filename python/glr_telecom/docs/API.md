# GLR Telecom SDK API Reference

## GLRErrorCorrector Class

### Methods

#### `golay_encode(data)`
Encodes 12-bit data into 24-bit Golay code.

**Parameters:**
- `data`: List of 12 bits (0s and 1s)

**Returns:**
- List of 24 encoded bits

#### `golay_decode(code)`
Decodes 24-bit Golay code with error correction.

**Parameters:**
- `code`: List of 24 bits (0s and 1s)

**Returns:**
- List of 12 decoded bits

#### `find_leech_neighbors(vector)`
Finds neighbors in Leech lattice.

**Parameters:**
- `vector`: 24-dimensional vector

**Returns:**
- List of neighbor vectors

#### `correct_frequencies(observed_freqs, target_freqs, nrcis)`
Corrects frequencies using NRCI-weighted sums.

**Parameters:**
- `observed_freqs`: List of observed frequencies
- `target_freqs`: List of target frequencies
- `nrcis`: List of NRCI values

**Returns:**
- List of corrected frequencies

## TelecomProcessor Class

### Methods

#### `process_5g_signal(iq_samples)`
Processes 5G NR signal with UBP error correction.

**Parameters:**
- `iq_samples`: List of complex IQ samples

**Returns:**
- Dictionary containing processed signal data