# Lecture 13: Dijkstra's Algorithm（Dijkstra 算法）

> Introduction to Algorithms: 6.006，Massachusetts Institute of Technology
> Instructors: Erik Demaine, Jason Ku, and Justin Solomon

---

## Review（回顾）

- Weighted graphs（加权图）上的 Single-Source Shortest Paths（单源最短路径，SSSP）。
- 此前：对权重较小的非负图或 DAG，有 $O(|V| + |E|)$ 时间的 algorithms。
- 上次课：Bellman-Ford，对 general graphs（一般图）且允许 negative weights（负权）时耗时 $O(|V||E|)$。
- 今天：对 general graphs 且 edge weights 非负，即对任意 $e \in E$ 有 $w(e) \ge 0$ 的情形，做到更快 —— $O(|V| \log |V| + |E|)$。

| Graph（图） | Weights（权重） | SSSP Algorithm | Running Time $O(\cdot)$ | Lecture |
|---|---|---|---|---|
| General | Unweighted | BFS | $\lvert V \rvert + \lvert E \rvert$ | L09 |
| DAG | Any | DAG Relaxation | $\lvert V \rvert + \lvert E \rvert$ | L11 |
| General | Any | Bellman-Ford | $\lvert V \rvert \cdot \lvert E \rvert$ | L12 |
| General | Non-negative | Dijkstra | $\lvert V \rvert \log \lvert V \rvert + \lvert E \rvert$ | L13（Today!） |

† 原 PDF 该表为合并单元格，文字层中行列顺序被打散、Lecture 一列只留下 L09/L11/L12/L13 四个孤立标签；上表的对应关系按课程顺序与各 algorithm 的适用前提推定重建。

## Non-negative Edge Weights（非负边权）

- Idea！把 BFS 的思路推广到 weighted graphs：
  - 以 source（源点）$s$ 为球心，生长一个 sphere（球面）。
  - 反复先探索较近的 vertices，再探索较远的。
  - 但若事先不知道 distances，怎么知道哪些 vertices 更近呢？:(
- Observation 1：若 weights 非负，则沿 shortest path 的 distance 单调递增。
  - 即：若 vertex $u$ 出现在从 $s$ 到 $v$ 的某条 shortest path 上，则 $\delta(s, u) \le \delta(s, v)$。
  - 令 $V_x \subset V$ 为从 $s$ 出发 distance $\le x$ 可达的 vertex 子集。
  - 若 $v \in V_x$，则从 $s$ 到 $v$ 的任何 shortest path 只含 $V_x$ 中的 vertices。
  - 也许可以每次只把一个 vertex 加入 $V_x$！（但若 weights 很大，对每个 $x$ 都生长一次会很慢。）
- Observation 2：如果已经知道 vertices 按到 $s$ 的 distance 递增的 order（顺序），就能很快解出 SSSP。
  - 删掉逆着这个 order 走的 edges（它们不可能参与 shortest paths）。
  - 若存在 zero-weight edges，仍可能有 cycles：把它们反复 collapse（收缩）成单个 vertex。
  - 然后用 DAG relaxation 在 $O(|V| + |E|)$ 时间内算出每个 $v \in V$ 的 $\delta(s, v)$。

## Dijkstra's Algorithm（Dijkstra 算法）

- 以荷兰著名 computer scientist（计算机科学家）Edsger Dijkstra 命名（其实原拼写是 Dÿkstra！）。
- Idea！按到 source $s$ 的 distance 递增的顺序，从每个 vertex relax 它的 edges。
- Idea！用 data structure（数据结构）高效地找出 order 中的下一个 vertex。
- Changeable Priority Queue（可改键优先队列）$Q$：item 带 key 与唯一 ID，支持以下 operations：

| Operation | 含义 |
|---|---|
| `Q.build(X)` | 用 iterator $X$ 中的 items 初始化 $Q$ |
| `Q.delete_min()` | 删除 key 最小的 item |
| `Q.decrease_key(id, k)` | 找到 ID 为 `id` 的 item，把 key 改成 $k$ |

- 实现方式：把一个 Priority Queue $Q'$ 与一个 Dictionary（字典）$D$ cross-link（交叉链接），$D$ 把 IDs 映射到 $Q'$ 中的位置。
- 假设 vertex IDs 是 $0$ 到 $|V| - 1$ 的整数，于是 $D$ 可以用 direct access array（直接访问数组）。
- 为简洁起见，称 item $x$ 是 tuple（元组）$(x.id, x.key)$。
- 对所有 $v \in V$ 置 $d(s, v) = \infty$，再置 $d(s, s) = 0$。
- 用每个 vertex $v \in V$ 的 item $(v, d(s, v))$ 构造 changeable priority queue $Q$。
- 当 $Q$ 非空时，从 $Q$ 中删掉 $d(s, u)$ 最小的 item $(u, d(s, u))$：
  - 对 $u$ 的 outgoing adjacencies（出邻接）$Adj^+(u)$ 中的每个 vertex $v$：
    - 若 $d(s, v) > d(s, u) + w(u, v)$：
      - Relax edge $(u, v)$，即置 $d(s, v) = d(s, u) + w(u, v)$。
      - 把 $Q$ 中 $v$ 的 key 降到新的估计值 $d(s, v)$。
- 在示例图上运行 Dijkstra。

## Example（例子）

[Figure 1：左侧为加权有向图 $G$，vertices 为 $s, a, b, c, d$；可见 edge weights 包括 $s \to a$ 为 $10$、$s \to c$ 为 $3$、$s \to b$ 为 $1$、$a \to b$ 为 $4$、$a \to d$ 为 $5$、$b \to c$ 为 $2$、$b \to d$ 为 $7$、$c \to d$ 为 $5$、$d \to$ 其他为 $8$ 等；原 PDF 中 edge 与 weight 的文字层严重错位，上述读法按图中箭头与数字位置判读，具体权重以原图为准。右侧为一张按「从 $Q$ 中 Delete 的 vertex 顺序」排列的 $d(s, v)$ 更新表，行方向为 $v = s, a, b, c, d$。]

- 示例的 $\delta(s, v)$ 最终值可由下表读取（列对应每一步从 $Q$ 中 delete 的 vertex，最后一行为稳定后的 $d(s, v)$）：

| $v$ | $s$ | $a$ | $b$ | $c$ | $d$ |
|---|---|---|---|---|---|
| $\delta(s, v)$ | 0 | 7 | 9 | 3 | 10 |

† 该表的列头（Delete $v$ from $Q$ 的先后）与中间状态在 PDF 文字层中互相穿插、无法逐格对齐；上表按 Dijkstra 在示例图上的实际执行顺序推定重建，中间更新过程见原文插图。

## Correctness（正确性）

- Claim：Dijkstra's algorithm 结束时，对所有 $v \in V$ 有 $d(s, v) = \delta(s, v)$。
- Proof：
  - 若某次 relaxation 把 $d(s, v)$ 置为 $\delta(s, v)$，那么 algorithm 结束时 $d(s, v) = \delta(s, v)$。
    - Relaxation 只会让估计值 $d(s, v)$ 减小。
    - Relaxation 是 safe（安全的），即始终保证每个 $d(s, v)$ 是某条到 $v$ 的 path 的 weight（或 $\infty$）。
  - 只需证明：当 vertex $v$ 从 $Q$ 中被取出时，$d(s, v) = \delta(s, v)$。
    - 对从 $Q$ 中取出的前 $k$ 个 vertices 做 induction（归纳）。
    - Base case（$k = 1$）：$s$ 是第一个从 $Q$ 中取出的 vertex，且 $d(s, s) = 0 = \delta(s, s)$。
    - Inductive Step：假设对 $k < k_0$ 成立，考察第 $k_0$ 个从 $Q$ 中取出的 vertex $v_0$。
    - 考察从 $s$ 到 $v_0$ 的某条 shortest path $\pi$，满足 $w(\pi) = \delta(s, v_0)$。
    - 令 $(x, y)$ 为 $\pi$ 中第一条 $y$ 不属于前 $k_0 - 1$ 个 vertices 的 edge（可能有 $y = v_0$）。
    - 当 $x$ 从 $Q$ 中被取出时，由 induction 有 $d(s, x) = \delta(s, x)$，于是：

```math
\begin{aligned}
d(s, y) &\le \delta(s, x) + w(x, y) && \text{取出 } x \text{ 时 relax 了 edge } (x, y) \\
&= \delta(s, y) && \text{shortest path 的 subpath 仍是 shortest path} \\
&\le \delta(s, v_0) && \text{edge weights 非负} \\
&\le d(s, v_0) && \text{relaxation 是 safe 的} \\
&\le d(s, y) && v_0 \text{ 是 } Q \text{ 中 } d(s, v_0) \text{ 最小的 vertex}
\end{aligned}
```

    - 于是 $d(s, v_0) = \delta(s, v_0)$，证毕。

## Running Time（运行时间）

- 统计 changeable priority queue $Q$ 上的 operations，假设它含 $n$ 个 items：

| Operation | 时间 | Dijkstra 中的出现次数 |
|---|---|---|
| `Q.build(X)`（$n = \lvert X \rvert$） | $B_n$ | $1$ |
| `Q.delete_min()` | $M_n$ | $\lvert V \rvert$ |
| `Q.decrease_key(id, k)` | $D_n$ | $\lvert E \rvert$ |

- 总 running time 为 $O(B|V| + |V| \cdot M|V| + |E| \cdot D|V|)$。
- 假设已把 graph 剪枝成只含从 source 可达的 vertices，于是 $|V| = O(|E|)$。

| Priority Queue $Q'$ | `build(X)` | `delete_min()` | `decrease_key(id, k)` | Dijkstra $O(\cdot)$，$n = \lvert V \rvert = O(\lvert E \rvert)$ |
|---|---|---|---|---|
| Array | $n$ | $n$ | $1$ | $\lvert V \rvert^2$ |
| Binary Heap | $n$ | $\log n$ (a) | $\log n$ | $\lvert E \rvert \log \lvert V \rvert$ |
| Fibonacci Heap | $n$ | $\log n$ (a) | $1$ (a) | $\lvert E \rvert + \lvert V \rvert \log \lvert V \rvert$ |

- 若 graph 是 dense（稠密的），即 $|E| = \Theta(|V|^2)$，用 Array 作 $Q'$ 可得 $O(|V|^2)$ 时间。
- 若 graph 是 sparse（稀疏的），即 $|E| = \Theta(|V|)$，用 Binary Heap 作 $Q'$ 可得 $O(|V| \log |V|)$ 时间。
- Fibonacci Heap 在理论上对所有情形都好，但在实践中用得不多。
- 6.006 不讨论 Fibonacci Heaps（细节见 6.854 或 CLRS 第 19 章）。
- 做理论题时，应假设 Dijkstra 运行时间为 $O(|E| + |V| \log |V|)$。

## Summary: Weighted Single-Source Shortest Paths（小结：加权单源最短路径）

| Graph | Weights | SSSP Algorithm | Running Time $O(\cdot)$ |
|---|---|---|---|
| General | Unweighted | BFS | $\lvert V \rvert + \lvert E \rvert$ |
| DAG | Any | DAG Relaxation | $\lvert V \rvert + \lvert E \rvert$ |
| General | Non-negative | Dijkstra | $\lvert V \rvert \log \lvert V \rvert + \lvert E \rvert$ |
| General | Any | Bellman-Ford | $\lvert V \rvert \cdot \lvert E \rvert$ |

- 那么 All-Pairs Shortest Paths（全对最短路径）呢？
- 把某个 SSSP algorithm 跑 $|V|$ 次其实已经相当不错，因为 output 的规模就是 $O(|V|^2)$。
- 对带 negative weights 的 general graphs，还能做得比 $|V| \cdot O(|V| \cdot |E|)$ 更好（下次课！）。
