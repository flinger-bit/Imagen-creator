"""
Ejemplos de generación de imágenes para usar en Imagen Creator
"""

# EJEMPLO 1: Crear un gradiente rojo a azul
# -----------------------------------------
print("Generando gradiente...")
from PIL import Image

img = Image.new('RGB', (600, 400))
pixels = img.load()

for y in range(400):
    for x in range(600):
        # Gradiente rojo a azul
        r = int(255 * (1 - x / 600))
        b = int(255 * (x / 600))
        pixels[x, y] = (r, 0, b)

img.save(f'{output_dir}/gradiente.png')
print("✓ Guardado: gradiente.png")


# EJEMPLO 2: Ruido aleatorio
# ---------------------------
import numpy as np
from PIL import Image

print("Generando ruido...")
noise = np.random.randint(0, 256, (500, 500, 3), dtype=np.uint8)
img = Image.fromarray(noise)
img.save(f'{output_dir}/ruido.png')
print("✓ Guardado: ruido.png")


# EJEMPLO 3: Patrón de damas
# --------------------------
from PIL import Image, ImageDraw

print("Generando patrón...")
size = 400
square_size = 25
img = Image.new('RGB', (size, size), 'white')
draw = ImageDraw.Draw(img)

for y in range(0, size, square_size):
    for x in range(0, size, square_size):
        if (x // square_size + y // square_size) % 2 == 0:
            draw.rectangle([x, y, x + square_size, y + square_size], fill='black')

img.save(f'{output_dir}/damas.png')
print("✓ Guardado: damas.png")


# EJEMPLO 4: Formas geométricas
#------------------------------
from PIL import Image, ImageDraw

print("Generando formas...")
img = Image.new('RGB', (600, 600), 'white')
draw = ImageDraw.Draw(img)

# Círculo rojo
draw.ellipse([50, 50, 200, 200], fill='red', outline='black', width=2)

# Cuadrado azul
draw.rectangle([250, 50, 400, 200], fill='blue', outline='black', width=2)

# Triángulo verde
triangle = [(300, 250), (400, 400), (200, 400)]
draw.polygon(triangle, fill='green', outline='black')

# Línea amarilla
draw.line([(50, 450), (550, 450)], fill='yellow', width=5)

img.save(f'{output_dir}/formas.png')
print("✓ Guardado: formas.png")


# EJEMPLO 5: Mandala (artes matemático)
# ------------------------------------
import numpy as np
from PIL import Image, ImageDraw

print("Generando mandala...")
size = 600
center = size // 2
img = Image.new('RGB', (size, size), 'black')
draw = ImageDraw.Draw(img)

colors = ['red', 'yellow', 'blue', 'green', 'cyan', 'magenta']

for i in range(1, 20):
    color = colors[i % len(colors)]
    radius = i * 20
    draw.ellipse(
        [center - radius, center - radius, center + radius, center + radius],
        outline=color,
        width=2
    )

img.save(f'{output_dir}/mandala.png')
print("✓ Guardado: mandala.png")
