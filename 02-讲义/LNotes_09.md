# Lecture 9: Breadth-First Search（广度优先搜索）

> Introduction to Algorithms: 6.006，Massachusetts Institute of Technology
> Instructors: Erik Demaine, Jason Ku, and Justin Solomon

---

## New Unit: Graphs!（新单元：图）

- Quiz 1 在下周，范围是 L01–L08，即 Data Structures 与 Sorting 两部分。
- 今天开始新单元：L09–L14 讲 Graph Algorithms（图算法）。

## Graph Applications（图的应用）

- 为什么要学？因为 graphs 无处不在！
- 任何 network system（网络系统）都与 graphs 有直接联系。
  - 例如 road networks（路网）、computer networks（计算机网络）、social networks（社交网络）。
- 任何 discrete system（离散系统）的 state space（状态空间）都能用 transition graph（转移图）表示。
  - 例如 puzzle 与 games：Chess、Tetris、Rubik's cube。
  - 例如 application workflows（应用工作流）与 specifications（规格说明）。
- 这条第二个理由值得单独记住：**图不是「一种数据结构」，而是一种把离散系统的全部状态及其可达关系铺开的建模方式**。图的 size 就是你问题的 size，这是后面所有复杂度分析的出发点。

## Graph Definitions（图的定义）

- 一个 graph $G = (V, E)$ 由一个 vertices（顶点）集合 $V$ 与一个顶点对的集合 $E \subseteq V \times V$ 组成。
- Directed edge（有向边）是有序对，例如对 $u, v \in V$ 的 $(u, v)$。
- Undirected edge（无向边）是无序对，例如对 $u, v \in V$ 的 $\{u, v\}$，即 $(u, v)$ 与 $(v, u)$ 视为同一条。
- 本课假设所有 graphs 都是 simple（简单）的：
  - edges 互不相同，例如 $(u, v)$ 在 $E$ 里只出现一次（但 $(v, u)$ 可能同时出现）。
  - edges 的两端是不同 vertices，即对所有 $(u, v) \in E$ 有 $u \ne v$（没有 self-loop）。
- Simple 这个假设推出 $|E| = O(|V|^2)$：因为 $|E| \le \binom{|V|}{2}$（无向情形），有向情形下 $\le 2\binom{|V|}{2}$。

[Figure 1：原文给出三个示例图 $G_1$、$G_2$、$G_3$ 的示意图。$G_1$ 是节点 0/1/2/3 上的无向图，$G_2$ 是同一节点集上的有向图，$G_3$ 是节点 a/b/s/c/d/e/f/g 上的无向图。原 PDF 为矢量插图，文字层只留下节点标签，边的信息在后面的 adjacency list 代码里可以完整读出，此处不重复绘制]

## Neighbor Sets / Adjacencies（邻居集合）

- $u \in V$ 的 outgoing neighbor set（出邻居集）是 $\mathrm{Adj}^+(u) = \{v \in V \mid (u,v) \in E\}$。
- $u \in V$ 的 incoming neighbor set（入邻居集）是 $\mathrm{Adj}^-(u) = \{v \in V \mid (v,u) \in E\}$。
- vertex $u \in V$ 的 out-degree（出度）是 $\deg^+(u) = |\mathrm{Adj}^+(u)|$。
- vertex $u \in V$ 的 in-degree（入度）是 $\deg^-(u) = |\mathrm{Adj}^-(u)|$。
- 对 undirected graph，$\mathrm{Adj}^-(u) = \mathrm{Adj}^+(u)$ 且 $\deg^-(u) = \deg^+(u)$。
- 省略上标时默认指 outgoing，即 $\mathrm{Adj}(u) = \mathrm{Adj}^+(u)$、$\deg(u) = \deg^+(u)$。

## Graph Representations（图的表示）

- 要存一个 graph $G = (V, E)$，需要为所有 $u \in V$ 存下 outgoing edges $\mathrm{Adj}(u)$。
- 首先需要一个 Set data structure `Adj`，把 $u$ 映射到 $\mathrm{Adj}(u)$。
- 然后对每个 $u$，把 $\mathrm{Adj}(u)$ 存在另一个叫 adjacency list（邻接表）的 data structure 里。
- `Adj` 通常用 direct access array 或 hash table，因为我们想按 vertex 快速 lookup。
- 每个 $\mathrm{Adj}(u)$ 通常用 array 或 linked list，因为一般只需要 iteration（遍历）。
- 对常见的这几种表示，`Adj` 的 size 是 $\Theta(|V|)$，而每个 $\mathrm{Adj}(u)$ 的 size 是 $\Theta(\deg(u))$。
- 由 handshaking lemma（握手引理）$\sum_{u \in V}\deg(u) \le 2|E|$，整个 graph 可以存在 $\Theta(|V| + |E|)$ 空间里。
- 因此，讲 graph 上的 algorithms 时，「linear time」指的是 $\Theta(|V| + |E|)$，也就是与 graph 的 size 成线性。

## Examples（三个具体例子）

- 例 1 与例 2 假设 vertices 被标号为 $\{0, 1, \dots, |V|-1\}$，所以 `Adj` 可以用 direct access array，且 $\mathrm{Adj}(u)$ 存在 array 里。例 3 的 `Adj` 用 hash table。

### Ex 1（Undirected，无向）

```python
G1 = [
    [2, 1],        # 0
    [2, 0, 3],     # 1
    [1, 3, 0],     # 2
    [1, 2],        # 3
]
```

- 边集（无向，去重后）：$\{0,1\}, \{0,2\}, \{1,2\}, \{1,3\}, \{2,3\}$。
- 注意每条边出现两次，这就是无向图「每条 edge 是 outgoing 两遍」的意思。

### Ex 2（Directed，有向）

```python
G2 = [
    [2],           # 0
    [2, 0],        # 1
    [1],           # 2
    [],            # 3
]
```

- 边集（有向）：$(0,2), (1,2), (1,0), (2,1)$。节点 3 出度为 0。

### Ex 3（Undirected，无向，用 hash table 做 `Adj`）

```python
G3 = {
    'a': ['s', 'b'],
    'b': ['a'],
    's': ['a', 'c'],
    'c': ['s', 'd', 'e'],
    'd': ['c', 'e', 'f'],
    'e': ['c', 'd', 'f'],
    'f': ['d', 'e'],
    'g': [],
}
```

- 节点 `g` 是孤立的，`Adj(g)` 为空。
- 注意无向图中 connections 是 symmetric（对称）的，因为每条 edge 都是 outgoing 两次。

> 原文脚注：若每个 $\mathrm{Adj}(u)$ 也用 hash table，则检查一条 edge $(u,v) \in E$ 是否存在可以做到 $O(1)^{(e)}$ 时间，$(e)$ 表示 expected。

## Paths（路径）

- 一个 path（路径）是一串 vertices $p = (v_1, v_2, \dots, v_k)$，满足对所有 $1 \le i < k$ 有 $(v_i, v_{i+1}) \in E$。
- 若一条 path 不重复 vertices，称它是 simple（简单的）。
- path $p$ 的 length（长度）$\ell(p)$ 是这条 path 上 edges 的条数。
- 从 $u \in V$ 到 $v \in V$ 的 distance（距离）$\delta(u, v)$ 是从 $u$ 到 $v$ 任何 path 的最小长度，也就是从 $u$ 到 $v$ 的最短路径的长度。
  - 按约定，若 $u$ 与 $v$ 不连通，则 $\delta(u, v) = \infty$。

> 原文脚注：6.006 里的 path 就是 6.042 里的 walk；而 6.042 里的 path 才是 6.006 里的 simple path。这个术语错位要留意。

## Graph Path Problems（图上的路径问题）

- 关于 graph 中的 paths，有很多你可能想解决的问题：
  - `SINGLE_PAIR_REACHABILITY(G, s, t)`：$G$ 中是否存在从 $s \in V$ 到 $t \in V$ 的 path？
  - `SINGLE_PAIR_SHORTEST_PATH(G, s, t)`：返回 distance $\delta(s, t)$，以及 $G = (V, E)$ 中从 $s$ 到 $t$ 的一条 shortest path。
  - `SINGLE_SOURCE_SHORTEST_PATHS(G, s)`：对所有 $v \in V$ 返回 $\delta(s, v)$，以及一棵含「从 $s$ 到每个 $v$ 的最短路径」的 shortest-path tree（最短路径树，定义见下）。
- 上面每个问题都不比它前面的问题容易——也就是说，你可以用解决下方问题的 black box 去解决上方任何问题。
- 本讲不会给出解决所有这些问题的一堆 algorithms。
- 而是给出**一个** algorithm，在 $O(|V| + |E|)$ 时间内解决其中最难的、也就是 `SINGLE_SOURCE_SHORTEST_PATHS`！

## Shortest Paths Tree（最短路径树）

- 怎么能为 graph 中每个 vertex 都返回一条从 source vertex $s$ 出发的最短路径？
- 很多 paths 的长度可能达到 $\Omega(|V|)$，所以把每条 path 都返回出来可能要 $\Omega(|V|^2)$ 时间。
- 换一种做法：对所有 $v \in V$，存下它的 parent $P(v)$——即从 $s$ 到 $v$ 的某条最短路径上的倒数第二个 vertex。
- 约定 $P(s)$ 为 null（从 $s$ 到 $s$ 的最短路径上没有倒数第二个 vertex）。
- 这组 parents 就构成一棵 size 为 $O(|V|)$ 的 shortest paths tree。
  - 换句话说，把所有最短路径反向，就是从每个可达 vertex 回到 $s$ 的路径集合，它们天然构成一棵树。

## Breadth-First Search（BFS，广度优先搜索）

- 怎么为所有 $v \in V$ 算出 $\delta(s, v)$ 与 $P(v)$？
- 把 $\delta(s, v)$ 与 $P(v)$ 存在 Set data structures 里，把 vertex $v$ 映射到 distance 与 parent。
- （若从 $s$ 到 $v$ 没有 path，就不把 $v$ 存进 $P$，并把 $\delta(s, v)$ 设为 $\infty$。）
- Idea！按 distance 递增的顺序去 explore（探索）graph 的 nodes。
- 目标：算出 level sets（层集）$L_i = \{v \mid v \in V,\ d(s,v) = i\}$，也就是所有 distance 为 $i$ 的 vertices。
- Claim：每个 vertex $v \in L_i$ 必须与某个 vertex $u \in L_{i-1}$ 相邻（即 $v \in \mathrm{Adj}(u)$）。
- Claim：任何落在某个 $L_j$（$j < i$）中的 vertex，都不会出现在 $L_i$ 里。
- Invariant（不变式）：对所有落在任何 $L_j$（$j < i$）中的 $v$，$\delta(s, v)$ 与 $P(v)$ 都已正确算出。
- Base case（$i = 1$）：$L_0 = \{s\}$，$\delta(s, s) = 0$，$P(s) = \text{None}$。
- Inductive Step：为算出 $L_i$：
  - 对 $L_{i-1}$ 中每个 vertex $u$：
    - 对每个 $v \in \mathrm{Adj}(u)$ 且 $v$ 未出现在任何 $L_j$（$j < i$）中者：
      - 把 $v$ 加入 $L_i$，设 $\delta(s, v) = i$，并设 $P(v) = u$。
- 让 $i$ 递增，反复由 $L_j$（$j < i$）算出 $L_i$，直到 $L_i$ 是 empty set 为止。
- 对那些 $\delta(s, v)$ 始终没被设过的 $v \in V$，把 $\delta(s, v)$ 设为 $\infty$。
- 由 induction，breadth-first search 正确地算出了所有 $\delta(s, v)$ 与 $P(v)$。
- Running time analysis：
  - 把每个 $L_i$ 存在一个支持 $\Theta(|L_i|)$ 时间 iteration、$O(1)$ 时间 insertion 的 data structure 里（也就是 dynamic array 或 linked list）。
  - 「检查 $v$ 是否出现在任何 $L_j$（$j < i$）中」可以改成检查 $v$ 是否在 $P$ 里。
  - 用支持 $O(1)$ 时间 dictionary ops 的 Set data structures 维护 $\delta$ 与 $P$（也就是 direct access array 或 hash table）。
  - Algorithm 把每个 vertex $u$ 加入至多 1 个 level，并对每个 $v \in \mathrm{Adj}(u)$ 花 $O(1)$ 时间：

```math
\text{work} \le O(1)\times\sum_{u\in V}\deg(u) = O(|E|)
```

  - 最后的 $\Theta(|V|)$ 花在为「从 $s$ 不可达」的那些 $v \in V$ 赋 $\delta(s, v) = \infty$ 上。
  - 所以 breadth-first search 跑线性时间！$O(|V| + |E|)$。
- 最后一步练习：在 Example 3 的 graph 上从 $s$ 跑一遍 breadth-first search。

## 为什么 BFS 值得单独拿出来看

- 它的核心机制不是「递归」，而是**用一个按层增长的 frontier 去维持「已解决集合是距离单调的」这个不变式**。这正是后面 Dijkstra 的雏形：把 level set 换成 priority queue，把「距离为 $i$」换成「当前最小 tentative distance」，就得到加权图上的版本。
- $\sum_u \deg(u) = 2|E|$ 这个 handshaking lemma 是全讲的关键一跃：没有它，遍历的代价只能写成「每个 vertex 各自看一遍邻居」，写不出 $O(|E|)$；有了它，「每个 edge 被看两遍」就把代价锁死在 edge 数上。
