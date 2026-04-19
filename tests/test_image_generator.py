"""
Tests para image_generator.py
"""

import pytest
import os
import sys
import tempfile
from pathlib import Path

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from modules.image_generator import ImageGenerator


class TestImageGenerator:
    """Suite de tests para ImageGenerator"""
    
    @pytest.fixture
    def temp_dir(self):
        """Crear directorio temporal para tests"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir
    
    def test_gradient_creation(self, temp_dir):
        """Test: Crear una imagen con gradiente"""
        output = os.path.join(temp_dir, "test_gradient.png")
        result = ImageGenerator.create_gradient_image(
            100, 100, 
            (255, 0, 0), (0, 0, 255), 
            output
        )
        
        assert os.path.exists(result)
        assert os.path.getsize(result) > 0
    
    def test_noise_creation(self, temp_dir):
        """Test: Crear imagen de ruido"""
        output = os.path.join(temp_dir, "test_noise.png")
        result = ImageGenerator.create_noise_image(100, 100, output)
        
        assert os.path.exists(result)
        assert os.path.getsize(result) > 0
    
    def test_pattern_creation(self, temp_dir):
        """Test: Crear patrones"""
        for pattern in ['checkerboard', 'circles', 'stripes']:
            output = os.path.join(temp_dir, f"test_{pattern}.png")
            result = ImageGenerator.create_pattern_image(100, 100, pattern, output)
            
            assert os.path.exists(result)
            assert os.path.getsize(result) > 0
    
    def test_invalid_dimensions(self):
        """Test: Rechazar dimensiones inválidas"""
        with pytest.raises(ValueError):
            ImageGenerator._validate_dimensions(0, 100)
        
        with pytest.raises(ValueError):
            ImageGenerator._validate_dimensions(100, -50)
    
    def test_oversized_dimensions(self):
        """Test: Rechazar dimensiones demasiado grandes"""
        with pytest.raises(ValueError):
            ImageGenerator._validate_dimensions(5000, 5000)
    
    def test_invalid_pattern(self, temp_dir):
        """Test: Rechazar patrón inválido"""
        output = os.path.join(temp_dir, "test_invalid.png")
        
        with pytest.raises(ValueError):
            ImageGenerator.create_pattern_image(100, 100, "invalid_pattern", output)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
