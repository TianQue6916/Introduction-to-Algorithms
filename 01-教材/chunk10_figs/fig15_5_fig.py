import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import *
import matplotlib.patches as mpatches
from math import log2, exp

OUT = os.path.dirname(os.path.abspath(__file__))
P = [0.15, 0.10, 0.05, 0.10, 0.20]
Q = [0.05, 0.10, 0.05, 0.05, 0.05, 0.10]
N = len(P)
NR = 12

def opt_bst(p, q):
    n = len(p)
    e = [[0.0] * (n + 2) for _ in range(n + 2)]
    w = [[0.0] * (n + 2) for _ in range(n + 2)]
    root = [[0] * (n + 2) for _ in range(n + 2)]
    for i in range(1, n + 2):
        e[i][i - 1] = q[i - 1]; w[i][i - 1] = q[i - 1]
    for l in range(1, n + 1):
        for i in range(1, n - l + 2):
            j = i + l - 1
            w[i][j] = w[i][j - 1] + p[j - 1] + q[j]
            e[i][j] = 1e18
            for r in range(i, j + 1):
                t = e[i][r - 1] + e[r + 1][j] + w[i][j]
                if t < e[i][j]:
                    e[i][j] = t; root[i][j] = r
    return e, w, root

def build(root, i, j):
    if i > j: return None
    r = root[i][j]
    return (r, build(root, i, r - 1), build(root, r + 1, j))

def cost(t, p, q, d=0):
    if t is None: return 0.0
    r, L, R = t
    c = p[r - 1] * (d + 1)
    c += cost(L, p, q, d + 1) + cost(R, p, q, d + 1)
    if L is None: c += q[r - 1] * (d + 2)
    if R is None: c += q[r] * (d + 2)
    return c

def greedy_bst(p, q, i, j):
    # 按位置中位数建树（忽略频率，只求平衡）
    if i > j: return None
    r = (i + j) // 2
    return (r, greedy_bst(p, q, i, r - 1), greedy_bst(p, q, r + 1, j))

e, w, root = opt_bst(P, Q)
topt = build(root, 1, N)
tgr = greedy_bst(P, Q, 1, N)
c_opt, c_gr = cost(topt, P, Q), cost(tgr, P, Q)
print('book opt', round(c_opt, 4), 'greedy', round(c_gr, 4), 'e[1,5]', round(e[1][5], 4))

def nl_count(t):
    if t is None: return 0
    return 1 + nl_count(t[1]) + nl_count(t[2])

def draw_bst(t, ax, x0, x1, y, dy, color):
    if t is None: return
    r, L, R = t
    nl, nr = nl_count(L), nl_count(R)
    xm = x0 + (x1 - x0) * (nl + 1) / (nl + nr + 1)
    for ch, xx0, xx1 in ((L, x0, xm), (R, xm, x1)):
        if ch is not None:
            mm = nl_count(ch[1]) + 1
            tt = nl_count(ch) + 1
            xc = xx0 + (xx1 - xx0) * mm / tt
            ax.plot([xm, xc], [y, y - dy], color='#AAAAAA', lw=1.3, zorder=1)
    ax.add_patch(mpatches.Circle((xm, y), 0.19, facecolor=color, edgecolor='white', zorder=3))
    ax.text(xm, y, 'k%d' % r, ha='center', va='center', fontsize=10, color='white', zorder=4)
    draw_bst(L, ax, x0, xm, y - dy, dy, color)
    draw_bst(R, ax, xm, x1, y - dy, dy, color)

fig, axL, axR = two_panel(
    '§15.5 最优 BST 的期望代价由频率分布决定，尺度是熵 $H$ 而不是 $\\lg n$',
    '左：书上的 5 键例子，最优 2.75，按位置中位数建树 2.95；右：12 个键、频率按 $e^{-\lambda i}$ 偏斜时，最优代价 3.25→1.54 而贪心 3.25→3.22（$\lambda=3$ 时贵 2.09 倍）')
axL.set_title('$p=\\langle .15,.10,.05,.10,.20\\rangle$，$q=\\langle .05,.10,.05,.05,.05,.10\\rangle$', fontsize=12.5, pad=8)
axL.set_xlim(-0.6, 2.6); axL.set_ylim(-2.9, 1.0)
axL.set_aspect('equal'); axL.axis('off')
draw_bst(topt, axL, 0.0, 1.0, 0.5, 0.72, BLUE)
draw_bst(tgr, axL, 1.4, 2.4, 0.5, 0.72, VERM)
axL.text(0.5, -2.55, '最优：%.2f' % c_opt, ha='center', fontsize=13.5, color=BLUE, fontweight='bold')
axL.text(1.9, -2.55, '中位数贪心：%.2f' % c_gr, ha='center', fontsize=13.5, color=VERM, fontweight='bold')

def entropy(p, q):
    h = 0.0
    for x in list(p) + list(q):
        if x > 0: h -= x * log2(x)
    return h

lams = np.linspace(0, 3.0, 31)
oc, gc, hs = [], [], []
for lam in lams:
    wv = np.array([exp(-lam * i) for i in range(NR)])
    pv = (0.9 * wv / wv.sum()).tolist()
    qv = [0.1 / (NR + 1)] * (NR + 1)
    ee, _, rr = opt_bst(pv, qv)
    oc.append(ee[1][NR])
    gc.append(cost(greedy_bst(pv, qv, 1, NR), pv, qv))
    hs.append(entropy(pv, qv))
print('lam0 opt/greedy/H', round(oc[0], 3), round(gc[0], 3), round(hs[0], 3))
print('lam3 opt/greedy/H', round(oc[-1], 3), round(gc[-1], 3), round(hs[-1], 3), 'ratio', round(gc[-1] / oc[-1], 3))
print('lg12', round(log2(NR), 3))

axR.plot(lams, oc, color=BLUE, lw=2.8, label='最优 BST 的期望代价')
axR.plot(lams, gc, color=VERM, lw=2.8, label='中位数贪心 BST 的期望代价')
axR.plot(lams, hs, color=GREEN, lw=2.4, ls='--', label='熵 $H$（比特）')
axR.axhline(log2(NR), color=GREY, ls=':', lw=1.8)
axR.text(1.55, log2(NR) + 0.05, '$\\lg 12 = 3.58$', fontsize=12, color=GREY)
axR.set_xlabel('频率偏斜度 $\\lambda$（$p_i \\propto e^{-\\lambda(i-1)}$，$n=12$）', fontsize=13)
axR.set_ylabel('期望搜索代价', fontsize=13)
axR.set_ylim(0.9, 4.45)
axR.grid(alpha=0.3, ls=':')
axR.legend(fontsize=12, loc='lower left', framealpha=0.95)
axR.annotate('$\\lambda=3$：贪心 %.2f，最优 %.2f\n贪心贵 %.2f 倍；$H$ = %.2f' % (gc[-1], oc[-1], gc[-1] / oc[-1], hs[-1]),
             xy=(3.0, gc[-1]), xytext=(1.20, 4.02), fontsize=12.5,
             bbox=dict(facecolor='white', edgecolor=LGREY, boxstyle='round,pad=0.5'),
             arrowprops=dict(arrowstyle='->', color=GREY, lw=1.4))
fig.savefig(os.path.join(OUT, 'fig15_5_two_panel.png'), dpi=100)
print('png', os.path.getsize(os.path.join(OUT, 'fig15_5_two_panel.png')))

def render(t):
    lam = t * 3.0
    m = max(1, int(round(1 + t * 30)))
    axR.clear()
    axR.plot(lams[:m], oc[:m], color=BLUE, lw=2.8)
    axR.plot(lams[:m], gc[:m], color=VERM, lw=2.8)
    axR.plot(lams[:m], hs[:m], color=GREEN, lw=2.4, ls='--')
    axR.axhline(log2(NR), color=GREY, ls=':', lw=1.8)
    axR.set_xlim(0, 3.05); axR.set_ylim(0, max(gc) * 1.12)
    axR.set_xlabel('频率偏斜度 $\\lambda$'); axR.set_ylabel('期望搜索代价')
    axR.grid(alpha=0.3, ls=':')
    axR.axvline(lam, color=GREY, ls='--', lw=1.3)
    axR.text(0.03, 0.95, '$\\lambda$ = %.2f\n最优 %.3f / 贪心 %.3f\n$H$ = %.3f' % (lam, oc[m - 1], gc[m - 1], hs[m - 1]),
             transform=axR.transAxes, fontsize=12.5, va='top',
             bbox=dict(facecolor='white', edgecolor=LGREY, boxstyle='round,pad=0.45'))
    axR.legend(['最优', '贪心', '熵 $H$'], fontsize=12, loc='lower right')

print('gif', frames_to_gif(fig, render, np.linspace(0, 1, 26), os.path.join(OUT, 'fig15_5_dual.gif')))
