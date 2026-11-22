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
>
> 这道题真正要练的模板只有一个：**relax（松弛）的顺序由谁买单**。两个算法做的动作一模一样，都是对每条 edge $(u, v)$ 执行 $d[v] \leftarrow \min\{d[v],\ d[u] + w(u, v)\}$；分歧只在"$u$ 什么时候有资格去松弛自己的出边"。DAG Relaxation 的答案是"按拓扑序轮到你时"，Dijkstra 的答案是"你的估计值恰好是全场最小、被弹出时"。把这两句话记住，两张 relaxation order（松弛顺序）列表就是这两句话的直接展开，不需要背。
>
> 两种顺序都合法，是因为各自背了一条 invariant（不变式）。DAG 那条：处理到拓扑序上第 $i$ 个 vertex 时，它所有入边都已从更早的 vertices 松弛完毕，估计值此后不可能再降，处理完即定型——这条论证只用到"无环"，一个字没用到权重符号，所以负权也无所谓。Dijkstra 那条：弹出估计值最小的 $u$ 时，任何另一条通往 $u$ 的路径都必须先经过某个当时还在队列里的 $x$，而 $x$ 的估计值已不小于 $u$ 的，再加一条非负的边只会更大。这一步是 Dijkstra 全部正确性的落脚点，也是它唯一的软肋：一旦出现负权，"加非负边只会更大"当场失效。
>
> 用本题这张图算清楚。图有 6 个 vertex、9 条 edge。DAG 那侧处理顺序是 $a, d, b, e, f, c$，9 次松弛尝试里 6 次真把某个估计值改小了：$(a,b)$ 给出 2、$(a,d)$ 给出 6、$(d,e)$ 把 $e$ 从 $\infty$ 降到 6、$(b,c)$ 给出 3、$(b,e)$ 把 $e$ 从 6 再压到 5、$(b,f)$ 给出 4。Dijkstra 那侧弹出顺序是 $a, b, c, f, e, d$，9 次尝试里只有 5 次改小。差的正是 $(d,e)$：DAG 里处理 $d$ 时估计值是 6，把 $e$ 压到 6，一个当时"对但不最对"的值；Dijkstra 里 $d$ 被弹出时已是最后一轮，$e$ 早定型在 5，$6 + 0 = 6 > 5$，这次松弛白跑。两者尝试次数相同、都是 9，区别只在"谁在什么时候把一个暂时正确的值当定论"。
>
> 顺手核对答案量级：$a=0,\ b=2,\ c=3,\ d=6,\ e=5,\ f=4$。$d$ 走直连边 $a \to d$（权重 6），而 $e$、$f$、$c$ 都绕道 $b$：$2+3=5$、$2+2=4$、$2+1=3$——最短路比的从来不是"哪条边最小"，而是整条路径的累加和。
>
> 跨课程连接在 6.042J：那里你证过，有向无环图上的可达关系去掉自反性后满足传递性与反对称性，是个 strict partial order（严格偏序），而 topological order 正是这个偏序的一个 linear extension（线性扩展）——把偏序拉成一条不违反它的全序。连接路径：把"必须先经过 $u$ 才能到 $v$"读作 $u \prec v$，拓扑排序就是给这个偏序排一条满足它的直线。**区别**是 6.042J 只回答"这样的直线存在吗"（存在，当且仅当无环），6.006 要在 $O(|V| + |E|)$ 内造出来并立刻当松弛顺序用。
>
> 第二个连接放在 CSAPP 第 6 章：cache（高速缓存）的替换策略也在维护一个"先弹谁"的顺序，但排错了只是 hit rate（命中率）下降，答案不会错；Dijkstra 排错一次，$\delta(a, v)$ 就是错的。启发式排序与决定性排序的差别全在这里。
>
> 一个术语提醒：topological order 里的 topology 只是命名遗留，与拓扑学那门课无关，它只表示"把箭头都朝前的一种排队"，不认识拓扑学不影响读这段。
>
> 一句话收束：DAG Relaxation 的顺序是图的结构白送的，Dijkstra 的顺序要用"权重非负 + 每次取最小"才买得下来；那两张 relaxation order 列表，就是这个价差的账单。

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
>
> 把机制再推一层：Bellman-Ford 是一个**逐层逼近**的过程，第 $i$ 轮结束时的估计值恰好是"至多 $i$ 条 edge 的最短路" $\delta_i(v)$，而 $\delta_i$ 关于 $i$ 单调不增、又有下界，所以这个序列必然在有限步后停住；停住的那一步就是"真正用得上的最大边数" $k'$。题目给出的 $k$ 只是在预先告诉你 $k' \le k$，于是把"固定跑 $|V|-1$ 轮"的预算，换成"跑到不动为止"的预算。本题的全部技巧就这一句话：**把上界从顶点的个数换成路径的深度**。
>
> 单调性是可以算出来的：$\delta_{i+1}(v) = \min\{\delta_i(v),\ \min_{(u,v) \in E} \delta_i(u) + w(u,v)\}$——第 $i+1$ 层既允许"沿用旧值"，也允许"再多走一条边"，取两者的更小者，所以只降不升。停止判据的正确性来自一个引理：若某一层之后所有 vertex 都满足 $\delta_{k'}(v) = \delta_{k'+1}(v)$，则对所有 $j > k'$ 都有 $\delta_j = \delta_{k'}$，因为第 $j+1$ 层只是拿一对相等的数再做一次 min 与加法，结果必然不动。这就是"再多的边也改变不了任何距离"的形式化版本；换句话说，$\delta$ 序列的不动点就是答案，而检查不动点只要一次逐 vertex 比较。
>
> 手算一个小例子。取 $V = \{s, a, b, c, d, e\}$，共 6 个 vertex、7 条 edge：$(s,a,5)$、$(s,b,4)$、$(s,c,3)$、$(s,d,2)$、$(s,e,1)$，再加两条负权边 $(a,e,-10)$ 与 $(b,d,-10)$。初始化 $\delta_0 = (0, 5, 4, 3, 2, 1)$ 之外的项全为 $\infty$，第一层松弛后 $\delta_1 = (0, 5, 4, 3, 2, 1)$；第二层用负权边改进：$e$ 从 1 降到 $5 + (-10) = -5$，$d$ 从 2 降到 $4 + (-10) = -6$，于是 $\delta_2 = (0, 5, 4, 3, -6, -5)$；第三层再做一遍，值完全不变，$\delta_3 = \delta_2$，判定 $k' = 2$ 并停机。此时总共做了 $3 \times 7 = 21$ 次松弛，而朴素 Bellman-Ford 要跑 $|V| - 1 = 5$ 轮、$5 \times 7 = 35$ 次——省掉的那 14 次全是"再走 3 条以上边也到不了更短"的无效工作。注意这个例子里 $k' = 2 < |V| - 1 = 5$，正是题设那种"最短路都很浅"的图；如果换成一条 6 个顶点的长链，$k' = 5$，本算法就退化成原始 Bellman-Ford，一点不省——**结构假设是有条件的红利，不是免费加速**。
>
> 把规模放大就明白这个红利有多值钱：取 $|V| = 10^6$、$|E| = 2 \times 10^6$、$k = 5$，朴素 Bellman-Ford 是 $10^6 \times 2 \times 10^6 = 2 \times 10^{12}$ 次松弛，本题算法是 $5 \times 2 \times 10^6 = 10^7$ 次，差 20 万倍；同一台机器上这是"几分钟"与"几毫秒"的差别。
>
> 跨课程连接放在 100B 实分析：$\delta_i(v)$ 是一个单调不增且有下界的实数序列，Rudin 那套语言会立刻告诉你它收敛——收敛是免费的。但收敛定理只保证极限存在，不告诉你第几步到位；算法的全部工作量在于把"收敛"翻译成"某个层之后恒等"。这正是迭代法与精确算法那条模糊的界线：**收敛率决定你要跑多少轮，结构假设决定这个轮数的上界是多少**。区别在于实分析关心极限与 $\epsilon$-$N$ 的存在性，这里关心 $N$ 的显式上界 $k$。
>
> 另一个连接在 CSAPP 第 6 章：原始做法要建整张复制图，占 $O(k|V|)$ 的 vertex；本题的 online（在线）做法只保留相邻两层，等于把 working set（工作集）缩到 $O(|V|)$——和 cache（高速缓存）里"只把当前用得到的那一页留在片上"是同一个成本直觉。
>
> 一句话收束：这道题练的是把"最坏情况上界"替换成"由输入结构给出的紧上界"，再用不动点检查把这个上界自动找出来。

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
>
> 先把"为什么一条边就够"说透：状态空间其实是 $V \times \{0, 1\}$ 这个二元组集合，第二个分量记录"炸药引爆了没有"。由于引爆是**二值的、最多一次、触发地点唯一**的动作，跨界只发生在 $D$ 这一格，所以只需要一条边。三个条件缺一个，边数就要涨：若能在任意 clearing 引爆，就得加 $n$ 条跨界边；若允许引爆两次，就得配 $k+1$ 份副本图并加 $k$ 条跨界边；若引爆不再免费，就在跨界边上加权。这题真正练的模板就叫"一次性动作换一份副本"，判据是上面那三句话，是可以照着套的。
>
> 反面也要说清：引爆**并不单调有利**，所以解答只写"取最小值"而不敢写"引爆后更优"。把 $e_D$ 降低，等于把"离开 $D$ 的下降门槛"抬高，$D$ 的出边只会变少；被埋炸药的那几个 clearing 则相反，它们海拔降低后，"从高处进入它们"的边变多。于是一个版本图的边集不是另一个的子集，两条支路必须都算出来再比。顺带说一句细节：因为 $G_2$ 内部仍然严格降海拔，她进了 $G_2$ 之后回不到 $D_2$，所以"降低 $D$ 自身引来的新入边"在 $G_2$ 里是死代码——这解释了为什么这一题的收益只能来自被埋炸药的 clearing，而不能来自 $D$ 自己。
>
> 手算一个例子把它落实。取 $C = \{L, A, D, S\}$，elevation 依次是 $10, 12, 8, 0$；炸药埋在 $A$（引爆后 $e'_A = 7$），引爆器在 $D$。坡道与长度：$\{L, A\}$ 长 4、$\{A, D\}$ 长 1、$\{L, D\}$ 长 9、$\{D, S\}$ 长 5、$\{A, S\}$ 长 2。在 $G_1$ 里可用的下坡方向是 $A \to L$、$A \to D$、$L \to D$、$D \to S$、$A \to S$；从 $L$ 出发到 $S$ 只有 $L \to D \to S = 9 + 5 = 14$，因为 $A$ 在海拔 12，她上不去。在 $G_2$ 里 $A$ 降到 7，$D(8) \to A(7)$ 这条原本上坡的坡道变成下坡、可用，长度仍是 1；而 $A \to D$ 因为 $7 < 8$ 变成上坡，消失了。于是 $L \to D$（9）$\to$ 引爆（0）$\to A \to S$（$1 + 2 = 3$），总长 12，比 14 省 2。若把 $e'_A$ 改成 9，$D \to A$ 又变成上坡，这条路断掉，答案退回 14——"引爆一定更省"的直觉在这里就被一个数推翻了。
>
> 跨课程连接放在 6.042J：状态集 $V \times \{0, 1\}$ 就是两个集合的 cartesian product（笛卡尔积），在它上面建的图叫 product graph（积图）。连接路径：把"是否引爆"当成一个布尔变量 $b$，跑一次标号算法等于在有序对 $(v, b)$ 上做搜索，这和你用有序对造关系、再去数关系个数的做法同源。区别是 6.042J 关心关系本身的性质（自反、对称、传递），这里关心在这个关系上走一趟的最短长度。
>
> 第二个连接就在本份作业里：Johnson's algorithm（Johnson 算法）那题是"换权重、不换拓扑"——重加权后边集一模一样，只有数值变了；这题正相反，是"换拓扑、不换权重"——坡道长度一个没改，只是把可用的边集拆成两份。同一份 PS 里并列出现这两种手法，正好说明建模只有两只手：改数值，或者改结构。
>
> 一句话收束：看到"某个动作最多做一次、而且只能在固定地点做"，就先问状态要不要多一维；要多一维，就只加一条跨界边，再把两版图的终点都接进同一个 supernode（超级节点），最后取最小。

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
>
> 把机制推到底：这题的第一性原理是"路径无关性"。说"每个 cycle 的权和为零"，等价于说存在一个 potential（势函数）$p: V \to \mathbb{R}$，使每条 edge 都满足 $w(u, v) = p(v) - p(u)$。两个方向都不难：若这样的 $p$ 存在，沿任何一个闭合回路走一圈，权和是一个 telescoping sum（望远镜和），逐项相消必为 0；反过来，固定一个起点 $r$，令 $p(v)$ 等于"从 $r$ 走到 $v$ 的任意一条路径的权和"，那么任意两条这样的路径拼起来就是一个闭合回路，权和为 0，所以两条路径权和相同、$p(v)$ 与路径的选取无关，这就是 well-defined（良定义）的全部内容；再由 $p(v) = p(u) + w(u, v)$ 就得到所需等式。做题时这条等价刻画比"检查所有 cycle"好用得多，因为 cycle 有指数多个，而 $p$ 只有 $n$ 个未知数。
>
> 为什么必须跑两趟 Bellman-Ford？因为它的检测机制是"第 $n$ 轮还能把某个估计值改小"——只认"越走越小"，即只认 negative-weight cycle（负权环）。而"权和非零"有两种符号，正环它看不见。把所有 edge weight 取负，正环就变成负环，于是第二趟补齐。想省掉第二趟是不行的：这等于要求一个只会找"下降"的机制去识别"上升"，机制本身不允许。
>
> 手算一个三角形把两趟的必要性算出来。取三个位置 $\ell_1, \ell_2, \ell_3$，transition 为 $(\ell_1, \ell_2, 3)$、$(\ell_2, \ell_3, -1)$、$(\ell_3, \ell_1, -2)$，权和 $3 - 1 - 2 = 0$，力场保守。验证势函数：令 $p(\ell_1) = 0$，沿边推得 $p(\ell_2) = 3$、$p(\ell_3) = 2$，回头检查第三条边 $w(\ell_3, \ell_1) = -2 = p(\ell_1) - p(\ell_3) = 0 - 2$，吻合，说明这一组 $p$ 真的存在。现在把 $(\ell_2, \ell_3)$ 从 $-1$ 改成 $+1$：权和变成 $3 + 1 - 2 = 2 > 0$，存在正环。此时第一趟 Bellman-Ford 白跑（原图没有负环，跑了 $n$ 轮什么都没检出），只有取反之后再跑第二趟，权和 $-2$ 暴露成负环，才判定不保守。对照之下若把那条边改成 $-3$，权和 $3 - 3 - 2 = -2 < 0$，第一趟就检出了——两个方向各有一个例子，正好说明两趟不是冗余。
>
> 复杂度也要算清楚：$|E| = O(n)$，Bellman-Ford 是 $O(|V| \cdot |E|) = O(n \cdot n) = O(n^2)$，加 supernode（超级节点）与它的 $n$ 条零权边不改变量级。但 $O(n^2)$ 并不便宜：$n = 10^4$ 时是 $10^8$ 次松弛，实数秒级；这也正是解答末尾那个 $O(n)$ 改进的动机：只在 strongly connected component（强连通分量）内部找环。
>
> 跨课程连接放在 18.065 与 Strang 的线性代数。把每条 edge 的权重排成一个向量 $w$，再写一个 incidence matrix（关联矩阵）$B$：每行对应一条 edge，起点位置写 $-1$、终点写 $+1$。那么"存在势函数"这句话就是 $w = Bp$——$w$ 落在 $B$ 的列空间里。四个基本子空间的语言一翻译就通：$B$ 的零空间里的向量是"每个顶点涨落相同"的那些方向，列空间则与它正交，于是"$w$ 有解"等价于"$w$ 与每个环向量正交"。连接路径就这么直：离散的保守场 = 边权是一个顶点标量的差分。**区别**在于连续版本（$\mathbb{R}^3$ 的向量场）判断保守只需要局部条件（旋度为零，且区域单连通），离散版本没有"局部"，只有"每个 cycle 权为零"这条全局条件，所以真正省时间的做法不是找更快的检测器，而是先把图按强连通分量拆小。
>
> 第二个连接放在 6.042J 的等价关系：在同一强连通分量内定义 $u \sim v$ 为"到 $v$ 的所有路径权和相同"，保守恰好使它在分量内成立；区别是那边只需证明自反、对称、传递，这里要用它反推势函数的数值。
>
> 一句话收束：遇到"沿闭环求和为零 / 与路径无关"的题，先找势函数（$n$ 个未知数），实在要检测环再退回 Bellman-Ford（两趟）；判据是"可解性 = 与所有环正交"，这就是离散版的路径无关。

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
>
> 先把"为什么非展开不可"讲清。判断一条路能不能继续走，依赖她此刻剩多少油；而剩多少油又依赖她之前走过哪些上坡——也就是说，**剩余油量不是路径权重和的函数**，你无法从最短路距离 $d(v)$ 里把它恢复出来。凡是"未来的可行性依赖一个不能从累计代价反推的副产品"的题，唯一干净的出路就是把那个副产品娶进 vertex。反过来也可以反过来验：如果把规则改成"上坡耗时正比于爬升高度、下坡耗时固定"，那么耗油与已花时间一一对应、可以从 $d(v)$ 恢复，就不必分层，直接跑 Dijkstra 即可。这题之所以必须分层，全在"耗油与时间不同步"这一点上。
>
> 边的三条规则各自对应一句物理事实，值得逐条核对。下坡边 $(v_i, u_i)$ 对所有 $i$ 都成立：不耗油，油量一格不动。上坡边只在 $i \ge \ell + 1$ 时存在：走完剩 $i - \ell$，而题设要求**始终 strictly positive（严格为正）**，所以剩 0 也不许，最低那一档只能是 $i = \ell + 1$。这个 $+1$ 就是"严格为正"与"非负"的全部差别，也是这一题评分里最容易丢分的地方——写成 $i \ge \ell$ 会把"油刚好吃光"的路线也算合法。加油站边 $(v_i, v_{i+1})$ 权重 $t_G$：把"买 1 单位油"建模成一条边，于是"要不要加、加几单位"这些决策全部自动交给最短路去选，你不需要写任何分支。
>
> 规模和例子都能手算。取 $n = 10$ 个路口、$g = 3$，平均度 $< 5$ 给出 $2r < 5n = 50$，即 $r \le 24$。分层图的 vertices $= gn = 30$；下坡边 $= gr \le 72$；上坡边至多 $gr \le 72$；加油站边至多 $(g - 1)n = 20$，合计 $E \le 164$。用 binary heap（二叉堆）的 Dijkstra：$O(E \log V) \approx 164 \times \log_2 30 \approx 164 \times 5 \approx 820$ 次基本操作，毫秒级都不到。再算一个具体路线：设 $t_G = 2$，从 $s$（海拔 0，有加油站）到 $t$，中间只有一个 $x$（海拔 3），$s \to x$ 耗时 5、$x \to t$ 下坡耗时 1。若 $g = 3$，出发满油 3 单位，$s \to x$ 恰好耗 $3 - 0 = 3$ 单位，到达时剩 0，违反严格为正，这条路不合法；而 $s$ 处已经满油、加不进去，所以 $g = 3$ 时无解。若 $g = 4$，到 $x$ 剩 1 单位，合法，总时间 $5 + 1 = 6$。一个数就说明容量是硬约束，不是可以"多花点时间"绕过去的软约束。
>
> 跨课程连接第一处放在 CSAPP 第 6 章：cache（高速缓存）的地址也是被切成 (tag, set, offset) 三段，本质是"把原本藏在一维地址里的维度拆出来当索引"，这样二维表就能查；这里把"油量"从隐含状态里拆出来当第二维，是同一手。**区别**在于层数是固定的常数（通常三级），而这里的层数 $g$ 由输入决定，可以到 $n - 1$，所以规模是乘上去的而不是加上去的。
>
> 第二处放在 18.065 与 Strang 的直积直觉：分层图的 vertex 集合是 $V \times \{1, \dots, g\}$，规模 $|V| \cdot g$；算法代价随之按 $O(gn \log(gn))$ 增长。线性代数里取两个空间的积几乎是免费的（只是把坐标拼在一起），算法里每多一维就要多付一整倍时间——这就是"维度增加是乘法而不是加法"在复杂度上的具体样子。
>
> 第三处回到 6.042J 的离散性：上坡耗油是 $e_j - e_i$，而海拔被规定为正整数，所以剩余油量只取整数值、状态空间有限；如果海拔是实数，状态就不可数、这招当场失效。这类题动笔前先确认"资源是整数且上界已知"，否则分层图根本建不出来。
>
> 一句话收束：判据是两句——副产品不能从 $d(v)$ 反推就必须进 vertex；资源上界是 $g$、于是复杂度乘 $g$。这题能到 $O(n^2 \log n)$，全靠 $g < n$ 这条题设给的分母。

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
>
> 把"保持最短路不变"这句话算出来，只要一行求和：对任意 path $P$ 从 $u$ 到 $v$，$w'(P) = w(P) + h[u] - h[v]$，因为中间顶点的 $h$ 一正一负逐项抵消。也就是说所有 $u \to v$ 的候选路径被整体平移了同一个常数，谁最小还是谁最小，argmin 不变。这一条只用到代数，与权重正负无关，所以"稀疏图上先重加权再跑 Dijkstra"的思路是干净的。第二条性质（新权重非负）来自 Bellman-Ford 给出的不等式：$h[v] \le h[u] + w(u, v)$，移项就是 $w(u, v) + h[u] - h[v] \ge 0$。这两条缺一不可：少了第一条，重加权后算出来的距离不是原图的距离；少了第二条，Dijkstra 本身就不成立。
>
> 这题是编程题，所以注要停在实现的边界上，四个地方值得盯。第一，`INF = 99999` 是题目给出的上界承诺，`if d[v] < INF` 用它判不可达；自己造用例时若真的跑出更长的距离，会把可达误判成不可达。第二，`W[(u, v)] = w` 用字典存边权，**平行边会被静默覆盖**——同一对端点若有多条权重不同的 edge，后写的把先写的吃掉，答案就错；这是整套模板里最隐蔽的坑。第三，supernode 的下标是 $n$，它只出现在 `Adj` 的末尾、只有零权出边，因此从它跑 Bellman-Ford 等价于"所有顶点初值都持 0 这组虚拟初值"，保证 $h$ 处处有限（否则不可达顶点的 $h$ 是 $\infty$，重加权时会出现 $\infty - \infty$）。第四，Dijkstra 只对 $u < n$ 跑，supernode 不做源；若误把它当源，`D` 的维度就对不上。
>
> 手算一个三点图核对三个阶段的数值。图：$(0,1,-2)$、$(1,2,1)$、$(0,2,3)$。加 supernode 后 $h = (0, -2, -1)$（到 2 的最短路是 $0 \to 1 \to 2$，$-2 + 1 = -1$，比直达 3 短）。重加权：$w'(0,1) = -2 + 0 - (-2) = 0$，$w'(1,2) = 1 + (-2) - (-1) = 0$，$w'(0,2) = 3 + 0 - (-1) = 4$，三条全部非负，负权确实被抹掉了。从 0 跑 Dijkstra 得 $d' = (0, 0, 0)$，还原 $D[0][1] = 0 - 0 + (-2) = -2$、$D[0][2] = 0 - 0 + (-1) = -1$，与真值 $\min(3, -2 + 1) = -1$ 吻合。
>
> 复杂度也算一遍：$n$ 次 Dijkstra，用 binary heap（二叉堆）每次 $O(E \log V)$，合计 $O(VE \log V)$。取 $n = 100$、$E = 1000$：$100 \times 1000 \times \log_2 100 \approx 7 \times 10^5$；同样规模 Floyd-Warshall 是 $n^3 = 10^6$，两者同量级。把 $E$ 降到 100，Johnson 掉到 $7 \times 10^4$，快一个数量级——"稀疏"两个字值多少钱，就看这个比值。
>
> 跨课程连接第一处放在 18.065 与 Strang 的矩阵语言：重加权可以整体写成 $W' = W + h\mathbf{1}^{\top} - \mathbf{1}h^{\top}$，即给权重矩阵加一个反对称的 rank-2 项。路径和只保留端点值，正是这个低秩结构造成的 telescoping（望远镜相消）。**区别**在于：线性代数里低秩扰动一般不改变矩阵的"可用性"，而这里我们恰恰是靠它把"存在负元"变成"全部非负"——扰动是为可行性服务的。
>
> 第二处放在 6.006 后面的 A* search（A* 搜索）：A* 用的约化代价 $w(u,v) + h[u] - h[v]$ 与这里的 `wf` 一模一样，而 A* 要求 `h` 是 consistent heuristic（一致启发式），条件也正是这条 triangle inequality（三角不等式）。所以 Johnson 的重加权与 A* 是同一套势函数的两种包装：前者为了让权重非负好让 Dijkstra 跑，后者为了剪掉不必展开的顶点。
>
> 一点历史坐标：Johnson 的这篇工作发表在 1977 年的 Journal of the ACM 第 24 卷第 1 期，要解决的具体问题是"稀疏图上全源最短路"——Floyd-Warshall 的 $n^3$ 对稀疏图太浪费，而负权又让 Dijkstra 不能直接上。他的办法就是"一次 Bellman-Ford 修好权重，再调用 $n$ 次便宜的子程序"，这个"先修正、再复用"的结构后来在最小费用流里反复出现。
>
> 一句话收束：这题的评分点不在把 20 行抄对，而在能说清"$h$ 必须同时满足望远镜相消与非负性"，以及那个 `INF` 与平行边两个实现陷阱。

---

> <span style="color:#7f8c8d;">MIT OpenCourseWare · 6.006 Introduction to Algorithms, Spring 2020 · https://ocw.mit.edu</span>
