# Contributing Guide

¡Gracias por tu interés en contribuir a Imagen Creator!

## Cómo Contribuir

### Reportar Bugs
1. Abre un issue en GitHub
2. Describe el bug con detalle
3. Incluye pasos para reproducir
4. Añade logs/screenshots si es posible

### Proponer Features
1. Abre un issue de discusión
2. Describe la funcionalidad propuesta
3. Explica el caso de uso

### Pull Requests

1. **Fork** el repositorio
2. **Crea una rama**: `git checkout -b feature/mi-feature`
3. **Commits claros**: `git commit -m "Descripción clara del cambio"`
4. **Push**: `git push origin feature/mi-feature`
5. **Open PR** con descripción detallada

### Standards de Código

- Python 3.9+
- Type hints donde sea posible
- Docstrings en todas las funciones públicas
- Tests para nuevas funcionalidades
- Logging with levels (DEBUG, INFO, WARNING, ERROR)

### Testing

```bash
pytest tests/ -v --cov=src
```

### Linting

```bash
pylint src/
flake8 src/
```

## Desarrollo Local

```bash
# Clonar repo
git clone https://github.com/flinger-bit/Imagen-creator.git
cd Imagen-creator

# Crear venv
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows

# Instalar dependencias
pip install -r requirements.txt
pip install pytest pytest-cov pylint flake8

# Ejecutar tests
pytest tests/ -v

# Ejecutar app
python src/main.py
```

## Código de Conducta

- Sé respetuoso
- Sé inclusivo
- Reporta problemas de forma constructiva

## Preguntas?

Abre un issue o contacta a los mantenedores.

¡Gracias por contribuir! 🎉
