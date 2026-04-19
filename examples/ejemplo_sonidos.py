"""
Ejemplos de generación de sonidos para usar en Imagen Creator
"""

# EJEMPLO 1: Nota musical simple
# --------------------------------
print("Generando nota musical...")
from scipy.io import wavfile
import numpy as np

sample_rate = 44100
frequency = 440  # La
duration = 2

t = np.linspace(0, duration, sample_rate * duration, False)
wave = 0.3 * np.sin(2 * np.pi * frequency * t)
wave = np.int16(wave * 32767)

wavfile.write(f'{output_dir}/nota_la.wav', sample_rate, wave)
print("✓ Guardado: nota_la.wav")


# EJEMPLO 2: Melodía simple (Escala)
# -----------------------------------
print("Generando escala...")

frequencies = [262, 294, 330, 349, 392, 440, 494, 523]  # Do, Re, Mi, Fa, Sol, La, Si, Do
duration_note = 0.5

waves = []
for freq in frequencies:
    t = np.linspace(0, duration_note, int(sample_rate * duration_note), False)
    wave = 0.3 * np.sin(2 * np.pi * freq * t)
    waves.append(wave)

full_wave = np.concatenate(waves)
full_wave = np.int16(full_wave * 32767)

wavfile.write(f'{output_dir}/escala.wav', sample_rate, full_wave)
print("✓ Guardado: escala.wav")


# EJEMPLO 3: Acorde (múltiples notas simultáneas)
# ------------------------------------------------
print("Generando acorde...")

# Do Mayor: Do, Mi, Sol (262, 330, 392)
frequencies = [262, 330, 392]
duration = 2

t = np.linspace(0, duration, sample_rate * duration, False)
wave = np.zeros_like(t)

for freq in frequencies:
    wave += 0.3 * np.sin(2 * np.pi * freq * t)

wave = wave / len(frequencies)  # Normalizar
wave = np.int16(wave * 32767)

wavfile.write(f'{output_dir}/acorde_do_mayor.wav', sample_rate, wave)
print("✓ Guardado: acorde_do_mayor.wav")


# EJEMPLO 4: Sweep (barrido de frecuencia)
# -----------------------------------------
print("Generando sweep...")
from scipy import signal

duration = 2
freq_start = 100
freq_end = 2000

t = np.linspace(0, duration, sample_rate * duration, False)
wave = signal.chirp(t, freq_start, duration, freq_end, method='linear')
wave = 0.3 * wave
wave = np.int16(wave * 32767)

wavfile.write(f'{output_dir}/sweep.wav', sample_rate, wave)
print("✓ Guardado: sweep.wav")


# EJEMPLO 5: Ruido blanco
# -----------------------
print("Generando ruido blanco...")

duration = 3
samples = sample_rate * duration
noise = 0.3 * np.random.randn(samples)
noise = np.int16(noise * 32767)

wavfile.write(f'{output_dir}/ruido_blanco.wav', sample_rate, noise)
print("✓ Guardado: ruido_blanco.wav")


# EJEMPLO 6: Texto a voz (si tienes festival instalado)
# -------------------------------------------------------
print("Generando voz...")
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

# Guardar a archivo
engine.save_to_file('Hola, soy Imagen Creator', f'{output_dir}/saludo.wav')
engine.runAndWait()

print("✓ Guardado: saludo.wav")
