# -*- coding: utf-8 -*-
"""
Drop-in размещение безликого фото: cover-crop по центру до точных размеров,
сохранение в формате назначения (JPEG/PNG), оптимизация. Размеры/имя/формат
исходного файла НЕ меняются — поэтому правок в коде не требуется.

  python .gsd-build/place_photo.py <src> <dest> <W> <H> [focus_y=0.5]

focus_y — вертикальная точка кадрирования (0=верх,1=низ) для широких исходников.
"""
import sys
from PIL import Image, ImageOps

src, dest, W, H = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
focus_y = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
focus_x = float(sys.argv[6]) if len(sys.argv) > 6 else 0.5

im = Image.open(src)
im = ImageOps.exif_transpose(im)
im = im.convert("RGB")

# cover: масштабируем так, чтобы покрыть WxH, затем центр-кроп
sw, sh = im.size
scale = max(W / sw, H / sh)
nw, nh = round(sw * scale), round(sh * scale)
im = im.resize((nw, nh), Image.LANCZOS)
left = int((nw - W) * focus_x)
top = int((nh - H) * focus_y)
im = im.crop((left, top, left + W, top + H))

assert im.size == (W, H), im.size

if dest.lower().endswith((".jpg", ".jpeg")):
    im.save(dest, "JPEG", quality=86, optimize=True, progressive=True)
elif dest.lower().endswith(".png"):
    im.save(dest, "PNG", optimize=True)
else:
    im.save(dest)

import os
print(f"{dest} <- {os.path.basename(src)}  {im.size}  {os.path.getsize(dest)//1024}KB")
