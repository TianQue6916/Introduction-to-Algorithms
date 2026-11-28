# -*- coding: utf-8 -*-
"""Three teaching figures for CLRS chunk09 (p323-362).
Each figure = one canvas, two panels (left object view / right parameter view).
  G1  §14.1  OS-SELECT rank 17 in 4 steps vs 17-step inorder scan
  G2  §14.3  interval tree prunes a subtree that low-endpoint sort cannot
  G3  §13.4  RB-DELETE-FIXUP <= 3 rotations, iterations << lg n

usage:  python teach_figs.py static   -> fig_g1.png fig_g2.png fig_g3.png (16x7.2 @110dpi)
        python teach_figs.py frames   -> frames_g{1,2,3}/fNNN.png (1600x900)
"""
import json
import math
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle

plt.rcParams["font.family"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

BLUE = "#0072B2"
ORANGE = "#E69F00"
GREEN = "#009E73"
VERM = "#D55E00"
GREY = "#888888"
LIGHT = "#EDEDED"

# ---------------------------------------------------------------- tree helper


def layout(tree, root):
    """tree: key -> (left, right, line1, line2). Returns key -> (x, depth)."""
    pos = {}
    counter = [0]

    def walk(k, d):
        if k is None:
            return
        left, right = tree[k][0], tree[k][1]
        walk(left, d + 1)
        pos[k] = (counter[0], -d)
        counter[0] += 1
        walk(right, d + 1)

    walk(root, 0)
    return pos


def draw_tree(ax, tree, root, pos, node_r=0.34, fs=10.5, hl=(), hl_edges=(),
              dim=(), xs=1.0, ys=0.95, labels=None, colors=None,
              xoff=0.0, yoff=0.0, edge_w=1.4):
    """Draw a binary tree. hl = highlighted keys, hl_edges = set of (a,b)."""
    xs_ = [p[0] for p in pos.values()]
    x0, x1 = min(xs_), max(xs_)
    for k, (x, y) in pos.items():
        left, right = tree[k][0], tree[k][1]
        for ch in (left, right):
            if ch is None:
                continue
            cx, cy = pos[ch]
            on = (k, ch) in hl_edges
            ax.plot([x * xs + xoff, cx * xs + xoff],
                    [y * ys + yoff, cy * ys + yoff],
                    color=BLUE if on else "#444444",
                    lw=(3.0 if on else edge_w), zorder=1,
                    solid_capstyle="round")
    for k, (x, y) in pos.items():
        cx, cy = x * xs + xoff, y * ys + yoff
        lab = labels[k] if labels else (tree[k][2] if len(tree[k]) > 2 else str(k))
        face = "#FFFFFF"
        if colors and k in colors:
            face = colors[k]
        elif k in hl:
            face = "#CFE4F5"
        elif k in dim:
            face = LIGHT
        ax.add_patch(Circle((cx, cy), node_r, facecolor=face,
                            edgecolor=BLUE if k in hl else "#333333",
                            lw=(2.2 if k in hl else 1.0), zorder=3))
        lines = lab.split("\n")
        for i, line in enumerate(lines):
            dy = 0.165 - i * 0.33 if len(lines) == 2 else 0.0
            ax.text(cx, cy + dy * (node_r / 0.34), line, ha="center",
                    va="center", fontsize=fs, zorder=4, color="#111111")
    ax.set_aspect("equal")
    ax.axis("off")
    return (x0 * xs + xoff - node_r, x1 * xs + xoff + node_r)


# ---------------------------------------------------------------- G1 数据
# 20-node order-statistic tree; OS-SELECT(T.root, 17) visits 13 -> 14 -> 16 -> 18
G1_TREE = {
    13: (6, 14, "13\n20"), 6: (3, 9, "6\n12"), 3: (1, 4, "3\n5"),
    1: (None, 2, "1\n2"), 4: (None, 5, "4\n2"), 9: (7, 11, "9\n6"),
    7: (None, 8, "7\n2"), 11: (10, 12, "11\n3"), 2: (None, None, "2\n1"),
    5: (None, None, "5\n1"), 8: (None, None, "8\n1"), 10: (None, None, "10\n1"),
    12: (None, None, "12\n1"),
    14: (None, 16, "14\n7"), 16: (15, 18, "16\n6"), 15: (None, None, "15\n1"),
    18: (None, 19, "18\n4"), 19: (None, 20, "19\n3"), 20: (None, 21, "20\n2"),
    21: (None, None, "21\n1"),
}
G1_LABELS = {k: v[2] for k, v in G1_TREE.items()}
G1_PATH = [13, 14, 16, 18]
G1_POS = layout(G1_TREE, 13)


def g1_left(ax, step):
    """step: how many nodes of the select path are already consumed (0..4)."""
    n = 4
    show = G1_PATH[:step]
    edges = {(G1_PATH[i], G1_PATH[i + 1]) for i in range(max(0, step - 1))}
    # 前 17 个结点（中序）标灰，表示线性扫描要走的结点数
    order = sorted(G1_POS, key=lambda k: G1_POS[k][0])
    scanned = int(round(step / n * 17))
    dim = set(order[:scanned]) - set(show)
    draw_tree(ax, G1_TREE, 13, G1_POS, hl=show, hl_edges=edges, dim=dim,
              node_r=0.34, fs=8.6, xs=1.10, ys=0.95)
    ax.set_title("order-statistic tree：结点写「key / size」\n"
                 "OS-SELECT(T.root, 17) 已经走过的结点数：%d 步" % len(show),
                 fontsize=11.5, color=BLUE, pad=6)


def g1_right(ax, step, scanned):
    n = [2 ** (0.05 * i) for i in range(0, 121)]      # 2 .. 64
    ax.plot(n, n, color=VERM, lw=2.2, label="不带 size：中序遍历 17 个结点")
    ax.plot(n, [math.log2(v + 1) for v in n], color=BLUE, lw=2.2,
            label=r"带 size：至多 $\lceil \lg(n+1)\rceil$ 步")
    ax.set_xscale("log")
    ax.set_xlim(2, 64); ax.set_ylim(0, 22)
    ax.set_xlabel("树的结点数 n（对数轴）", fontsize=10.5)
    ax.set_ylabel("访问的结点数", fontsize=10.5)
    ax.grid(alpha=0.25)
    steps = min(4, max(1, step))
    ax.plot([20], [steps], "o", ms=11, color=BLUE, zorder=5)
    ax.plot([20], [scanned if scanned else 1], "o", ms=11, color=VERM, zorder=5)
    ax.annotate("n=20：%d 步" % steps, (20, steps), textcoords="offset points",
                xytext=(8, 8), fontsize=11, color=BLUE,
                bbox=dict(fc="white", ec="none", alpha=0.9, pad=1.5))
    ax.annotate("n=20：%d 步" % max(1, scanned), (20, max(1, scanned)),
                textcoords="offset points", xytext=(8, -14), fontsize=11,
                color=VERM, bbox=dict(fc="white", ec="none", alpha=0.9, pad=1.5))
    ax.legend(fontsize=9.5, loc="upper left", framealpha=0.95)
    ax.set_title("同一棵树、同一个秩 17：\\lg n 与 n 的差距",
                 fontsize=11.5, color=BLUE, pad=6)


# ---------------------------------------------------------------- G2 数据
G2_DATA = {  # low -> (low, high, max, left, right)
    8.0: (8, 9, 18, 5.0, 15.0),
    5.0: (5, 8, 10, 0.0, 6.0),
    0.0: (0, 3, 3, None, None),
    6.0: (6, 10, 10, None, None),
    15.0: (15, 18, 18, None, 16.4),
    16.4: (16.4, 16.7, 16.9, 16.2, 16.6),
    16.2: (16.2, 16.5, 16.5, 16.0, None),
    16.0: (16.0, 16.3, 16.3, 15.8, None),
    15.8: (15.8, 16.1, 16.1, None, None),
    16.6: (16.6, 16.9, 16.9, None, None),
}


def _lab(v):
    lo, hi = v[0], v[1]
    f = lambda z: ("%g" % z)
    return "[%s,%s]\n%d" % (f(lo), f(hi), v[2])


G2_TREE = {k: (v[3], v[4], _lab(v)) for k, v in G2_DATA.items()}
G2_POS = layout(G2_TREE, 8.0)
G2_PATH = [8.0, 15.0]
G2_QUERY = (17.0, 19.0)
# 按左端点由近及远：前 5 个都比 [15,18] 更靠近 17，但都不与 q 重叠
G2_NEAR = [(16.6, 16.9), (16.4, 16.7), (16.2, 16.5), (16.0, 16.3),
           (15.8, 16.1), (15, 18)]


def g2_left(ax, probe):
    show = G2_PATH[:probe] if probe else []
    edges = {(G2_PATH[0], G2_PATH[1])} if probe >= 2 else set()
    skipped = {0.0, 5.0, 6.0}
    far = {15.8, 16.0, 16.2, 16.4, 16.6}
    draw_tree(ax, G2_TREE, 8.0, G2_POS, hl=show, hl_edges=edges,
              dim=(skipped | far) if probe >= 2 else (),
              node_r=0.40, fs=7.6, xs=1.05, ys=1.0)
    ax.set_title("interval tree：结点写「区间 / max（子树里最大的高端点）」\n"
                 "查询 q = [17,19]：probe %d" % max(1, probe),
                 fontsize=11.5, color=BLUE, pad=6)
    if probe >= 2:
        ax.text(0.5, -0.02,
                "x.left.max = 10 < 17 → 左子树 3 个区间被剪掉；"
                "右子树的 5 个「更近」区间根本没访问",
                transform=ax.transAxes, ha="center", fontsize=10,
                color=VERM, bbox=dict(fc="white", ec=VERM, lw=0.8, pad=3))


def g2_right(ax, probe):
    ax.set_xlim(14.55, 19.5); ax.set_ylim(0, 5.2)
    ax.axhline(0.35, color="#333333", lw=1.2)
    for xx in range(15, 20):
        ax.plot([xx, xx], [0.30, 0.40], color="#333333", lw=1.0)
        ax.text(xx, 0.12, str(xx), ha="center", fontsize=9, color="#333333")
    ax.axvspan(G2_QUERY[0], G2_QUERY[1], ymin=0.20, ymax=0.96, color=ORANGE,
               alpha=0.30, zorder=0)
    ax.text((G2_QUERY[0] + G2_QUERY[1]) / 2, 5.05, "查询 q=[17,19]",
            ha="center", fontsize=10.5, color=VERM)
    for i, (lo, hi) in enumerate(G2_NEAR):
        y = 4.55 - i * 0.72
        hit = lo <= G2_QUERY[1] and hi >= G2_QUERY[0]
        on = (i == probe - 1)
        col = GREEN if hit else (VERM if on else GREY)
        ax.plot([lo, hi], [y, y], color=col, lw=(7.0 if on else 3.0),
                solid_capstyle="butt", zorder=3 if on else 2)
        for e in (lo, hi):
            ax.plot([e, e], [y - 0.10, y + 0.10], color=col, lw=1.8)
        tag = "第 %d 近：%s" % (i + 1, "重叠" if hit else "不重叠")
        ax.text(14.62, y, tag, fontsize=9.5, va="center", ha="left",
                color=GREEN if hit else "#333333")
    ax.set_title("按左端点由近到远逐个试：前 5 个都不重叠，第 6 个才重叠",
                 fontsize=11.5, color=BLUE, pad=6)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)


# ---------------------------------------------------------------- G3 数据
RB = json.load(open("rb_measure.json"))


def case_tree(ax, kind, cx, cy, s=1.0):
    """One schematic case: two 3-node sketches linked by an arrow."""
    def node(x, y, txt, dark=False):
        ax.add_patch(Circle((x, y), 0.33 * s, facecolor="#222222" if dark else "white",
                            edgecolor="#333333", lw=1.2, zorder=3))
        ax.text(x, y, txt, ha="center", va="center", fontsize=9,
                color="white" if dark else "#111111", zorder=4)

    def link(a, b, w=1.2, col="#333333", dashed=False):
        ax.plot([a[0], b[0]], [a[1], b[1]], color=col, lw=w,
                ls="--" if dashed else "-", zorder=2)

    def tri(x, y):
        ax.add_patch(plt.Polygon([[x - 0.28 * s, y - 0.22 * s], [x + 0.28 * s, y - 0.22 * s],
                                  [x, y + 0.2 * s]], facecolor=LIGHT,
                                 edgecolor="#666666", lw=1.0, zorder=2))

    if kind == 1:      # w 红：左旋 x.p，循环继续
        node(cx - 1.9 * s, cy + 0.9 * s, "B", True); node(cx - 1.9 * s, cy, "A")
        node(cx - 0.85 * s, cy, "D")                 # w 红
        link((cx - 1.9 * s, cy + 0.9 * s), (cx - 1.9 * s, cy))
        link((cx - 1.9 * s, cy + 0.9 * s), (cx - 0.85 * s, cy))
        tri(cx - 2.45 * s, cy - 0.55 * s); tri(cx - 1.35 * s, cy - 0.55 * s)
        tri(cx - 1.25 * s, cy - 0.55 * s); tri(cx - 0.45 * s, cy - 0.55 * s)
        ax.annotate("", xy=(cx + 0.55 * s, cy + 0.45 * s),
                    xytext=(cx - 0.1 * s, cy + 0.45 * s),
                    arrowprops=dict(arrowstyle="->", lw=1.6, color=BLUE))
        ax.text(cx + 0.22 * s, cy + 0.68 * s, "左旋 x.p（1 次）", ha="center",
                fontsize=9, color=BLUE)
        node(cx + 1.45 * s, cy + 0.9 * s, "D"); node(cx + 1.45 * s, cy, "B", True)
        node(cx + 2.5 * s, cy, "E", True)
        link((cx + 1.45 * s, cy + 0.9 * s), (cx + 1.45 * s, cy))
        link((cx + 1.45 * s, cy + 0.9 * s), (cx + 2.5 * s, cy))
        ax.text(cx + 2.25 * s, cy - 0.9 * s, "→ 落入 Case 2/3/4", fontsize=8.5,
                color="#444444")
    elif kind == 2:    # w 黑、两子黑：0 次旋转，x 上移
        node(cx - 1.5 * s, cy + 0.8 * s, "B", True); node(cx - 1.5 * s, cy, "A")
        node(cx - 0.6 * s, cy, "D", True)
        link((cx - 1.5 * s, cy + 0.8 * s), (cx - 1.5 * s, cy))
        link((cx - 1.5 * s, cy + 0.8 * s), (cx - 0.6 * s, cy))
        tri(cx - 1.05 * s, cy - 0.55 * s); tri(cx - 0.15 * s, cy - 0.55 * s)
        ax.annotate("", xy=(cx + 0.5 * s, cy + 0.4 * s), xytext=(cx - 0.05 * s, cy + 0.4 * s),
                    arrowprops=dict(arrowstyle="->", lw=1.6, color=GREY))
        ax.text(cx + 0.2 * s, cy + 0.62 * s, "0 次旋转", ha="center", fontsize=9,
                color=GREY)
        node(cx + 1.3 * s, cy + 0.8 * s, "B", True)
        node(cx + 0.85 * s, cy - 0.05 * s, "D")
        node(cx + 1.8 * s, cy - 0.05 * s, "E")
        link((cx + 1.3 * s, cy + 0.8 * s), (cx + 0.85 * s, cy - 0.05 * s))
        link((cx + 1.3 * s, cy + 0.8 * s), (cx + 1.8 * s, cy - 0.05 * s))
        ax.text(cx + 1.4 * s, cy - 1.0 * s, "x ← x.p，循环继续", fontsize=8.5,
                color="#444444")
    elif kind == 3:    # 右旋 w，转 Case 4
        node(cx - 1.6 * s, cy + 0.85 * s, "B", True); node(cx - 1.6 * s, cy, "A")
        node(cx - 0.7 * s, cy, "D", True); node(cx - 1.15 * s, cy - 0.75 * s, "C")
        link((cx - 1.6 * s, cy + 0.85 * s), (cx - 1.6 * s, cy))
        link((cx - 1.6 * s, cy + 0.85 * s), (cx - 0.7 * s, cy))
        link((cx - 0.7 * s, cy), (cx - 1.15 * s, cy - 0.75 * s))
        ax.annotate("", xy=(cx + 0.35 * s, cy + 0.45 * s), xytext=(cx - 0.2 * s, cy + 0.45 * s),
                    arrowprops=dict(arrowstyle="->", lw=1.6, color=BLUE))
        ax.text(cx + 0.08 * s, cy + 0.68 * s, "右旋 w（1 次）", ha="center",
                fontsize=9, color=BLUE)
        node(cx + 1.15 * s, cy + 0.85 * s, "B", True); node(cx + 1.15 * s, cy, "C", True)
        node(cx + 2.05 * s, cy - 0.05 * s, "D")
        link((cx + 1.15 * s, cy + 0.85 * s), (cx + 1.15 * s, cy))
        link((cx + 1.15 * s, cy + 0.85 * s), (cx + 2.05 * s, cy - 0.05 * s))
        ax.text(cx + 1.5 * s, cy - 1.0 * s, "→ 转 Case 4", fontsize=8.5,
                color="#444444")
    else:              # 左旋 x.p，结束
        node(cx - 1.5 * s, cy + 0.85 * s, "B", True); node(cx - 1.5 * s, cy, "A")
        node(cx - 0.55 * s, cy, "D", True); node(cx - 0.05 * s, cy - 0.8 * s, "E", True)
        link((cx - 1.5 * s, cy + 0.85 * s), (cx - 1.5 * s, cy))
        link((cx - 1.5 * s, cy + 0.85 * s), (cx - 0.55 * s, cy))
        link((cx - 0.55 * s, cy), (cx - 0.05 * s, cy - 0.8 * s))
        ax.annotate("", xy=(cx + 0.5 * s, cy + 0.45 * s), xytext=(cx - 0.05 * s, cy + 0.45 * s),
                    arrowprops=dict(arrowstyle="->", lw=1.6, color=GREEN))
        ax.text(cx + 0.22 * s, cy + 0.68 * s, "左旋 x.p（1 次）", ha="center",
                fontsize=9, color=GREEN)
        node(cx + 1.35 * s, cy + 0.85 * s, "D")
        node(cx + 0.85 * s, cy, "B", True); node(cx + 1.9 * s, cy, "E", True)
        link((cx + 1.35 * s, cy + 0.85 * s), (cx + 0.85 * s, cy))
        link((cx + 1.35 * s, cy + 0.85 * s), (cx + 1.9 * s, cy))
        ax.text(cx + 1.6 * s, cy - 1.05 * s, "x ← T.root，循环结束", fontsize=8.5,
                color="#444444")


def g3_left(ax, t):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    cells = [(0.00, 0.53, "(a) Case 1：w 红 → 左旋 x.p", 1),
             (0.50, 0.53, "(b) Case 2：w 黑、两子黑 → 0 次", 2),
             (0.00, 0.02, "(c) Case 3：w.left 红 → 右旋 w", 3),
             (0.50, 0.02, "(d) Case 4：w.right 红 → 左旋 x.p", 4)]
    for x, y, title, kind in cells:
        sub = ax.inset_axes([x, y, 0.49, 0.43])
        sub.set_xlim(-2.95, 2.95); sub.set_ylim(-1.5, 1.75)
        sub.axis("off")
        sub.set_title(title, fontsize=9.2, color="#222222", pad=1)
        case_tree(sub, kind, 0.0, 0.15, 0.82)
    ax.text(0.5, -0.02, "合计旋转 ≤ 1（Case 1）+ 1（Case 3）+ 1（Case 4）= 3 次",
            ha="center", va="bottom", fontsize=10, color=VERM)


def g3_right(ax, t):
    ns = [d["n"] for d in RB]
    ax.set_xscale("log", base=2)
    ax.plot(ns, [d["ceil_lg"] for d in RB], color=GREY, lw=2.0, ls="--",
            label=r"$\lceil \lg(n+1)\rceil$：while 循环步数上界")
    ax.plot(ns, [d["max_iters"] for d in RB], "o-", color=BLUE, ms=8, lw=2.0,
            label="实测最大修复步数（每 n 跑 120–300 棵树）")
    ax.plot(ns, [d["max_rot"] for d in RB], "s-", color=VERM, ms=8, lw=2.0,
            label="实测最大旋转次数（恒为 3）")
    ax.set_ylim(0, 12)
    ax.set_xlabel("结点数 n（对数轴）", fontsize=10.5)
    ax.set_ylabel("删除一次的开销", fontsize=10.5)
    ax.grid(alpha=0.25, which="both")
    ax.legend(fontsize=9, loc="upper left", framealpha=0.95)
    ax.set_title("实测：修复步数远在 lg n 之下，旋转次数始终撞到 3 这个上界",
                 fontsize=11.5, color=BLUE, pad=6)


# ---------------------------------------------------------------- 组装


def build(kind, t):
    if kind == 1:
        fig = plt.figure(figsize=(16, 9), dpi=100)
        axL = fig.add_axes([0.03, 0.06, 0.46, 0.80])
        axR = fig.add_axes([0.56, 0.16, 0.40, 0.60])
        step = 4 if t >= 1 else int(round(t * 4))
        g1_left(axL, step)
        g1_right(axR, step, int(round(t * 17)))
        fig.text(0.5, 0.955, "秩 17 只要 4 步：size 字段把 n 步压到 lg(n+1) 步",
                 ha="center", fontsize=17, color="#111111")
        fig.add_artist(plt.Line2D([0.5, 0.5], [0.05, 0.90], color="#E6E6E6", lw=2))
    elif kind == 2:
        fig = plt.figure(figsize=(16, 9), dpi=100)
        axL = fig.add_axes([0.03, 0.10, 0.44, 0.72])
        axR = fig.add_axes([0.52, 0.10, 0.45, 0.72])
        probe = 2 if t >= 1 else 1 + int(round(t))
        g2_left(axL, probe)
        g2_right(axR, probe)
        fig.text(0.5, 0.955, "区间树 2 次比较就命中：5 个左端点更近的区间一个都没访问",
                 ha="center", fontsize=17, color="#111111")
        fig.add_artist(plt.Line2D([0.5, 0.5], [0.06, 0.90], color="#E6E6E6", lw=2))
    else:
        fig = plt.figure(figsize=(16, 9), dpi=100)
        axL = fig.add_axes([0.02, 0.05, 0.47, 0.78])
        axR = fig.add_axes([0.55, 0.14, 0.42, 0.64])
        g3_left(axL, t)
        g3_right(axR, t)
        fig.text(0.5, 0.955, "红黑树删除的修复最多 3 次旋转，而 BST 删除本身只改常数个指针",
                 ha="center", fontsize=17, color="#111111")
        fig.add_artist(plt.Line2D([0.5, 0.5], [0.05, 0.90], color="#E6E6E6", lw=2))
    return fig


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "static"
    if mode == "static":
        for k in (1, 2, 3):
            fig = build(k, 1.0)
            fig.subplots_adjust(left=0.02, right=0.98, top=0.90, bottom=0.06)
            fig.savefig("fig_g%d.png" % k, dpi=110, facecolor="white")
            plt.close(fig)
            print("fig_g%d.png" % k, os.path.getsize("fig_g%d.png" % k) // 1024, "KB")
    else:
        import numpy as np
        N = 25
        for k in (1, 2, 3):
            os.makedirs("frames_g%d" % k, exist_ok=True)
            for i in range(N):
                fig = build(k, i / (N - 1))
                fig.savefig("frames_g%d/f%03d.png" % (k, i), dpi=100,
                            facecolor="white")
                plt.close(fig)
            print("frames_g%d" % k, N, "frames")


if __name__ == "__main__":
    main()
