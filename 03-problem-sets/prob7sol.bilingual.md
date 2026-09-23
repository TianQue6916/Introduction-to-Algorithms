# Introduction to Algorithms: 6.006（算法导论）

Massachusetts Institute of Technology
Instructors: Erik Demaine（埃里克·德梅因）, Jason Ku（顾杰森）, and Justin Solomon（贾斯汀·所罗门）

## <span style="color:#2471a3;">**[session]**</span> <span style="color:#c0392b">Problem Session 7（习题课 7）</span>

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 7-1. Dijkstra Practice（Dijkstra 练习）</span>

**(a)** 在以下 graph（图）上从 vertex（顶点）**s** 到 $V = \{a, b, c, d, e, f, g, h, s\}$ 中的每个顶点运行 Dijkstra's algorithm（Dijkstra 算法）。写出 (1) 每个顶点 $v \in V$ 的 minimum-weight path weight（最小权重路径权重）$\delta(s, v)$，以及 (2) vertices 从 Dijkstra's queue（Dijkstra 队列）中被移除的顺序。

```
         s        8       a        0       b

     7       1            0        1       3

         c        4       d                e

                  0       1        2       1

         f        0       g        2       h
```

> **[solution] Solution（解答）:**
> 
> | Vertex $v$     | $a$ | $b$ | $c$ | $d$ | $e$ | $f$      | $g$ | $h$ | $s$ |
> |:--------------:|:---:|:---:|:---:|:---:|:---:|:--------:|:---:|:---:|:---:|
> | $\delta(s, v)$ | 8   | 9   | 7   | 8   | 11  | $\infty$ | 12  | 10  | 0   |
> | Removal order  | 3   | 5   | 2   | 4   | 7   | 9        | 8   | 6   | 1   |
> 
> 节点按 $\delta(s, v)$ 递增顺序处理，在此 graph（图）中是唯一的。处理顺序并不总是唯一的；如果两个 vertices（顶点）具有相同的 shortest path distance（最短路径距离），Dijkstra 可能根据其在 priority queue（优先队列）中 tie-breaking（断连）的实现以任意顺序处理它们。虽然 $a$ 和 $d$ 距 $s$ 的 shortest path distance 相同，但 $d$ 只能通过 $a$ 到达，因此 $a$ 必须先被处理。

**(b)** 将 edge（边）$(g, c)$ 的 weight（权重）改为 $-6$。找出一个 vertex $v$，使得从 $s$ 运行 Dijkstra 会在 $v$ 不在 queue 中时改变到 $v$ 的 shortest path estimate（最短路径估计值）。

> **[solution] Solution（解答）:** 如果将 edge $(g, c)$ 的 weight 改为 $-6$，运行 Dijkstra 会以与 (a) 部分相同的顺序从 queue 中移除 vertices。但当 $g$ 从 queue 中被移除时，$c$ 已经被弹出 queue，此时到 $c$ 的 shortest path estimate 会从 $7$ 变为 $6$，因此 $c$ 具有所要求的性质。
> 
> <span style="color:#7d3c98;">**[alternative] Modern practice（现代实践）:**</span> 工业级 shortest path 引擎（如 Google Maps、OSRM）使用 **Contraction Hierarchies（收缩层次）** 或 **ALT（A$^*$ + landmarks + triangle inequality）** 预处理图结构，可在毫秒级回答单源 shortest path queries，远优于 Dijkstra 的 $O(E \log V)$。这些算法在静态图上预处理后查询极快，适用于 routing 场景。

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 7-2. Weighted Graph Radius（带权图半径）</span>

在带权有向图 $G = (V, E)$ 中，vertex $u \in V$ 的 weighted eccentricity（带权离心率）$\varepsilon(u)$ 是其到最远 vertex $v$ 的最短 weighted distance（带权距离），即 $\varepsilon(u) = \max\{\delta(u, v) \mid v \in V\}$。带权有向图 $G = (V, E)$ 的 weighted radius（带权半径）$R(G)$ 是所有 vertices 中最小的 eccentricity，即 $R(G) = \min\{\varepsilon(u) \mid u \in V\}$。给定一个带权有向图 $G$，其中 edge weights（边权）可能为正或负，但 $G$ 不包含 negative-weight cycle（负权环），描述一个 $O(|V|^3)$ 时间的 algorithm（算法）来确定图的 weighted radius（与 PS5 的 Problem 2 比较）。

> **[solution] Solution（解答）:** 使用 **Johnson's algorithm**（约翰逊算法）计算所有有序不同 vertex 对 $(a, b)$ 的 all-pairs shortest paths distances（全源最短路径距离）$\delta(a, b)$，时间复杂度 $O(|V||E| + |V|^2 \log |V|) = O(|V|^3)$（因为图中不含 negative-weight cycles，没有 $-\infty$）。然后直接对每个 $u \in V$ 计算 $\varepsilon(u)$，每个 vertex $O(|V|)$ 时间，总共 $O(|V|^2)$ 时间，再在 $O(|V|)$ 时间内找出最小的 $\varepsilon(u)$。该 algorithm 是正确的，因为我们直接执行所需的计算，且 Johnson's algorithm 对任何不含 negative-weight cycles 的图都能正确计算每个 $\delta(a, b)$。该 algorithm 的时间复杂度由 Johnson's 决定，因此总运行时间为 $O(|V|^3)$。也可以将 **Floyd-Warshall algorithm**（弗洛伊德-沃歇尔算法）与 Bellman-Ford 结合使用，但由于我们尚未讨论该 algorithm，学生需要完整描述和分析 Floyd-Warshall 才能使用它。

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 7-3. Under Games（地下游戏）</span>

Atniss Keverdeen 是一名 rebel spy（反叛间谍），受命前往暴君 President Rain（雷总统）的 mansion（宅邸）执行 reconnaissance mission（侦察任务）。为减少 exposure（暴露），她决定通过地下 sewer network（下水道网络）travel（行进）。她有一张下水道地图，由 $n$ 条 bidirectional pipes（双向管道）组成，这些管道在 junctions（节点）处相互连接。每个 junction 最多连接四条 pipes，且每个 junction 都可通过 sewer network 到达其他任何 junction。每条 pipe 标记有正整数 length（长度），而某些 junctions 标记为包含相同的 motion sensors（运动传感器），如果 Atniss 到该 sensor 的距离（沿下水道网络中的 pipes 测量）太近，sensor 就能感知到她。不幸的是，Atniss 不知道传感器的 sensitivity（灵敏度）。描述一个 $O(n \log n)$ 时间的 algorithm，找到一条沿 pipes 从给定 entrance junction（入口节点）到 President Rain 宅邸下方 junction 的 path（路径），该路径尽可能远离 motion sensors。

> **[solution] Solution（解答）:** 构建图 $G$，其中下水道网络中的每个 junction（节点）对应一个 vertex（顶点），如果 junction $a$ 和 $b$ 由长度为 $w$ 的 pipe 连接，则在 $a$ 和 $b$ 之间添加一条 weight（权重）为 $w$ 的 undirected edge（无向边）。由于每个 junction 最多连接常数条 pipes，该图中的 edges 和 vertices 均为 $O(n)$。令 $s$ 为 entrance junction 对应的 vertex，$t$ 为 President Rain 宅邸下方的 junction。定义 $G_k$ 为 $G$ 的 subgraph（子图），仅包含到任何 sensor（传感器）的距离严格大于 $k$ 的 vertices。我们的目标是找到 $k^*$，使得 $s$ 和 $t$ 在 $G_{k^*}$ 中属于同一个 connected component（连通分量），但在 $G_{k^*+1}$ 中不属于同一个 connected component，即 $k^*$ 是 Atniss 仍能不被察觉地从 $s$ 到达 $t$ 的最大 sensor sensitivity（传感器灵敏度）。如果能找到 $k^*$，则只需返回 $G_{k^*}$ 中从 $s$ 到 $t$ 的任意 path。
> 
> 为找到 $k^*$，首先标记每个 junction 到最近 sensor 的最短距离。为此，从 $G$ 构建新图 $G'$，添加一个 auxiliary vertex（辅助顶点）$x$，以及从 $x$ 到 $G$ 中每个标记为含有 motion sensor 的 vertex 的 weight 为 $0$ 的 undirected edge，然后从 $x$ 运行 Dijkstra，时间复杂度 $O(n \log n)$。则 $\delta(x, v)$ 即为从 $v$ 到任意 sensor 的所需最短距离标签。然后，对任意 $k$，通过遍历 vertices，移除所有 $\delta(x, v) \le k$ 的 vertices（同时移除其邻接 edges），可在 $O(n)$ 时间内构建 $G_k$。进一步地，可通过 **breadth-first search**（广度优先搜索）或 **depth-first search**（深度优先搜索）在 $O(n)$ 时间内检查 $t$ 是否在 $G_k$ 中从 $s$ 可达。
> 
> 我们可以通过为每个 $k \in \{1, \dots, k^*+1\}$ 构建 $G_k$ 在 $O(nk^*)$ 时间内找到 $k^*$，但可以通过 **binary search**（二分查找）更快地找到 $k^*$。使用任意最优 comparison sort algorithm（比较排序算法）（如 **merge sort**（归并排序））在 $O(n \log n)$ 时间内将 vertices 按到 sensor 的距离 $\delta(x, v)$ 排序，令 $d_i$ 为排序后第 $i$ 大的距离（$i \in \{1, \dots, n\}$），$d_1$ 最小，$d_n$ 最大。然后对 $i = \lceil n/2 \rceil$ 构建 $G_{d_i}$ 并在 $O(n)$ 时间内检查 $t$ 是否从 $s$ 可达。如果是，则对 $i > \lceil n/2 \rceil$ 递归；否则对 $i < \lceil n/2 \rceil$ 递归。binary search 进行 $O(\log n)$ 轮迭代，每轮最多 $O(n)$ 时间，直到找到最小的 $d_i = d^*$ 使得 $t$ 不可从 $s$ 到达。则对于 $k < d^*$ 时 $t$ 可从 $s$ 到达，而 $k \ge d^*$ 时不可，因此 $k^* = d^* - 1$。最后，可使用 **breadth-first search** 或 **depth-first search** 同时存储 parent pointers（父指针），在 $O(n)$ 时间内重构 $G_{k^*}$ 中从 $s$ 到 $t$ 的某条 path。如果 $k^* = 0$，则从 $s$ 到 $t$ 的每条 path 都经过含有 sensor 的 junction，因此可返回任意 path。

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 7-4. Critter Collection（小生物收集）</span>

Ashley Getem（来自 PS3）试图从 Trundle Town（特兰德尔镇）步行到 Blue Bluff（蓝崖），两者都是 Tanko 地区的 clearings（空地）。她有一张 Tanko 所有 clearings 和 two-way trails（双向小径）的地图。$n$ 个 clearings 每个最多连接五条 trails，每条 trail $t$ 直接连接两个 clearings，并标记有 length $\ell_t$ 和其上生活的 critters（小生物）容量 $c_t$，均为正整数。Ashley 是一个 compulsive collector（强迫性收集者），她会通过向遇到的每个 critter 投掷空的 Pocket Sphere（口袋球）来收集它（这会填满 Pocket Sphere 使其无法再使用）。如果她在没有空 Pocket Sphere 的情况下遇到 critter，她会感到 sad（悲伤）。每当 Ashley 到达一个 clearing，所有 trails 上的 critters 都会 respawn（重生）至最大容量。某些 clearings 包含 stores（商店），Ashley 可以在那里购买空的 Pocket Spheres 并存放已满的。Ashley 的钱多到花不完，但她的 backpack（背包）一次只能装 $k$ 个 Pocket Spheres。给定 Ashley 的地图，描述一个 $O(nk \log(nk))$ 时间的 algorithm，返回 Ashley 从 Trundle Town（背包里装满空的 Pocket Spheres）步行到 Blue Bluff 且从不感到悲伤的最短 route（路线），或者返回 sadness is unavoidable（悲伤不可避免）。

> **[solution] Solution（解答）:** 构建一个图 $G = (V, E)$，每个 clearing（空地）有 $k+1$ 个 vertices（顶点），其中 vertex $v_{c,i}$ 对应于在 clearing $c$ 且拥有 $i$ 个空的 pocket spheres。然后，对每对由 trail $t$ 连接的有向 clearing 对 $(a, b)$（具有 length $\ell_t$ 和 critters），添加以下 directed edges（有向边）：
> 
> - 如果 clearing $a$ 不包含 store，则对每个 $i \in \{c_t, \dots, k\}$ 添加一条 weight 为 $\ell_t$ 的 edge 从 $v_{a,i}$ 到 $v_{b,\,i-c_t}$，因为 Ashley 在 traversing（穿行）trail 时会用掉 $c_t$ 个 pocket spheres。
> - 否则，如果 clearing $a$ 包含 store，则对每个 $i \in \{0, \dots, k\}$ 添加一条 weight 为 $\ell_t$ 的 edge 从 $v_{a,i}$ 到 $v_{b,\,k-c_t}$，因为 Ashley 在离开 store 时把 backpack 装满空的 pocket spheres 从不会是坏事。
> 
> $G$ 有 $(k+1)n = O(kn)$ 个 vertices，每条 trail 最多 $k$ 条 edges。由于每个 clearing 最多五条 trails，$G$ 中最多有 $5kn = O(kn)$ 条 edges，因此 $G$ 的大小为 $O(nk)$。令 $s$ 为 Trundle Town 对应的 vertex，$t$ 为 Blue Bluff 对应的 vertex。则 $G$ 中从 $v_{s,k}$ 到任意 vertex $v_{t,i}$（$i \in \{0, \dots, k\}$）的 path 可避免 sadness，且每条避免 sadness 的 path 都对应于 $G$ 中的一条 path。由于 $G$ 中的 weights 非负，我们可以运行 Dijkstra，同时存储 parent pointers（父指针）来重构从 $s$ 到 $t$ 且避免 sadness 的最短 route，时间复杂度 $O(nk \log(nk))$。如果 $G$ 中到每个 $v_{t,i}$ 的最短 path weight 均为无穷大，则返回 sadness is unavoidable（悲伤不可避免）。

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 7-5. Shipping Servers（运输服务器）</span>

The video streaming service UsTube（UsTube 视频流服务）has decided to relocate across country, and needs to ship their servers（服务器）by truck from San Francisco, CA to Cambridge, MA. They will pay third-party trucking companies to transport servers from city to city. 一名 intern（实习生）编制了一份列表 $R$，包含所有 $n$ 条可用的 trucking routes（货运路线）；每条可用 route $r_i \in R$ 是一个 tuple（元组）$(s_i, t_i, w_i, c_i)$，其中 $s_i$ 和 $t_i$ 分别是 trucking route 起点和终点城市的 names（名称），$w_i$ 是卡车的正整数 weight capacity（重量容量），$c_i$ 是沿该 route 运输的正整数 cost（成本）（$0$ 到 $w_i$ 的任何重量 cost 相同）。注意，从 $s_i$ 到 $t_i$ 的 shipping route（运输路线）的存在并不暗示从 $t_i$ 到 $s_i$ 的 shipping route。UsTube 的某些 servers 太重而无法装在任何 truck 上，因此他们需要 transfer（转移）到更小的 servers。Assume that it is possible to ship some finite weight from San Francisco to Cambridge via some routes in $R$. 帮助 UsTube 评估他们的 shipping options（运输方案）。

<span style="color:#2471a3;">**[part]**</span> <span style="color:#00838f">**(a) (Useful Digression（有用的引子）)**</span>

给定一条 weighted path（带权路径）$\pi$，其 **bottleneck**（瓶颈）是路径上所有 edges 的 weight 的最小值。给定一个包含 vertices $s$ 和 $t$ 的有向图，令 $b(s, t)$ 表示从 $s$ 到 $t$ 的所有 paths 的最大 bottleneck，令 $I(t)$ 表示 $t$ 的 incoming neighbors（入邻居）集合。Argue（论证）that $b(s, t) \ge \min(b(s, v), w(v, t))$ for every $v \in I(t)$, and that $b(s, t) = \min(b(s, v^*), w(v^*, t))$ for at least one $v^* \in I(t)$.

> **[solution] Solution（解答）:** 首先论证对每个 $v \in I(t)$，$b(s, t) \ge \min(b(s, v), w(v, t))$。假设存在 vertices $s$ 和 $t$ 使得 $b(s, t) < \min(b(s, v), w(v, t))$ 以引出 contradiction（矛盾）。则存在一条从 $s$ 到 $v$ 的 path，其所有 edges 的最小 weight 严格大于 $b(s, t)$。沿 edge $(v, t)$ 延伸该 path 将得到一条从 $s$ 到 $t$ 的 path，其中每条 edge 的 weight 都大于 $b(s, t)$，即具有更大的 bottleneck，这与 $b(s, t)$ 是所有 paths 的最大 bottleneck 矛盾。
> 
> 接下来论证至少存在一个 $v^* \in I(t)$ 使得 $b(s, t) = \min(b(s, v^*), w(v^*, t))$。假设对每个 $v \in I(t)$ 都有 $b(s, t) > \min(b(s, v), w(v, t))$ 以引出矛盾。则存在一条从 $s$ 到 $t$ 的 path $\pi$，其 bottleneck 等于 $b(s, t)$。令 $v$ 为 path 上 $t$ 之前的 vertex。$\pi$ 的 bottleneck 不可能是 edge $(v, t)$ 的 weight，否则 $b(s, t) = w(v, t)$；但 bottleneck 也不可能出现在 $\pi$ 中从 $s$ 到 $v$ 的某条其他 edge 上，否则 $b(s, t) = b(s, v)$，矛盾。

<span style="color:#2471a3;">**[part]**</span> <span style="color:#00838f">**(b)**</span>

Assuming that the number of cities appearing in any of the $n$ trucking routes is less than $\sqrt[3]{n}$, describe an $O(n)$-time algorithm to return both: (1) the weight $w^*$ of the largest single server that can be shipped from San Francisco to Cambridge via a sequence of trucking routes, and (2) the minimum cost to ship such a server with weight $w^*$.

假设出现在 $n$ 条 trucking routes 中的城市数量小于 $\sqrt[3]{n}$，描述一个 $O(n)$ 时间的 algorithm，返回：(1) 可以通过一系列 trucking routes 从 San Francisco 运到 Cambridge 的最大单个 server 的 weight $w^*$，以及 (2) 运输 weight 为 $w^*$ 的这样一个 server 的最小 cost。

> **[solution] Solution（解答）:** 假设我们知道 $w^*$。那么我们可以构建一个图 $G_c = (V_c, E_c)$，每个城市对应一个 vertex（顶点），对每条满足 $w_i \ge w^*$ 的 trucking route $(s_i, t_i, w_i, c_i)$ 添加一条从 vertex $s_i$ 到 $t_i$ 的、weight 为 $c_i$ 的 directed edge（有向边），然后从 San Francisco 对应的 vertex 运行 Dijkstra，以找到将 weight $w^*$ 运到 Cambridge 的最小 cost。该图有 $n$ 条 edges 和最多 $O(\sqrt[3]{n})$ 个 vertices（根据题目陈述），因此即使使用 direct access array（直接访问数组）或 hash table（哈希表）作为 Dijkstra 的 priority queue（优先队列），Dijkstra 也能在 $O(n)$ 时间内运行。
> 
> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 此处的 bottleneck path 问题即 classic **widest path problem（最宽路径问题）**，也称 maximum capacity path，是 network flow 和 routing 中的基础问题。当边权为 capacity 时，求最大 bottleneck 等价于找最大传输容量路径。
> 
> 为找到 $w^*$，我们构建一个类似于 $G_c$ 的图 $G_w = (V_w, E_w)$，每个城市对应一个 vertex，对每条 trucking route $(s_i, t_i, w_i, c_i)$ 添加一条从 vertex $s_i$ 到 $t_i$ 的、weight 为 $w_i$ 的 directed edge，令 $s$ 和 $t$ 分别为 San Francisco 和 Cambridge 对应的 vertices。问题即转化为确定从 $s$ 到 $t$ 的所有 paths 的最大 bottleneck（瓶颈）。我们可以 modify（修改）Dijkstra 来计算 bottleneck，方法是将 shortest path distance estimates（最短路径距离估计值）替换为 bottleneck estimates（瓶颈估计值）$b_s(v)$。具体来说，将所有 bottleneck estimates 初始化为 $0$（不运输任何东西即达到此值），$b_s(s)$ 除外，将其设为 positive infinity（正无穷），因为开始时我们没有任何限制；然后将它们全部加入一个 maximum priority queue（最大优先队列）。然后，重复从 priority queue 中移除具有最大 bottleneck estimate 的 vertex，并 relax（松弛）其所有 outgoing edges（出边）。为 relax 一条 weight 为 $w_i$ 的 edge $(u, v)$，设 $b_s(v) = \max(\min(b_s(u), w_i), b_s(v))$（要么通过 $u$ 到 $v$ 的 path 改进了 $b_s(v)$ 的 estimate，要么没有）。
> 
> 为证明对该修改后的 Dijkstra 是正确的，可以遵循 Lecture 13 笔记中证明正常 Dijkstra 正确性的相同 proof structure（证明结构）。具体来说，可以证明 Claim 2 的类比：对每个 $v \in V_w$，当 $v$ 从 Dijkstra's queue 中移除时，$b_s(v) = b(s, v)$。在此省略完整 proof。对于此问题，学生只需正确描述 algorithm 即可得满分，无需完整的 correctness proof（正确性证明）。
> 
> 修改后的 Dijkstra 完成后，根据 $w^*$ 的定义有 $w^* = b_s(t) = b(s, t)$。由于我们只将 relaxation step（松弛步骤）从一个 constant time operation（常数时间操作）改为另一个，并且遵循与在具有 $O(n)$ 条 edges 和 $O(\sqrt[3]{n})$ 个 vertices 的图上运行 Dijkstra 相同的结构，此修改后的 Dijkstra 也在 $O(n)$ 时间内运行（使用 direct access array 或 hash table 作为 Dijkstra 的 priority queue）。

<span style="color:#2471a3;">**[part]**</span> <span style="color:#00838f">**(c)**</span>

Write a Python function `ship_server_stats(R, s, t)` that implements your algorithm from (b).

编写一个 Python 函数 `ship_server_stats(R, s, t)`，实现你在 (b) 中的 algorithm。

> **[solution] Solution（解答）:**

```python
def dijkstra(Adj, w, s):
    d = [float('inf') for _ in Adj]
    d[s] = 0
    Q = [i for i in range(len(Adj))]
    while len(Q) > 0:
        u = Q[0]
        for v in Q:
            if d[v] < d[u]:
                u = v
        Q.remove(u)
        for v in Adj[u]:
            d[v] = min(d[v], d[u] + w(u, v))
    return d

def dijkstra_bottleneck(Adj, w, s):
    d = [0 for _ in Adj]
    d[s] = float('inf')
    Q = [i for i in range(len(Adj))]
    while len(Q) > 0:
        u = Q[0]
        for v in Q:
            if d[v] > d[u]:
                u = v
        Q.remove(u)
        for v in Adj[u]:
            d[v] = max(d[v], min(d[u], w(u, v)))
    return d

def ship_server_stats(R, s, t):
    n = 0
    city_idx = {}
    for (_s, _t, _w, _c) in R:
        for city in (_s, _t):
            if city not in city_idx:
                city_idx[city] = n
                n += 1
    Adj = [[] for i in range(n)]
    w_w, w_c = {}, {}
    for (_s, _t, _w, _c) in R:
        si, ti = city_idx[_s], city_idx[_t]
        Adj[si].append(ti)
        w_w[(si, ti)], w_c[(si, ti)] = _w, _c
    si, ti = city_idx[s], city_idx[t]
    w = dijkstra_bottleneck(Adj, lambda u,v: w_w[(u,v)], si)[ti]
    for i in range(n):
        for j in Adj[i]:
            if w_w[(i, j)] < w:
                w_c[(i, j)] = float('inf')
    c = dijkstra(Adj, lambda u,v: w_c[(u,v)], si)[ti]
    return w, c
```

---

<span style="color:#2471a3;">**[source]**</span> **Source（来源）:** MIT OpenCourseWare — https://ocw.mit.edu

**6.006 Introduction to Algorithms（算法导论）** — Spring 2020 · [Terms of Use](https://ocw.mit.edu/terms)
