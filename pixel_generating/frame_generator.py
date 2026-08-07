# Interpolerer hver pixel gjennom en bildeserie for å generere nye bilder

import numpy as np
from PIL import Image

# Bildeserien - legg inn filnavnene i riktig rekkefølge
image_paths = [
    "bilde_0.jpg",
    "bilde_1.jpg", 
    "bilde_2.jpg",
    "bilde_3.jpg",
]

# x-verdiene til hvert bilde (f.eks. 0, 1, 2, 3, ...)
x_values = list(range(len(image_paths)))

# Punktene du vil generere nye bilder for
sample_points = list(x * 0.01 for x in range(0, 501)) 

# Last inn bildene som numpy-array
images = [np.asarray(Image.open(p).convert("RGB"), dtype=np.float64) for p in image_paths]
images = np.stack(images, axis=0)   # Stable bildene i en 4D-array
height, width = images.shape[1], images.shape[2]   # Hent dimensjonene

def interpolate(x, x_values, y_values):
    """
    Generisk Lagrange-interpolasjon. 
    Virker for både enkeltverdier (float) og hele arrays (numpy-array).
    """
    def _basis(j):
        p = 1
        for m in range(k):
            if m != j:
                p = p * (x - x_values[m]) / (x_values[j] - x_values[m])
        return p
    
    k = len(x_values)  # Antall punkter
    return sum(_basis(j) * y_values[j] for j in range(k))

def generate_frame(x):
    """
    Generer et nytt bilde ved punkt x.
    Bruker interpolate() direkte på hele bildeserien (3D-array).
    """
    return interpolate(x, x_values, images)

# Generer de nye bildene
for i in sample_points:
    print(f"Genererer bilde for x={i}...")
    
    frame = generate_frame(i)  # Interpoler for punkt i
    frame = np.clip(np.round(frame), 0, 255).astype(np.uint8)  # Clamp verdier til [0, 255] og konverter til uint8
    
    Image.fromarray(frame).save(f"interpolated_image_{i:.2f}.jpg")  # Lagre bildet

print("Ferdig!")
