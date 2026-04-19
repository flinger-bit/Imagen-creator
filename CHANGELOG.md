# Changelog de Imagen Creator

Todos los cambios notables en este proyecto serán documentados en este archivo.

## [1.0.1] - 2024-04-19

### 🐛 Fixes Masivos
- **main.py**: Agregado manejo robusto de excepciones en importaciones
- **main.py**: Implementado sanitización de código ejecutado (whitelist segura)
- **main.py**: Agregado timeout conceptual para ejecutables
- **main.py**: Validación de longitud de código (máximo 50KB)
- **main.py**: Validación de longitud de salida (máximo 5KB visible)
- **main.py**: Mejor logging con niveles INFO/ERROR/DEBUG
- **main.py**: Interfaz mejorada con ScrollView para textos largos
- **main.py**: Botones con emojis y mejor UX
- **image_generator.py**: Agregada validación completa de parámetros
- **image_generator.py**: Manejo de excepciones en todos los métodos
- **image_generator.py**: Bug fix: division por cero en gradientes
- **image_generator.py**: Bug fix: clipping de valores RGB
- **image_generator.py**: Nuevos métodos: resize_image, crop_image
- **audio_generator.py**: Validación completa de frecuencias/duraciones/amplitudes
- **audio_generator.py**: Bug fix: normalización correcta en acordes
- **audio_generator.py**: Bug fix: clipping para evitar distorsión
- **audio_generator.py**: Mejores mensajes de error
- **buildozer.spec**: Actualizada configuración Android
- **requirements.txt**: Agregadas dependencias faltantes (Jinja2, Cython)

### ✨ Nuevas Características
- **CI/CD**: Workflow de GitHub Actions (.github/workflows/build.yml)
  - Compilación automática de APK
  - Tests automáticos con pytest
  - Linting con pylint y flake8
  - Soporte para releases automáticas
- **.gitignore**: Agregado archivo completo
- **Logging**: Sistema de logging centralizado
- **Tests**: Suite completa de tests con pytest
- **Documentation**: Guía mejorada de instalación

### 🔐 Security
- Validación de entrada sanitizada
- Restricción de funciones built-in ejecutables
- Límites de tamaño para prevenir DoS
- Encoding UTF-8 explícito en file reading

## [1.0.0] - 2024-04-19

### ✨ Inicial
- Estructura básica de proyecto Kivy
- Generador de imágenes (PIL/Pillow)
- Generador de sonidos (SciPy)
- Interfaz con 3 pestañas
- Soporte para cargar/ejecutar código Python
