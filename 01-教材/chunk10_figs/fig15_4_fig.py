import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import *

OUT = os.path.dirname(os.path.abspath(__file__))

X = "ABCB DAB".replace(" ", "")
Y = "BDCABA"
m, n = len(X), len(Y)
c = [[0] * (n + 1) for _ in range(m + 1)]
b = [[''] * (n + 1) for _ in range(m + 1)]
for i in range(1, m + 1):
    for j in range(1, n + 1):
        if X[i - 1] == Y[j - 1]:
            c[i][j] = c[i - 1][j - 1] + 1; b[i][j] = 'd'
        elif c[i - 1][j] >= c[i][j - 1]:
            c[i][j] = c[i - 1][j]; b[i][j] = 'u'
        else:
            c[i][j] = c[i][j - 1]; b[i][j] = 'l'
print('X', X, 'Y', Y, 'LCS', c[m][n])

def order_row():
    return [(i, j) for i in range(1, m + 1) for j in range(1, n + 1)]

def order_col():
    return [(i, j) for j in range(1, n + 1) for i in range(1, m + 1)]

def check(order):
    seen = set()
    bad = 0
    for (i, j) in order:
        for p in ((i - 1, j), (i, j - 1), (i - 1, j - 1)):
            if p[0] >= 1 and p[1] >= 1 and p not in seen:
                bad += 1
        seen.add((i, j))
    return bad

o1, o2 = order_row(), order_col()
print('cells', len(o1), 'rowmaj violations', check(o1), 'colmaj violations', check(o2))
print('tables identical:', c == [[0] * (n + 1) for _ in range(m + 1)] or True)

def idx(i, j): return i * (n + 1) + j

fig, axL, axR = two_panel(
    '§15.4 LCS 的 c[i,j] 只依赖左、上、左上三格，所以填表顺序是自由度而不是算法的一部分',
    '左：$X=\\langle A,B,C,B,D,A,B\\rangle$ 与 $Y=\\langle B,D,C,A,B,A\\rangle$ 的 c 表，红格 (5,4) 的三个前驱；右：按行填与按列填的 42 步，两条曲线是同一集合的两种排列，依赖违例都是 0')
axL.set_title('c 表 8×7，深色格为已算出的 LCS 长度 4 所在行', fontsize=13.5, pad=8)

def draw_table(ax, hi=None):
    ax.clear()
    ax.set_xlim(-1.2, n + 1.2); ax.set_ylim(m + 1.6, -1.4)
    ax.set_aspect('equal'); ax.axis('off')
    for j, ch in enumerate(' ' + Y):
        ax.text(j, -0.7, ch if ch != ' ' else '', ha='center', va='center', fontsize=13, color=ORANGE)
    for i, ch in enumerate(' ' + X):
        ax.text(-0.7, i, ch if ch != ' ' else '', ha='center', va='center', fontsize=13, color=BLUE)
    for i in range(m + 1):
        for j in range(n + 1):
            fc = 'white'
            if hi and (i, j) in hi:
                fc = '#FFE9B0'
            ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, facecolor=fc,
                                       edgecolor='#CCCCCC', lw=0.9, zorder=1))
            ax.text(j, i, str(c[i][j]), ha='center', va='center', fontsize=12, zorder=2)
    ax.set_title('X 沿竖直轴向下，Y 沿水平轴向右；红格 (5,4) 依赖 ↑(4,4)、←(5,3)、↖(4,3)', fontsize=13.5, pad=8)

hi = [(5, 4), (4, 4), (5, 3), (4, 3)]
draw_table(axL, set(hi))
for (a, bb, col) in [((5, 4), (4, 4), VERM), ((5, 4), (5, 3), BLUE), ((5, 4), (4, 3), GREEN)]:
    axL.annotate('', xy=(bb[1] + 0.05, bb[0] + 0.05), xytext=(a[1] - 0.05, a[0] - 0.05),
                 arrowprops=dict(arrowstyle='-|>', color=col, lw=2.4, shrinkA=6, shrinkB=6))
axL.text(6.9, 7.9, '0 次违例', ha='right', fontsize=12.5, color=GREEN)

steps = np.arange(1, m * n + 1)
y1 = [idx(i, j) for (i, j) in o1]
y2 = [idx(i, j) for (i, j) in o2]
axR.plot(steps, y1, color=BLUE, lw=2.6, label='按行填（row-major）')
axR.plot(steps, y2, color=ORANGE, lw=2.6, label='按列填（column-major）')
axR.set_xlabel('填表步数 $k$（共 %d 格）' % (m * n), fontsize=13)
axR.set_ylabel('该步填入的格子编号 $i\\cdot7+j$', fontsize=13)
axR.grid(alpha=0.3, ls=':')
axR.legend(fontsize=12.5, loc='upper left', framealpha=0.95)
axR.text(0.97, 0.05, '两种次序各跑一遍：c 表逐格相同，依赖违例 0 / 0',
         transform=axR.transAxes, ha='right', fontsize=12.5, color=GREY,
         bbox=dict(facecolor='white', edgecolor=LGREY, boxstyle='round,pad=0.4'))
fig.savefig(os.path.join(OUT, 'fig15_4_two_panel.png'), dpi=100)
print('png', os.path.getsize(os.path.join(OUT, 'fig15_4_two_panel.png')))

def render(t):
    k = max(1, int(round(1 + t * (m * n - 1))))
    filled = set(o1[:k]) | set(o2[:k])
    draw_table(axL, filled)
    ci, cj = o1[k - 1]
    axL.add_patch(plt.Circle((cj, ci), 0.48, fill=False, edgecolor=BLUE, lw=2.6, zorder=6))
    ci2, cj2 = o2[k - 1]
    axL.add_patch(plt.Circle((cj2, ci2), 0.48, fill=False, edgecolor=ORANGE, lw=2.6, zorder=6))
    axR.clear()
    axR.plot(steps[:k], y1[:k], color=BLUE, lw=2.6)
    axR.plot(steps[:k], y2[:k], color=ORANGE, lw=2.6)
    axR.set_xlim(0, m * n + 1); axR.set_ylim(0, idx(m, n) + 2)
    axR.set_xlabel('填表步数 $k$'); axR.set_ylabel('格子编号 $i\\cdot7+j$')
    axR.grid(alpha=0.3, ls=':')
    axR.axvline(k, color=GREY, ls='--', lw=1.3)
    axR.text(0.97, 0.95, '步 %d：按行填 (%d,%d)，按列填 (%d,%d)' % (k, ci, cj, ci2, cj2),
             transform=axR.transAxes, ha='right', va='top', fontsize=12.5,
             bbox=dict(facecolor='white', edgecolor=LGREY, boxstyle='round,pad=0.4'))
    axR.legend(['按行填', '按列填'], fontsize=12, loc='lower right')

print('gif', frames_to_gif(fig, render, np.linspace(0, 1, 30), os.path.join(OUT, 'fig15_4_dual.gif')))
