import math
import json
import os
import pandas as pd
import numpy as np

class HexDictionary:
    """
    Universal Binary Principle Hexagonal Dictionary System
    Handles .hexubp files, binary toggles, resonance, spatial vectors, validation, etc.
    """

    def __init__(self, output_dir="hexubp_files",
                 words_path=None, zipf_path=None, freqs_path=None, pi_config_path=None):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        # Config paths, can be None for defaults
        self.words_path = words_path
        self.zipf_path = zipf_path
        self.freqs_path = freqs_path
        self.pi_config_path = pi_config_path
        self.base_freq = None
        # Data dictionaries
        self.words = set()
        self.zipf_dict = {}
        self.freqs = []
        self.load_config()
        self.load_existing_words()

    def load_config(self):
        # Load UBP Pi constant
        self.base_freq = None
        if self.pi_config_path and os.path.exists(self.pi_config_path):
            with open(self.pi_config_path, 'r') as f:
                self.base_freq = float(f.read().strip())
        if self.base_freq is None:
            self.base_freq = self.calc_ubp_pi()
        # Load words
        if self.words_path and os.path.exists(self.words_path):
            with open(self.words_path, 'r') as f:
                self.config_words = [line.strip() for line in f if line.strip()]
        else:
            self.config_words = ["and", "the", "is", "to", "of"]
        # Load zipf
        if self.zipf_path and os.path.exists(self.zipf_path):
            zipf_map = pd.read_csv(self.zipf_path)
            self.zipf_dict = dict(zip(zipf_map['word'], zipf_map['index']))
        else:
            self.zipf_dict = {"the": 1, "and": 2, "is": 3, "to": 4, "of": 5}
        # Load freqs
        if self.freqs_path and os.path.exists(self.freqs_path):
            with open(self.freqs_path, 'r') as f:
                self.freqs = [float(line.strip()) for line in f if line.strip()]
        else:
            self.freqs = [7.83, 14.134725, 21.022040]

    def calc_ubp_pi(self):
        tc_td = 6 / 2
        p_gci = math.cos(2 * math.pi * 7.83 * 0.318309886)
        return tc_td * p_gci  # ~2.427

    def resonance_freq(self, word):
        freq = 7.83 if word == "and" else self.base_freq + (hash(word) % 5)
        phase = 0.1 if word == "and" else (hash(word) % 10) / 100
        return [freq, phase]

    def toggle_vector(self, binary):
        binary = binary.ljust(6, "0")
        return [int(b) for b in binary]

    def spatial_vector(self, word, binary):
        base = [85, 85, 85, 2.5, 1, 1]
        toggle_sum = sum(int(b) for b in binary.ljust(6, "0"))
        freq = self.resonance_freq(word)[0]
        x = base[0] + toggle_sum
        y = base[1] - toggle_sum
        z = base[2] + (freq - self.base_freq)
        t = base[3] + (hash(word) % 10) / 10
        p = self.resonance_freq(word)[1]
        q = base[5]
        return [x, y, z, t, p, q]

    def glr_validate(self, vertex, distance=1.0, bin_width=0.078):
        if vertex["type"] == "binary":
            if sum(vertex["value"]) > 6:
                return "Warning: Binary toggle count excessive"
        elif vertex["type"] == "freq":
            freq = vertex["value"][0]
            if abs(freq - 7.83) >= bin_width:
                return f"Warning: Frequency drift {freq} Hz"
        elif vertex["type"] == "spatial":
            center = [85, 85, 85, 2.5, 1, 1]
            dist = sum((x - c) ** 2 for x, c in zip(vertex["value"], center)) ** 0.5
            if dist > distance:
                return f"Warning: Spatial drift {dist}"
        return "Valid"

    def create_hexubp(self, word="and", binary=None, definition=""):
        if not binary:
            binary = "001011" if word == "and" else "000000"
        hex_data = {
            "center": word,
            "definition": definition,
            "vertices": [
                {"id": 1, "type": "binary", "value": self.toggle_vector(binary)},
                {"id": 2, "type": "qr", "value": f"3x3_hex_{sum(int(b) for b in binary)}lit"},
                {"id": 3, "type": "fib_zipf", "value": self.zipf_dict.get(word, hash(word) % 10)},
                {"id": 4, "type": "spatial", "value": self.spatial_vector(word, binary)},
                {"id": 5, "type": "freq", "value": self.resonance_freq(word)},
                {"id": 6, "type": "glr", "value": "validated"},
                {"id": 7, "type": "tgic", "value": "AND" if word == "and" else "NONE"},
                {"id": 8, "type": "cultural", "value": [0.2, 0.0]},
                {"id": 9, "type": "bittime", "value": [0.318309886, 0.0]},
                {"id": 10, "type": "harmonic", "value": [3, 0.0]},
                {"id": 11, "type": "waveform", "value": ["sine", 0.0]},
                {"id": 12, "type": "amplitude", "value": [0.5, 0.0]}
            ]
        }
        hex_data["validation"] = [self.glr_validate(v) for v in hex_data["vertices"]]
        return hex_data

    def save_hexubp(self, word, binary=None, definition=""):
        hex_data = self.create_hexubp(word, binary, definition)
        file_path = os.path.join(self.output_dir, f"{word}.hexubp")
        with open(file_path, "w") as f:
            json.dump(hex_data, f, indent=2)
        self.words.add(word)
        return file_path

    def load_existing_words(self):
        if os.path.exists(self.output_dir):
            for file in os.listdir(self.output_dir):
                if file.endswith(".hexubp"):
                    self.words.add(file[:-7])

    def add_word(self, word, binary=None, definition=""):
        word = word.lower().strip()
        if binary:
            if not all(bit in '01' for bit in binary):
                return "Error: Binary must contain only 0s and 1s"
            binary = binary.ljust(6, '0')[:6]
        else:
            binary = "001011" if word == "and" else "000000"
        self.save_hexubp(word, binary, definition)
        return f"Added word '{word}' with binary {binary}"

    def edit_word(self, word, new_binary=None, new_definition=None, new_word=None):
        word = word.lower().strip()
        if word not in self.words:
            return f"Error: Word '{word}' not found"
        if new_word:
            new_word = new_word.lower().strip()
        else:
            new_word = word
        binary = new_binary if new_binary else "001011" if new_word == "and" else "000000"
        self.save_hexubp(new_word, binary, new_definition or "")
        if new_word != word:
            old_path = os.path.join(self.output_dir, f"{word}.hexubp")
            if os.path.exists(old_path):
                os.remove(old_path)
            self.words.remove(word)
        self.words.add(new_word)
        return f"Updated word '{word}' to '{new_word}' with binary {binary}"

    def delete_word(self, word):
        word = word.lower().strip()
        if word not in self.words:
            return f"Error: Word '{word}' not found"
        file_path = os.path.join(self.output_dir, f"{word}.hexubp")
        if os.path.exists(file_path):
            os.remove(file_path)
        self.words.remove(word)
        return f"Deleted word '{word}'"

    def read_word(self, word):
        word = word.lower().strip()
        file_path = os.path.join(self.output_dir, f"{word}.hexubp")
        if not os.path.exists(file_path):
            return f"Error: Word '{word}' not found"
        with open(file_path, "r") as f:
            return json.load(f)

    def list_words(self):
        return sorted(list(self.words))

    def get_word_count(self):
        return len(self.words)

    def search_words(self, query):
        query = query.lower().strip()
        return [word for word in self.words if query in word]

    def export_dictionary(self, file_path="dictionary_export.csv"):
        data = []
        for word in self.list_words():
            hex_data = self.read_word(word)
            if isinstance(hex_data, str):
                continue
            binary_vertex = next(v for v in hex_data["vertices"] if v["type"] == "binary")
            binary_value = ''.join(str(b) for b in binary_vertex["value"])
            freq_vertex = next(v for v in hex_data["vertices"] if v["type"] == "freq")
            freq = freq_vertex["value"][0]
            phase = freq_vertex["value"][1]
            definition = hex_data.get("definition", "")
            data.append({
                'word': word,
                'binary': binary_value,
                'frequency': freq,
                'phase': phase,
                'definition': definition
            })
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
        return f"Exported {len(data)} words to {file_path}"

    def import_dictionary(self, file_path):
        try:
            df = pd.read_csv(file_path)
            imported_count = 0
            for _, row in df.iterrows():
                word = row['word']
                binary = row['binary'] if 'binary' in df.columns else None
                definition = row['definition'] if 'definition' in df.columns else ""
                if word not in self.words:
                    self.add_word(word, binary, definition)
                    imported_count += 1
            return f"Imported {imported_count} new words from {file_path}"
        except Exception as e:
            return f"Error importing dictionary: {str(e)}"

    def get_dictionary_stats(self):
        words = self.list_words()
        if not words:
            return "Dictionary is empty"
        frequencies = []
        toggle_counts = []
        word_lengths = []
        has_definition = 0
        for word in words:
            hex_data = self.read_word(word)
            if isinstance(hex_data, str):
                continue
            binary_vertex = next(v for v in hex_data["vertices"] if v["type"] == "binary")
            binary_value = binary_vertex["value"]
            toggle_counts.append(sum(binary_value))
            freq_vertex = next(v for v in hex_data["vertices"] if v["type"] == "freq")
            freq_value = freq_vertex["value"]
            frequencies.append(freq_value[0])
            word_lengths.append(len(word))
            if hex_data.get("definition", ""):
                has_definition += 1
        stats = {
            "total_words": len(words),
            "avg_frequency": np.mean(frequencies) if frequencies else 0,
            "avg_toggle_count": np.mean(toggle_counts) if toggle_counts else 0,
            "avg_word_length": np.mean(word_lengths) if word_lengths else 0,
            "words_with_definition": has_definition,
            "definition_percentage": (has_definition / len(words) * 100) if words else 0
        }
        return stats
