"""
Módulo para generación de sonidos
Incluye síntesis de audio, generación de ondas y utilidades de sonido
"""

import os
import logging
import numpy as np
from typing import List, Tuple, Optional
from scipy.io import wavfile
from scipy import signal

logger = logging.getLogger(__name__)

class AudioGenerator:
    """Generador de sonidos usando SciPy"""
    
    MAX_DURATION = 60  # Máximo 60 segundos
    MIN_AMPLITUDE = 0.0
    MAX_AMPLITUDE = 1.0
    
    def __init__(self, sample_rate: int = 44100):
        """
        Inicializar el generador de audio
        
        Args:
            sample_rate: Tasa de muestreo en Hz (default: 44100)
        """
        if sample_rate < 8000 or sample_rate > 48000:
            logger.warning(f"Tasa de muestreo inusual: {sample_rate}")
        
        self.sample_rate = sample_rate
        logger.info(f"✓ AudioGenerator inicializado con tasa {sample_rate} Hz")
    
    @staticmethod
    def _validate_duration(duration: float) -> bool:
        """
        Validar duración
        
        Args:
            duration: Duración en segundos
        
        Returns:
            True si es válida
        
        Raises:
            ValueError: Si la duración es inválida
        """
        if duration <= 0:
            raise ValueError(f"Duración inválida: {duration}")
        if duration > AudioGenerator.MAX_DURATION:
            raise ValueError(f"Duración demasiado larga: máximo {AudioGenerator.MAX_DURATION}s")
        return True
    
    @staticmethod
    def _validate_amplitude(amplitude: float) -> bool:
        """Validar amplitud"""
        if not (AudioGenerator.MIN_AMPLITUDE <= amplitude <= AudioGenerator.MAX_AMPLITUDE):
            raise ValueError(f"Amplitud inválida: {amplitude} (debe estar entre 0 y 1)")
        return True
    
    @staticmethod
    def _validate_frequency(frequency: float) -> bool:
        """Validar frecuencia"""
        if frequency <= 0 or frequency > 20000:
            raise ValueError(f"Frecuencia inválida: {frequency} Hz")
        return True
    
    def generate_sine_wave(self, frequency: float, duration: float, amplitude: float, 
                          output_path: str) -> str:
        """
        Generar onda sinusoidal
        
        Args:
            frequency: Frecuencia en Hz
            duration: Duración en segundos
            amplitude: Amplitud (0-1)
            output_path: Ruta de salida
        
        Returns:
            Ruta del archivo guardado
        """
        try:
            self._validate_frequency(frequency)
            self._validate_duration(duration)
            self._validate_amplitude(amplitude)
            
            t = np.linspace(0, duration, int(self.sample_rate * duration), False)
            wave = amplitude * np.sin(2 * np.pi * frequency * t)
            
            # Convertir a 16-bit entero (BUG FIX: clamp al rango válido)
            wave = np.clip(wave, -1, 1)
            wave = np.int16(wave * 32767)
            
            wavfile.write(output_path, self.sample_rate, wave)
            logger.info(f"✓ Onda sinusoidal guardada: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"✗ Error en generate_sine_wave: {e}", exc_info=True)
            raise
    
    def generate_chord(self, frequencies: List[float], duration: float, amplitude: float, 
                      output_path: str) -> str:
        """
        Generar un acorde (múltiples frecuencias)
        
        Args:
            frequencies: Lista de frecuencias en Hz
            duration: Duración en segundos
            amplitude: Amplitud (0-1)
            output_path: Ruta de salida
        
        Returns:
            Ruta del archivo guardado
        """
        try:
            for freq in frequencies:
                self._validate_frequency(freq)
            self._validate_duration(duration)
            self._validate_amplitude(amplitude)
            
            if not frequencies:
                raise ValueError("Lista de frecuencias vacía")
            
            t = np.linspace(0, duration, int(self.sample_rate * duration), False)
            wave = np.zeros_like(t)
            
            for freq in frequencies:
                wave += amplitude * np.sin(2 * np.pi * freq * t)
            
            # Normalizar (BUG FIX)
            wave_max = np.max(np.abs(wave))
            if wave_max > 0:
                wave = wave / wave_max * 0.9  # 90% para evitar clipping
            
            wave = np.clip(wave, -1, 1)
            wave = np.int16(wave * 32767)
            
            wavfile.write(output_path, self.sample_rate, wave)
            logger.info(f"✓ Acorde guardado: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"✗ Error en generate_chord: {e}", exc_info=True)
            raise
    
    def generate_noise(self, duration: float, amplitude: float, output_path: str) -> str:
        """
        Generar ruido blanco
        
        Args:
            duration: Duración en segundos
            amplitude: Amplitud (0-1)
            output_path: Ruta de salida
        
        Returns:
            Ruta del archivo guardado
        """
        try:
            self._validate_duration(duration)
            self._validate_amplitude(amplitude)
            
            samples = int(self.sample_rate * duration)
            noise = amplitude * np.random.randn(samples)
            noise = np.clip(noise, -1, 1)
            noise = np.int16(noise * 32767)
            
            wavfile.write(output_path, self.sample_rate, noise)
            logger.info(f"✓ Ruido blanco guardado: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"✗ Error en generate_noise: {e}", exc_info=True)
            raise
    
    def generate_sweep(self, freq_start: float, freq_end: float, duration: float, 
                      amplitude: float, output_path: str) -> str:
        """
        Generar barrido de frecuencia (sweep/chirp)
        
        Args:
            freq_start: Frecuencia inicial en Hz
            freq_end: Frecuencia final en Hz
            duration: Duración en segundos
            amplitude: Amplitud (0-1)
            output_path: Ruta de salida
        
        Returns:
            Ruta del archivo guardado
        """
        try:
            self._validate_frequency(freq_start)
            self._validate_frequency(freq_end)
            self._validate_duration(duration)
            self._validate_amplitude(amplitude)
            
            t = np.linspace(0, duration, int(self.sample_rate * duration), False)
            wave = signal.chirp(t, freq_start, duration, freq_end, method='linear')
            wave = amplitude * wave
            wave = np.clip(wave, -1, 1)
            wave = np.int16(wave * 32767)
            
            wavfile.write(output_path, self.sample_rate, wave)
            logger.info(f"✓ Sweep guardado: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"✗ Error en generate_sweep: {e}", exc_info=True)
            raise
    
    def generate_melody(self, notes: List[float], durations: List[float], 
                       amplitude: float, output_path: str) -> str:
        """
        Generar una melodía
        
        Args:
            notes: Lista de frecuencias en Hz (0 para silencio)
            durations: Lista de duraciones en segundos
            amplitude: Amplitud (0-1)
            output_path: Ruta de salida
        
        Returns:
            Ruta del archivo guardado
        """
        try:
            if len(notes) != len(durations):
                raise ValueError(f"Número de notas ({len(notes)}) debe coincidir con duraciones ({len(durations)})")
            
            if not notes:
                raise ValueError("Lista de notas vacía")
            
            self._validate_amplitude(amplitude)
            
            for note in notes:
                if note > 0:  # 0 es silencio
                    self._validate_frequency(note)
            
            for dur in durations:
                self._validate_duration(dur)
            
            waves = []
            
            for frequency, duration in zip(notes, durations):
                if frequency == 0:  # Silencio
                    wave = np.zeros(int(self.sample_rate * duration))
                else:
                    t = np.linspace(0, duration, int(self.sample_rate * duration), False)
                    wave = amplitude * np.sin(2 * np.pi * frequency * t)
                
                waves.append(wave)
            
            # Concatenar todas las notas
            full_wave = np.concatenate(waves)
            full_wave = np.clip(full_wave, -1, 1)
            full_wave = np.int16(full_wave * 32767)
            
            wavfile.write(output_path, self.sample_rate, full_wave)
            logger.info(f"✓ Melodía guardada: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"✗ Error en generate_melody: {e}", exc_info=True)
            raise
    
    @staticmethod
    def note_to_frequency(note: str) -> float:
        """
        Convertir nota musical a frecuencia
        
        Args:
            note: Nota como string (ej: 'C4', 'D#5', 'Bb3')
        
        Returns:
            Frecuencia en Hz
        
        Raises:
            ValueError: Si la nota es inválida
        """
        try:
            notes_dict = {
                'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11
            }
            
            note = note.strip().upper()
            
            if len(note) < 2:
                raise ValueError(f"Nota inválida: {note} (formato: C4, D#5, etc)")
            
            base_note = note[0]
            octave_str = note[-1]
            
            # Validar octava
            try:
                octave = int(octave_str)
            except ValueError:
                raise ValueError(f"Octava inválida en nota: {note}")
            
            # Verificar alteraciones (# o b)
            semitone_shift = 0
            if '#' in note:
                semitone_shift = 1
            elif 'b' in note or 'B' in note[1]:  # Lowercase 'b' indica bemol
                semitone_shift = -1
            
            if base_note not in notes_dict:
                raise ValueError(f"Nota inválida: {base_note}")
            
            semitone = notes_dict[base_note] + semitone_shift
            
            # Validar rango de octava
            if octave < 0 or octave > 8:
                logger.warning(f"Octava inusual: {octave}")
            
            # Frecuencia de A4 = 440 Hz
            frequency = 440 * (2 ** ((octave - 4 + semitone / 12) / 12))
            
            return frequency
        
        except Exception as e:
            logger.error(f"✗ Error en note_to_frequency: {e}")
            raise


# Constantes de notas para referencia rápida (BUG FIX: agregar tabla de referencia)
NOTES = {
    'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23, 'G4': 392.00, 'A4': 440.00, 'B4': 493.88,
    'C5': 523.25, 'D5': 587.33, 'E5': 659.25, 'F5': 698.46, 'G5': 783.99, 'A5': 880.00, 'B5': 987.77,
}

            duration: Duración en segundos
            amplitude: Amplitud (0-1)
            output_path: Ruta de salida
        """
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        # Generar chirp (barrido)
        wave = signal.chirp(t, freq_start, duration, freq_end, method='linear')
        wave = amplitude * wave
        wave = np.int16(wave * 32767)
        
        wavfile.write(output_path, self.sample_rate, wave)
        return output_path
    
    def generate_melody(self, notes, durations, amplitude, output_path):
        """
        Generar una melodía
        
        Args:
            notes: Lista de frecuencias en Hz
            durations: Lista de duraciones en segundos
            amplitude: Amplitud (0-1)
            output_path: Ruta de salida
        """
        waves = []
        
        for frequency, duration in zip(notes, durations):
            if frequency == 0:  # Silencio
                wave = np.zeros(int(self.sample_rate * duration))
            else:
                t = np.linspace(0, duration, int(self.sample_rate * duration), False)
                wave = amplitude * np.sin(2 * np.pi * frequency * t)
            
            waves.append(wave)
        
        # Concatenar todas las notas
        full_wave = np.concatenate(waves)
        full_wave = np.int16(full_wave * 32767)
        
        wavfile.write(output_path, self.sample_rate, full_wave)
        return output_path
    
    @staticmethod
    def note_to_frequency(note):
        """
        Convertir nota musical a frecuencia
        
        Args:
            note: Nota como string (ej: 'C4', 'D#5')
        
        Returns:
            Frecuencia en Hz
        """
        notes_dict = {
            'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11
        }
        
        note = note.strip().upper()
        
        if len(note) < 2:
            raise ValueError(f"Nota inválida: {note}")
        
        base_note = note[0]
        octave = int(note[-1])
        
        # Verificar alteraciones (# o b)
        semitone_shift = 0
        if '#' in note:
            semitone_shift = 1
        elif 'b' in note:
            semitone_shift = -1
        
        if base_note not in notes_dict:
            raise ValueError(f"Nota inválida: {base_note}")
        
        semitone = notes_dict[base_note] + semitone_shift
        # Frecuencia de A4 = 440 Hz
        frequency = 440 * (2 ** ((octave - 4 + semitone / 12) / 12))
        
        return frequency
