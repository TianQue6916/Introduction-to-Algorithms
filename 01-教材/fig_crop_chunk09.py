# -*- coding: utf-8 -*-
"""Crop the vector figures of CLRS chunk09 (book p323-362) at 300 dpi.
Book page p -> pdf index p+20. Clips are PDF points (top-left origin).
Usage: python fig_crop_chunk09.py <outdir>
"""
import os
import sys

import fitz
from PIL import Image

PDF = r"D:/Desktop/工具箱/输出文件/Introduction to Algorithms (Thomas H. Cormen, Charles E. Leiserson etc.) (z-library.sk, 1lib.sk, z-lib.sk).pdf"
OUT = sys.argv[1] if len(sys.argv) > 1 else "fig"
CLIPS = {
    "p329_fig13.7": (329, (60, 68, 528, 440)),
    "p331_fig13.8": (331, (60, 370, 528, 545)),
    "p334_fig13.9": (334, (60, 66, 528, 186)),
    "p335_fig13.10": (335, (60, 88, 528, 530)),
    "p336_fig13.11": (336, (60, 66, 528, 198)),
    "p340_fig14.1": (340, (60, 66, 528, 200)),
    "p344_fig14.2": (344, (60, 65, 528, 163)),
    "p349_fig14.3": (349, (60, 70, 528, 200)),
    "p350_fig14.4": (350, (60, 68, 528, 362)),
    "p352_fig14.5": (352, (60, 65, 528, 176)),
    "p361_fig15.2": (361, (60, 78, 528, 208)),
}


def trim(path, pad=12):
    im = Image.open(path).convert("RGB")
    px = im.load()
    w, h = im.size
    xs, ys = [], []
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            if r < 246 or g < 246 or b < 246:
                xs.append(x); ys.append(y)
    if not xs:
        return
    box = (max(0, min(xs) - pad), max(0, min(ys) - pad),
           min(w, max(xs) + pad), min(h, max(ys) + pad))
    im.crop(box).save(path)


doc = fitz.open(PDF)
os.makedirs(OUT, exist_ok=True)
for name, (page, box) in CLIPS.items():
    pix = doc[page + 20].get_pixmap(dpi=300, clip=fitz.Rect(*box))
    path = os.path.join(OUT, name + ".png")
    pix.save(path)
    trim(path)
    im = Image.open(path)
    print(name, im.size, os.path.getsize(path) // 1024, "KB")
