import os
from PIL import Image

folder = "d:/Sites/14 Carrot Cafe/images"
for f in os.listdir(folder):
    if f.endswith('.jpg'):
        path = os.path.join(folder, f)
        img = Image.open(path)
        print(f"{f}: {img.size}")
