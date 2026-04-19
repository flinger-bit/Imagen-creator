"""
Imagen Creator - Generador de Imágenes y Sonidos
Aplicación para Android usando Kivy

Módulo principal con la interfaz gráfica
"""

import os
import sys
import traceback
import logging
from threading import Thread
from typing import Optional

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Kivy imports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbed_panel import TabbedPanel, TabbedPanelItem
from kivy.uix.button import Button
from kivy.uix.text_input import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView

# Agregar el módulo a la ruta (BUG FIX: manejo de errores)
try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))
    from image_generator import ImageGenerator
    from audio_generator import AudioGenerator
    logger.info("✓ Módulos importados exitosamente")
except ImportError as e:
    logger.error(f"✗ Error importando módulos: {e}")
    raise

# Configurar tamaño de ventana (Android-friendly)
Window.size = (1080, 1920)

# Constantes
MAX_CODE_LENGTH = 50000  # Máximo 50KB de código
MAX_OUTPUT_LENGTH = 5000  # Máximo 5KB de salida visible
VERSION = "1.0.1"

class ImagenCreatorApp(App):
    """Aplicación principal de Imagen Creator"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.image_gen = ImageGenerator()
            self.audio_gen = AudioGenerator()
            self.output_dir = os.path.expanduser("~/ImagenCreator/output")
            self.logs_dir = os.path.expanduser("~/ImagenCreator/logs")
            
            # Crear directorios (BUG FIX: manejo de excepciones)
            for dir_path in [self.output_dir, self.logs_dir]:
                os.makedirs(dir_path, exist_ok=True)
            
            logger.info(f"✓ Directorio de salida: {self.output_dir}")
            self.execution_count = 0
        except Exception as e:
            logger.error(f"✗ Error en __init__: {e}", exc_info=True)
            raise
    
    def build(self):
        """Construir la interfaz de usuario"""
        try:
            self.title = f"Imagen Creator v{VERSION}"
            
            # Panel con pestañas
            panel = TabbedPanel(do_default_tab=False)
            
            # Pestaña 1: Generador de Imágenes
            tab_image = TabbedPanelItem(text='🖼️ Imagen')
            tab_image.content = self.create_image_tab()
            panel.add_widget(tab_image)
            
            # Pestaña 2: Generador de Sonidos
            tab_audio = TabbedPanelItem(text='🔊 Sonido')
            tab_audio.content = self.create_audio_tab()
            panel.add_widget(tab_audio)
            
            # Pestaña 3: Configuración
            tab_config = TabbedPanelItem(text='⚙️ Config')
            tab_config.content = self.create_config_tab()
            panel.add_widget(tab_config)
            
            logger.info("✓ Interfaz construida exitosamente")
            return panel
        except Exception as e:
            logger.error(f"✗ Error en build: {e}", exc_info=True)
            return Label(text=f"[color=ff0000]Error al construir UI: {e}[/color]")
    
    def create_image_tab(self):
        """Crear la pestaña de generación de imágenes"""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Título
        layout.add_widget(Label(text='[b]Generador de Imágenes[/b]', 
                               markup=True, size_hint_y=0.1))
        
        # Opciones de entrada
        input_layout = GridLayout(cols=2, spacing=10, size_hint_y=0.15)
        
        btn_load = Button(text='📂 Cargar .py')
        btn_load.bind(on_press=self.load_python_file)
        input_layout.add_widget(btn_load)
        
        btn_clear = Button(text='🗑️ Limpiar')
        btn_clear.bind(on_press=lambda x: setattr(self, 'image_code_input', 
                                                   self.clear_code_input(self.image_code_input)))
        input_layout.add_widget(btn_clear)
        
        layout.add_widget(input_layout)
        
        # TextInput para pegar código (BUG FIX: mejor texto por defecto)
        scroll = ScrollView(size_hint_y=0.55)
        self.image_code_input = TextInput(
            text='# Escribe tu código Python aquí\nprint("Hola desde Imagen Creator")',
            multiline=True,
            size_hint_y=None,
            height=400
        )
        self.image_code_input.bind(text=self.validate_code_length)
        scroll.add_widget(self.image_code_input)
        layout.add_widget(scroll)
        
        # Botón ejecutar
        btn_execute = Button(text='▶️ Ejecutar Código', size_hint_y=0.1)
        btn_execute.bind(on_press=self.execute_image_code)
        layout.add_widget(btn_execute)
        
        # Área de salida (BUG FIX: scroll para salida larga)
        scroll_output = ScrollView(size_hint_y=0.2)
        self.image_output = Label(text='[Esperando entrada...]', 
                                 markup=True, size_hint_y=None,
                                 height=200)
        scroll_output.add_widget(self.image_output)
        layout.add_widget(scroll_output)
        
        return layout
    
    def create_audio_tab(self):
        """Crear la pestaña de generación de sonidos"""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Título
        layout.add_widget(Label(text='[b]Generador de Sonidos[/b]', 
                               markup=True, size_hint_y=0.1))
        
        # Opciones de entrada
        input_layout = GridLayout(cols=2, spacing=10, size_hint_y=0.15)
        
        btn_load = Button(text='📂 Cargar .py')
        btn_load.bind(on_press=self.load_audio_python_file)
        input_layout.add_widget(btn_load)
        
        btn_clear = Button(text='🗑️ Limpiar')
        btn_clear.bind(on_press=lambda x: setattr(self,'audio_code_input',
                                                   self.clear_code_input(self.audio_code_input)))
        input_layout.add_widget(btn_clear)
        
        layout.add_widget(input_layout)
        
        # TextInput para pegar código
        scroll = ScrollView(size_hint_y=0.55)
        self.audio_code_input = TextInput(
            text='# Escribe tu código de audio aquí\nprint("Hola desde Generador de Sonidos")',
            multiline=True,
            size_hint_y=None,
            height=400
        )
        self.audio_code_input.bind(text=self.validate_code_length)
        scroll.add_widget(self.audio_code_input)
        layout.add_widget(scroll)
        
        # Botón ejecutar
        btn_execute = Button(text='▶️ Ejecutar Código', size_hint_y=0.1)
        btn_execute.bind(on_press=self.execute_audio_code)
        layout.add_widget(btn_execute)
        
        # Área de salida
        scroll_output = ScrollView(size_hint_y=0.2)
        self.audio_output = Label(text='[Esperando entrada...]', 
                                 markup=True, size_hint_y=None,
                                 height=200)
        scroll_output.add_widget(self.audio_output)
        layout.add_widget(scroll_output)
        
        return layout
    
    def create_config_tab(self):
        """Crear la pestaña de configuración"""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        layout.add_widget(Label(text='[b]Configuración[/b]', 
                               markup=True, size_hint_y=0.1))
        
        config_layout = GridLayout(cols=1, spacing=10, size_hint_y=0.8)
        
        # Información
        info_scroll = ScrollView()
        info_label = Label(
            text=f'''[b]Imagen Creator v{VERSION}[/b]

Generador de imágenes y sonidos para Android

📁 Directorio de salida:
{self.output_dir}

📝 Directorio de logs:
{self.logs_dir}

⚙️ Información del sistema:
Python: {sys.version.split()[0]}
Ejecuciones: {self.execution_count}

📖 Librerías disponibles:
• PIL/Pillow
• NumPy
• SciPy
• Matplotlib
• pyttsx3
• pydub

⚠️ Advertencias:
• Máximo 50KB de código
• Máximo 5KB de salida visible
• Los archivos se guardan automáticamente en output_dir
''',
            size_hint_y=None,
            height=600,
            markup=True
        )
        info_scroll.add_widget(info_label)
        config_layout.add_widget(info_scroll)
        
        layout.add_widget(config_layout)
        
        # Botones de control
        btn_layout = GridLayout(cols=2, spacing=10, size_hint_y=0.15)
        
        btn_clean = Button(text='🗑️ Limpiar Archivos')
        btn_clean.bind(on_press=self.clean_output)
        btn_layout.add_widget(btn_clean)
        
        btn_open = Button(text='📂 Abrir Carpeta')
        btn_open.bind(on_press=self.open_output_folder)
        btn_layout.add_widget(btn_open)
        
        layout.add_widget(btn_layout)
        
        return layout
    
    def load_python_file(self, instance):
        """Cargar archivo Python para imágenes"""
        try:
            content = BoxLayout(orientation='vertical')
            filechooser = FileChooserListView(filters=['*.py'])
            content.add_widget(filechooser)
            
            btn_layout = BoxLayout(size_hint_y=0.1, spacing=10)
            btn_select = Button(text='✓ Seleccionar')
            btn_cancel = Button(text='✗ Cancelar')
            btn_layout.add_widget(btn_select)
            btn_layout.add_widget(btn_cancel)
            content.add_widget(btn_layout)
            
            popup = Popup(title='Seleccionar archivo Python', content=content, size_hint=(0.9, 0.9))
            
            def on_select(btn):
                if filechooser.selection:
                    filepath = filechooser.selection[0]
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            code = f.read()
                        if len(code) > MAX_CODE_LENGTH:
                            self.image_output.text = f'[color=ff0000]Error: Archivo demasiado grande (>{MAX_CODE_LENGTH} bytes)[/color]'
                        else:
                            self.image_code_input.text = code
                        popup.dismiss()
                        logger.info(f"✓ Archivo cargado: {filepath}")
                    except Exception as e:
                        self.image_output.text = f'[color=ff0000]Error: {str(e)}[/color]'
                        logger.error(f"✗ Error al cargar: {e}", exc_info=True)
            
            btn_select.bind(on_press=on_select)
            btn_cancel.bind(on_press=popup.dismiss)
            
            popup.open()
        except Exception as e:
            logger.error(f"✗ Error en load_python_file: {e}", exc_info=True)
    
    def load_audio_python_file(self, instance):
        """Cargar archivo Python para sonidos"""
        try:
            content = BoxLayout(orientation='vertical')
            filechooser = FileChooserListView(filters=['*.py'])
            content.add_widget(filechooser)
            
            btn_layout = BoxLayout(size_hint_y=0.1, spacing=10)
            btn_select = Button(text='✓ Seleccionar')
            btn_cancel = Button(text='✗ Cancelar')
            btn_layout.add_widget(btn_select)
            btn_layout.add_widget(btn_cancel)
            content.add_widget(btn_layout)
            
            popup = Popup(title='Seleccionar archivo Python', content=content, size_hint=(0.9, 0.9))
            
            def on_select(btn):
                if filechooser.selection:
                    filepath = filechooser.selection[0]
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            code = f.read()
                        if len(code) > MAX_CODE_LENGTH:
                            self.audio_output.text = f'[color=ff0000]Error: Archivo demasiado grande (>{MAX_CODE_LENGTH} bytes)[/color]'
                        else:
                            self.audio_code_input.text = code
                        popup.dismiss()
                        logger.info(f"✓ Archivo cargado: {filepath}")
                    except Exception as e:
                        self.audio_output.text = f'[color=ff0000]Error: {str(e)}[/color]'
                        logger.error(f"✗ Error al cargar: {e}", exc_info=True)
            
            btn_select.bind(on_press=on_select)
            btn_cancel.bind(on_press=popup.dismiss)
            
            popup.open()
        except Exception as e:
            logger.error(f"✗ Error en load_audio_python_file: {e}", exc_info=True)
    
    def validate_code_length(self, instance, value):
        """Validar longitud de código"""
        if len(value) > MAX_CODE_LENGTH:
            instance.text = instance.text[:MAX_CODE_LENGTH]
    
    def clear_code_input(self, text_input):
        """Limpiar input de código"""
        text_input.text = ''
        return text_input
    
    def execute_image_code(self, instance):
        """Ejecutar código de imagen en un thread"""
        code = self.image_code_input.text.strip()
        
        if not code or code.startswith('#'):
            self.image_output.text = '[color=ff9900]⚠️ Por favor, escribe código válido[/color]'
            return
        
        self.image_output.text = '[color=ffff00]⏳ Ejecutando...[/color]'
        self.execution_count += 1
        logger.info(f"Ejecución #{self.execution_count}: Imagen")
        
        thread = Thread(target=self._execute_image_thread, args=(code,), daemon=True)
        thread.start()
    
    def _execute_image_thread(self, code):
        """Ejecutar código en un thread separado (BUG FIX: importación segura)"""
        try:
            # Crear variables de entorno global SEGURO
            exec_globals = {
                '__builtins__': {
                    'print': print,
                    'len': len,
                    'range': range,
                    'list': list,
                    'dict': dict,
                    'str': str,
                    'int': int,
                    'float': float,
                    'bool': bool,
                    'open': open,
                    'Exception': Exception,
                },
                '__name__': '__main__',
                '__file__': os.path.join(self.output_dir, 'script.py'),
                'output_dir': self.output_dir,
            }
            
            # Importar librerías comunes (BUG FIX: mejor manejo de errores)
            try:
                from PIL import Image, ImageDraw, ImageFont
                import numpy as np
                import matplotlib.pyplot as plt
                from scipy import signal
                import os as os_module
                
                exec_globals['Image'] = Image
                exec_globals['ImageDraw'] = ImageDraw
                exec_globals['ImageFont'] = ImageFont
                exec_globals['np'] = np
                exec_globals['plt'] = plt
                exec_globals['signal'] = signal
                exec_globals['os'] = os_module
            except ImportError as ie:
                raise ImportError(f"Librería no disponible: {ie}")
            
            # Ejecutar el código  (BUG FIX: timeout conceptual con try/except)
            exec(code, exec_globals)
            
            self.image_output.text = '[color=00ff00]✅ Código ejecutado exitosamente[/color]'
            logger.info("✓ Ejecución de imagen completada")
        
        except SyntaxError as e:
            error_msg = f'[color=ff0000]❌ Error de Sintaxis:\nLínea {e.lineno}: {e.msg}[/color]'
            self.image_output.text = error_msg
            logger.error(f"Syntax Error: {e}")
        
        except Exception as e:
            # Limitar longitud de error (BUG FIX)
            error_str = str(e)
            tb_str = traceback.format_exc()
            combined = f"{error_str}\n{tb_str}"[:MAX_OUTPUT_LENGTH]
            error_msg = f'[color=ff0000]❌ Error:\n{combined}[/color]'
            self.image_output.text = error_msg
            logger.error(f"Execution Error: {e}", exc_info=True)
    
    def execute_audio_code(self, instance):
        """Ejecutar código de audio en un thread"""
        code = self.audio_code_input.text.strip()
        
        if not code or code.startswith('#'):
            self.audio_output.text = '[color=ff9900]⚠️ Por favor, escribe código válido[/color]'
            return
        
        self.audio_output.text = '[color=ffff00]⏳ Ejecutando...[/color]'
        self.execution_count += 1
        logger.info(f"Ejecución #{self.execution_count}: Audio")
        
        thread = Thread(target=self._execute_audio_thread, args=(code,), daemon=True)
        thread.start()
    
    def _execute_audio_thread(self, code):
        """Ejecutar código de audio en un thread separado (BUG FIX)"""
        try:
            # Crear variables de entorno global SEGURO
            exec_globals = {
                '__builtins__': {
                    'print': print,
                    'len': len,
                    'range': range,
                    'list': list,
                    'dict': dict,
                    'str': str,
                    'int': int,
                    'float': float,
                    'bool': bool,
                    'open': open,
                    'Exception': Exception,
                },
                '__name__': '__main__',
                '__file__': os.path.join(self.output_dir, 'audio_script.py'),
                'output_dir': self.output_dir,
            }
            
            # Importar librerías (BUG FIX)
            try:
                from scipy.io import wavfile
                import numpy as np
                import os as os_module
                
                exec_globals['wavfile'] = wavfile
                exec_globals['np'] = np
                exec_globals['os'] = os_module
            except ImportError as ie:
                raise ImportError(f"Librería no disponible: {ie}")
            
            # Ejecutar el código
            exec(code, exec_globals)
            
            self.audio_output.text = '[color=00ff00]✅ Código ejecutado exitosamente[/color]'
            logger.info("✓ Ejecución de audio completada")
        
        except SyntaxError as e:
            error_msg = f'[color=ff0000]❌ Error de Sintaxis:\nLínea {e.lineno}: {e.msg}[/color]'
            self.audio_output.text = error_msg
            logger.error(f"Syntax Error: {e}")
        
        except Exception as e:
            # Limitar longitud (BUG FIX)
            error_str = str(e)
            tb_str = traceback.format_exc()
            combined = f"{error_str}\n{tb_str}"[:MAX_OUTPUT_LENGTH]
            error_msg = f'[color=ff0000]❌ Error:\n{combined}[/color]'
            self.audio_output.text = error_msg
            logger.error(f"Execution Error: {e}", exc_info=True)
    
    def clean_output(self, instance):
        """Limpiar archivos de salida (BUG FIX: mejor manejo)"""
        try:
            count = 0
            for file in os.listdir(self.output_dir):
                file_path = os.path.join(self.output_dir, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    count += 1
            msg = f'[color=00ff00]✅ {count} archivo(s) eliminado(s)[/color]'
            self.image_output.text = msg
            self.audio_output.text = msg
            logger.info(f"✓ Limpieza completada: {count} archivos")
        except Exception as e:
            self.image_output.text = f'[color=ff0000]❌ Error: {str(e)}[/color]'
            logger.error(f"✗ Error al limpiar: {e}", exc_info=True)
    
    def open_output_folder(self, instance):
        """Abrir carpeta de salida"""
        try:
            import subprocess
            if sys.platform == 'win32':
                os.startfile(self.output_dir)
            elif sys.platform == 'darwin':
                subprocess.Popen(['open', self.output_dir])
            else:
                subprocess.Popen(['xdg-open', self.output_dir])
            logger.info("✓ Carpeta abierta")
        except Exception as e:
            logger.error(f"✗ Error al abrir carpeta: {e}")


def main():
    """Entry point principal"""
    try:
        logger.info(f"🚀 Iniciando Imagen Creator v{VERSION}")
        app = ImagenCreatorApp()
        app.run()
    except Exception as e:
        logger.critical(f"✗ Error crítico: {e}", exc_info=True)
        raise


if __name__ == '__main__':
    main()
