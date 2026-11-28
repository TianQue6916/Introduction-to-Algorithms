import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import *
import matplotlib.patches as mpatches

OUT = os.path.dirname(os.path.abspath(__file__))
COL = [BLUE, ORANGE, GREEN, VERM, PURPLE, SKY]

def build(n, depth=0, parent=None, nodes=None):
    if nodes is None: nodes = []
    idx = len(nodes)
    nodes.append({'lab': n, 'depth': depth, 'parent': parent, 'x': None, 'id': idx})
    if n > 0:
        for c in range(n - 1, -1, -1):
            build(c, depth + 1, idx, nodes)
    return nodes

def layout(nodes):
    for i, nd in enumerate([d for d in nodes if d['lab'] == 0]):
        nd['x'] = i
    for nd in sorted(nodes, key=lambda d: -d['depth']):
        if nd['x'] is None:
            ch = [c for c in nodes if c['parent'] == nd['id']]
            nd['x'] = sum(c['x'] for c in ch) / len(ch)
    return nodes

def draw_tree(ax, n):
    nodes = layout(build(n))
    for nd in nodes:
        if nd['parent'] is not None:
            p = nodes[nd['parent']]
            ax.plot([p['x'], nd['x']], [-p['depth'], -nd['depth']], color='#BBBBBB', lw=1.0, zorder=1)
    for nd in nodes:
        ax.add_patch(mpatches.Circle((nd['x'], -nd['depth']), 0.36, facecolor=COL[nd['lab'] % 6],
                                     edgecolor='white', lw=1.0, zorder=2))
        ax.text(nd['x'], -nd['depth'], str(nd['lab']), ha='center', va='center', fontsize=11,
                color='white' if nd['lab'] in (0, 3, 5) else '#111111', zorder=3)
    w = max(nd['x'] for nd in nodes)
    ax.set_xlim(-0.8, w + 0.8); ax.set_ylim(-n - 0.8, 1.6)
    ax.set_aspect('equal'); ax.axis('off')
    cnt = {}
    for nd in nodes: cnt[nd['lab']] = cnt.get(nd['lab'], 0) + 1
    return cnt, 2 ** n

CALLS = {n: 2 ** n for n in range(1, 41)}
DPS = {n: n * (n + 1) / 2 for n in range(1, 41)}

fig, axL, axR = two_panel(
    '§15.1 朴素 CUT-ROD 要 2ⁿ 次调用，动态规划只要 n²/2 次',
    '左：n = 5 的递归树，同一颜色 = 同一 subproblem（子问题），标签 0 被重复画了 16 次；右：两条曲线在对数轴上差 6 个数量级')
axL.set_title('n = 5：32 次调用，只有 6 个不同的 subproblem', fontsize=14, pad=8, color='#111111')
cnt, tot = draw_tree(axL, 5)
axL.text(0.5, -0.02, '  '.join('%d：%d 次' % (k, v) for k, v in sorted(cnt.items())),
         transform=axL.transAxes, ha='center', fontsize=12.5, color=GREY)

ns = np.arange(1, 41)
axR.plot(ns, [CALLS[n] for n in ns], color=VERM, lw=2.8, label='递归调用次数 $T(n)=2^n$')
axR.plot(ns, [DPS[n] for n in ns], color=BLUE, lw=2.8, label='动态规划迭代次数 $n^2/2$')
axR.set_yscale('log')
axR.set_xlabel('钢条长度 $n$', fontsize=13)
axR.set_ylabel('基本操作次数（对数轴）', fontsize=13)
axR.grid(alpha=0.3, which='both', ls=':')
axR.axvline(30, color=GREY, ls='--', lw=1.5)
axR.annotate('$n=30$：叶结点 $2^{29}=5.4\\times10^{8}$\n总调用 $2^{30}=1.07\\times10^{9}$\n动态规划 $n^2/2=450$\n比值 $1.2\\times10^{6}$',
             xy=(30, 1.07e9), xytext=(7.0, 3.0e5), fontsize=12.5,
             bbox=dict(facecolor='white', edgecolor=LGREY, boxstyle='round,pad=0.5'),
             arrowprops=dict(arrowstyle='->', color=GREY, lw=1.4))
axR.legend(fontsize=12.5, loc='lower right', framealpha=0.95)
fig.savefig(os.path.join(OUT, 'fig15_1_two_panel.png'), dpi=100)
print('png', os.path.getsize(os.path.join(OUT, 'fig15_1_two_panel.png')))
print('n=30 T=', CALLS[30], ' leaves=', 2 ** 29, ' dp=', DPS[30], ' ratio=', CALLS[30] / DPS[30])
print('counts n=5:', dict(sorted(cnt.items())), 'calls', tot)

def render(t):
    axL.clear(); axR.clear()
    nn = int(round(1 + t * 4))
    axL.set_title('n = %d 的递归树（n ≥ 6 时结点已画不下）' % nn, fontsize=14, pad=8)
    c2, t2 = draw_tree(axL, nn)
    axL.text(0.5, -0.02, '  '.join('%d：%d 次' % (k, v) for k, v in sorted(c2.items())),
             transform=axL.transAxes, ha='center', fontsize=12.5, color=GREY)
    m = max(1, int(round(1 + t * 39)))
    axR.plot(ns[:m], [CALLS[x] for x in ns[:m]], color=VERM, lw=2.8)
    axR.plot(ns[:m], [DPS[x] for x in ns[:m]], color=BLUE, lw=2.8)
    axR.set_yscale('log'); axR.set_ylim(1, 1e12); axR.set_xlim(0, 41)
    axR.set_xlabel('钢条长度 $n$'); axR.set_ylabel('基本操作次数（对数轴）')
    axR.grid(alpha=0.3, which='both', ls=':')
    axR.axvline(m, color=GREY, ls='--', lw=1.4)
    axR.text(0.03, 0.95, '$T(n)=2^n$ = %.3e\n$n^2/2$ = %.4g' % (CALLS[m], DPS[m]),
             transform=axR.transAxes, fontsize=13, va='top',
             bbox=dict(facecolor='white', edgecolor=LGREY, boxstyle='round,pad=0.45'))
    axR.legend(['递归调用 $2^n$', '动态规划 $n^2/2$'], fontsize=12, loc='lower right')

print('gif', frames_to_gif(fig, render, np.linspace(0, 1, 26), os.path.join(OUT, 'fig15_1_dual.gif')))
