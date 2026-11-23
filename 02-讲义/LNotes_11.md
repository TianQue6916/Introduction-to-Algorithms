# Lecture 11: Weighted Shortest Paths（带权最短路径）

> Introduction to Algorithms: 6.006，Massachusetts Institute of Technology
> Instructors: Erik Demaine, Jason Ku, and Justin Solomon

---

## Review（回顾）

- Single-Source Shortest Paths：用 BFS，$O(|V| + |E|)$ 时间（给每个 vertex 返回 distance）。
- Single-Source Reachability：用 BFS 或 DFS，$O(|E|)$ 时间（只返回可达的 vertices）。
- Connected components：用 Full-BFS 或 Full-DFS，$O(|V| + |E|)$ 时间。
- DAG 的 Topological Sort：用 Full-DFS，$O(|V| + |E|)$ 时间。
- 此前 distance 的定义是「path 上 edges 的条数」；今天要把 distance 这个概念推广。

## Weighted Graphs（带权图）

- weighted graph（带权图）是 graph $G = (V, E)$ 外加一个 weight function（权函数）$w : E \to \mathbb{Z}$。
- 也就是说，给每条 edge $e = (u, v) \in E$ 指定一个 integer weight（整数权）：$w(e) = w(u, v)$。
- graph 中 edge weights 的应用非常多：
  - road network 中的 distances（距离）。
  - network connections 中的 latency（延迟）。
  - social network 中关系的 strength（强度）。
- 计算上有两种常见的表示 weights 的方式：
  - 内嵌在 graph representation 里：在 adjacency lists 中把 edge weight 与每个 vertex 一起存。
  - 另存一个 Set data structure，把每条 edge 映射到它的 weight。
- 我们假设所用的表示支持在 $O(1)$ 时间内查询一条 edge 的 weight。

## Examples（示例图）

[Figure 1：原文给出两个带权示例图 $G_1$ 与 $G_2$，共用 vertices $\{a, b, c, d, e, f, g, h\}$。文字层抽出的 weight 数值依次为 $6, 8, -2, 5, 9, -5, 7, 3, 2, -1, -4, 1, 4$，但这些数值与具体 edge 的对应关系在矢量图里、未进入文字层，故此处不臆造边集。后文提到 $G_1$ 中含负权环 $(b, f, g, c, b)$，$G_2$ 是一个 DAG（DAG Relaxation 的例子在 $G_2$ 上从 $a$ 出发跑）]

## Restrictions（各种 SSSP algorithm 的适用条件）

| Graph | Weights | SSSP Algorithm | Running Time $O(\cdot)$ | Lecture |
|---|---|---|---|---|
| General | Unweighted | BFS | $\lvert V\rvert + \lvert E\rvert$ | L09 |
| General | Any | （本讲不给通用解）$^†$ | — | L11（今天） |
| DAG | Any | DAG Relaxation | $\lvert V\rvert + \lvert E\rvert$ | L11 |
| General | Any | Bellman-Ford | $\lvert V\rvert\cdot\lvert E\rvert$ | L12 |
| General | Non-negative | Dijkstra | $\lvert V\rvert\log\lvert V\rvert + \lvert E\rvert$ | L13 |

> 表注：原 PDF 这张表用合并单元格排版，文字层只能抽出 `L11 (Today!)` / `L12` / `L13` 三行的 lecture 编号与部分行列名，`Restrictions` 两列（Graph / Weights）的配对关系有残缺。上表的行列配对按 6.006 的课程安排重建，其中「General / Any」一行的算法名为空，标 `†` 表明这是推定：本讲只解决 DAG 与部分特殊情形，通用情形留到 L12 的 Bellman-Ford。

## Weighted Paths（带权路径）

- weighted graph 中 path $\pi$ 的 weight $w(\pi)$ 是 path 上所有 edges 的 weights 之和。
- 从 $s \in V$ 到 $t \in V$ 的（带权）shortest path 就是从 $s$ 到 $t$ 的 weight 最小的 path。
- $\delta(s, t) = \inf\{w(\pi) \mid \pi \text{ 是从 } s \text{ 到 } t \text{ 的 path}\}$ 是从 $s$ 到 $t$ 的 shortest-path weight。
- （在 weighted graphs 里，常用 "distance" 指 shortest-path weight，而不再指 edges 的条数。）
- 与 unweighted graphs 一样：
  - 若从 $s$ 到 $t$ 没有 path，则 $\delta(s, t) = \infty$。
  - shortest paths 的 subpaths（子路径）也是 shortest paths（否则可以把更短的那一段 splice 进去）。
- 为什么定义里用 infimum 而不是 minimum？因为可能存在**不存在**有限长最小 weight path 的情形。
- 什么时候会发生？当 graph 里存在 negative-weight cycle（负权环）时，例如 $G_1$ 中的 $(b, f, g, c, b)$。
- 一个 negative-weight cycle 是一条起点与终点为同一 vertex 且 $w(\pi) < 0$ 的 path $\pi$。
- 若从 $s$ 到 $t$ 的某条 path 经过了负权环上的某个 vertex，则 $\delta(s, t) = -\infty$。
- 一旦出现这种情形，我们想要的不再是 shortest path，而可能是那个 negative-weight cycle 本身。
- 这条区分是本质性的：**有负权环时，问题从「求最小值」变成了「检测最小值不存在」**。所以后面所有 algorithm 都必须先处理这个前提。

## Weighted Shortest Paths Algorithms（带权最短路算法概览）

- 接下来四讲讲的是在 weighted graphs 中求 shortest-path weights 的 algorithms。
- （先不管 parent pointers：算完 distance 之后可以在线性时间内重建 shortest paths tree，见下一页。）
- 我们已经会一个 algorithm 了：Breadth-First Search！它在下列情形跑 $O(|V| + |E|)$ 时间：
  - graph 的 weights 全为正，且所有 weights 都相同。
  - graph 的 weights 全为正，且所有 weights 之和至多 $O(|V| + |E|)$。
- 对 general weighted graphs，我们不知道如何在 $O(|V| + |E|)$ 时间内解决 SSSP。
- 但如果你的 graph 是 Directed Acyclic Graph，你就能做到！

## Shortest-Paths Tree（最短路径树）

- 做 BFS 时我们边搜索边记 parent pointers。另一种做法是**事后**再算它们！
- 若已知所有 vertices $v \in V$ 的 $\delta(s, v)$，就能在 $O(|V| + |E|)$ 时间内构造出 shortest-path tree。
- 对从 $s$ 出发的 weighted shortest paths，只需要为那些 $\delta(s, v)$ 有限的 vertices $v$ 设 parent pointers。
- 初始化空的 $P$，并设 $P(s) = \text{None}$。
- 对每个 $\delta(s, v)$ 有限的 vertex $u \in V$：
  - 对每个 outgoing neighbor $v \in \mathrm{Adj}^+(u)$：
    - 若 $P(v)$ 尚未赋值，且 $\delta(s, v) = \delta(s, u) + w(u, v)$：
      - 说明存在一条经过 edge $(u, v)$ 的 shortest path，于是设 $P(v) = u$。
- 但 parent pointers 可能会绕过 zero weight（零权）的 cycles。要把这种 cycle 上的每个 vertex 标记出来。
- 对每个未标记的 vertex $u \in V$（包括稍后被取消标记的）：
  - 对每个 $v \in \mathrm{Adj}^+(u)$，其中 $v$ 已标记且 $\delta(s, v) = \delta(s, u) + w(u, v)$：
    - 从 $v$ 出发沿 parent pointers 走，把包含 $v$ 的那个 cycle 上的 vertices 取消标记。
    - 设 $P(v) = u$，从而 break（打断）这个 cycle。
- Exercise：证明这个 algorithm 在 linear time 内正确算出 parent pointers。
- 正因为 parent pointers 可以事后补，我们把注意力集中到「怎么算距离」上。

## DAG Relaxation（DAG 松弛）

- Idea！为每个 vertex $v \in V$ 维护一个 distance estimate（距离估计）$d(s, v)$（初值 $\infty$），它始终是真实距离 $\delta(s, v)$ 的上界，然后逐步下调，直到 $d(s, v) = \delta(s, v)$。
- 什么时候下调？当某条 edge 违反了 triangle inequality（三角不等式）时！
- Triangle Inequality：从 $u$ 到 $v$ 的 shortest-path weight 不可能大于「从 $u$ 经过另一个 vertex $x$ 到 $v$」的 shortest path，即对所有 $u, v, x \in V$ 有

```math
\delta(u, v) \le \delta(u, x) + \delta(x, v)
```

- 若对某条 edge $(u, v)$ 有 $d(s, v) > d(s, u) + w(u, v)$，则 triangle inequality 被违反了 :(
- 修复办法是把 $d(s, v)$ 下调到 $d(s, u) + w(u, v)$，也就是 relax（松弛）edge $(u, v)$，使那个被违反的约束重新成立。
- Claim：Relaxation 是安全的：它维持「每个 $d(s, v)$ 都是某条到 $v$ 的 path 的 weight（或 $\infty$）」这个性质对所有 $v \in V$ 成立。
- Proof：设对所有 $v_0 \in V$ 都有 $d(s, v_0)$ 是某条 path 的 weight（或 $\infty$）。松弛某条 edge $(u, v)$ 会把 $d(s, v)$ 设为 $d(s, u) + w(u, v)$，而这正是「从 $s$ 经 $u$ 到 $v$ 的某条 path」的 weight。
- 这个「安全」二字是整个 relaxation 框架的支点：它保证 $d$ 永远不低于真值，也就是 $d(s, v) \ge \delta(s, v)$ 恒成立。没有这一条，后面的正确性证明就无法闭合。

### 算法本体

- 先对所有 $v \in V$ 设 $d(s, v) = \infty$，再设 $d(s, s) = 0$。
- 按 $G$ 的某个 topological sort order 依次处理每个 vertex $u$：
  - 对每个 outgoing neighbor $v \in \mathrm{Adj}^+(u)$：
    - 若 $d(s, v) > d(s, u) + w(u, v)$：
      - relax edge $(u, v)$，即设 $d(s, v) = d(s, u) + w(u, v)$。
- 例子：在 $G_2$ 上从 vertex $a$ 跑一遍 DAG Relaxation。

## Correctness（正确性）

- Claim：DAG Relaxation 结束时，对所有 $v \in V$ 有 $d(s, v) = \delta(s, v)$。
- Proof：对 $k$ 做 induction：对 topological order 中前 $k$ 个 vertices $v$ 有 $d(s, v) = \delta(s, v)$。
  - Base case：vertex $s$ 以及 topological order 中排在 $s$ 之前的每个 vertex，在开始时就已经满足 claim。
  - Inductive step：设 claim 对前 $k_0$ 个 vertices 成立，令 $v$ 是第 $k_0 + 1$ 个。
  - 考虑一条从 $s$ 到 $v$ 的 shortest path，令 $u$ 是这条 path 上紧邻 $v$ 之前的那个 vertex。
  - $u$ 在 topological order 中出现在 $v$ 之前，所以由 induction $d(s, u) = \delta(s, u)$。
  - 处理 $u$ 时，$d(s, v)$ 被设成不大于（$\le$）$\delta(s, u) + w(u, v) = \delta(s, v)$ 的值。
  - 但由 relaxation 的安全性有 $d(s, v) \ge \delta(s, v)$，故 $d(s, v) = \delta(s, v)$。
- 另一种证明思路：
  - 对任何 vertex $v$，DAG relaxation 会把 $d(s, v)$ 设成 $\min\{d(s, u) + w(u, v) \mid u \in \mathrm{Adj}^-(v)\}$。
  - 到 $v$ 的 shortest path 必然经过 $v$ 的某个 incoming neighbor $u$。
  - 所以若由 induction 有「对所有 $u \in \mathrm{Adj}^-(v)$ 都 $d(s, u) = \delta(s, u)$」，则 $d(s, v) = \delta(s, v)$。
- 这两条证明的共同前提是「按 topological order 处理」：它保证在处理 $u$ 的时候，$d(s, u)$ 已经不会再变了。这就是 DAG 这个限制换来的全部好处。

## Running Time（运行时间）

- 初始化花 $O(|V|)$ 时间，Topological Sort 花 $O(|V| + |E|)$ 时间。
- 额外的 work 上界是：

```math
O(1)\times\sum_{u\in V}\deg^+(u) = O(|E|)
```

- 总 running time 是线性的，$O(|V| + |E|)$。
- 这个结果本身值得单独强调：**边权可以任意（包括负数），只要图无环，SSSP 仍是线性的**。负权在这里不是问题，因为 DAG 里没有环可以绕回去反复降低距离——这也解释了为什么 L12 的 Bellman-Ford 需要 $|V|\cdot|E|$：它付出的代价就是「在没有 topological order 的情况下，怎样判定谁是下一个该处理的 vertex」。
