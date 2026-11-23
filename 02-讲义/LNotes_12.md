# Lecture 12: Bellman-Ford（Bellman-Ford 算法）

> Introduction to Algorithms: 6.006，Massachusetts Institute of Technology
> Instructors: Erik Demaine, Jason Ku, and Justin Solomon

---

## Previously（回顾）

- Weighted graphs（加权图）、shortest-path weight（最短路径权重）、negative-weight cycles（负权环）。
- 从 shortest-path weights（最短路径权重）构造 shortest-path tree（最短路径树），耗时 $O(|V| + |E|)$。
- DAG Relaxation：在加权 DAG 上求解 SSSP（single-source shortest paths，单源最短路径）的 algorithm，耗时 $O(|V| + |E|)$。
- 对带 negative weights（负权）的 graph 求解 SSSP：
  - 对所有 $v \in V$ 计算 $\delta(s, v)$；若 $v$ 能通过 negative-weight cycle 到达，则 $\delta(s, v) = -\infty$。
  - 若存在一条从 $s$ 可达的 negative-weight cycle，就返回其中一条。

## Warmups（热身）

- Exercise 1：给定 undirected graph（无向图）$G$，返回 $G$ 是否含 negative-weight cycle。
- Solution：只要 $G$ 中存在一条 negative weight 的 edge，就返回 Yes，耗时 $O(|E|)$ :O
- 所以本节 lecture 把讨论限制在 directed graphs（有向图）上。

- Exercise 2：给定一个在 $O(|V|(|V| + |E|))$ 时间内运行的 SSSP algorithm $A$，说明如何用它把 SSSP 解到 $O(|V||E|)$ 时间。
- Solution：先跑 BFS 或 DFS，找出从 $s$ 可达的 vertices，耗时 $O(|E|)$。
  - 对每个从 $s$ 不可达的 vertex $v$，置 $\delta(s, v) = \infty$，耗时 $O(|V|)$。
  - 构造 graph $G' = (V', E')$，只保留从 $s$ 可达的 vertices，耗时 $O(|V| + |E|)$。
  - 在 $G'$ 上从 $s$ 运行 $A$。
  - $G'$ 是 connected（连通的），于是 $|V'| = O(|E'|) = O(|E|)$，因此 $A$ 的运行时间为 $O(|V||E|)$。

- 今天，我们要找出一个具有同样 running time、却对 general graphs（一般图）都成立的 SSSP algorithm！

| Graph（图） | Weights（权重） | Name（算法名） | Running Time $O(\cdot)$ | Lecture |
|---|---|---|---|---|
| General | Unweighted | BFS | $\lvert V \rvert + \lvert E \rvert$ | L09 |
| DAG | Any | DAG Relaxation | $\lvert V \rvert + \lvert E \rvert$ | L11 |
| General | Any | Bellman-Ford | $\lvert V \rvert \cdot \lvert E \rvert$ | L12（Today!） |
| General | Non-negative | Dijkstra | $\lvert V \rvert \log \lvert V \rvert + \lvert E \rvert$ | L13 |

† 原 PDF 该表为合并单元格，文字层顺序错乱、行列对应关系残缺；上表的 Graph / Weights / Lecture 三列由 L09–L13 的课程顺序与各 algorithm 的前提条件推定重建。

## Simple Shortest Paths（简单最短路径）

- 若 graph 含 cycles 且有 negative weights，就可能含 negative-weight cycles :(
- 若 graph 不含 negative-weight cycles，那么 shortest paths 都是 simple（简单的）！
- Claim 1：若 $\delta(s, v)$ 有限，则存在一条到 $v$ 的 shortest path 是 simple 的。
- Proof：用 contradiction（反证法）。
  - 假设不存在 simple 的 shortest path；令 $\pi$ 为 vertices 数最少的那个 shortest path。
  - $\pi$ 不是 simple 的，故 $\pi$ 中存在 cycle $C$；$C$ 的 weight 非负（否则 $\delta(s, v) = -\infty$）。
  - 从 $\pi$ 中删去 $C$，得到 path $\pi'$，其 vertices 更少且 weight $w(\pi') \le w(\pi)$。

- 由于 simple paths 不能重复 vertices，有限的 shortest paths 至多含 $|V| - 1$ 条 edges。

## Negative Cycle Witness（负环见证点）

- k-Edge Distance（k 边距离）$\delta_k(s, v)$：从 $s$ 到 $v$、使用至多 $k$ 条 edges 的任意 path 的最小 weight。
- Idea！对所有 $v \in V$ 计算 $\delta_{|V|-1}(s, v)$ 与 $\delta_{|V|}(s, v)$。
  - 若 $\delta(s, v) \ne -\infty$，则 $\delta(s, v) = \delta_{|V|-1}(s, v)$，因为 shortest path 是 simple 的（或者根本不存在）。
  - 若 $\delta_{|V|}(s, v) < \delta_{|V|-1}(s, v)$：
    - 说明存在一条更短的 non-simple path 到 $v$，于是 $\delta_{|V|}(s, v) = -\infty$。
    - 称这样的 $v$ 为一个 (negative cycle) witness（负环见证点）。
  - 然而，也可能有些 vertices 的 shortest-path weight 为 $-\infty$，却并不是 witness。
- Claim 2：若 $\delta(s, v) = -\infty$，则 $v$ 从某个 witness 可达。
- Proof：只需证明：每条从 $s$ 可达的 negative-weight cycle 都含有一个 witness。

```math
\sum_{v \in C} \delta_{|V|}(s, v) \le \sum_{v \in C} \delta_{|V|-1}(s, v') + \sum_{v \in C} w(v', v) < \sum_{v \in C} \delta_{|V|-1}(s, v)
```

  - 考虑一条从 $s$ 可达的 negative-weight cycle $C$。
  - 对 $v \in C$，令 $v' \in C$ 表示 $v$ 在 $C$ 上的 predecessor（前驱），其中 $\sum_{v \in C} w(v', v) < 0$。
  - 于是 $\delta_{|V|}(s, v) \le \delta_{|V|-1}(s, v') + w(v', v)$（右端是某条 vertices 数不超过 $|V|$ 的 path 的 weight）。
  - 把上式对 $C$ 上所有 $v$ 求和，即得上方的块级不等式。
  - 若 $C$ 中不含 witness，则对所有 $v \in C$ 都有 $\delta_{|V|}(s, v) \ge \delta_{|V|-1}(s, v)$，矛盾。

## Bellman-Ford（Bellman-Ford 算法）

- Idea！使用 graph duplication（图复制）：把 graph 复制成多份 copy（或称 level，层）。
- $|V| + 1$ 个 levels：level $k$ 中的 vertex $v_k$ 表示「从 $s$ 出发、用至多 $k$ 条 edges 到达 vertex $v$」。
- 若 edges 只能让 level 上升，得到的 graph 就是一个 DAG！

- 从 $G = (V, E)$ 构造新的 DAG $G' = (V', E')$：
  - $G'$ 有 $|V|(|V| + 1)$ 个 vertices：对每个 $v \in V$ 与 $k \in \{0, \dots, |V|\}$ 有一个 $v_k$。
  - $G'$ 有 $|V|(|V| + |E|)$ 条 edges：
    - 对每个 $v \in V$、$k \in \{1, \dots, |V|\}$，有 $|V|$ 条 weight 为零的 edge $(v_{k-1}, v_k)$；
    - 对每条 $(u, v) \in E$、$k \in \{1, \dots, |V|\}$，有 $|V|$ 条 weight 为 $w(u, v)$ 的 edge $(u_{k-1}, v_k)$。

- 在 $G'$ 上从 $s_0$ 运行 DAG Relaxation，计算所有 $v_k \in V'$ 的 $\delta(s_0, v_k)$。
- 对每个 vertex：置 $d(s, v) = \delta(s_0, v_{|V|-1})$。
- 对每个满足 $\delta(s_0, u_{|V|}) < \delta(s_0, u_{|V|-1})$ 的 witness $u \in V$：
  - 对每个从 $u$ 在 $G$ 中可达的 vertex $v$：置 $d(s, v) = -\infty$。

## Example（例子）

[Figure 1：左侧为原图 $G$，含 vertices $a, b, c, d$；edges 与 weights：$a \to b$ 为 $-5$，$b \to c$ 为 $6$（figure 中亦有 $6$ 标在 $a$ 附近）、$b \to d$ 为 $-4$、$c \to d$ 为 $-1$、$a \to c$ 为 $3$。右侧为 graph duplication 后的 $G'$，共 $|V| + 1 = 5$ 层，每层含 $a_k, b_k, c_k, d_k$，层间 edge 分两类：$(v_{k-1}, v_k)$ weight 为 $0$，$(u_{k-1}, v_k)$ weight 为 $w(u, v)$。原图 edge 方向与具体权重在文字层中有残缺，上述权重以图中可见标注为准。]

- 下表为 $\delta(a_0, v_k)$，即从 $a_0$ 出发到第 $k$ 层各 vertex 的 k-Edge Distance：

| $k \backslash v$ | $a$ | $b$ | $c$ | $d$ |
|---|---|---|---|---|
| 0 | 0 | $\infty$ | $\infty$ | $\infty$ |
| 1 | 0 | $-5$ | $6$ | $\infty$ |
| 2 | 0 | $-5$ | $-9$ | $9$ |
| 3 | 0 | $-5$ | $-9$ | $-6$ |
| 4 | 0 | $-7$ | $-9$ | $-6$ |

- 最终得到的 $\delta(a, v)$：

| $v$ | $a$ | $b$ | $c$ | $d$ |
|---|---|---|---|---|
| $\delta(a, v)$ | 0 | $-\infty$ | $-\infty$ | $-\infty$ |

† 原 PDF 中该两表的部分数值与负号在文字层中错位、缺行；上表按 $G'$ 的 level 语义（$\delta_k(s, v) = \min\{\delta_{k-1}(s, v), \min_{(u,v) \in E}\{\delta_{k-1}(s, u) + w(u, v)\}\}$）逐层递推重建。

## Correctness（正确性）

- Claim 3：对所有 $v \in V$ 与 $k \in \{0, \dots, |V|\}$，有 $\delta(s_0, v_k) = \delta_k(s, v)$。
- Proof：对 $k$ 做 induction（归纳）。
  - Base case：当 $k = 0$ 时对所有 $v \in V$ 成立（从 $s_0$ 可达的 $v_0$ 只有 $v = s$）。
  - Inductive Step：假设对所有 $k < k_0$ 成立，证明 $k = k_0$ 时成立。

```math
\begin{aligned}
\delta(s_0, v_{k_0}) &= \min\bigl(\{\delta(s_0, u_{k_0-1}) + w(u_{k_0-1}, v_{k_0}) \mid u_{k_0-1} \in Adj^-(v_{k_0})\} \cup \{\delta(s_0, v_{k_0-1})\}\bigr) \\
&= \min\bigl(\{\delta_{k_0-1}(s, u) + w(u, v) \mid u \in Adj^-(v)\} \cup \{\delta_{k_0-1}(s, v)\}\bigr) \quad \text{(by induction)} \\
&= \delta_{k_0}(s, v)
\end{aligned}
```

- Claim 4：Bellman-Ford 结束时，$d(s, v) = \delta(s, v)$。
- Proof：由 Claim 3，它正确地算出了所有 $v \in V$ 的 $\delta_{|V|-1}(s, v)$ 与 $\delta_{|V|}(s, v)$。
  - 若 $\delta(s, v) \ne -\infty$，则正确地置 $d(s, v) = \delta_{|V|-1}(s, v) = \delta(s, v)$。
  - 随后把从 witness 可达的任何 $v$ 置为 $d(s, v) = -\infty$；由 Claim 2 这是正确的。

## Running Time（运行时间）

- $G'$ 的规模为 $O(|V|(|V| + |E|))$，构造它的时间同阶。
- 在 $G'$ 上运行 DAG Relaxation 的时间与 $G'$ 的规模成线性。
- 对每个从 witness 可达的 vertex 做 $O(1)$ 的工作。
- 求 witness 的可达性耗时 $O(|E|)$，而 witness 至多 $O(|V|)$ 个，故为 $O(|V||E|)$。
- （另一种做法：用一个 super node（超级结点）$x$ 以 $0$-weight edges 连到所有 witnesses，再从 $x$ 做线性搜索。）
- 一开始就把 $G$ 剪枝成从 $s$ 可达的 subgraph，可得到 $O(|V||E|)$ 时间的 algorithm。

## Extras: Return Negative-Weight Cycle or Space Optimization（附加：返回负权环或空间优化）

- Claim 5：对任何 witness $v$，最短的 $s_0$–$v_{|V|}$ path $\pi$ 在 $G$ 中含有一个 negative-weight cycle。
- Proof：由于 $\pi$ 含 $|V| + 1$ 个 vertices，它在 $G$ 中必然至少含一个 cycle $C$。
  - $C$ 的 weight 为负（否则删去 $C$ 可得到 vertices 更少、且 $w(\pi') \le w(\pi)$ 的 path $\pi'$，与 $v$ 是 witness 矛盾）。

- 只需 $O(|V|)$ 的 space（空间）：对每个 $k$ 从 $1$ 到 $|V|$，只保存 $\delta(s_0, v_{k-1})$ 与 $\delta(s_0, v_k)$。
- 传统上，Bellman-Ford 对每个 vertex 只存一个值，在 $|V|$ 轮中尝试 relax 每条 edge；但这些估计值并不对应 k-Edge Distances，所以分析更棘手。
- 不过这些 space optimizations 就不再能返回 negative weight cycle 了。
