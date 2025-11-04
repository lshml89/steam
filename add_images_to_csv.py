import pandas as pd
import os

# Ruta a movies.csv
csv_path = "data/movies.csv"

# Carpeta donde están las imágenes
img_folder = "static/images/"

# Cargar CSV
df = pd.read_csv(csv_path)

# Crear nueva columna img si no existe
if "img" not in df.columns:
    df["img"] = ""

# Obtener lista de imágenes
images = os.listdir(img_folder)

def match_image(title):
    title_clean = title.lower().replace(" ", "").replace("-", "").replace(":", "").replace(",", "")
    for img in images:
        img_clean = img.lower().replace(" ", "").replace("-", "").replace(":", "").replace(",", "")
        if title_clean in img_clean:
            return img
    return ""  # si no encuentra, deja vacío

df["img"] = df["title"].apply(match_image)

df.to_csv(csv_path, index=False)

print("✅ Column 'img' added and images matched successfully.")
