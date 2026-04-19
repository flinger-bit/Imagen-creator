"""
Imagen Creator - Logging configuration
"""

import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging(log_level=logging.INFO):
    """
    Configurar sistema de logging
    
    Args:
        log_level: Nivel de logging (DEBUG, INFO, WARNING, ERROR)
    
    Returns:
        Logger configurado
    """
    # Crear directorio de logs
    log_dir = os.path.expanduser("~/ImagenCreator/logs")
    os.makedirs(log_dir, exist_ok=True)
    
    logger = logging.getLogger('ImagenCreator')
    logger.setLevel(log_level)
    
    # Handler para archivo
    log_file = os.path.join(log_dir, 'imagencreator.log')
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(log_level)
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # Formato
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Agregar handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Logger global
logger = setup_logging()
