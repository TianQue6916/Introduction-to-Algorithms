# Lecture 14: Johnson's Algorithm（Johnson 算法）

> Introduction to Algorithms: 6.006，Massachusetts Institute of Technology
> Instructors: Erik Demaine, Jason Ku, and Justin Solomon

---

## Previously（回顾）

| Graph（图） | Weights（权重） | SSSP Algorithm | Running Time $O(\cdot)$ |
|---|---|---|---|
| General | Unweighted | BFS | $\lvert V \rvert + \lvert E \rvert$ |
| DAG | Any | DAG Relaxation | $\lvert V \rvert + \lvert E \rvert$ |
| General | Non-negative | Dijkstra | $\lvert V \rvert \log \lvert V \rvert + \lvert E \rvert$ |
| General | Any | Bellman-Ford | $\lvert V \rvert \cdot \lvert E \rvert$ |

† 原 PDF 该表为合并单元格，文字层中行列被打散、`|V | · |E|` 等项落在表单之外；上表按各 algorithm 的前提条件与 L09–L13 的对应关系推定重建。

## All-Pairs Shortest Paths (APSP)（全对最短路径）

- Input（输入）：directed graph（有向图）$G = (V, E)$，weights（权重）为 $w : E \to \mathbb{Z}$。
- Output（输出）：对所有 $u, v \in V$ 给出 $\delta(u, v)$。
- 若 $G$ 含 negative-weight cycle（负权环），则 abort（中止）。
- 当需要理解整个 network（网络）时这很有用，例如 transportation（交通）、circuit layout（电路布局）、supply chains（供应链）……
- 直接把某个 SSSP algorithm 跑 $|V|$ 次其实已经相当不错，因为 output 的规模是 $O(|V|^2)$：
  - 若 weights 为正且被 $O(|V| + |E|)$ 界住，用 BFS 为 $|V| \cdot O(|V| + |E|)$。
  - 若图无环（acyclic），用 DAG Relaxation 为 $|V| \cdot O(|V| + |E|)$。
  - 若 weights 非负或 graph 是 undirected（无向的），用 Dijkstra 为 $|V| \cdot O(|V| \log |V| + |E|)$。
  - 一般情形用 Bellman-Ford 为 $|V| \cdot O(|V| \cdot |E|)$。
- 今天：对任意 weighted graph，在 $|V| \cdot O(|V| \log |V| + |E|)$ 时间内解出 APSP。

## Approach（思路）

- Idea：让所有 edge weights 变成非负，同时保持 shortest paths 不变！
- 也就是把 $G$ reweight（重赋权）成 $G'$，使其不含 negative weights。
- 并且要求 $G$ 中的 shortest path 在 $G'$ 中仍然最短。
- 若已非负，就只需跑 $|V|$ 次 Dijkstra 来解 APSP。
- Claim：可以在 $O(|V|(|V| + |E|))$ 时间内从 $G'$ 中的 distances 算出 $G$ 中的 distances。
  - 先对每个 $s \in V'$ 用 $O(|V| + |E|)$ 时间从 distances 构造 shortest-path tree（L11）。
  - 这棵树在 $G$ 中也是 shortest-paths tree，于是用 DFS 遍历它，同时算出 distances。
  - 总耗时 $O(|V| \cdot (|V| + |E|))$（比跑 $|V|$ 次 Dijkstra 更省时）。
- 但怎样才能构造出权重非负的 $G'$ 呢？这真的总是可能的吗？
- Claim：若 $G$ 含 negative-weight cycle，则不可能。
- Proof：没有 negative weights 时 shortest paths 是 simple（简单）的。
- 一旦存在 negative-weight cycle，shortest path 就不再是 simple 的。
- 于是问题变成：给定一个带 negative weights 但不含 negative-weight cycles 的 graph $G$。
- 能否在保持 shortest paths 的前提下，把它的 edge weights 变成非负？

## Making Weights Non-negative（把权重变成非负）

- Idea！给每条 edge 都加上「$G$ 中最小 weight 的相反数」！这样所有 weights 都非负了！:)
- FAIL：这不能保持 shortest paths！它会 bias（偏袒）经过 edges 更少的那些 paths。:(
- Idea！给定 vertex $v$，给它所有 outgoing edges 加 $h$，并给它所有 incoming edges 减 $h$。
- Claim：在上述 reweighting 下，shortest paths 保持不变。
- Proof：
  - 每条从 $v$ 出发的 path 的 weight 改变 $h$。
  - 每条终止于 $v$ 的 path 的 weight 改变 $-h$。
  - 每条经过 $v$ 的 path 的 weight（在局部上）不变。
- 这是一个非常 general（一般）且有用的 trick（技巧）。
- 它能在保持 shortest paths 的同时 transform（变换）一个 graph！

- 对多个 vertices 同时做也成立！
- 定义一个 potential function（势函数）$h : V \to \mathbb{Z}$，把每个 vertex $v \in V$ 映射到势 $h(v)$。
- 构造 graph $G'$：与 $G$ 相同，但每条 edge $(u, v) \in E$ 的 weight 为 $w'(u, v) = w(u, v) + h(u) - h(v)$。
- Claim：$G$ 中的 shortest paths 在 $G'$ 中也是 shortest paths。
- Proof：
  - path $\pi = (v_0, \dots, v_k)$ 在 $G$ 中的 weight 为 $w(\pi) = \sum_{i=1}^{k} w(v_{i-1}, v_i)$。
  - $\pi$ 在 $G'$ 中的 weight 为：

```math
w'(\pi) = \sum_{i=1}^{k} \bigl(w(v_{i-1}, v_i) + h(v_{i-1}) - h(v_i)\bigr) = w(\pi) + h(v_0) - h(v_k)
```

  - （$h$ 的求和 telescope（望远镜式相消）：每个内部下标 $i$ 都有一个正的与一个负的 $h(v_i)$。）
  - 每条从 $v_0$ 到 $v_k$ 的 path 都改变同一个量。
  - 因此任何 shortest path 仍然最短。

- 能否找到一个 potential function，使 $G'$ 中没有 negative edge weights？
- 也就是：是否存在 $h$，使得对每条 $(u, v) \in E$ 都有 $w(u, v) + h(u) - h(v) \ge 0$？
- 把这个条件整理成 $h(v) \le h(u) + w(u, v)$。
- 这看起来就像 triangle inequality（三角不等式）！
- Idea！若取 $h(v) = \delta(s, v)$ 且对某个 $s$ 有 $\delta(s, v)$ 有限，则条件自然满足。
- 但 graph 可能是 disconnected（不连通的）。
- 这样的 vertex $s$ 未必存在……:(
- Idea！新增一个 vertex $s$，并对每个 $v \in V$ 加一条指向它的 directed $0$-weight edge！:)
- 于是对所有 $v \in V$ 都有 $\delta(s, v) \le 0$，因为存在一条 weight 为 $0$ 的 path。
- Claim：若对某个 $v \in V$ 有 $\delta(s, v) = -\infty$，则原 graph 含有 negative-weight cycle。
- Proof：
  - 加入 $s$ 不会引入新的 cycles（$s$ 没有 incoming edges）。
  - 所以若 reweight 后的 graph 含 negative-weight cycle，原 graph 也含。
- 反之，若对所有 $v \in V$ 都有 $\delta(s, v)$ 有限：
  - 由 triangle inequality，对每条 $(u, v) \in E$ 都有 $w'(u, v) = w(u, v) + h(u) - h(v) \ge 0$！
  - $G'$ 中的新 weights 非负，同时 shortest paths 保持不变！

## Johnson's Algorithm（Johnson 算法）

- 从 $G$ 构造 $G_x$：新增 vertex $x$，用 $0$-weight edge 把它连到每个 vertex $v \in V$。
- 用 Bellman-Ford 对每个 $v \in V$ 计算 $\delta_x(x, v)$。
- 若对某个 $v \in V$ 有 $\delta_x(x, v) = -\infty$：
  - Abort（中止），因为 $G$ 中存在 negative-weight cycle。
- 否则：
  - 对每条 edge 重赋权 $w'(u, v) = w(u, v) + \delta_x(x, u) - \delta_x(x, v)$，得到 graph $G'$。
  - 对每个 $u \in V$：
    - 用 Dijkstra 在 $G'$ 中算出到所有 $v$ 的 shortest-path distances $\delta'(u, v)$。
    - 对所有 $v \in V$ 回算 $\delta(u, v) = \delta'(u, v) - \delta_x(x, u) + \delta_x(x, v)$。

## Correctness（正确性）

- 已经证明：从 $G$ 到 $G'$ 的 transformation 保持 shortest paths。
- 剩下的部分归结为 Bellman-Ford 与 Dijkstra 的正确性。
- 这里做的是从 Signed APSP（带符号的 APSP）到 Non-negative APSP（非负 APSP）的 reduction（归约）。
- Reductions 省时间！今天不需要 induction！:)

## Running Time（运行时间）

- 构造 $G_x$ 耗时 $O(|V| + |E|)$。
- Bellman-Ford 耗时 $O(|V||E|)$。
- 构造 $G'$ 耗时 $O(|V| + |E|)$。
- $|V|$ 次 Dijkstra 耗时 $O(|V| \cdot (|V| \log |V| + |E|))$。
- 从 $G'$ 中的 distances 算出 $G$ 中的 distances 耗时 $O(|V|^2)$。
- 总计 $O(|V|^2 \log |V| + |V||E|)$。
