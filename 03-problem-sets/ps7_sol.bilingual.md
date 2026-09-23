# Introduction to Algorithms: 6.006（算法导论）

Massachusetts Institute of Technology（麻省理工学院）
Instructors（授课教师）: Erik Demaine（埃里克·德梅因）, Jason Ku（顾杰森）, and Justin Solomon（贾斯汀·所罗门）

## <span style="color:#2471a3;">**[session]**</span> <span style="color:#c0392b">Problem Set 7（习题集 7）</span>

> <span style="color:#7f8c8d;">MIT 6.006 Spring 2020, Problem Set 7 Solutions（习题集 7 解答）· 主题：Dynamic Programming（动态规划）· 对应 Lecture 15-18 与 CLRS §15（动态规划）</span>

---

请在提供的 LaTeX 和 Python templates（模板）中写出你的解答。追求 concise（简洁）的解答；convoluted and obtuse（复杂晦涩）的描述即使正确也可能得低分。

请用 dynamic programming（动态规划）解决以下每个问题。对每个问题，务必：定义一组 subproblems（子问题）、递归地建立子问题间的 Relate（关系）、论证该关系是 acyclic（无环）的、给出 base cases（基本情况）、由子问题构造原问题的解、并分析运行时间。正确但低效的动态规划将获得大量部分分。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 上面的"务必"清单就是 6.006 动态规划的 **SRTBOT** 六步模板：**S**ubproblems（子问题）、**R**elate（递归关系）、**T**opological order（拓扑序）、**B**ase cases（基本情况）、**O**riginal problem（原问题）、**T**ime（时间）。🎥 *Demaine 在 Lecture 15 开头这样介绍它*："It's just an acronym for subproblems, relations, topological order, base case, original problem, and time."（翻译：它只是 subproblems、relations、topological order、base case、original problem、time 的首字母缩写。）——本习题集 7-1 到 7-5 的官方解答全部按这六步组织（每题的 Solution 里依次标着 1. Subproblems → 6. Time），你照着这个骨架写 DP 就不会漏步骤。这六步同时也是你在 6.042J 学的 mathematical induction（数学归纳法）的算法化：子问题 = 归纳命题，Relate = 归纳步骤，Base = 归纳奠基，而 Topo 保证归纳步骤真正可执行（子问题之间无环，从"小"到"大"逐层推进）。其中 T（Topo）是 DP 区别于普通递归的关键：普通递归天然在调用图上可能成环，DP 要求子问题依赖图是一个 DAG——这正是"为什么每个 DP 都要论证 acyclic"的原因。

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 7-1. Effective Campaigning（有效竞选）</span>

众议员 Zena Torr（泽娜·托尔）正与参议员 Kong Grossman（孔·格罗斯曼）在一场激烈的总统初选中对决：连续 $n$ 天，每天一场一对一的州级竞赛，共 $n$ 场。每场州级竞赛 $i \in \{1, \ldots, n\}$ 有已知的正整数 delegate count（代表数）$d_i$，以及一个预测的 delegate count $z_i < d_i$——如果 Rep. Torr 不再采取任何行动，她将赢得这么多。总共有 $D = \sum_i d_i$ 个 delegates，Rep. Torr 需要至少 $\lfloor D/2 \rfloor + 1$ 个 delegates 才能获胜。不幸的是，由于 $\sum_i z_i < \lfloor D/2 \rfloor + 1$，预测显示 Rep. Torr 会输掉竞选，所以她需要采取行动。Rep. Torr 有一个有限但高效的竞选团队，每天最多只能在一个州竞选。如果团队在第 $i$ 天竞选，他们将赢得州 $i$ 的全部 $d_i$ 个 delegates，但第 $i$ 天之后的两天将完全无法竞选，因为需要时间转移阵地。描述一个 $O(n)$ 时间的 algorithm，判断 Rep. Torr 是否可能通过有效竞选赢得初选。

> **[solution] Solution（解答）:**
>
> **1. Subproblems（子问题）**
> - $x(i)$: 在第 $i$ 天可以竞选的前提下，Torr 在州 $i$ 到 $n$ 中能赢得的 delegate 最大数
> - 对 $i \in \{1, \ldots, n+1\}$
>
> **2. Relate（关系）**
> - 在第 $i$ 天要么竞选要么不竞选。猜一个！
> - 若竞选，获得 $d_i$ 个 delegates，但接下来两天不能竞选
> - 否则无限制，但只能获得 $z_i$ 个 delegates
> - $x(i) = \max\{d_i + z_{i+1} + z_{i+2} + x(i + 3),\; z_i + x(i + 1)\}$
>
> **3. Topo（拓扑序）**
> - $x(i)$ 只依赖下标严格更大的子问题，所以无环
>
> **4. Base（基本情况）**
> - $x(n + 1) = 0$（没有更多州可赢）
> - $x(n) = d_n$（最后一天竞选，因为 $d_n > z_n$）
> - $x(n - 1) = \max\{d_{n-1} + z_n,\; z_{n-1} + d_n\}$（在最后两天中任选一天竞选）
>
> **5. Original（原问题）**
> - 用递归 top-down（自顶向下）或迭代 bottom-up（自底向上）求解子问题
> - 返回 $x(1) \ge \lfloor D/2 \rfloor + 1$ 是否成立（她能获得的最大 delegate 数是否至少等于她获胜所需的数量）
>
> **6. Time（时间）**
> - 子问题数: $n + 1$
> - 每个子问题的工作量: $O(1)$
> - $O(n)$ 运行时间

> **Rubric（评分标准）:**（与 PS7 所有理论题相同）
> - S: 正确的子问题描述 3 分
> - R: 正确的递归关系 3 分
> - T: 指出关系无环 1 分
> - B: 用子问题表示的正确的 base cases 1 分
> - O: 用子问题表示的正确原问题解 1 分
> - T: 正确的运行时间分析 2 分
> - 若正确的动态规划是高效的（满足要求的上界）: 4 分
> - 可酌情给部分分

---

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这题有两个值得留意的建模细节。**第一**，为什么"第 $i$ 天竞选"的收益是 $d_i + z_{i+1} + z_{i+2}$ 而不是 $d_i$？因为竞选日之后的两个"休息日"虽然不能竞选，但休息日当天如果不再行动仍能拿到预测值 $z$——收益是"竞选日的全量 $d$ + 两个休息日的被动 $z$"。**第二**，base case 的边界：$x(n) = d_n$ 不是直接套用递推（若套用，$x(n+1)=0$ 且 $z_{n+1}$ 无定义），而是单独处理的角情况；同理 $x(n-1)$ 的表达式排除了"第 $n-1$ 天竞选后第 $n$ 天也能拿 $d_n$"的非法选项（因为第 $n-1$ 天竞选会封死第 $n$ 天）。这类"递推式在边界处失效、需要手写 base cases"的情况在 DP 里非常常见，是你在 6.006 刷题时最容易失分的地方之一。时间 $O(n)$ 的来源：子问题数 $n+1$ 且每个子问题只做常数次比较。

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 7-2. Caged Cats（笼中虎）</span>

Ting Kiger（廷·凯格）是一个古怪的人物，他拥有 $n$ 只宠物老虎和 $n^2$ 个笼子。

- 每只老虎 $i$ 有已知的正整数 age（年龄）$a_i$ 和 size（体型）$s_i$（没有两只老虎有相同的 age 或 size）。
- 每个笼子 $j$ 有已知的正整数 capacity（容量）$c_j$ 和离 Ting 卧室的 distance（距离）$d_j$（没有两个笼子有相同的 capacity 或 distance）。

Ting 需要给每只老虎分配一个专属笼子。

- Ting 偏爱年长的老虎，希望它们睡在离他卧室更近的地方，即：任意两只老虎 $x$ 和 $y$，若 $a_x < a_y$，则必须分配到笼子 $X$ 和 $Y$，使得 $d_Y < d_X$。
- 分配给笼子 $c_j$ 的老虎 $i$，如果 $s_i > c_j$，会经历正的不适感 $s_i - c_j$；如果 $s_i \le c_j$，则不会经历任何不适。

描述一个 $O(n^3)$ 时间的 algorithm，在偏爱年长老虎的前提下，把老虎分配到笼子，使老虎的总不适感最小。

> **[solution] Solution（解答）:** "偏爱年长老虎"这一条件保证：按年龄递减排序的老虎序列 $T$，会被匹配到按离 Ting 卧室距离递增排序的笼子序列 $C$ 的一个 subsequence（子序列）上。所以先在 $O(n \log n)$ 时间内把老虎按年龄递减排序成序列 $T$，再在 $O(n^2 \log n)$ 时间内把笼子按距离递增排序成序列 $C$（例如用 merge sort（归并排序））。现在用 dynamic programming 找出从 $T$ 到 $C$ 的某个 subsequence 的最优匹配。
>
> **1. Subproblems（子问题）**
> - $x(i, j)$: 把老虎 $T[i:]$ 匹配到 $C[j:]$ 的某个 subsequence 上的最小总不适感
> - 对 $i \in \{0, \ldots, n\}$ 和 $j \in \{0, \ldots, n^2\}$
>
> **2. Relate（关系）**
> - 可以把老虎 $T[i]$ 与笼子 $C[j]$ 匹配，也可以不匹配。猜一个！
> - 若匹配，则承担该匹配的不适感（如果有）。
> - 无论哪种情况，$C[j]$ 都不会与 $T[i+1:]$ 中的任何老虎匹配，所以对剩余部分递归
> - 令 $d(i, j)$ 为把老虎 $T[i]$ 与笼子 $C[j]$ 匹配的不适感
> - 即 $d(i, j) = s_i - c_j$（若 $s_i > c_j$），否则为 $0$
> - $x(i, j) = \min\{d(i, j) + x(i + 1, j + 1),\; x(i, j + 1)\}$
>
> **3. Topo（拓扑序）**
> - $x(i, j)$ 只依赖下标严格更大的 $j$，所以无环
>
> **4. Base（基本情况）**
> - $x(n, j) = 0$（所有老虎都已匹配，所以没有不适）
> - 对 $i > 0$，$x(i, n^2) = \infty$（没有更多笼子，且不允许有无家可归的老虎）
>
> **5. Original（原问题）**
> - 用递归 top-down 或迭代 bottom-up 求解子问题
> - $x(0, 0)$ 是把所有老虎匹配到笼子的最小总不适感
> - 存储 parent pointers（父指针）以重构最优分配
>
> **6. Time（时间）**
> - 子问题数: $(n + 1)(n^2 + 1) = O(n^3)$
> - 每个子问题的工作量: $O(1)$
> - $O(n^3)$ 运行时间

> **Rubric（评分标准）:**（与 PS7 所有理论题相同，见 Problem 7-1）

---

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这道题的关键洞察是"**偏爱约束把二维匹配压成一维序列匹配**"：年长者必须睡得更近，等价于"按年龄降序的老虎序列"和"按距离升序的笼子序列"之间保持顺序的一对一匹配（monotone matching（单调匹配））。这正是你在 6.006 Lecture 16 学过的 **LCS（Longest Common Subsequence，最长公共子序列）** 思想的变形——LCS 中 $x(i,j)$ 的递推是"匹配或不匹配"，这里同样如此，只是"匹配收益"换成了"匹配代价 $d(i,j)$"，目标从最大化改为最小化。笼子数量是 $n^2$ 而非 $n$，这是刻意的陷阱：如果笼子只有 $n$ 个，这就是标准 assignment 问题；但 $n^2$ 个笼子让子问题维度变成 $(n+1)(n^2+1)$，从而得到 $O(n^3)$ 上界。为什么 $x(i, n^2) = \infty$ 只对 $i > 0$ 成立？因为 $i = 0$ 时没有老虎需要匹配，$x(0, n^2) = 0$（一个笼子都不用）——这是"空匹配合法"的角情况。

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 7-3. Odd Paths（奇权路径）</span>

给定一个带整数权重的 weighted directed acyclic graph（带权有向无环图）$G = (V, E, w)$ 和两个 vertices $s, t \in V$，描述一个 linear-time（线性时间）algorithm，求出从 $s$ 到 $t$ 的具有 odd weight（奇权重）的 paths 的数量。解题时，你可以假设单个 machine word（机器字）足够大，能容纳算法中计算出的任何整数。

> **[solution] Solution（解答）:** 从 $s$ 到 $t$ 的奇权重路径数，取决于 $t$ 的每个 incoming neighbor（入邻居）的路径数：若入边为偶数权重，则需要奇权重路径数；若入边为奇数权重，则需要偶权重路径数。所以我们对每个 vertex 建立两类子问题，分别表示到达该 vertex 的偶权重与奇权重路径数。
>
> **1. Subproblems（子问题）**
> - $x(v, i)$: 从 $s$ 到 $v$ 的路径数，其中 $i = 0$ 表示偶权重、$i = 1$ 表示奇权重
> - 对所有 $v \in V$ 和 $i \in \{0, 1\}$
>
> **2. Relate（关系）**
> - 在 DAG 中，到达 $v$ 的偶或奇权重路径数是到达其入邻居的相关路径数之和
> - 令 $p(i)$ 为整数 $i$ 的 parity（奇偶性），即 $i$ 为偶数时 $p(i) = 0$，$i$ 为奇数时 $p(i) = 1$
> - $x(v, i) = \sum \{x(u, p(w(u, v) + i)) \mid u \in \text{Adj}^-(v)\}$
>
> **3. Topo（拓扑序）**
> - $x(v, i)$ 只依赖 $G$ 的 topological order（拓扑序）中更靠前的 vertex $u$ 的子问题 $x(u, j)$，所以无环
>
> **4. Base（基本情况）**
> - $x(s, 0) = 1$（因为零条边是偶数权重）
> - $x(s, 1) = 0$（从 $s$ 到 $s$ 没有奇权重路径）
> - 对任何其他满足 $\text{Adj}^-(v) = \varnothing$ 的 $v$，$x(v, 0) = x(v, 1) = 0$
>
> **5. Original（原问题）**
> - $x(t, 1)$，即从 $s$ 到 vertex $t$ 的奇权重路径数
>
> **6. Time（时间）**
> - 子问题数: $2|V|$
> - 每个子问题的工作量: $O(\deg^-(v))$
> - $O\left(2 \sum_{v \in V} \deg^-(v)\right) = O(|V| + |E|)$ 运行时间（关于图的大小是线性的）

> **Rubric（评分标准）:**（与 PS7 所有理论题相同，见 Problem 7-1）

---

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这题是一个"**用额外维度消除非局部依赖**"的教科书示例。如果只问"路径数"，一维子问题 $x(v)$ 就够；但"奇偶"这个属性让递推需要知道前驱路径的奇偶性，于是把状态空间加倍成 $x(v, 0/1)$。这个"属性状态化"技巧与你在 CSAPP 里见过的 finite state machine（有限状态机）是同一思想：奇偶就是一个二元状态，走一条权重为 $w$ 的边相当于状态翻转 $p(w)$ 次。递推式 $x(v, i) = \sum_u x(u, p(w(u,v) + i))$ 的含义是：一条到达 $u$ 的路径，若其权重奇偶性加上边权 $w(u,v)$ 等于 $i$，那么它延长到 $v$ 后权重奇偶性就是 $i$。注意这题**不能**用"总路径数减去偶路径数"偷懒——那仍然需要算偶路径数，等价于 $x(v, 0)$。运行时间 $O(|V|+|E|)$ 来自"每条边在两个状态上各被用一次"，即 $\sum_v 2\deg^-(v) = 2|E|$。

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 7-4. Pizza Partitioning（披萨分割）</span>

Liza Pover（莉莎·波弗）和她的小弟弟 Lie Pover（莱·波弗）想分享一个圆形披萨，披萨沿从圆心出发、角度为 $\alpha_i = i\pi/n$（$i \in \{0, 1, \ldots, 2n\}$，其中 $\alpha_0 = \alpha_{2n}$）的射线被切成了 $2n$ 个相等的扇形 slice（切片）。角度 $\alpha_i$ 与 $\alpha_{i+1}$ 之间的每个切片 $i$ 有已知的整数 tastiness（美味值）$t_i$（可能为负）。为了对弟弟"公平"，Liza 决定按以下方式吃切片：

- 他们轮流选择要吃的披萨切片：Liza 先当 chooser（选择者）。
- 如果只剩一个切片，选择者吃掉它，吃披萨停止。
- 否则选择者执行以下操作：
  - 如果穿过披萨圆心、角度为 $\alpha_i$ 的直线两侧各至少有一片未吃掉的切片，则角度 $\alpha_i$ 是 proper（恰当的）。
  - 选择者任选一个 $\alpha_i$ 为 proper 的数 $i \in \{1, \ldots, 2n\}$，并吃掉从角度 $\alpha_i$ 到角度 $\alpha_i + \pi$ 之间沿逆时针方向的所有未吃切片。
  - 选择者吃完后，另一个孩子成为选择者，继续吃。

Liza 想要最大化她将吃到的切片的总美味值。描述一个 $O(n^3)$ 时间的 algorithm，找出 Liza 通过这一选择过程能保证的最大总美味值。

> **[solution] Solution（解答）:** 随着兄妹俩吃披萨，未吃的切片始终是 cyclically consecutive（循环连续的）（因为移除半平面是 convex operation（凸操作））。所以我们选择连续循环子数组作为子问题。由于每个孩子都想最大化自己的美味值，我们根据当前谁是选择者建立不同的子问题。
>
> 在做选择时，知道任意子数组的美味值会很有用。令 $v(i, j)$ 为从角度 $\alpha_i$ 起逆时针的 $j$ 个切片的美味值，即 $v(i, j) = \sum_{k=0}^{j-1} t_{(i+k) \bmod 2n}$，其中下标按模 $2n$ 取，对 $i \in \{0, \ldots, 2n-1\}$ 和 $j \in \{0, \ldots, n\}$。这样的 $v(i, j)$ 有 $O(n^2)$ 个，每个可用 $O(n)$ 时间朴素地计算，总计 $O(n^3)$ 时间。注意它们也可以用 dynamic programming 在 $O(n^2)$ 时间内算好，但朴素方法已满足题目要求的时间上界。
>
> **1. Subproblems（子问题）**
> - $x(i, j, p)$: 当剩余从 $\alpha_i$ 起逆时针的 $j$ 个切片时 Liza 能获得的最大美味值，其中 $p = 1$ 表示 Liza 是选择者、$p = 2$ 表示 Lie 是选择者
> - 对 $i \in \{0, \ldots, 2n-1\}$、$j \in \{0, \ldots, n\}$、$p \in \{1, 2\}$
> - （第一次选择后最多只剩 $n$ 个切片，所以我们不对 $j > n$ 计算）
>
> **2. Relate（关系）**
> - Liza 试图最大化，而 Lie 可能试图最小化（所以最坏情况下他会这么做）
> - 选择者可以选任意 proper angle，然后选一侧。猜一个！
> - 对任意 $k \in \{1, \ldots, j-1\}$，角度 $\alpha_{i+k}$ 是 proper 的
> - 选择者吃掉 $\alpha_i$ 与 $\alpha_{i+k}$ 之间的 $k$ 个切片，或 $\alpha_{i+k}$ 与 $\alpha_{i+j}$ 之间的 $j-k$ 个切片
> - Lie 吃时 Liza 不获得也不失去美味值
>
> ```math
> x(i, j, 1) = \max_{k \in \{1, \ldots, j-1\}} \max\{ v(i, k) + x(i + k, j - k, 2),\; v(i + k, j - k) + x(i, k, 2) \}
> ```
>
> ```math
> x(i, j, 2) = \min_{k \in \{1, \ldots, j-1\}} \min\{ x(i + k, j - k, 1),\; x(i, k, 1) \}
> ```
>
> **3. Topo（拓扑序）**
> - $x(i, j, p)$ 只依赖 $j$ 严格更小的子问题，所以无环
>
> **4. Base（基本情况）**
> - $x(i, 1, 1) = t_i$（Liza 吃掉最后一片）
> - $x(i, 1, 2) = 0$（Lie 吃掉最后一片）
> - 对所有 $i \in \{1, \ldots, 2n\}$
>
> **5. Original（原问题）**
> - Liza 首先选择吃哪一半
> - 最大值 = 某一半的美味值 + 让 Lie 在另一半上选择时她能获得的美味值
> - $\max\{x(i, n, 2) + v(((i + n) \bmod 2n), n) \mid i \in \{0, \ldots, 2n-1\}\}$
>
> **6. Time（时间）**
> - 计算所有 $v(i, j)$ 的工作量: $O(n^3)$
> - 子问题数: $2(2n)(n + 1) = O(n^2)$
> - 每个子问题的工作量: $O(n)$
> - 计算原问题的工作量: $O(n)$
> - $O(n^3)$ 运行时间

> **Rubric（评分标准）:**（与 PS7 所有理论题相同，见 Problem 7-1）

---

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这题的本质是一个 **zero-sum game（零和博弈）的 minimax DP**：Liza 最大化、Lie 最小化，所以 $p=1$ 的递推取 $\max$，$p=2$ 的递推取 $\min$。你在大一离散数学 6.042J 学的 game tree（博弈树）概念在这里有了算法形态——每个子问题就是博弈树上的一个节点，minimax 值由子节点递归决定。两个关键观察：**(1)** 未吃切片永远是循环连续的，所以"剩余披萨"完全由"起点角度 $i$ + 切片数 $j$"刻画，状态数 $O(n^2)$；**(2)** 第一次选择后剩余切片数 $\le n$，因此 $j$ 的上界取 $n$ 而不是 $2n$（否则子问题数翻倍，仍是 $O(n^3)$ 但常数更大）。为什么 base case 是 $x(i, 1, 2) = 0$？因为只剩一片时 Lie 吃掉它，Liza 的收益是 $0$——minimax 中每个玩家只关心自己的 payoff。一个容易踩的坑：$v(i + k, j - k)$ 在 $\max$ 的第二项中下标是 $i+k$（吃后半段），别写成 $v(i, \cdot)$。

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 7-5. Shorting Stocks（做空股票）</span>

Bordan Jelfort（博尔丹·杰尔福特）是一家金融交易公司的做空者。他收集了 $s$ 家不同公司 $C = (c_0, \ldots, c_{s-1})$ 在连续 $n$ 天内的股票价格信息。公司 $c_i$ 的股票价格信息是一个按时间顺序排列的序列 $P_i = (p_0, \ldots, p_{nk-1})$，共 $nk$ 个价格，其中每个价格都是正整数，且价格 $\{p_{kj}, \ldots, p_{kj+k-1}\}$ 都出现在第 $j$ 天（$j \in \{0, \ldots, n-1\}$）。一家公司的 shorting value（做空值）是该公司严格递减价格的最长时间顺序子序列的长度，且该子序列不跳过天数：如果序列包含第 $i$ 天和第 $j$ 天（$i < j$）的两个价格，那么该序列必须也包含 $\{i, \ldots, j\}$ 中每一天的至少一个价格。

**(a) [15 points]** 描述一个 $O(snk^2)$ 时间的 algorithm，确定哪家公司 $c_i$ 具有最高的 shorting value，并返回来自 $P_i$ 的一条不跳过天数的最长递减价格子序列 $S$。

> **[solution] Solution（解答）:** 我们将用 dynamic programming 计算每家公司的 shorting value（假设 $P = P_i$），然后在 $O(s)$ 时间内返回最长的那家。
>
> **1. Subproblems（子问题）**
> - $x(j)$: $P[j:]$ 中不跳过天数、且包含价格 $P[j]$ 的最长递减子序列长度
> - 对 $j \in \{0, \ldots, nk - 1\}$
>
> **2. Relate（关系）**
> - 序列中的下一个价格在更晚的时刻，要么在同一天，要么在下一天。猜一个！
> - 在价格下标 $j$ 处，同一天还剩 $(k - 1) - (j \bmod k)$ 个价格
> - 然后下一天还有 $k$ 个价格（如果存在的话）
> - 所以下一个价格的最后一个可能下标是 $f(j) = \min\{j + (k - 1) - (j \bmod k) + k,\; nk - 1\}$
> - $x(j) = 1 + \max\{\{x(d) \mid d \in \{j + 1, \ldots, f(j)\} \text{ 且 } P[j] > P[d]\} \cup \{0\}\}$
>
> **3. Topo（拓扑序）**
> - $x(j)$ 只依赖下标严格更大的子问题，所以无环
>
> **4. Base（基本情况）**
> - 递推关系在取最小值集合只含 $0$ 时已经包含 base case
> - 也可以说: $x(nk - 1) = 1$（只剩一个元素）
>
> **5. Original（原问题）**
> - 用递归 top-down 或迭代 bottom-up 求解子问题
> - shorting value 是 $\max_{j=0}^{nk-1} x(j)$
> - 存储 parent pointers（父指针）以重构 $S$
>
> **6. Time（时间）**
> - 子问题数: $nk$
> - 每个子问题的工作量: $O(k)$
> - 计算原问题的工作量: $O(nk)$
> - $O(nk^2)$ 运行时间

**(b) [25 points]** 使用提供的模板代码，编写一个 Python 函数 `short_company(C, P, n, k)`，实现你在 (a) 部分的算法。你可以从网站下载代码模板和一些 test cases。

> **[solution] Solution（解答）:**（Python 代码，保持原文）

```python
# iterative bottom-up
def short_company(C, P, n, k):
    S = []
    for i in range(len(C)):
        p = P[i]
        x = [1 for _ in range(n*k)]      # subproblem memo
        r = [None for _ in range(n*k)]   # parent pointer memo
        best = 0
        for j in range(n*k - 1, -1, -1):
            # compute memos
            f = min(j + (k - 1) - (j % k) + k, n*k - 1)
            for d in range(j + 1, f + 1):
                if (p[j] > p[d]) and (1 + x[d] > x[j]):
                    x[j] = 1 + x[d]
                    r[j] = d
                    if x[best] < x[j]:
                        best = j
        if x[best] > len(S):
            # reconstruct from parent pointers
            c, S = C[i], []
            while best != None:
                S.append(p[best])
                best = r[best]
        S = tuple(S)
    return (c, S)
```

```python
# recursive top-down
def short_company(C, P, n, k):
    S = []
    for i in range(len(C)):
        p = P[i]
        memo = [None for _ in range(n*k)]  # memo for subproblems and parents
        def dp(j):
            # recursive function
            if memo[j] is None:
                f = min(j + (k - 1) - (j % k) + k, n*k - 1)
                x, r = 1, None
                for d in range(j + 1, f + 1):
                    x_, _ = dp(d)
                    if (p[j] > p[d]) and (1 + x_ > x):
                        x, r = 1 + x_, d
                memo[j] = (x, r)
            return memo[j]
        best, opt = 0, 0
        for j in range(n*k):
            # compute subproblems
            x, _ = dp(j)
            if x > opt:
                best, opt = j, x
        if opt > len(S):
            # reconstruct from parent pointers
            c, S = C[i], []
            while best != None:
                S.append(p[best])
                _, best = dp(best)
        S = tuple(S)
    return (c, S)
```

> **Rubric（评分标准）:**（与 PS7 所有理论题相同，见 Problem 7-1；编程题按测试用例评分）

---

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> (a) 部分的递推有一个隐蔽但关键的点：$f(j) = \min\{j + (k - 1) - (j \bmod k) + k,\; nk - 1\}$ 是"从 $j$ 出发能跳到的最远下标"——$(k-1) - (j \bmod k)$ 是当天剩余价格数，$+k$ 是下一天的 $k$ 个价格。这保证了"不跳过天数"约束：从第 $i$ 天跳到第 $j$ 天时，中间每一天都必须贡献至少一个价格，因此只能在"当天剩余 + 次日全部"的窗口内选后继。这与 Lecture 16 的 **LIS（Longest Increasing Subsequence，最长递增子序列）** 的 $O(n^2)$ 版本同构，只是候选后继被窗口限制在 $O(k)$ 个，所以每步 $O(k)$、总时间 $O(nk^2)$。代码部分的两版实现互为镜像：iterative bottom-up 从后往前填表并记录 parent pointer $r[j]$；recursive top-down 用 memoization 的 `dp(j)` 返回 `(长度, 父指针)` 二元组。🎥 *Demaine 在 Lecture 16 里这样解释 parent pointers 的作用*："parent pointers so we can recover solutions, like in shortest paths."（翻译：父指针让我们能够恢复解，就像最短路径里那样。）——重构最优解时，从 $best$ 出发沿着 $r$ 一路跳到 `None` 即可得到完整子序列。注意 bottom-up 版里 `x[best]` 初值为 `x[0]` 的比较在 `best=0` 时自我比较，无害；若所有公司的最大值都是 1（全序列无递减对），函数仍会返回第一家公司的单元素序列——与题意一致。

---

> <span style="color:#7f8c8d;">MIT OpenCourseWare · 6.006 Introduction to Algorithms, Spring 2020 · https://ocw.mit.edu</span>
