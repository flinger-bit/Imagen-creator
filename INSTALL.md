"""
Guía de instalación y compilación para Imagen Creator
"""

# PASO 1: Instalar dependencias en Linux
# =======================================

# Ubuntu/Debian:
sudo apt-get update
sudo apt-get install -y \
    python3 python3-pip python3-dev \
    libssl-dev libffi-dev \
    build-essential git \
    openjdk-11-jdk android-sdk

# Fedora/CentOS:
sudo dnf install -y \
    python3 python3-pip python3-devel \
    gcc gcc-c++ make \
    openssl-devel libffi-devel \
    java-11-openjdk java-11-openjdk-devel


# PASO 2: Instalar dependencias Python
# =====================================

pip3 install -r requirements.txt

# Instalar Buildozer específicamente
pip3 install buildozer cython


# PASO 3: Compilar APK
# ====================

# APK Debug (desarrollo, no requiere firma):
buildozer android debug

# APK Release (producción, requiere firma):
buildozer android release

# El APK estará en:
# bin/imagencreator-1.0.0-debug.apk


# PASO 4: Enviar a Android
# =========================

# Conectar dispositivo Android con USB
adb devices

# Instalar APK
adb install bin/imagencreator-1.0.0-debug.apk

# Desinstalar
adb uninstall org.flinger.imagencreator


# PASO 5: Ver logs en dispositivo
# ================================

adb logcat | grep python
adb shell


# SOLUCIÓN DE PROBLEMAS
# ======================

# Error: "No suitable Android SDK found"
# Instalar Android SDK:
python3 -m pip install android-ndk
buildozer android debug --ndk 25b

# Error: "cython: command not found"
pip3 install Cython

# Error: "gradle not found"
buildozer android aclean
buildozer android debug

# BuildBox lento la primera vez:
# (Es normal, descarga 2GB de dependencias)
# Espera pacientemente...


# COMPILAR MANUALMENTE
# ====================

cd src
python3 main.py  # Para probar en escritorio


# LIMPIAR ARCHIVOS DE COMPILACIÓN
# ================================

buildozer android clean
buildozer android aclean  # Limpia más profundamente
"""