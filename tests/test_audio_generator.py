"""
Tests para audio_generator.py
"""

import pytest
import os
import sys
import tempfile
import numpy as np

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from modules.audio_generator import AudioGenerator


class TestAudioGenerator:
    """Suite de tests para AudioGenerator"""
    
    @pytest.fixture
    def generator(self):
        """Crear instancia del generador"""
        return AudioGenerator(sample_rate=44100)
    
    @pytest.fixture
    def temp_dir(self):
        """Crear directorio temporal para tests"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir
    
    def test_sine_wave(self, generator, temp_dir):
        """Test: Generar onda sinusoidal"""
        output = os.path.join(temp_dir, "sine.wav")
        result = generator.generate_sine_wave(440, 1, 0.5, output)
        
        assert os.path.exists(result)
        assert os.path.getsize(result) > 0
    
    def test_chord(self, generator, temp_dir):
        """Test: Generar acorde"""
        output = os.path.join(temp_dir, "chord.wav")
        result = generator.generate_chord([262, 330, 392], 1, 0.3, output)
        
        assert os.path.exists(result)
        assert os.path.getsize(result) > 0
    
    def test_noise(self, generator, temp_dir):
        """Test: Generar ruido blanco"""
        output = os.path.join(temp_dir, "noise.wav")
        result = generator.generate_noise(1, 0.3, output)
        
        assert os.path.exists(result)
        assert os.path.getsize(result) > 0
    
    def test_sweep(self, generator, temp_dir):
        """Test: Generar barrido"""
        output = os.path.join(temp_dir, "sweep.wav")
        result = generator.generate_sweep(100, 1000, 1, 0.3, output)
        
        assert os.path.exists(result)
        assert os.path.getsize(result) > 0
    
    def test_melody(self, generator, temp_dir):
        """Test: Generar melodía"""
        output = os.path.join(temp_dir, "melody.wav")
        notes = [262, 294, 330, 349, 392]  # Do Re Mi Fa Sol
        durations = [0.5] * 5
        result = generator.generate_melody(notes, durations, 0.3, output)
        
        assert os.path.exists(result)
        assert os.path.getsize(result) > 0
    
    def test_invalid_frequency(self, generator):
        """Test: Rechazar frecuencia inválida"""
        with pytest.raises(ValueError):
            generator._validate_frequency(0)
        
        with pytest.raises(ValueError):
            generator._validate_frequency(-100)
    
    def test_invalid_duration(self, generator):
        """Test: Rechazar duración inválida"""
        with pytest.raises(ValueError):
            generator._validate_duration(0)
        
        with pytest.raises(ValueError):
            generator._validate_duration(100)  # Mayor al máximo
    
    def test_invalid_amplitude(self, generator):
        """Test: Rechazar amplitud inválida"""
        with pytest.raises(ValueError):
            generator._validate_amplitude(-0.5)
        
        with pytest.raises(ValueError):
            generator._validate_amplitude(1.5)
    
    def test_note_to_frequency(self):
        """Test: Convertir notas a frecuencias"""
        # A4 debe ser 440 Hz
        freq = AudioGenerator.note_to_frequency('A4')
        assert abs(freq - 440.0) < 1.0
        
        # C4 debe estar alrededor de 261.63 Hz
        freq = AudioGenerator.note_to_frequency('C4')
        assert abs(freq - 261.63) < 1.0
    
    def test_invalid_note(self):
        """Test: Rechazar nota inválida"""
        with pytest.raises(ValueError):
            AudioGenerator.note_to_frequency('X4')
        
        with pytest.raises(ValueError):
            AudioGenerator.note_to_frequency('C')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
