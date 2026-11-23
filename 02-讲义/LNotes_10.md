# Lecture 10: Depth-First Search（深度优先搜索）

> Introduction to Algorithms: 6.006，Massachusetts Institute of Technology
> Instructors: Erik Demaine, Jason Ku, and Justin Solomon

---

## Previously（上一讲回顾）

- Graph definitions（图的定义）：directed / undirected、simple、neighbors、degree 这一套术语。
- Graph representations：用 Set 把 vertices 映射到 adjacency lists。
- Paths 与 simple paths、path length、distance、shortest path。
- Graph Path Problems 一整套：
  - `Single_Pair_Reachability(G, s, t)`
  - `Single_Source_Reachability(G, s)`
  - `Single_Pair_Shortest_Path(G, s, t)`
  - `Single_Source_Shortest_Paths(G, s)`，简称 SSSP。
- Breadth-First Search（BFS）：
  - 一个解决 Single Source Shortest Paths 的 algorithm。
  - 配上合适的 data structures，它跑 $O(|V| + |E|)$ 时间，即与 input size 线性。

## Examples（本讲要用的两个示例图）

[Figure 1：原文给出两个示例图 $G_1$ 与 $G_2$，两者共用同一组 vertices $\{a, b, c, d, e, f\}$。$G_1$ 是无向图，$G_2$ 是有向图；原 PDF 为矢量插图，文字层只留下 vertices 标签、没有边集，故此处不臆造边的具体形态。后文所有 DFS / Full-DFS / topological sort 的例子都在这两个图上做]

## Depth-First Search（DFS，深度优先搜索）

- 从一个 vertex $s$ 出发搜索一个 graph，与 BFS 类似。
- 它解决的是 Single Source Reachability，**不是** SSSP——但它对解决后面别的问题非常有用。
- 返回一棵由 parent pointers 构成的 parent tree（父树），它不一定是最短路径树。
- Idea！递归地访问 outgoing adjacencies，但**永不重复访问**同一个 vertex。
- 换句话描述：沿任意 path 一直走到走不动为止，然后 backtrack（回溯）到最近一个还有未探索 path 的地方继续。
- 初始化 $P(s) = \text{None}$，然后跑 `visit(s)`，其中：

```python
def visit(u):
    for v in Adj(u):
        if v not in P:              # 尚未访问过
            P[v] = u
            visit(v)                # 递归下潜
    # DFS 在这里「结束」对 vertex u 的访问，供后面使用
```

- 这段代码值得逐行看清楚三件事：
  - 「是否已访问」这个判断与 BFS 一样，都是靠 `P` 里有没有 `v` 来做的，不需要额外的 visited 数组。
  - `P[v] = u` 在**递归之前**设置，所以 parent tree 在搜索过程中一直是完整的。
  - `visit(u)` 返回之前那一行注释是 DFS 与 BFS 最大的区别：DFS 有一个明确的「完成时刻」，topological sort 与 cycle detection 全靠它。
- 例子：在 $G_1$ 和 / 或 $G_2$ 上从 $a$ 出发跑一遍 DFS。

## Correctness（正确性）

- Claim：对每个从 $s$ 可达的 vertex $v$，DFS 都会访问到 $v$ 并正确设置 $P(v)$。
- Proof：对 $k$ 做 induction，命题限定在「与 $s$ 的 distance 不超过 $k$」的那些 vertices 上。
  - Base case（$k = 0$）：对 $s$ 而言 $P(s)$ 被正确设置，且 $s$ 被访问。
  - Inductive step：考虑满足 $\delta(s, v) = k_0 + 1$ 的 vertex $v$。
  - 考虑 vertex $u$，它是从 $s$ 到 $v$ 某条 shortest path 上的倒数第二个 vertex。
  - 由 induction，既然 $\delta(s, u) = k_0$，DFS 会访问 $u$ 并正确设置 $P(u)$。
  - 在访问 $u$ 的过程中，DFS 会考察 $v \in \mathrm{Adj}(u)$。
  - 要么 $v$ 已在 $P$ 里，即早已被访问过；要么 $v$ 会在访问 $u$ 期间被访问。
  - 两种情形下 $v$ 都会被 DFS 访问到，并被正确地加入 $P$。

## Running Time（运行时间）

- Algorithm 对每个 vertex $u$ 至多访问一次，并对每个 $v \in \mathrm{Adj}(u)$ 花 $O(1)$ 时间。
- Work 的上界是：

```math
O(1)\times\sum_{u\in V}\deg(u) = O(|E|)
```

- 与 BFS 不同，DFS 不给每个 vertex 返回 distance，所以它跑 $O(|E|)$ 时间（省掉了 BFS 里那个 $\Theta(|V|)$ 的收尾步骤）。
- 要注意这个 $O(|E|)$ 的含义：它靠的仍是「每个 vertex 只被访问一次」+ handshaking lemma。若 graph 里有很多 isolated vertices，实际的完整搜索会退到 $O(|V| + |E|)$，见下面的 Full-DFS。

## Full-BFS and Full-DFS（全图版）

- 假设我们要 explore 整个 graph，而不只是从一个 vertex 可达的那部分。
- Idea！把某个 graph search algorithm $A$ 反复跑在任意一个尚未访问的 vertex 上。
- 重复以下动作，直到所有 vertices 都被访问过：
  - 任选一个未访问的 vertex $s$，用 $A$ 去 explore 从 $s$ 可达的所有 vertices。
- 我们把这个算法叫 Full-$A$：若 $A$ 是 BFS 就叫 Full-BFS，若 $A$ 是 DFS 就叫 Full-DFS。
- 它把每个 vertex 访问一次，所以 Full-BFS 与 Full-DFS 都跑 $O(|V| + |E|)$ 时间。
- 例子：在 $G_1$ 和 / 或 $G_2$ 上跑一遍 Full-DFS / Full-BFS。

[Figure 2：原文再次给出 $G_1$（无向）与 $G_2$（有向）两个示例图，用来演示 Full-DFS / Full-BFS 的外层循环。原 PDF 为矢量插图，文字层只有 vertices 标签 $\{a, b, c, d, e, f\}$，边集未进入文字层]

## Graph Connectivity（图的连通性）

- 若每两个 vertices 之间都存在一条 connecting path，称一个 undirected graph 是 connected（连通的）。
- 在有向图里，vertex $u$ 可能从 $v$ 可达，但 $v$ 未必从 $u$ 可达。
- 对 directed graphs，connectivity 要复杂得多（本课不讨论）。
- `Connectivity(G)`：undirected graph $G$ 是否连通？
- `Connected_Components(G)`：给定 undirected graph $G = (V, E)$，返回 $V$ 的一个划分，分成若干 subsets $V_i \subseteq V$，这些 $V_i$ 就是 connected components（连通分量），要求每个 $V_i$ 在 $G$ 中连通，且不同 connected components 的 vertices 之间没有边。
- 考虑任何解决 Single Source Reachability 的 graph algorithm $A$。
- Claim：$A$ 可以用来解决 Connected Components。
- Proof：跑 Full-$A$。$A$ 每跑一次，就把这次访问到的 vertices 归入同一个 connected component。
- 这个 proof 的机制值得点明：**Full-$A$ 的外层循环次数恰好等于 connected components 的个数**，而每次跑 $A$ 得到的那一团就是其中一个分量——所以不需要额外的数据结构，外层的控制流本身就是答案。

## Topological Sort（拓扑排序）

- Directed Acyclic Graph（DAG，有向无环图）是不含 directed cycle（有向环）的 directed graph。
- graph $G = (V, E)$ 的 Topological Order（拓扑序）是 vertices 上的一个 ordering $f$，满足：每条 edge $(u, v) \in E$ 都有 $f(u) < f(v)$。
- Exercise：证明一个 directed graph 存在 topological ordering 当且仅当它是 DAG。
- 怎么找到一个 topological order？
- Finishing Order（完成序）是 Full-DFS 访问完 $G$ 中每个 vertex 的先后顺序。
- Claim：若 $G = (V, E)$ 是 DAG，则 finishing order 的 reverse（逆序）就是一个 topological order。
- Proof：需要证明对每条 edge $(u, v) \in E$ 都有 $u$ 排在 $v$ 之前，也就是「对 $v$ 的访问先于对 $u$ 的访问结束」。分两种情形：
  - 若 $u$ 先于 $v$ 被访问：
    - 在对 $u$ 的访问结束之前，必然会（经由 $(u,v)$ 或别的路径）访问 $v$。
    - 因此对 $v$ 的访问先于对 $u$ 的访问结束。
  - 若 $v$ 先于 $u$ 被访问：
    - 因为 graph 无环，$u$ 不可能从 $v$ 到达。
    - 因此对 $v$ 的访问先于对 $u$ 的访问结束。
- 这两条合起来就给出「$u$ 的访问总是后结束」，于是 $u$ 在 reverse finishing order 里排在 $v$ 前面。
- 注意 acyclic 这个假设在第二种情形里是**必须**的：如果存在环，$v$ 就可能绕回 $u$，那条 edge 的次序关系就崩了。

## Cycle Detection（环检测）

- 若 graph $G = (V, E)$ 无环，Full-DFS 会找到一个 topological order。
- 若 Full-DFS 的 reverse finishing order 不是 topological order，那 $G$ 必然含一个 cycle。
- 检查 $G$ 是否无环：对每条 edge $(u, v)$，检查在 reverse finishing order 里 $v$ 是否排在 $u$ 之前。
- 这可以用 hash table 或 direct access array 在 $O(|E|)$ 时间内完成。
- 若要返回这样一条 cycle，就在 Full-DFS 中维护「沿 path 回到 $s$ 的那些 ancestors」这个集合。
- Claim：若 $G$ 含一个 cycle，Full-DFS 必然会走一条从 $v$ 指向 $v$ 的 ancestor 的 edge。
- Proof：考虑 $G$ 中的一个 cycle $(v_0, v_1, \dots, v_k, v_0)$。
  - Wlog（不失一般性），令 $v_0$ 是这个 cycle 上 Full-DFS 最先访问到的 vertex。
  - 对每个 $v_i$，在对 $v_i$ 的访问结束之前，都会访问 $v_{i+1}$ 并结束对它的访问。
  - 会考察 edge $(v_i, v_{i+1})$，若 $v_{i+1}$ 尚未被访问，则此时会访问它。
  - 于是，在对 $v_0$ 的访问结束之前，会（依 $v_0$ 的假设，这是第一次）访问到 $v_k$。
  - 所以，在对 $v_k$ 的访问结束之前，会考察 $(v_k, v_0)$，而 $v_0$ 正是 $v_k$ 的一个 ancestor。
- 这条 back edge（回边）就是 cycle 的指纹：它在 DFS 树里指向自己的祖先，而拓扑序不可能容纳一条这样的边。

## BFS 与 DFS 的分工

- 两者的骨架几乎一样：都靠 `P` 判重、都对每条 edge 花 $O(1)$、都跑线性时间。
- 差别只在「以什么顺序展开 frontier」：
  - BFS 用 level set（层集）逐层推进，因此给出 distance 与 shortest path，但需要 $\Theta(|V|)$ 的额外收尾。
  - DFS 用 recursion stack 一路下潜，因此不给 distance，但免费获得 finishing order——这是它相比 BFS 多出来的、BFS 拿不到的信息。
- 后续讲义会在这个 finishing order 上继续做文章（strongly connected components）。
