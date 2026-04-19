"""
Configuración de pytest
"""

import os
import sys

# Agregar src al path para todos los tests
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
