import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import *
import matplotlib.patches as mpatches

OUT = os.path.dirname(os.path.abspath(__file__))
P = [30, 35, 15, 5, 10, 20, 25]
N = len(P) - 1

def parens(i, j):
    if i == j:
        return [(i, 0)]
    out = []
    for k in range(i, j):
        for lt, lc in parens(i, k):
            for rt, rc in parens(k + 1, j):
                out.append((('*', lt, rt, k + 1), lc + rc + P[i] * P[k + 1] * P[j + 1]))
    return out

ALL = parens(0, N - 1)
costs = [c for _, c in ALL]
mn, mx = min(costs), max(costs)
tmin = ALL[costs.index(mn)][0]
tmax = ALL[costs.index(mx)][0]

def leaves(t):
    if isinstance(t, int): return 1
    return leaves(t[1]) + leaves(t[2])

def draw(t, ax, x0, x1, y, dy, color):
    if isinstance(t, int):
        x = (x0 + x1) / 2
        ax.add_patch(mpatches.FancyBboxPatch((x - 0.19, y - 0.115), 0.38, 0.23,
                                             boxstyle='round,pad=0.02',
                                             facecolor=SKY, edgecolor='white', zorder=4))
        ax.text(x, y, 'A%d' % (t + 1), ha='center', va='center', fontsize=11, zorder=5)
        return x
    nl, nr = leaves(t[1]), leaves(t[2])
    xm = x0 + (x1 - x0) * nl / (nl + nr)
    xl = draw(t[1], ax, x0, xm, y - dy, dy, color)
    xr = draw(t[2], ax, xm, x1, y - dy, dy, color)
    ax.plot([xm, xl], [y, y - dy], color='#AAAAAA', lw=1.3, zorder=1)
    ax.plot([xm, xr], [y, y - dy], color='#AAAAAA', lw=1.3, zorder=1)
    ax.add_patch(mpatches.Circle((xm, y), 0.095, facecolor=color, edgecolor='white', zorder=4))
    ax.text(xm, y, 'k%d' % t[3], ha='center', va='center', fontsize=9, color='white', zorder=5)
    return xm

def cat(m):
    c = 1
    for i in range(m):
        c = c * (4 * i + 2) // (i + 2)
    return c

PTXT = '$p=\\langle 30,35,15,5,10,20,25\\rangle$'

def left_panel(ax, title=None):
    ax.clear()
    ax.set_xlim(-1.80, 1.80); ax.set_ylim(-1.30, 2.62)
    ax.set_aspect('equal'); ax.axis('off')
    if title: ax.set_title(title, fontsize=14, pad=8)
    draw(tmin, ax, -1.74, -0.26, 2.12, 0.40, BLUE)
    draw(tmax, ax, 0.26, 1.74, 2.12, 0.40, VERM)
    ax.text(-1.00, -0.30, '最优：15125', ha='center', fontsize=13.5, color=BLUE, fontweight='bold')
    ax.text(1.00, -0.30, '最差：58000', ha='center', fontsize=13.5, color=VERM, fontweight='bold')
    ax.annotate('', xy=(0.62, -0.62), xytext=(-0.62, -0.62),
                arrowprops=dict(arrowstyle='<->', color=VERM, lw=2.0))
    ax.text(0.0, -0.52, '3.83×', ha='center', fontsize=13, color=VERM)
    ax.text(0.0, 2.45, '图 15.5(b) 给的 53750 只是 42 种里第二贵，真正最差是 58000',
            ha='center', fontsize=11.5, color=GREY)

fig, axL, axR = two_panel(
    '§15.2 n = 6 的矩阵链有 Catalan(5) = 42 种加括号方式，最优与最差差 3.83 倍',
    '左：同一串 6 个矩阵的两种极端括号化（k 是分割点），代价 15125 与 58000；右：方案数 Catalan(n−1) 与动态规划 O(n³) 在对数轴上分道扬镳')
left_panel(axL, PTXT)

ns = np.arange(4, 101)
cvals = [cat(n - 1) for n in ns]
dvals = [n ** 3 / 3 for n in ns]
axR.plot(ns, cvals, color=VERM, lw=2.8, label='加括号方案数 Catalan$(n-1)$')
axR.plot(ns, dvals, color=BLUE, lw=2.8, label='动态规划基本操作 $n^3/3$')
axR.set_yscale('log'); axR.set_xlabel('矩阵个数 $n$', fontsize=13)
axR.set_ylabel('基本操作次数（对数轴）', fontsize=13)
axR.grid(alpha=0.3, which='both', ls=':'); axR.set_xlim(4, 100)
axR.annotate('$n=6$：42 种 vs 72 次\n$n=100$：$5.7\\times10^{56}$ 种\n vs $3.3\\times10^{5}$ 次',
             xy=(99, cvals[-1]), xytext=(30, 1e22), fontsize=12.5,
             bbox=dict(facecolor='white', edgecolor=LGREY, boxstyle='round,pad=0.5'),
             arrowprops=dict(arrowstyle='->', color=GREY, lw=1.4))
axR.legend(fontsize=12.5, loc='lower right', framealpha=0.95)
fig.savefig(os.path.join(OUT, 'fig15_2_two_panel.png'), dpi=100)
print('png', os.path.getsize(os.path.join(OUT, 'fig15_2_two_panel.png')))
print('schemes', len(ALL), 'min', mn, 'max', mx, 'ratio', round(mx / mn, 3))

def render(t):
    left_panel(axL, 'n = 6 的 42 种括号化（左图固定），右图扫 $n$')
    axR.clear()
    m = max(4, int(round(4 + t * 96)))
    axR.plot(ns[:m - 3], cvals[:m - 3], color=VERM, lw=2.8)
    axR.plot(ns[:m - 3], dvals[:m - 3], color=BLUE, lw=2.8)
    axR.set_yscale('log'); axR.set_ylim(1, 1e60); axR.set_xlim(4, 101)
    axR.set_xlabel('矩阵个数 $n$'); axR.set_ylabel('基本操作次数（对数轴）')
    axR.grid(alpha=0.3, which='both', ls=':')
    axR.axvline(m, color=GREY, ls='--', lw=1.4)
    axR.text(0.03, 0.95, '$n$ = %d\nCatalan$(n-1)$ = %.3e\n$n^3/3$ = %.4g' % (m, cat(m - 1), m ** 3 / 3),
             transform=axR.transAxes, fontsize=13, va='top',
             bbox=dict(facecolor='white', edgecolor=LGREY, boxstyle='round,pad=0.45'))
    axR.legend(['Catalan$(n-1)$', '$n^3/3$'], fontsize=12, loc='lower right')

print('gif', frames_to_gif(fig, render, np.linspace(0, 1, 26), os.path.join(OUT, 'fig15_2_dual.gif')))
