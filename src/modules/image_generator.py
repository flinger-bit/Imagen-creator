"""
Módulo para generación de imágenes
Incluye utilidades para crear y manipular imágenes
"""

import os
import logging
from typing import Tuple, Optional
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import numpy as np

logger = logging.getLogger(__name__)

class ImageGenerator:
    """Generador de imágenes usando PIL y NumPy"""
    
    MAX_DIMENSION = 4096  # Máximo 4096x4096 píxeles
    OUTPUT_FORMATS = ['PNG', 'JPG', 'BMP', 'GIF', 'TIFF']
    
    def __init__(self):
        """Inicializar el generador"""
        self.output_formats = self.OUTPUT_FORMATS
        logger.info("✓ ImageGenerator inicializado")
    
    @staticmethod
    def _validate_dimensions(width: int, height: int) -> bool:
        """
        Validar dimensiones de imagen
        
        Args:
            width: Ancho en píxeles
            height: Alto en píxeles
        
        Returns:
            True si son válidas, False caso contrario
        """
        if width <= 0 or height <= 0:
            raise ValueError(f"Dimensiones inválidas: {width}x{height}")
        if width > ImageGenerator.MAX_DIMENSION or height > ImageGenerator.MAX_DIMENSION:
            raise ValueError(f"Dimensiones demasiado grandes: máximo {ImageGenerator.MAX_DIMENSION}x{ImageGenerator.MAX_DIMENSION}")
        return True
    
    @staticmethod
    def create_gradient_image(width: int, height: int, 
                            color1: Tuple[int, int, int], 
                            color2: Tuple[int, int, int], 
                            output_path: str) -> str:
        """
        Crear imagen con gradiente
        
        Args:
            width: Ancho de la imagen
            height: Alto de la imagen
            color1: Color inicial (RGB tuple)
            color2: Color final (RGB tuple)
            output_path: Ruta de salida
        
        Returns:
            Ruta del archivo guardado
        
        Raises:
            ValueError: Si las dimensiones o colores son inválidas
        """
        try:
            ImageGenerator._validate_dimensions(width, height)
            
            # Validar colores
            if not all(isinstance(c, (list, tuple)) and len(c) == 3 for c in [color1, color2]):
                raise ValueError("Los colores deben ser tuplas RGB (r, g, b)")
            
            img = Image.new('RGB', (width, height))
            pixels = img.load()
            
            for y in range(height):
                ratio = y / max(height - 1, 1)  # BUG FIX: evitar división por cero
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                
                for x in range(width):
                    pixels[x, y] = (r, g, b)
            
            img.save(output_path, format='PNG')
            logger.info(f"✓ Gradiente guardado: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"✗ Error en create_gradient_image: {e}", exc_info=True)
            raise
    
    @staticmethod
    def create_noise_image(width: int, height: int, output_path: str) -> str:
        """
        Crear imagen de ruido aleatorio
        
        Args:
            width: Ancho de la imagen
            height: Alto de la imagen
            output_path: Ruta de salida
        
        Returns:
            Ruta del archivo guardado
        """
        try:
            ImageGenerator._validate_dimensions(width, height)
            
            noise = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
            img = Image.fromarray(noise)
            img.save(output_path, format='PNG')
            logger.info(f"✓ Ruido guardado: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"✗ Error en create_noise_image: {e}", exc_info=True)
            raise
    
    @staticmethod
    def create_pattern_image(width: int, height: int, pattern_type: str, 
                            output_path: str) -> str:
        """
        Crear imagen con patrones
        
        Args:
            width: Ancho de la imagen
            height: Alto de la imagen
            pattern_type: 'checkerboard', 'circles', 'stripes'
            output_path: Ruta de salida
        
        Returns:
            Ruta del archivo guardado
        
        Raises:
            ValueError: Si el tipo de patrón es inválido
        """
        try:
            ImageGenerator._validate_dimensions(width, height)
            
            valid_patterns = ['checkerboard', 'circles', 'stripes']
            if pattern_type not in valid_patterns:
                raise ValueError(f"Patrón inválido: {pattern_type}. Válidos: {valid_patterns}")
            
            img = Image.new('RGB', (width, height), 'white')
            draw = ImageDraw.Draw(img)
            
            if pattern_type == 'checkerboard':
                square_size = 20
                for y in range(0, height, square_size):
                    for x in range(0, width, square_size):
                        if (x // square_size + y // square_size) % 2 == 0:
                            draw.rectangle([x, y, x + square_size, y + square_size], 
                                         fill='black')
            
            elif pattern_type == 'circles':
                circle_size = 10
                for y in range(0, height, circle_size * 3):
                    for x in range(0, width, circle_size * 3):
                        draw.ellipse([x, y, x + circle_size, y + circle_size], 
                                   fill='blue')
            
            elif pattern_type == 'stripes':
                stripe_width = 10
                for x in range(0, width, stripe_width * 2):
                    draw.rectangle([x, 0, x + stripe_width, height], fill='red')
            
            img.save(output_path, format='PNG')
            logger.info(f"✓ Patrón guardado: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"✗ Error en create_pattern_image: {e}", exc_info=True)
            raise
    
    @staticmethod
    def apply_filter(input_path: str, filter_type: str, output_path: str) -> str:
        """
        Aplicar filtros a una imagen existente
        
        Args:
            input_path: Ruta de la imagen de entrada
            filter_type: 'blur', 'sharpen', 'grayscale', 'invert', 'edge'
            output_path: Ruta de salida
        
        Returns:
            Ruta del archivo guardado
        
        Raises:
            FileNotFoundError: Si la imagen no existe
            ValueError: Si el filtro es inválido
        """
        try:
            if not os.path.exists(input_path):
                raise FileNotFoundError(f"Imagen no encontrada: {input_path}")
            
            valid_filters = ['blur', 'sharpen', 'grayscale', 'invert', 'edge']
            if filter_type not in valid_filters:
                raise ValueError(f"Filtro inválido: {filter_type}. Válidos: {valid_filters}")
            
            img = Image.open(input_path)
            
            if filter_type == 'blur':
                img = img.filter(ImageFilter.GaussianBlur(radius=5))
            elif filter_type == 'sharpen':
                img = img.filter(ImageFilter.SHARPEN)
            elif filter_type == 'grayscale':
                img = ImageOps.grayscale(img)
            elif filter_type == 'invert':
                img = ImageOps.invert(img.convert('RGB'))
            elif filter_type == 'edge':
                img = img.filter(ImageFilter.FIND_EDGES)
            
            img.save(output_path, format='PNG')
            logger.info(f"✓ Filtro aplicado: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"✗ Error en apply_filter: {e}", exc_info=True)
            raise
    
    @staticmethod
    def resize_image(input_path: str, width: int, height: int, output_path: str) -> str:
        """
        Redimensionar una imagen
        
        Args:
            input_path: Ruta de la imagen de entrada
            width: Nuevo ancho
            height: Nuevo alto
            output_path: Ruta de salida
        
        Returns:
            Ruta del archivo guardado
        """
        try:
            if not os.path.exists(input_path):
                raise FileNotFoundError(f"Imagen no encontrada: {input_path}")
            
            ImageGenerator._validate_dimensions(width, height)
            
            img = Image.open(input_path)
            img_resized = img.resize((width, height), Image.Resampling.LANCZOS)
            img_resized.save(output_path, format='PNG')
            logger.info(f"✓ Imagen redimensionada: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"✗ Error en resize_image: {e}", exc_info=True)
            raise
    
    @staticmethod
    def crop_image(input_path: str, left: int, top: int, right: int, 
                  bottom: int, output_path: str) -> str:
        """
        Recortar una imagen
        
        Args:
            input_path: Ruta de la imagen de entrada
            left: Coordenada X izquierda
            top: Coordenada Y superior
            right: Coordenada X derecha
            bottom: Coordenada Y inferior
            output_path: Ruta de salida
        
        Returns:
            Ruta del archivo guardado
        """
        try:
            if not os.path.exists(input_path):
                raise FileNotFoundError(f"Imagen no encontrada: {input_path}")
            
            img = Image.open(input_path)
            img_cropped = img.crop((left, top, right, bottom))
            img_cropped.save(output_path, format='PNG')
            logger.info(f"✓ Imagen recortada: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"✗ Error en crop_image: {e}", exc_info=True)
            raise

            circle_size = 10
            for y in range(0, height, circle_size * 3):
                for x in range(0, width, circle_size * 3):
                    draw.ellipse([x, y, x + circle_size, y + circle_size], 
                               fill='blue')
        
        elif pattern_type == 'stripes':
            stripe_width = 10
            for x in range(0, width, stripe_width * 2):
                draw.rectangle([x, 0, x + stripe_width, height], fill='red')
        
        img.save(output_path)
        return output_path
    
    @staticmethod
    def apply_filter(input_path, filter_type, output_path):
        """
        Aplicar filtros a una imagen existente
        
        Args:
            input_path: Ruta de la imagen de entrada
            filter_type: 'blur', 'sharpen', 'grayscale', 'invert'
            output_path: Ruta de salida
        """
        from PIL import ImageFilter, ImageOps
        
        img = Image.open(input_path)
        
        if filter_type == 'blur':
            img = img.filter(ImageFilter.GaussianBlur(radius=5))
        elif filter_type == 'sharpen':
            img = img.filter(ImageFilter.SHARPEN)
        elif filter_type == 'grayscale':
            img = ImageOps.grayscale(img)
        elif filter_type == 'invert':
            img = ImageOps.invert(img.convert('RGB'))
        
        img.save(output_path)
        return output_path
