# Introduction to Algorithms: 6.006（算法导论）

Massachusetts Institute of Technology（麻省理工学院）
Instructors（授课教师）: Erik Demaine（埃里克·德梅因）, Jason Ku（顾杰森）, and Justin Solomon（贾斯汀·所罗门）

## <span style="color:#2471a3;">**[session]**</span> <span style="color:#c0392b">Problem Set 6（习题集 6）</span>

> <span style="color:#7f8c8d;">MIT 6.006 Spring 2020, Problem Set 6 Solutions（习题集 6 解答）· 主题：Single Source Shortest Paths（SSSP，单源最短路径）· 对应 Lecture 11-14 与 CLRS §24（单源最短路径）、§25.3（Johnson 算法）</span>

---

请在提供的 LaTeX 和 Python templates（模板）中写出你的解答。追求 concise（简洁）的解答；convoluted and obtuse（复杂晦涩）的描述即使正确也可能得低分。

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 6-1. Dijkstra Practice（Dijkstra 练习）</span>

考虑下方这个 weighted graph（带权图）$G = (V, E, w)$，它是 acyclic（无环）的，且具有非负 edge weights（边权）。

**(a)** 从 vertex（顶点）$a$ 出发，在 $G$ 上分别运行 **DAG Relaxation**（DAG 松弛）与 **Dijkstra's algorithm**（Dijkstra 算法）。每个算法都会尝试 relax（松弛）每条 edge $(u, v) \in E$，但尝试的顺序不同。对每个算法，按 relaxation order（松弛顺序）写下所有 edges 的列表：即算法尝试松弛它们的顺序。如果下一个要处理的 vertex 或 outgoing adjacency（出边邻接）存在歧义，按字母顺序处理。

```
            2           1
    a ────────→ b ────────→ c
    │         ╱│  ╲          ↑
    │6     1 ╱ │3   ╲ 2      │1
    ↓     ╱   ↓     ╲        │
    d ──0────→ e ──2─→ f ────┘
```

**(b)** 列出每个 $v \in V$ 的 $\delta(a, v)$（用任一算法均可）。

> **[solution] Solution（解答）:** 两个算法的 relaxation order 都是唯一的。
>
> **DAG Relaxation（DAG 松弛）:** $[(a, b), (a, d), (d, b), (d, e), (b, c), (b, e), (b, f), (e, f), (f, c)]$
>
> **Dijkstra:** $[(a, b), (a, d), (b, c), (b, e), (b, f), (f, c), (e, f), (d, b), (d, e)]$
>
> | vertex $v$ | $a$ | $b$ | $c$ | $d$ | $e$ | $f$ |
> |:---:|:---:|:---:|:---:|:---:|:---:|:---:|
> | $\delta(a, v)$ | $0$ | $2$ | $3$ | $6$ | $5$ | $4$ |

> **Rubric（评分标准）:**
> - 每个 relaxation order 5 分（共 2 个）
> - shortest path distances（最短路径距离）5 分
> - 每个错误（添加、遗漏、顺序颠倒）扣 1 分
> - 三部分各自最低 0 分

---

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这题值得停下来对比两种 SSSP 算法"松弛什么、按什么顺序松弛"。DAG Relaxation 按 topological order（拓扑序）处理——由于本题图是无环的，每个 vertex 只被处理一次，且一旦处理完，它的 distance estimate（距离估计）就定型了；而 Dijkstra 按当前最小 distance 顺序从 priority queue（优先队列）弹出 vertices，每弹出一个才松弛它的出边。🎥 *Demaine 在 Lecture 14 开头这样划定三种 SSSP 算法的适用边界*："So we're only concerned about needing to run Bellman-Ford on directed graphs that potentially have negative edge weight."（翻译：所以我们只关心需要在可能含负边权的有向图上运行 Bellman-Ford 的情形）——Dijkstra 处理非负权，DAG Relaxation 处理无环图（可含负权），Bellman-Ford 处理一般图，三者构成 SSSP 的完整武器库；这正是你在 review2 讲义里见过的那张"算法选择决策树"表格的三行。注意本题两个列表的差异：Dijkstra 中 $(d, b)$ 出现在最后（因为 $b$ 先通过 $a \to b$ 定型，$d$ 很晚才被弹出），而 DAG Relaxation 中 $(d, b)$ 紧跟 $(a, d)$——处理顺序由算法性质决定：前者是"贪心的最短路优先"，后者是"无条件的拓扑序优先"，同一个图、同一条边，两种视角下松弛时机完全不同。

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 6-2. Short Circuits（短路）</span>

给定 weighted directed graph（带权有向图）$G = (V, E, w)$ 与 vertex $s \in V$，且满足性质：对每个 vertex $v \in V$，存在某条从 $s$ 到 $v$ 的 minimum-weight path（最小权重路径）至多经过 $k$ 条 edges。描述一个在 $O(|V| + k|E|)$ 时间内求出从 $s$ 到每个 $v \in V$ 的 shortest-path weight（最短路径权重）的 algorithm（算法）。

> **[solution] Solution（解答）:** 由于该图可能包含 cycles（环）和 negative weights（负权），乍一看我们似乎无法做得比 Bellman-Ford 更好。幸运的是，题目给出了额外限制：到每个 vertex 的最短路径经过的 edges 很少。由于 Bellman-Ford 的 duplicated graph（复制图）$G'$ 的第 $k'$ 层对应"使用至多 $k'$ 条 edges 到达该 vertex 的最短路径"，我们的做法是修改 Bellman-Ford，使其只增量式地构建复制图的各层，在线地把 edges 松弛进新层以计算 $k'$ 条边最短路径，当 $k'$ 条边最短路径距离在相邻层之间不再变化时停止。
>
> 具体来说，与其一次性创建整个复制图 $G'$ 再运行 DAG Relaxation，我们开始时让 $G'$ 只包含第一层（对 $v \in V$ 的 $v_0$），并把 $\delta$ 初始化为第一层距离：对 $v \in V$ 令 $\delta(s_0, v_0) = \infty$，除了 $\delta(s_0, s_0) = 0$。
>
> 然后从 $i = 0$ 开始，归纳地假设 $G'$ 已包含第 $0$ 到 $i$ 层，且对 $v \in V$、$j \in \{0, \ldots, i\}$ 已计算出 $\delta(s_0, v_j)$；现在追加第 $i+1$ 层，即加入 vertices $v_{i+1}$（$v \in V$）以及来自第 $i$ 层的关联 edges。这一新层不会影响前面各层的距离（因为新层在 topological order（拓扑序）中位于更后面）。于是继续 DAG Relaxation，松弛第 $i$ 层 vertices 出发的新 edges，这能正确计算出所有 $v \in V$ 的 $\delta(s_0, v_{i+1})$。
>
> 由于从 $s$ 到每个 vertex 的最短路径至多使用 $k$ 条 edges，对每个 $k' \ge k$，距离 $\delta(s, v)$ 都等于 $k'$ 条边距离 $\delta_{k'}(s, v) = \delta(s_0, v_{k'})$。因此，一旦对 $v \in V$ 都有 $\delta(s_0, v_{k'}) = \delta(s_0, v_{k'+1})$，就有 $k' = k$，可以终止并输出 $\delta(s, v) = \delta(s_0, v_k)$（$v \in V$）。
>
> 由于每个 vertex 都从 $s$ 可达，$|V| = O(|E|)$；又因为我们只构建 $G'$ 的 $k+1$ 层就找到两个相等的层，且每层处理至多 $O(|E|)$ 时间，该算法运行时间为 $O(k|E|)$（亦即 $O(|V| + k|E|)$）。题目中原本给出 $|V|$ 是为了允许输入包含不连通图的情形——此时可以先运行一次 single-source reachability（单源可达性）算法，把图限制到从 $s$ 可达的子集上；但对连通输入图，这一项不再相关。

> **Rubric（评分标准）:**
> - 描述一个运行时间为 $O(k|E|)$ 的正确算法：6 分
> - 正确性论证正确：2 分
> - 运行时间论证正确：2 分
> - 可酌情给部分分
> - 正确的 $O(|V||E|)$ 时间算法最多 4 分

---

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这道题的本质是**利用"最短路径很浅"这个结构假设来剪掉 Bellman-Ford 的无效迭代**。Bellman-Ford 之所以要跑 $|V|-1$ 轮，是因为最坏情况下最短路径要经过 $|V|-1$ 条边；如果题设保证路径至多 $k$ 条边，那么只需 $k$ 轮。而"相邻两层距离相等就停止"相当于一个 termination condition（终止条件）：一旦再多的边也不会让任何距离变小，说明所有 shortest path 都已经被找到。这和你在 6.006 Lecture 14 学的"Bellman-Ford 第 $i$ 轮后得到至多 $i$ 条边的最短路径"是同一个事实的两种用法。这与 Lecture 14 的核心结论一致：Bellman-Ford 第 $i$ 轮结束后，计算出的最短路径至多使用 $i$ 条边——本题只是把这个"至多 $i$ 条边"的上界从 $|V|-1$ 收紧到已知的 $k$，并利用"相邻两层距离不再变化"作为终止条件。另外注意：这个算法本质上是 online（在线）地构建分层图，而不是像原始 Bellman-Ford 那样整张图建好再跑 DAG Relaxation，空间上更省。

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 6-3. Dynamite Detonation（炸药引爆）</span>

超级间谍 Bames Jond（邦姆斯·琼德）正在逃离邪恶大亨 Silvertoe（西尔弗托）位于阿尔卑斯山的巢穴。Bames 偷了一副滑雪板和一张 trail map（小径地图），上面列出了山上的 clearings（空地）与 slopes（坡道）（共 $n$ 处），她想从巢穴旁的 clearing $L$ 滑到停放雪地摩托的 clearing $S$。

- 每个 clearing $c_i \in C$ 有一个整数 elevation（海拔）$e_i$（海平面以上）。
- 每条 slope（坡道）$(c_i, c_j, \ell_{ij})$ 连接一对 clearings $c_i$ 和 $c_j$，是一条 monotonic trail（单调小径）（海拔严格递减或递增），具有正整数 length（长度）$\ell_{ij}$。Bames 没有时间向上滑，所以她只会沿降低海拔的方向通过 slopes。

- 在上山的路上，Bames 在已知位置 $C_D \subset C$ 埋设了 dynamite（炸药）。引爆后，$c_i \in C_D$ 处 clearings 的海拔会立即改变已知的量，从 $e_i$ 降到更低的 $e'_i < e_i$。引爆器在 clearing $D \in C$ 处（那里没有炸药）。如果她到达 clearing $D$，她可以选择在继续前进前引爆炸药。

给定 Bames 的地图和炸药数据，描述一个 $O(n)$ 时间的 algorithm，求出她必须滑雪到达雪地摩托的最短距离（沿途可能引爆炸药）。

> **[solution] Solution（解答）:** 我们可以把这座山建模为一个 DAG，其中的小径是 Bames 可能下坡滑行的方向——无论引爆前还是引爆后都是如此。构造图 $G_1$：每个 clearing 一个 vertex，每条 slope 一条指向更低 clearing 的 directed edge（有向边）；删去沿路海拔不变的那些 slopes（因为 Bames 不会沿任一方向通过这种 slope）。再以同样的方式构造第二个图 $G_2$，只是使用修正后的海拔 $e'_i$，表示爆炸后山的状态。在两个图中，都用对应 slope 的长度 $\ell_{ij}$ 作为 edge weight（边权）。把 $G_1$ 与 $G_2$ 连接成单个图 $G$：添加一条从图 $G_1$ 中节点 $D_1$ 到图 $G_2$ 中节点 $D_2$ 的权重为 $0$ 的 directed edge（走这条边表示引爆炸药）；再添加一个 supernode（超级节点）$T$，它接收来自图 $G_1$ 中节点 $S_1$ 与图 $G_2$ 中节点 $S_2$ 的零权重入边（分别表示不引爆或引爆后到达 $S$）。
>
> 现在从图 $G$ 中的节点 $L_1$ 对 supernode $T$ 运行 DAG Relaxation；最短的这样一条路径就是「无论是否引爆，在遵守 Bames 只降低海拔的约束下，从 $L$ 到 $S$ 的最小距离」。图 $G$ 有 $O(n)$ 个 vertices 和 edges，所以 DAG Relaxation 在 $O(n)$ 时间内运行完毕，符合要求。

> **Rubric（评分标准）:**
> - 构造一个可用于求解该问题的图：6 分
> - 正确算法的描述：3 分
> - 正确性论证正确：2 分
> - 运行时间论证正确：3 分
> - 若算法高效，即 $O(n)$ 时间：6 分
> - 可酌情给部分分

---

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这题展示了一个在算法设计中反复出现的**"世界分裂为两个版本"的建模手法**：把"可选动作"（这里是一次引爆）编码为从一个副本图到另一个副本图的一条零权边。你在 6.006 里会多次见到这个模式——Quiz 2 的 Color Cost（换颜色付费）用 3 个颜色副本，Bellham's Fjord 用 Johnson 重加权处理负权，本质都是"把状态差异展开成图的结构"。这里的建模要点是：**引爆只发生一次且发生在到达 $D$ 的时刻**，所以从 $G_1$（未引爆世界）到 $G_2$（引爆后世界）只有一条单向边 $D_1 \to D_2$；一旦进入 $G_2$ 就再也回不去 $G_1$，这恰好对应"炸药只能引爆一次"的物理现实。直觉上可以把它想成 CSAPP 里的 state machine（状态机）：$G_1$ 和 $G_2$ 是两个状态，$D_1 \to D_2$ 是唯一的状态迁移边。为什么答案是 DAG Relaxation 而不是 Dijkstra？因为两个图里都只保留了"海拔下降"方向的边，整个 $G$ 天然无环。

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 6-4. Conservative Cycles（保守环）</span>

在 Wentonian physics（温托尼亚物理学）中，一个 force field（力场）通过对粒子沿任意 path（路径）运动要求一定量的正功或负功来作用于粒子。若沿每条 closed loop（闭合回路）的总功之和为零，则该力场是 conservative（保守）的。给定一个离散 force field，由 $n$ 个可能的粒子位置 $\ell_i$ 和 $O(n)$ 条可能的 particle transitions（粒子转移）表示，其中 transition $(\ell_i, \ell_j, w_{ij})$ 沿一条从位置 $\ell_i$ 到位置 $\ell_j$ 的有向路径移动粒子，需要（正或负）整数功 $w_{ij}$。描述一个 $O(n^2)$ 时间的 algorithm，判断该力场是否 conservative。

> <span style="color:#7f8c8d;">Footnote（脚注）: 注意从 $\ell_i$ 到 $\ell_j$ 的 transition 并不暗示存在从 $\ell_j$ 到 $\ell_i$ 的 transition。</span>

> **[solution] Solution（解答）:** 构造图 $G$：每个粒子位置 $\ell_i$ 一个 vertex，每条 transition $(\ell_i, \ell_j, w_{ij})$ 一条权重为 $w_{ij}$ 的 directed edge $(\ell_i, \ell_j)$。要反驳力场是保守的，只需在 $G$ 中找到一条 non-zero weight（非零权重）的 cycle。添加一个 supernode（超级节点）$s$，用零权重 directed edge $(s, v)$ 连到每个 $v \in V$（这不会给图增加任何新 cycles）。然后从 $s$ 运行 Bellman-Ford，判断是否存在 negative-weight cycles（负权环）；再把所有 edge weights 取负，从 $s$ 再运行一次 Bellman-Ford，判断是否存在 negative-weight cycles（即原图中的 positive-weight cycles（正权环））。如果 Bellman-Ford 检测到任一类 cycle，就返回该力场不保守（因为我们找到了一个 non-zero weight 的 cycle）；否则不存在任何非零权 cycle，可以返回该力场是保守的。
>
> 由于我们只是给一个具有 $n$ 个 vertices、$O(n)$ 条 edges 的图加了一个节点和 $O(|n|)$ 条 edges，Bellman-Ford 将耗时 $O(n^2)$，符合要求。
>
> 注意：这个问题其实可以用本课程尚未学过的算法在 $O(n)$ 时间内解决，但这超出了本课程范围。具体来说：
> - 用 modified DFS（修改版 DFS）在 $O(n)$ 时间内找出 $G$ 的 strongly connected components（强连通分量，SCCs）；
> - 在每个 SCC 内用 DFS 给每个 vertex 赋 shortest-path length potentials（最短路径长度势）；
> - 然后用 $O(n)$ 时间把每个 SCC 的每条 edge 与这些 potentials 对照检查。

> **Rubric（评分标准）:**
> - 正确算法的描述：3 分
> - 正确性论证正确：2 分
> - 运行时间论证正确：2 分
> - 若算法高效，即 $O(n^2)$：3 分
> - 可酌情给部分分

---

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这个问题的物理内核你已经在高中物理见过：**conservative force（保守力）沿闭合路径做功为零**（例如重力、静电力），而 non-conservative force（非保守力）（如摩擦力）沿闭合路径做功不为零。把"做功"建模为边权后，"闭合回路总功为零"就变成"所有 cycle 的权重和为 $0$"。于是问题归结为：**图中是否存在权重和非零的 cycle？** 由于任意 cycle 的权重要么为正要么为负（不可能既是零又非零），检查"是否有负权环或正权环"两步即可。你可能会问为什么不用一次 Bellman-Ford 检查 $\ne 0$——因为 Bellman-Ford 只能可靠地检测 negative-weight cycle（负权环），所以对原图跑一次查负环、对取反后的图再跑一次查正环。这里的 $O(n^2)$ 来自"图有 $O(n)$ 条边所以 Bellman-Ford 是 $O(n \cdot n)$"。脚注提到的"方向不对称"决定了必须用有向图建模，这也是为什么简单地把每条 transition 当成无向边会出错。

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 6-5. SparkPlug Derby（火花塞德比）</span>

LightQueen McNing（光女王·麦克宁）是一辆赛车，她想开到加州参加年度 road race（公路赛）：SparkPlug Derby（火花塞德比）。她有一幅地图，描绘了：

- 国内的 $n$ 个 intersections（路口），每个路口 $x_i$ 标有正整数 elevation（海拔）$e_i$，以及是否包含 gas station（加油站）；以及
- 连接它们之间的 $r$ 条 roads（道路），每条道路 $r_j$ 标有正整数 $t_j$，表示 LightQueen 沿任一方向开过它所需的时间。

有些路口连接很多 roads，但任意路口处 roads 的平均数小于 $5$。LightQueen 需要从路口 $s$ 处的 Carburetor Falls（化油器瀑布）到达路口 $t$ 处的 SparkPlug Derby 赛道，并满足以下条件：

- LightQueen 的 gas tank（油箱）容量为小于 $n$ 的正整数 $g$：它一次最多可容纳 $g$ 单位汽油（出发时是满的）。沿途她可以在任何标有 gas station 的路口加油（任意整数单位）。她每加满 1 单位汽油恰好需要 $t_G$ 时间。
- LightQueen 只在 uphill（上坡）行驶时耗油。具体地，如果她沿一条 road 从海拔分别为 $e_i$ 和 $e_j$ 的路口 $x_i$ 开到 $x_j$，当 $e_j > e_i$ 时恰好消耗 $e_j - e_i$ 单位汽油，否则消耗 $0$ 单位。

给定 LightQueen 的地图，描述一个 $O(n^2 \log n)$ 时间的 algorithm，返回一条到达赛道的、途中始终让油箱保持 strictly positive（严格为正）油量的最快路线（如果这样的路线存在的话）。

> **[solution] Solution（解答）:** 创建图 $G$：
>
> - **Vertices:** 对每个路口 $v$，为每个 $i \in \{1, \ldots, g\}$ 添加一个 vertex $v_i$，其中 $v_i$ 表示"位于路口 $v$ 且油箱里有 $i$ 单位汽油"的状态；
> - **Edges:** 对每条连接路口 $u$ 和 $v$、行驶时间为 $t(u, v)$ 的 bidirectional road（双向道路）$\{u, v\}$（设 $e(u)$ 与 $e(v)$ 分别为路口 $u$ 和 $v$ 的海拔，不失一般性假设 $e(u) \le e(v)$），构造如下 directed edges：
>   1. **(Down-hill Road Edges（下坡道路边）)**
>      – 对每个 $i \in \{1, \ldots, g\}$ 添加一条权重为 $t(u, v)$ 的边 $(v_i, u_i)$（因为沿该方向行驶不耗油）。
>   2. **(Up-hill Road Edges（上坡道路边）)**
>      – 若 $e(u) = e(v)$，再加一条与之前方向相反的权重为 $t(u, v)$ 的边：对每个 $i \in \{1, \ldots, g\}$ 添加 $(u_i, v_i)$；
>      – 否则 $e(v) - e(u) = \ell > 0$，则对每个 $i \in \{\ell + 1, \ldots, g\}$ 添加一条权重为 $t(u, v)$ 的边 $(u_i, v_{i-\ell})$（因为上坡要耗油，而她绝不允许把油耗尽）。
>   3. **(Gas Station Edges（加油站边）)**
>      – 对每个加油站，例如在路口 $v$ 处，对每个 $i \in \{1, \ldots, g-1\}$ 添加一条权重为 $t_G$ 的边 $(v_i, v_{i+1})$（对应在加油站给油箱加 1 单位油）。
>
> 下坡道路边共有 $gr$ 条，上坡道路边至多 $gr$ 条，加油站边至多 $(g-1)n$ 条，因此图 $G$ 有 $gn$ 个 vertices 和 $O(g(r+n))$ 条 edges。该图具有如下性质：任何从 vertex $s_g$ 到某个 vertex $t_i$（$i \in \{1, \ldots, g\}$）的 path 都对应于 LightQueen 满油出发、途中从不耗尽油、最终到达 SparkPlug Derby 的一条合法路线；且 path 的权重恰为她到达所需的时间。于是从 $s_g$ 求解 SSSP，找到到每个 $t_i$（$i \in \{1, \ldots, g\}$）的最小权重 path，返回其中权重最小的一条（若不存在则返回没有这样的路线）。该图可能包含 cycles，但所有 edge weights 均为正，所以用 Dijkstra 求解 SSSP。
>
> 由于每个路口的平均 degree（度数）$< 5$，且每条 road 连接两个路口，所以 $2r < 5n$，$r = O(n)$。又因为题目规定 $g < n$，$G$ 有 $O(n^2)$ 个 vertices 和 $O(n^2)$ 条 edges，构造耗时 $O(n^2)$。随后 Dijkstra 耗时 $O(n^2 \log(n^2) + n^2) = O(n^2 \log n)$，而找出到某个 $t_i$ 的最小 path 耗时 $O(n)$，总时间 $O(n^2 \log n)$，符合要求。

> **Rubric（评分标准）:**
> - 构造一个可用于求解该问题的图：6 分
> - 正确算法的描述：3 分
> - 正确性论证正确：2 分
> - 运行时间论证正确：3 分
> - 若算法高效，即 $O(n^2 \log n)$ 时间：6 分
> - 可酌情给部分分

---

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这是"**把资源量展开成图的一个维度**"的经典建模：油箱容量 $g$ 成为分层下标，$v_i$ 表示"在 $v$ 且有 $i$ 单位油"。你之前在 prob7sol 的 Critter Collection（背包 $k$ 个 Pocket Sphere）里见过完全相同的技巧——那里是 $k+1$ 个"球数状态"分层，这里是 $g$ 个"油量状态"分层。两个题的建模思路同构：**任何"受限于整数资源的移动"都可以通过把资源计数变成 vertex 下标来展开成普通最短路**。为什么油量只取 $1..g$？因为容量上界是 $g$，超过 $g$ 的状态不存在；为什么上坡边从 $i = \ell+1$ 开始？因为 $i \le \ell$ 时开完这条上坡路油就 $\le 0$，违反"严格为正"约束。注意这里和 Critter Collection 的一个差别：加油站边 $(v_i, v_{i+1})$ 让油量逐单位增加，等价于"在 $v$ 停留 $t_G$ 时间买 1 单位油"——把"等待/购买"也编码成了边。这道题的时间上界 $O(n^2 \log n)$ 来自 $g < n$，所以分层图规模从 $O(gn)$ 变成 $O(n^2)$。

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 6-6. Johnson's Algorithm（约翰逊算法）</span>

本题中，你将实现 **Johnson's Algorithm**（约翰逊算法）来计算一般 weighted directed graph（带权有向图）$G$ 中的 all-pairs shortest-path weights（全源最短路径权重），如 Lecture 14 所述。算法的输入为：一个正整数 $n$，表示图中 vertices 的个数（用连续整数 $0$ 到 $n-1$ 标识）；以及一个由三元组组成的 tuple（元组）$S$，其中每个 triple（三元组）$(u, v, w)$ 对应一条从 vertex $u$ 到 $v$、权重为 $w$ 的 directed edge。你的输出应该是一个长度为 $n$ 的 tuple $D$，其中每个元素是长度为 $n$ 的 tuple，且对所有 $u, v \in \{0, \ldots, n-1\}$ 有 $D[u][v] = \delta(u, v)$；但当输入图包含 negative-weight cycle（负权环）时，你应该返回 `None`。

请在提供的模板代码中实现 `johnson(n, S)` 函数。你的代码模板中包含可用的 Bellman–Ford 与 Dijkstra 实现（使用 binary heap（二叉堆）作为 priority queue（优先队列）），它们是从 recitation notes（习题课讲义）修改而来的。注意如果你要使用这些代码，需要自己构造 adjacency list（邻接表）和 weight function（权重函数）。你可以从网站下载代码模板和一些 test cases（测试用例）。

> **[solution] Solution（解答）:**（Python 代码，保持原文）

```python
INF = 99999  # distance magnitudes will not be larger than this number

def johnson(n, S):
    D = [[INF for _ in range(n)] for _ in range(n)]
    Adj = [[] for _ in range(n)]
    # construct graph
    W = {}
    for (u, v, w) in S:
        Adj[u].append(v)
        W[(u, v)] = w
    Adj.append([i for i in range(n)])
    # run bellman-ford from supernode
    for i in range(n):
        W[(n, i)] = 0
    def wf(u, v):
        return W[(u, v)]
    args = bellman_ford(Adj, wf, n)
    if args is None:
        return None
    h, _ = args
    def wf(u, v):
        return W[(u, v)] + h[u] - h[v]
    for u in range(n):
        # compute SSSP on reweighted graph
        d, parent = dijkstra(Adj, wf, u)
        for v in range(n):
            if d[v] < INF:
                D[u][v] = d[v] - h[u] + h[v]
    return tuple(tuple(row) for row in D)
```

---

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这段代码把 Johnson's Algorithm 的三个阶段浓缩成了 20 行：**(1) 加超节点**：`Adj.append([i for i in range(n)])` 与 `W[(n, i)] = 0` 添加了一个虚拟节点 $n$，从它到每个 vertex 有零权边；**(2) Bellman-Ford 求势**：从超节点跑 `bellman_ford(Adj, wf, n)`，若返回 `None`（检测到负权环）则整个算法失败，否则得到势函数 $h$；**(3) 重加权 + $n$ 次 Dijkstra**：`wf(u, v) = W[(u, v)] + h[u] - h[v]` 保证新权重非负（这正是势函数的核心性质），对每个 $u$ 跑 Dijkstra 后，再用 `d[v] - h[u] + h[v]` 把距离还原回原图尺度。🎥 *Demaine 在 Lecture 14 里对"为什么要重加权"这样解释*："So maybe there's a way I could reweight my edges so that shortest paths stay the same."（翻译：所以也许有办法重加权我的边，使得最短路径保持不变。）——重加权保持最短路径不变的原因在于：从 $u$ 到 $v$ 的任意 path 的总权重都整体加上同一个常数 $h[u] - h[v]$，路径之间的相对大小关系不受影响。最后 `return None` 的分支对应负权环存在的情形——此时 all-pairs shortest paths 无定义。如果你想验证这段代码，可以把 `INF = 99999` 换成更大的数并用已知图测试（比如 PS6-1 的图，$D[u][v]$ 应与手算 $\delta$ 一致）。

---

> <span style="color:#7f8c8d;">MIT OpenCourseWare · 6.006 Introduction to Algorithms, Spring 2020 · https://ocw.mit.edu</span>
