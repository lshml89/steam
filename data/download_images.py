import requests
import os

os.makedirs("images", exist_ok=True)

# URLs de ejemplo (20 imágenes gratuitas)
image_urls = [
    "https://via.placeholder.com/100x150?text=Movie+1",
    "https://via.placeholder.com/100x150?text=Movie+2",
    "https://via.placeholder.com/100x150?text=Movie+3",
    "https://via.placeholder.com/100x150?text=Movie+4",
    "https://via.placeholder.com/100x150?text=Movie+5",
    "https://via.placeholder.com/100x150?text=Movie+6",
    "https://via.placeholder.com/100x150?text=Movie+7",
    "https://via.placeholder.com/100x150?text=Movie+8",
    "https://via.placeholder.com/100x150?text=Movie+9",
    "https://via.placeholder.com/100x150?text=Movie+10",
    "https://via.placeholder.com/100x150?text=Movie+11",
    "https://via.placeholder.com/100x150?text=Movie+12",
    "https://via.placeholder.com/100x150?text=Movie+13",
    "https://via.placeholder.com/100x150?text=Movie+14",
    "https://via.placeholder.com/100x150?text=Movie+15",
    "https://via.placeholder.com/100x150?text=Movie+16",
    "https://via.placeholder.com/100x150?text=Movie+17",
    "https://via.placeholder.com/100x150?text=Movie+18",
    "https://via.placeholder.com/100x150?text=Movie+19",
    "https://via.placeholder.com/100x150?text=Movie+20",
]

for i, url in enumerate(image_urls, 1):
    r = requests.get(url)
    with open(f"images/movie_{i}.png", "wb") as f:
        f.write(r.content)
    print(f"Descargada imagen {i}")
