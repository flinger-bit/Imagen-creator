#!/usr/bin/env python
"""
Setup para Imagen Creator
"""

from setuptools import setup, find_packages

setup(
    name='ImagenCreator',
    version='1.0.0',
    description='Generador de imágenes y sonidos para Android',
    author='flinger-bit',
    packages=find_packages(),
    install_requires=[
        'kivy>=2.3.0',
        'Pillow>=10.1.0',
        'numpy>=1.24.3',
        'scipy>=1.11.4',
        'pyttsx3>=2.90',
        'pydub>=0.25.1',
    ],
    entry_points={
        'console_scripts': [
            'imagen-creator=src.main:main',
        ],
    },
)
