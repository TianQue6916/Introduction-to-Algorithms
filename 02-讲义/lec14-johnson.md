# Introduction to Algorithms: 6.006

## <span style="color:#2471a3;">**[lecture]**</span> <span style="color:#c0392b">Lecture 14: Johnson's Algorithm（Johnson 算法）</span>

Massachusetts Institute of Technology
Instructors: Erik Demaine, Jason Ku, and Justin Solomon

> <span style="color:#7f8c8d;">MIT 6.006 Spring 2020, Lecture 14 译注（对应视频：Johnson's Algorithm）</span>

---

## Previously（回顾）

上一讲我们用 **Dijkstra**（迪杰斯特拉算法）在**非负权**图上以 $O(|V|\log|V| + |E|)$ 时间解出了 **SSSP（Single-Source Shortest Paths，单源最短路径）**。但它在**任意权值**（含负权）的一般图上会失效——因为负权边会破坏「已确定顶点永不更新」这一前提。本讲要回答一个更宏大的问题：**任意权值图上的 APSP（All-Pairs Shortest Paths，全源最短路径）** 怎么解？

先看一张 SSSP 算法全景表（Restrictions，限制条件一览）：

| SSSP 算法 | 图类型 | 权值约束 | 名称 | 运行时间 $O(\cdot)$ |
|---|---|---|---|---|
| General | 一般图 | 无权（Unweighted） | BFS | $\|V\| + \|E\|$ |
| DAG | 有向无环图 | 任意（Any） | DAG Relaxation | $\|V\| + \|E\|$ |
| General | 一般图 | 非负（Non-negative） | Dijkstra | $\|V\|\log\|V\| + \|E\|$ |
| General | 一般图 | 任意（Any） | Bellman-Ford | $\|V\| \cdot \|E\|$ |

---

## All-Pairs Shortest Paths（APSP，全源最短路径）

- **输入**：有向图 $G = (V, E)$，权值函数 $w : E \to \mathbb{Z}$（边权为整数）。
- **输出**：对**所有**顶点对 $u, v \in V$ 给出最短路径权值 $\delta(u, v)$；若图中含**负权环**（negative-weight cycle，见 L11）则**中止**（abort）。
- **意义**：当我们需要理解「整张网络」的全貌时很有用，例如交通网络、circuit layout（电路布线）、supply chains（供应链）等。
- **朴素做法**：把某个 SSSP 算法跑 $|V|$ 次（每个源点各一次），其实就已经相当好了——因为输出本身就有 $O(|V|^2)$ 的大小：
  - 用 **BFS**（广度优先搜索）：当权值为正且被 $O(|V| + |E|)$ 所界定（bounded）时，总时间 $|V| \cdot O(|V| + |E|)$；
  - 用 **DAG Relaxation**（DAG 松弛）：当图无环（acyclic）时，总时间 $|V| \cdot O(|V| + |E|)$；
  - 用 **Dijkstra**：当权值非负或图无向时，总时间 $|V| \cdot O(|V|\log|V| + |E|)$；
  - 用 **Bellman-Ford**（一般情形）：总时间 $|V| \cdot O(|V| \cdot |E|)$。
- **本讲目标**：在**任意加权图**上，用 $|V| \cdot O(|V|\log|V| + |E|)$ 时间解出 APSP。

<!-- 并自 LNotes_14（v1 紧凑版） -->
- Input（输入）：directed graph（有向图）$G = (V, E)$，weights（权重）为 $w : E \to \mathbb{Z}$。
- Output（输出）：对所有 $u, v \in V$ 给出 $\delta(u, v)$。
- 若 $G$ 含 negative-weight cycle（负权环），则 abort（中止）。
- 当需要理解整个 network（网络）时这很有用，例如 transportation（交通）、circuit layout（电路布局）、supply chains（供应链）……
- 直接把某个 SSSP algorithm 跑 $|V|$ 次其实已经相当不错，因为 output 的规模是 $O(|V|^2)$：
  - 若 weights 为正且被 $O(|V| + |E|)$ 界住，用 BFS 为 $|V| \cdot O(|V| + |E|)$。
  - 若 weights 非负或 graph 是 undirected（无向的），用 Dijkstra 为 $|V| \cdot O(|V| \log |V| + |E|)$。
- 今天：对任意 weighted graph，在 $|V| \cdot O(|V| \log |V| + |E|)$ 时间内解出 APSP。

---

## Approach（总体思路）

- **核心 idea（一句话本质）**：把图的边权**全部改造成非负**，同时**保持最短路径不变**，这样就能用「跑 $|V|$ 次 Dijkstra」来高效解 APSP。
- 形式化：把 $G$ **重新加权**（reweight）成一张无负权的图 $G'$，使得「$G$ 中的一条最短路径，在 $G'$ 中仍是最短路径」。
- 一旦权值非负，只需对 $|V|$ 个源点各跑一次 Dijkstra 即可得到 APSP。
- **命题**：可以从 $G'$ 中的距离，用 $O(|V|(|V| + |E|))$ 时间反推 $G$ 中的距离：
  - 对每个源 $s \in V$，先从 $G'$ 中的距离重建**最短路径树**（shortest-path tree），耗时 $O(|V| + |E|)$（见 L11）；
  - 该树同时是 $G$ 中的最短路径树，于是用 **DFS（深度优先搜索）** 遍历这棵树的同时顺带算出 $G$ 中的距离；
  - 总耗时 $O(|V| \cdot (|V| + |E|))$，这比「跑 $|V|$ 次 Dijkstra」还要少。
- **但**：怎样造出边权非负的 $G'$？这件事到底可不可能？
- **命题**：若 $G$ 含**负权环**，则**不可能**。
- **证明**：当权值非负时，最短路径一定是**简单路径**（simple path，即不重复经过顶点的路径）；但若存在负权环，绕着环多走几圈会让权值任意小，最短路就不再是简单路径。二者矛盾，故不可能。
- 于是真正的问题是：**给定一张含负权边、但无负权环的图 $G$，能否把边权改成非负、同时保持最短路径不变？**

<!-- 并自 LNotes_14（v1 紧凑版） -->
- Idea：让所有 edge weights 变成非负，同时保持 shortest paths 不变！
- 也就是把 $G$ reweight（重赋权）成 $G'$，使其不含 negative weights。
- 并且要求 $G$ 中的 shortest path 在 $G'$ 中仍然最短。
- 若已非负，就只需跑 $|V|$ 次 Dijkstra 来解 APSP。
- Claim：可以在 $O(|V|(|V| + |E|))$ 时间内从 $G'$ 中的 distances 算出 $G$ 中的 distances。
  - 先对每个 $s \in V'$ 用 $O(|V| + |E|)$ 时间从 distances 构造 shortest-path tree（L11）。
  - 这棵树在 $G$ 中也是 shortest-paths tree，于是用 DFS 遍历它，同时算出 distances。
- 但怎样才能构造出权重非负的 $G'$ 呢？这真的总是可能的吗？
- Claim：若 $G$ 含 negative-weight cycle，则不可能。
- Proof：没有 negative weights 时 shortest paths 是 simple（简单）的。
- 一旦存在 negative-weight cycle，shortest path 就不再是 simple 的。
- 于是问题变成：给定一个带 negative weights 但不含 negative-weight cycles 的 graph $G$。
- 能否在保持 shortest paths 的前提下，把它的 edge weights 变成非负？

---

## Making Weights Non-negative（把权值变成非负）

### 第一次尝试（失败）

- **idea**：把 $G$ 中「最小权值的相反数」加到**每条边**上！于是所有边权都非负了。:)
- **FAIL（失败原因）**：这**不保持**最短路径！它会**偏向边数更少的路径**——因为每条边都被加了同样的常数，路径权值的增量与「边数」成正比，边数多的路径被「抬」得更高。:(
- 例：设两条从 $s$ 到 $t$ 的路径，权值分别为 $-100$（含 $100$ 条边）与 $-1$（含 $1$ 条边）。原始最短路是 $-100$ 那条；给每条边加 $1$ 后，前者变成 $0$，后者变成 $0$，两者打平，最短路被改变了。这直观说明了「全局加常数」不可行。

<!-- 并自 LNotes_14（v1 紧凑版） -->
- Idea！给每条 edge 都加上「$G$ 中最小 weight 的相反数」！这样所有 weights 都非负了！:)
- FAIL：这不能保持 shortest paths！它会 bias（偏袒）经过 edges 更少的那些 paths。:(

### 第二次尝试（局部调整，正确）

- **idea**：给定顶点 $v$，给 $v$ 的**所有出边**（outgoing edges）加 $h$，给 $v$ 的**所有入边**（incoming edges）减 $h$。
- **命题**：在上述**重新加权**下，最短路径保持不变。
- **证明**（按路径与 $v$ 的关系分三类讨论）：
  - 每条**以 $v$ 为起点**的路径，权值都变化 $+h$；
  - 每条**以 $v$ 为终点**的路径，权值都变化 $-h$；
  - 一条**穿过 $v$**（passing through $v$）的路径，其权值**（局部地）不变**——因为它经过 $v$ 时，进边被减了 $h$、出边被加了 $h$，两者抵消。
  - 由于「同起同终」的任意两条路径被改变了**相同的量**，其间的相对大小关系不变，故最短者仍最短。
- 这是一个非常通用且好用的技巧：**在保持最短路径不变的前提下变换一张图**。

<!-- 并自 LNotes_14（v1 紧凑版） -->
- Idea！给定 vertex $v$，给它所有 outgoing edges 加 $h$，并给它所有 incoming edges 减 $h$。
- Claim：在上述 reweighting 下，shortest paths 保持不变。
- Proof：
  - 每条从 $v$ 出发的 path 的 weight 改变 $h$。
  - 每条终止于 $v$ 的 path 的 weight 改变 $-h$。
  - 每条经过 $v$ 的 path 的 weight（在局部上）不变。
- 这是一个非常 general（一般）且有用的 trick（技巧）。
- 它能在保持 shortest paths 的同时 transform（变换）一个 graph！

---

## 推广到多顶点：Potential Function（势函数）

- 上面的技巧对**多个顶点**同时做也成立！
- 定义**势函数**（potential function）$h : V \to \mathbb{Z}$，把每个顶点 $v \in V$ 映射到一个整数**势**（potential）$h(v)$。
- 构造图 $G'$：与 $G$ 相同，但边 $(u, v) \in E$ 的新权值为

```math
w'(u, v) = w(u, v) + h(u) - h(v)
```

- **命题**：$G$ 中的最短路径，在 $G'$ 中仍是最短路径。
- **证明**（用「望远镜求和」telescoping）：
  - 设路径 $\pi = (v_0, \dots, v_k)$ 在 $G$ 中的权值为 $w(\pi) = \sum_{i=1}^{k} w(v_{i-1}, v_i)$。
  - 则 $\pi$ 在 $G'$ 中的权值为

```math
\sum_{i=1}^{k} \bigl(w(v_{i-1}, v_i) + h(v_{i-1}) - h(v_i)\bigr) = w(\pi) + h(v_0) - h(v_k)
```

  - **为什么相等**：把 $h$ 项单独求和，得 $\sum_{i=1}^{k} h(v_{i-1}) - \sum_{i=1}^{k} h(v_i)$。对每个**内部**顶点 $v_i$（$1 \le i \le k-1$），它既作为前一项的终点贡献 $+h(v_i)$，又作为后一项的起点贡献 $-h(v_i)$，二者抵消，故只剩首项 $h(v_0)$ 与末项 $-h(v_k)$。这正是「望远镜求和」（telescoping，即相邻项相消后只留首尾）。
  - 于是每条从 $v_0$ 到 $v_k$ 的路径都改变了**相同的量** $h(v_0) - h(v_k)$。
  - 因此相对大小不变，任何最短路径仍然最短。∎

<!-- 并自 LNotes_14（v1 紧凑版） -->
- 对多个 vertices 同时做也成立！
- 构造 graph $G'$：与 $G$ 相同，但每条 edge $(u, v) \in E$ 的 weight 为 $w'(u, v) = w(u, v) + h(u) - h(v)$。
- Claim：$G$ 中的 shortest paths 在 $G'$ 中也是 shortest paths。
- Proof：
  - $\pi$ 在 $G'$ 中的 weight 为：


```math
w'(\pi) = \sum_{i=1}^{k} \bigl(w(v_{i-1}, v_i) + h(v_{i-1}) - h(v_i)\bigr) = w(\pi) + h(v_0) - h(v_k)
```
  - （$h$ 的求和 telescope（望远镜式相消）：每个内部下标 $i$ 都有一个正的与一个负的 $h(v_i)$。）
  - 每条从 $v_0$ 到 $v_k$ 的 path 都改变同一个量。
  - 因此任何 shortest path 仍然最短。

---

## Making Weights Non-negative（继续：寻找合适的势函数）

- 现在的问题变成：**能否找到一个势函数 $h$，使得 $G'$ 没有负权边？**
- 即：是否存在 $h$，使对每条边 $(u, v) \in E$ 都满足 $w(u, v) + h(u) - h(v) \ge 0$？
- 把这个条件**移项**，得 $h(v) \le h(u) + w(u, v)$——这**看起来像三角不等式**（triangle inequality）！
  - 回顾 L11 的三角不等式：若 $\delta(s, v)$ 有限，则 $\delta(s, v) \le \delta(s, u) + w(u, v)$，即「经中间点不会更近」。
- **idea**：若取 $h(v) = \delta(s, v)$（$s$ 到 $v$ 的最短距离），且 $\delta(s, v)$ 对某个源 $s$ 有限，则三角不等式恰好保证上述条件成立！
- **但**：图可能**不连通**（disconnected），此时可能不存在「能到达所有顶点」的源点 $s$…… :(
- **idea（关键突破）**：**新加一个顶点 $s$**，从 $s$ 向每个 $v \in V$ 连一条**权值为 $0$ 的有向边**！:)
  - 这样对**所有** $v \in V$，都存在一条权值为 $0$ 的路径（即 $s \to v$ 这条边本身），故 $\delta(s, v) \le 0$。
- **命题**：若对某个 $v \in V$ 有 $\delta(s, v) = -\infty$，则原图 $G$ 含有负权环。
- **证明**：
  - 加入 $s$ **不会引入新环**——因为 $s$ **没有入边**（incoming edges），任何环若要经过 $s$ 就必须有入边指向 $s$，故不可能。
  - 所以若新图中出现了负权环，该环必然**完全位于原图** $G$ 中，即原图也有负权环。
- **反之**，若对所有 $v \in V$，$\delta(s, v)$ 都有限：
  - 由三角不等式，对每条边 $(u, v) \in E$ 有 $w'(u, v) = w(u, v) + h(u) - h(v) \ge 0$，其中 $h(v) = \delta(s, v)$。
  - 于是 $G'$ 的新权值**非负**，且**保持最短路径**不变！问题解决。

<!-- 并自 LNotes_14（v1 紧凑版） -->
- 能否找到一个 potential function，使 $G'$ 中没有 negative edge weights？
- 这看起来就像 triangle inequality（三角不等式）！
- Idea！若取 $h(v) = \delta(s, v)$ 且对某个 $s$ 有 $\delta(s, v)$ 有限，则条件自然满足。
- 但 graph 可能是 disconnected（不连通的）。
- 这样的 vertex $s$ 未必存在……:(
- Idea！新增一个 vertex $s$，并对每个 $v \in V$ 加一条指向它的 directed $0$-weight edge！:)
- 于是对所有 $v \in V$ 都有 $\delta(s, v) \le 0$，因为存在一条 weight 为 $0$ 的 path。
- Proof：
  - 加入 $s$ 不会引入新的 cycles（$s$ 没有 incoming edges）。
  - 所以若 reweight 后的 graph 含 negative-weight cycle，原 graph 也含。
  - $G'$ 中的新 weights 非负，同时 shortest paths 保持不变！

---

## Johnson's Algorithm（Johnson 算法）

- **核心 idea（一句话本质）**：加一个「超级源」$x$，用 Bellman-Ford 求出势函数 $h(v) = \delta_x(x, v)$，据此把边权重建成非负，再用 $|V|$ 次 Dijkstra 解出 APSP，最后把势抵消回去。

**Algorithm: Johnson**

1. 从 $G$ 构造 $G_x$：新增顶点 $x$，对每个 $v \in V$ 加一条从 $x$ 到 $v$ 的**零权边**。
2. 用 **Bellman-Ford** 计算 $\delta_x(x, v)$（对每个 $v \in V$）。
3. 若存在 $v \in V$ 使 $\delta_x(x, v) = -\infty$：
   - **中止**（abort），因为 $G$ 中存在负权环。
4. 否则（对所有 $v$，$\delta_x(x, v)$ 有限）：
   - 对每条边重加权 $w'(u, v) = w(u, v) + \delta_x(x, u) - \delta_x(x, v)$，得到图 $G'$。
   - 对每个 $u \in V$：
     - 用 **Dijkstra** 计算 $u$ 到所有 $v$ 在 $G'$ 中的最短距离 $\delta'(u, v)$；
     - 计算原图距离 $\delta(u, v) = \delta'(u, v) - \delta_x(x, u) + \delta_x(x, v)$（对每个 $v \in V$）。

> 说明第 4 步最后一条公式的方向：由势函数的 telescope 恒等式 $w'(\pi) = w(\pi) + h(u) - h(v)$，取最短路后得 $\delta'(u, v) = \delta(u, v) + h(u) - h(v)$。移项即 $\delta(u, v) = \delta'(u, v) - h(u) + h(v)$，代入 $h = \delta_x(x, \cdot)$ 得 $\delta(u, v) = \delta'(u, v) - \delta_x(x, u) + \delta_x(x, v)$。

<!-- 并自 LNotes_14（v1 紧凑版） -->
- 从 $G$ 构造 $G_x$：新增 vertex $x$，用 $0$-weight edge 把它连到每个 vertex $v \in V$。
- 否则：
    - 用 Dijkstra 在 $G'$ 中算出到所有 $v$ 的 shortest-path distances $\delta'(u, v)$。

---

## Correctness（正确性）

- 「从 $G$ 到 $G'$ 的变换保持最短路径」这一点，已经在**势函数**一节证明过了。
- 其余部分归结为 **Bellman-Ford** 与 **Dijkstra** 各自的正确性（分别在 L12、L13 用循环不变式论证过）。
- 这里的本质是**reduction（归约）**：把「任意权值的 APSP」**归约**为「非负权值的 APSP」（Signed APSP $\to$ Non-negative APSP）。
- 归约很省时间！今天不用再做归纳了。:)

<!-- 并自 LNotes_14（v1 紧凑版） -->
- 已经证明：从 $G$ 到 $G'$ 的 transformation 保持 shortest paths。
- 剩下的部分归结为 Bellman-Ford 与 Dijkstra 的正确性。
- 这里做的是从 Signed APSP（带符号的 APSP）到 Non-negative APSP（非负 APSP）的 reduction（归约）。
- Reductions 省时间！今天不需要 induction！:)

---

## Running Time（运行时间）

各项代价相加：

- 构造 $G_x$：$O(|V| + |E|)$ 时间（新增 $|V|$ 条边）。
- 一次 **Bellman-Ford**：$O(|V| \cdot |E|)$ 时间。
- 构造 $G'$（对所有边重加权）：$O(|V| + |E|)$ 时间。
- $|V|$ 次 **Dijkstra**：$|V| \cdot O(|V|\log|V| + |E|)$ 时间。
- 从 $G'$ 的距离反推 $G$ 的距离：$O(|V|^2)$ 时间（对每个顶点对做一次常数运算）。

**总复杂度**：

```math
O(|V| + |E|) + O(|V||E|) + O(|V| + |E|) + |V| \cdot O(|V|\log|V| + |E|) + O(|V|^2)
= O(|V|^2 \log|V| + |V||E|)
```

> **递推与主项说明**：这不是递推式，而是若干独立步骤的**累加**。主项来自「$|V|$ 次 Dijkstra」的 $O(|V|^2\log|V| + |V||E|)$ 与「一次 Bellman-Ford」的 $O(|V||E|)$。由于 $O(|V|^2\log|V|)$ 与 $O(|V||E|)$ 二者大小关系不定（取决于图是稠密还是稀疏），最终写成两者之和 $O(|V|^2\log|V| + |V||E|)$。在**稀疏图**上（$|E| = O(|V|)$）约为 $O(|V|^2\log|V|)$，与「跑 $|V|$ 次 Dijkstra 于非负图」同阶，仅多一个 Bellman-Ford 的 $O(|V||E|)$ 开销；而在**稠密图**上 $|E| = O(|V|^2)$，退化为 $O(|V|^3)$，与 Floyd–Warshall 同阶。

<!-- 并自 LNotes_14（v1 紧凑版） -->
- 构造 $G_x$ 耗时 $O(|V| + |E|)$。
- 从 $G'$ 中的 distances 算出 $G$ 中的 distances 耗时 $O(|V|^2)$。

---

## 小结（一图看懂）

- 本讲用「**势函数 + 超级源**」这一组合拳，把「任意权图 APSP」归约到「非负权图 APSP」，从而能用 $|V|$ 次 Dijkstra 高效求解。
- 三条关键结论：
  1. 全局「给每条边加同一常数」**会破坏**最短路（偏向少边路径）；
  2. 局部「入边减、出边加」的势函数调整**恰好保持**最短路（telescoping）；
  3. 超级源 $x$ 保证势函数 $\delta_x(x, \cdot)$ 处处有定义且 $\le 0$，同时把「负权环检测」交给 Bellman-Ford 一次搞定。

---

*MIT OpenCourseWare · https://ocw.mit.edu · 6.006 Introduction to Algorithms, Spring 2020*
