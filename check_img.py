from PIL import Image
import sys

img = Image.open(sys.argv[1])
print(f"Format: {img.format}")
print(f"Size: {img.size}")
print(f"Mode: {img.mode}")
