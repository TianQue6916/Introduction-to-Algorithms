import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np, os, io
from PIL import Image

# Okabe-Ito 色盲友好调色板
BLUE   = '#0072B2'
ORANGE = '#E69F00'
GREEN  = '#009E73'
VERM   = '#D55E00'
PURPLE = '#CC79A7'
SKY    = '#56B4E9'
YELLOW = '#F0E442'
GREY   = '#666666'
LGREY  = '#DDDDDD'

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 13
plt.rcParams['savefig.facecolor'] = 'white'


def two_panel(title, sub):
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(16, 7.6), dpi=100,
                                   gridspec_kw={'width_ratios': [1, 1]})
    fig.subplots_adjust(left=0.055, right=0.985, top=0.80, bottom=0.10, wspace=0.20)
    fig.text(0.055, 0.935, title, fontsize=21, fontweight='bold', color='#111111')
    fig.text(0.055, 0.885, sub, fontsize=13, color=GREY)
    fig.add_artist(Line2D([0.505, 0.505], [0.075, 0.85], color=LGREY, lw=2.5,
                          transform=fig.transFigure))
    fig.text(0.28, 0.845, '对象视角', fontsize=12, color=BLUE, ha='center')
    fig.text(0.735, 0.845, '参数视角', fontsize=12, color=ORANGE, ha='center')
    return fig, axL, axR


def frames_to_gif(fig, render, tvals, outgif, fps=8, colors=64):
    tmp = outgif + '_frames'
    os.makedirs(tmp, exist_ok=True)
    paths = []
    for i, t in enumerate(tvals):
        render(t)
        p = os.path.join(tmp, 'f%03d.png' % i)
        fig.savefig(p, dpi=100)
        paths.append(p)
    ims = [Image.open(p).convert('P', palette=Image.ADAPTIVE, colors=colors) for p in paths]
    ims[0].save(outgif, save_all=True, append_images=ims[1:], duration=int(1000 / fps),
                loop=0, optimize=True)
    for p in paths:
        os.remove(p)
    os.rmdir(tmp)
    return os.path.getsize(outgif)
