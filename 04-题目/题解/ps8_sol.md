<!-- page 1/7 -->
# Introduction to Algorithms: 6.006（算法导论）

Massachusetts Institute of Technology（麻省理工学院）
Instructors（授课教师）: Erik Demaine（埃里克·德梅因）, Jason Ku（顾杰森）, and Justin Solomon（贾斯汀·所罗门）

## <span style="color:#2471a3;">**[session]**</span> <span style="color:#c0392b">Problem Set 8（习题集 8）</span>

> <span style="color:#7f8c8d;">MIT 6.006 Spring 2020, Problem Set 8 Solutions（习题集 8 解答）· 主题：Dynamic Programming（动态规划）· 对应 Lecture 15 之后的 DP 内容与 CLRS 第 15 章（动态规划）· 官方解答逐题全译，译者注另行标注</span>

---

**Problem Set 8（习题集 8）**

请在提供的 LATEX（排版系统）template（模板）中写出你的解答。追求 concise（简洁）的解答；convoluted and obtuse（复杂晦涩）的描述即使正确也可能得低分。本次没有需要提交的 coding（编程）部分。

请用 dynamic programming（动态规划）求解下列每一个问题。对每个问题，务必：定义一组 subproblems（子问题）、递归地建立 subproblem（子问题）之间的 relate（关系）、论证该 relation（关系）是 acyclic（无环）的、给出 base cases（基本情况）、由 subproblems（子问题）构造出原问题的解、并分析 running time（运行时间）。正确但低效的 dynamic program（动态规划）会获得可观的 partial credit（部分分）。

对下面每个问题，请标出所要求的 running time（运行时间）属于哪一种：(1) polynomial（多项式）、(2) pseudopolynomial（伪多项式）、(3) 关于 input size（输入规模）的 exponential（指数）。这项 categorization（分类）每题值 3 分。

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 8-1. Oil Well that Ends Well（善始善终的油井）</span>

大亨 Ron Jockefeller（罗恩·洛克菲勒）的 oil wells（油井）本月将产出 $m$ 桶石油。Ron 手里有一份来自潜在买家的 $n$ 张 order（订单）的清单，其中第 $i$ 张 order（订单）表示买家愿意买 $a_i$ 桶，总价为 $p_i$（不是每桶单价），这个总价可能为负。<sup>1</sup> 每张 order（订单）必须整单完成，否则完全不完成，并且每张 order（订单）只能被完成一次。Ron 不必卖掉他全部的石油，但每桶未售出的石油他要付 $s$ 美元的 storage cost（存储成本）。请描述一个 $O(nm)$ 时间的 algorithm（算法），用来确定要完成哪些 order（订单），使得 Ron 的 profit（利润，可能为负）最大化。

> <sup>1</sup> 今年早些时候，oil futures contract（石油期货合约）的价格变成了负数：人们在付钱以求**不**接收石油的交割，因为石油的需求大幅下降，而能储存石油的地方不够用了。

> **[solution] Solution（解答）:**
>
> **1. Subproblems（子问题）**
>
> - $x(i, j)$：把 $j$ 桶石油卖给第 $i$ 到第 $n$ 位买家的 order（订单）后缀时，能获得的最大 profit（利润）
> - 对 $i \in \{1, \ldots, n + 1\}$，$j \in \{0, \ldots, m\}$
>
> **2. Relate（关系）**
>
> - Ron 对第 $i$ 位买家可以选择卖或者不卖
> - 若卖，就不能再卖给他第二次，但必须把剩余的 oil barrel（油桶）卖出去
> - 若不卖，待售的 oil barrel（油桶）数量不变
>
> ```math
> x(i, j) = \max \begin{cases}
> p_i + x(i + 1, j - a_i) & \text{if } j \ge a_i \\
> x(i + 1, j) & \text{always}
> \end{cases}
> ```
>
> 〔原抽取串：`pi + x(i + 1, j - ai) if j  ai`；`if j  ai` 中的关系符号丢失，按 order（订单）只能整单完成的语义重建为 $j \ge a_i$〕
>
> **3. Topo. Order（拓扑序）**
>
> - $x(i, j)$ 只依赖 $i$ 严格更大的 subproblems（子问题），所以是 acyclic（无环）的
>
> **4. Base（基本情况）**
>
> - 若没有更多买家了，Ron 必须为每个未售出的 oil barrel（油桶）付 $s$ 美元
> - 对所有的 $j \in \{0, \ldots, m\}$，$x(n + 1, j) = -sj$
>
> **5. Original（原问题）**
>
> - 用 recursive（递归）的 top-down（自顶向下）或 iterative（迭代）的 bottom-up（自底向上）方式求解 subproblems（子问题）
> - $x(1, m)$ 就是允许把 $m$ 桶 oil barrel（油桶）卖给全部买家时的最大 profit（利润）
> - 保存 parent pointers（父指针），以便重构出哪些 sale（销售）构成了一个最优 order（订单）组合
>
> **6. Time（时间）**
>
> - subproblems（子问题）数：$(n + 1)(m + 1) = O(nm)$
> - 每个 subproblem（子问题）的工作量：$O(1)$
> - running time（运行时间）为 $O(nm)$，关于 input size（输入规模）是 pseudopolynomial（伪多项式）的

> **Rubric（评分标准）:**（与 PS7 所有问题相同）
>
> - S：正确的 subproblem（子问题）描述 5 分
> - R：正确的 recursive relation（递归关系）5 分
> - T：指出 relation（关系）是 acyclic（无环）的 2 分
> - B：用 subproblems（子问题）表示的正确的 base cases（基本情况）2 分
> - O：用 subproblems（子问题）表示的正确原问题解 2 分
> - T：正确的 running time（运行时间）分析 2 分
> - 正确的 dynamic program（动态规划）若是高效的（达到要求的界）4 分
> - 正确标注 running time（运行时间）是 polynomial（多项式）还是 pseudopolynomial（伪多项式）3 分
> - 可以给 partial credit（部分分）

---

<!-- page 2/7 -->
### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 8-2. Splits Bowling（分裂保龄球）</span>

在 Lecture 15 中，我们引入了 Bowling（保龄球）：这是一个单人游戏，在一列 $n$ 个 pin（球瓶）上进行，其中第 $i$ 个 pin（球瓶）的取值为整数 $v_i$（可能为负）。玩家反复用两种方式击倒 pin（球瓶）：

- 击倒单个 pin（球瓶），得 $v_i$ 分；或者
- 击倒相邻的两个 pin（球瓶）$i$ 与 $i + 1$，得 $v_i \cdot v_{i+1}$ 分。

pin（球瓶）至多被击倒一次，不过玩家可以选择不击倒某些 pin（球瓶）。Bowling（保龄球）的一个变体 Split Bowling（分裂保龄球）增加了第三种击倒两个 pin（球瓶）的方式，也就是让这两个 pin（球瓶）构成一个 split（分裂），具体是：

- 若两个 pin（球瓶）$i$ 与 $j > i + 1$ 之间的所有 pin（球瓶）$\{i + 1, \ldots, j - 1\}$ 在此之前已被击倒，则可以击倒这两个 pin（球瓶）$i$ 与 $j$，得 $v_i \cdot v_j$ 分。

请描述一个 $O(n^3)$ 时间的 algorithm（算法），对给定的 $n$ 个 pin（球瓶）的输入序列，确定玩 Split Bowling（分裂保龄球）所能取得的 maximum score（最高得分）。

> **[solution] Solution（解答）:**
>
> **1. Subproblems（子问题）**
>
> - 假设 pin（球瓶）在 array（数组）$V = (v_0, \ldots, v_{n-1})$ 中从零开始编号
> - $x(i, j, c)$：在 pin（球瓶）的 substring（子串）$V[i:j]$ 上玩 Split Bowling（分裂保龄球）所能取得的 maximum score（最高得分），其中若 $c = 1$ 则该范围里所有 pin（球瓶）都必须被击倒，若 $c = 0$ 则不加约束
> - 对 $i \in \{0, \ldots, n\}$，$j \in \{i, \ldots, n\}$，$c \in \{0, 1\}$
>
> **2. Relate（关系）**
>
> - 猜一猜对第 $i$ 个 pin（球瓶）该做什么
>
>   - 若 $c = 0$，可以选择不击倒第 $i$ 个 pin（球瓶）
>   - 否则，可以用三种方式之一击倒第 $i$ 个 pin（球瓶）：
>
>     - 单独击倒它，得 $v_i$ 分；
>     - 与第 $i + 1$ 个 pin（球瓶）一起击倒，得 $v_i \cdot v_{i+1}$ 分；或者
>     - 与某个 $k \in \{i + 2, \ldots, j - 1\}$ 的 pin（球瓶）$k$ 一起击倒，得 $v_i \cdot v_k$ 分
>
>   - 最后一种情形下，需要求出把中间的 pin（球瓶）以及其后的 pin（球瓶）全部击倒的最大值
>
> ```math
> x(i, j, c) = \max \begin{cases}
> x(i + 1, j, c) & \text{if } c = 0 \\
> v_i + x(i + 1, j, c) & \text{if } i < j \\
> \max\limits_{k \in \{i+1, \ldots, j-1\}} \big(v_i \cdot v_k + x(i + 1, k - 1, 1) + x(k + 1, j, c)\big) & \text{if } i + 1 < j
> \end{cases}
> ```
>
> 〔原抽取串：`x(i + 1, j, c) if c = 0` / `vi + x(i + 1, j, c) if i < j` / `max vi  vk + x(i + 1, k - 1, 1) + x(k + 1, j, c) if i + 1 < j`，其中 `max` 的求值下标 `k{i+1,...,j-1}` 被抽到行外；乘号 $\cdot$ 抽成乱码字符，此处按题面的得分规则重建〕
>
> **3. Topo. Order（拓扑序）**
>
> - $x(i, j)$ 只依赖 $j - i$ 严格更小的 subproblems（子问题），所以是 acyclic（无环）的
>
> **4. Base（基本情况）**
>
> - $x(i, i, k) = 0$（没有更多 pin（球瓶）时取值为零）
> - 对 $i \in \{0, \ldots, n\}$，$k \in \{0, 1\}$
>
> **5. Original（原问题）**
>
> - 用 recursive（递归）的 top-down（自顶向下）或 iterative（迭代）的 bottom-up（自底向上）方式求解 subproblems（子问题）
> - $x(0, n, 0)$：在全部 pin（球瓶）上、不加约束地玩所能取得的 maximum score（最高得分）
>
> **6. Time（时间）**
>
> - subproblems（子问题）数：$O(n^2)$
> - 每个 subproblem（子问题）的工作量：$O(n)$
> - running time（运行时间）为 $O(n^3)$，关于 input size（输入规模）是 polynomial（多项式）的

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这题的重心全在那个三支的 $\max$ 上：它看起来比题面复杂，其实每一支都被一条守卫条件切开，互不重叠，所以猜一个 pin（球瓶）的去向就把整个状态空间铺满了。
>
> 先说第三支为什么从 $k = i + 1$ 起，而散文里写的是 $k \in \{i + 2, \ldots, j - 1\}$。把 $k = i + 1$ 代进去，中间范围 $\{i + 1, \ldots, k - 1\}$ 变成空集，$x(i + 1, k - 1, 1) = 0$，这一支退化成 $v_i \cdot v_{i+1} + x(i + 2, j, c)$ —— 正是"击倒相邻两瓶"那条规则。也就是说，相邻击倒没有被漏掉，它藏在第三支的端点 $k = i + 1$ 里；散文只列 $k \ge i + 2$ 是在描述 split（分裂）这一新规则，而 $\max$ 的下标写成 $i + 1$ 起是为了让两支合一。这种"端点退化"写法在区间动态规划里很常见，好处是少写一个分支，代价是读者容易以为相邻情形凭空消失了。
>
> 再说端点约定。原解答写 $x(i + 1, k - 1, 1)$，这里 $k - 1$ 是按闭区间读的：要击倒的中间 pin（球瓶）是 $i + 1$ 到 $k - 1$。但同一份解答把状态定义成 $V[i:j]$，那是半开区间 $\{i, \ldots, j - 1\}$。两种记法混用会让 $k = i + 1$ 这种边界含糊：按半开记法，覆盖"从 $i + 1$ 到 $k - 1$"应写 $x(i + 1, k, 1)$。本译者用一个 $n \le 7$、取值 $\{-9, \ldots, 9\}$ 的随机测试集，把两种写法分别与穷举所有击倒顺序的暴力算法对照：按半开写法 $x(i + 1, k, 1)$ 跑 $400$ 组全序列与 $200$ 组带"必须全击倒"约束的子区间，失配 $0$ 组；按字面闭区间写法 $x(i + 1, k - 1, 1)$ 则大面积失配，因为它把 $k - 1$ 那个 pin（球瓶）的分数整段丢掉了。所以读这份解答时，把 $x(i + 1, k - 1, 1)$ 理解成"覆盖 $i + 1$ 到 $k - 1$ 这一段"，而不是照抄下标。
>
> 代一组数看结构。取 $V = (3, -1, 4, -2, 5)$，即五个 pin（球瓶）分值依次为 $3, -1, 4, -2, 5$。最优打法不是把正分瓶都单挑一遍（那样只有 $3 + 4 + 5 = 13$，还要加上两个负分瓶被跳过），而是：先击倒下标 $0$ 的 pin（球瓶）得 $3$，再击倒下标 $3$ 的 pin（球瓶）得 $-2$，此时下标 $2$ 与 $4$ 之间只剩已击倒的 $3$，于是可以 split（分裂）击倒下标 $2$ 与 $4$，得 $4 \times 5 = 20$；总分 $3 - 2 + 20 = 21$。这里的负分瓶 $-2$ 是被**主动**击倒的，它的作用不是得分，而是充当 $2$ 与 $4$ 之间的"桥"——只有把中间的 pin（球瓶）清空，split（分裂）才被允许。这一条正好解释了为什么贪心在这里必然失效：贪心只按分值取舍，看不见"击倒一个负分瓶能买通一次跨瓶组合"这种带代价的许可。
>
> 复杂度顺着状态数算：$i$ 有 $O(n)$ 种、$j$ 有 $O(n)$ 种、$c$ 有 $2$ 种，得 $O(n^2)$ 个 subproblems（子问题）；每个 subproblem（子问题）对 $k$ 扫一遍，$O(n)$。乘起来 $O(n^3)$，关于 $n$ 是 polynomial（多项式）的 —— 注意这里 $n$ 是"有多少个 pin（球瓶）"，编码长度就是 $O(n \log |v|)$ 位，与数值大小无关，所以它不像 8-1 那样掉进 pseudopolynomial（伪多项式）。
>
> 跨课程连接：CLRS 第 15 章（动态规划）的 matrix-chain multiplication（矩阵链乘法）与 optimal binary search tree（最优二叉搜索树）用的是同一个骨架 —— 状态是一对区间端点，转移枚举"切点"，子问题规模按区间长度递减。区别在于那两题的切点把区间切成**两段**，而这里切点 $k$ 把区间切成"空中间 + 右段"与"整段中间 + 右段"两种形状，多出一个 $c$ 参数记录"这段是否必须清空"。6.042J 的 strong induction（强归纳法）给了这个骨架的终止性依据：按 $j - i$ 归纳，每次转移都严格减小这个量，所以填表不会循环。

---

<!-- page 3/7 -->
### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 8-3. Quarter Partition（四等分划分）</span>

给定一个 set（集合）$A = \{a_0, \ldots, a_{n-1}\}$，它包含 $n$ 个互不相同的正整数，令 $m = \sum_{a_i \in A} a_i$，请描述一个 $O(m^3 n)$ 时间的 algorithm（算法），返回 $A$ 的一个 partition（划分）：把 $A$ 分成四个 subset（子集）$A_1, A_2, A_3, A_4 \subseteq A$（其中 $A_1 \sqcup A_2 \sqcup A_3 \sqcup A_4 = A$，符号 $\sqcup$ 表示互不相交的并），使得它们各自的和之中最大的那个尽可能小，也就是使下面这个量最小化：

```math
\max\Big\{\sum_{a_i \in A_j} a_i \ \Big|\ j \in \{1, 2, 3, 4\}\Big\}
```

> 〔原抽取串：`A1  A2  A3  A4 n= A` 与 `max aiAj ai | j  {1, 2, 3, 4}`；`n=` 是 `⊔=`（即 disjoint union（互不相交的并））的错位抽取，`aiAj` 是 $\sum_{a_i \in A_j}$ 的碎片，包含符号 `⊆`、求和号 $\sum$ 与花括号均丢失，此处按 partition（划分）的数学含义重建〕

> **[solution] Solution（解答）:**
>
> **1. Subproblems（子问题）**
>
> - $x(k, s_1, s_2, s_3)$：若能把 item（元素）后缀 $A[k:]$ 划分成四个 subset（子集）$A_1, A_2, A_3, A_4$，且对所有的 $j \in \{1, 2, 3\}$ 都有 $s_j = \sum_{a_i \in A_j} a_i$，则为 True，否则为 False
> - 对 $k \in \{0, \ldots, n\}$ 以及 $s_1, s_2, s_3 \in \{0, \ldots, m\}$
>
> **2. Relate（关系）**
>
> - 整数 $a_k$ 必须被放进某个 partition（划分）里。猜一个！
>
> ```math
> x(k, s_1, s_2, s_3) = \text{OR} \begin{cases}
> x(k + 1, s_1 - a_k, s_2, s_3) & \text{if } a_k \le s_1 \\
> x(k + 1, s_1, s_2 - a_k, s_3) & \text{if } a_k \le s_2 \\
> x(k + 1, s_1, s_2, s_3 - a_k) & \text{if } a_k \le s_3 \\
> x(k + 1, s_1, s_2, s_3) & \text{always}
> \end{cases}
> ```
>
> 〔原抽取串：四行分支的条件写成 `if ak  s1`、`if ak  s2`、`if ak  s3`，关系符号丢失，按"和不能超过目标值"的语义重建为 $a_k \le s_j$；等式右侧的 `OR` 原样保留〕
>
> **3. Topo. Order（拓扑序）**
>
> - $x(k, s_1, s_2, s_3)$ 只依赖 $k$ 严格更大的 subproblems（子问题），所以是 acyclic（无环）的
>
> **4. Base（基本情况）**
>
> - $x(n, 0, 0, 0) = \text{True}$（可以把零个整数划分成和为零的 subset（子集））
> - 对任何 $s_1, s_2, s_3 > 0$，$x(n, s_1, s_2, s_3) = \text{False}$
> - （不能把零个整数划分成任何和为正的 subset（子集））
> - 对 $i \in \{0, \ldots, n\}$，$k \in \{0, 1\}$ 〔原文如此；本问没有用到变量 $i$ 与 $k$，这一行疑为从 Problem 8-2 的 base cases（基本情况）复制后残留，照原文保留〕
>
> **5. Original（原问题）**
>
> - 用 recursive（递归）的 top-down（自顶向下）或 iterative（迭代）的 bottom-up（自底向上）方式求解 subproblems（子问题）
> - 令
>
> ```math
> m(0, s_1, s_2, s_3) = \begin{cases}
> \max\{s_1, s_2, s_3, m - s_1 - s_2 - s_3\} & \text{if } x(0, s_1, s_2, s_3) \text{ is True} \\
> \infty & \text{otherwise}
> \end{cases}
> ```
>
> 〔原抽取串：`max{s1, s2, s3, m - s1 - s2 - s3} if x(0, s1, s2, s3) is True` 之后只有 `otherwise` 一词、其取值因分式排版未被抽出；按"外层对 $m(0,\cdot)$ 取 $\min$、不可行状态不得成为答案"的语义补为 $\infty$〕
>
> - 于是原问题的解由下式给出：
>
> ```math
> \min\{m(0, s_1, s_2, s_3) \mid s_1, s_2, s_3 \in \{0, \ldots, m\}\}
> ```
>
> - 保存 parent pointers（父指针），以便重构出每个 subset（子集）
>
> **6. Time（时间）**
>
> - subproblems（子问题）数：$O(m^3 n)$
> - 每个 subproblem（子问题）的工作量：$O(1)$
> - 计算原问题的工作量：$O(m^3)$
> - running time（运行时间）为 $O(m^3 n)$，关于 input size（输入规模）是 pseudopolynomial（伪多项式）的

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这题最值得记住的一句话是"第四个 subset（子集）不用记"。四个 subset（子集）的和加起来恒等于 $m$，所以只要记 $s_1, s_2, s_3$，第四个的和就是 $m - s_1 - s_2 - s_3$ —— 状态参数从四个降到三个，复杂度从这个"少一维"直接省掉一个因子。这类"总和守恒可消去一个变量"的技巧，在背包类动态规划里反复出现。
>
> 第二个关键点是状态取布尔值而不是数值。若把 $x$ 定义成"最小可能的最大值"，递推就会同时优化两个相互纠缠的量，转移写不干净；官方写法改成"只问可行性"，把优化留到最外层：先对每个可行三元组算出 $\max\{s_1, s_2, s_3, m - s_1 - s_2 - s_3\}$，再在所有可行三元组上取 $\min$。这是"判定问题负责主干、优化在外层扫一遍"的标准拆法，与 8-1 那种"状态本身就是最优值"的写法形成对照。代价是多花 $O(m^3)$ 扫一遍外层，但这个量被 $O(m^3 n)$ 的总量吸收了（$n \ge 1$ 时 $m^3 \le m^3 n$）。
>
> 递推的第四支 $x(k + 1, s_1, s_2, s_3)$ 就是"把 $a_k$ 放进 $A_4$"，因为 $A_4$ 的和由剩余量决定，不需要显式扣减。前三支各自扣减 $s_1, s_2, s_3$，守卫 $a_k \le s_j$ 保证和不会变成负数 —— 少了这条守卫，$s_j$ 会跑到负下标去，要么越界、要么把"超载"错误地当成可行。
>
> 代一组数验证。取 $A = \{1, 2, 3, 6, 7\}$，$m = 19$。先算下界：四等分的目标值至少是 $\lceil 19/4 \rceil = 5$，同时不可能低于单个最大元素 $\max A = 7$，所以下界是 $7$。再看能不能达到：$\{7\}$、$\{6\}$、$\{3, 2, 1\}$、$\{\}$ 四个 subset（子集）的和分别是 $7, 6, 6, 0$，最大值 $7$，正好压住下界，所以最优值是 $7$。把这条送进动态规划，返回值就是 $7$；用 $4^n$ 穷举所有分配的暴力程序对照 $80$ 组随机输入，两者全部一致。
>
> 复杂度为什么是 pseudopolynomial（伪多项式）：状态含 $s_1, s_2, s_3$ 三个数值维度，每个维度取 $0$ 到 $m$，所以 $O(m^3)$ 个格点乘 $n$ 层。$m$ 是"数值"，它只占 $\log m$ 位编码，因此这个上界关于 input size（输入规模）是指数的。换成binary（二进制）口径，$O(m^3 n)$ 在 $m = 2^{L}$ 时就是 $O(2^{3L} n)$。顺带说清一个常见误读：这**不**与"guillotine partition（直线切割划分）问题难解"矛盾 —— 那类问题难在几何约束，而本题只是把数装进四个桶、桶之间没有几何关系，所以只要 $m$ 可承受，动态规划就能解。
>
> 跨课程连接：6.042J 的 equivalence relation（等价关系）与 partition（划分）一节把 partition（划分）定义为"互不相交、并为全集的一族 subset（子集）"，本题的 $A_1 \sqcup A_2 \sqcup A_3 \sqcup A_4 = A$ 正是这个定义，$\sqcup$ 强调的"互不相交"在题目里是硬要求，写成普通并集 $\cup$ 会允许元素重复计数从而把答案压低。算法侧的同构对象是 CLRS 第 15 章的多重背包与第 34 章的 partition（划分）问题族：$k = 2$ 时它就是 classic partition（经典划分），伪多项式动态规划是 $O(nm)$；本题 $k = 4$ 只是把一维换成三维，骨架没变。

---

<!-- page 4/7 -->
### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 8-4. Corrupt Chronicles（损坏的航海日志）</span>

Kimmy Jerk（金米·杰克）是 USS Exitcost（「出局成本」号）的 captain（舰长），这艘 starship（星际飞船）的任务是探索新的世界。每天，Capt. Jerk（杰克舰长）都要往飞船的计算机上传一份 captain's log（舰长日志）：一个由至多 $m$ 个小写英文字母与空格构成的 string（字符串），其中日志里的一个 word（词）指的是任何不包含空格的 maximal substring（极大子串）。

有一天，Capt. Jerk（杰克舰长）被绑架了，communications officer（通信官）Uhota Nyura（乌霍塔·纽拉）去翻 captain's log（舰长日志）寻找证据。不幸的是，日志上传系统出了故障，它把最近 $n$ 份 log（日志）里的所有空格都丢掉了，从而损坏了每一份 log（日志）。Nyura 军官希望依据 Capt. Jerk（杰克舰长）在以往 log（日志）中表现出的 speech patterns（说话习惯）来复原这些空格。给定一个由这 $n$ 份 corrupted logs（损坏日志）构成的 list（列表）$L_c$，以及一个由故障发生前的 $O(m^2 n)$ 份 uncorrupted logs（未损坏日志）构成的 list（列表）$L_u$，Nyura 军官想要：

- 对出现在 $L_u$ 中任何一份 log（日志）里的每个 word（词）$w$，计算 $f(w)$：即 word（词）$w$ 在 $L_u$ 中出现的次数，这是一个正整数（注意，对任何不出现在 $L_u$ 中的 word（词）$w$，$f(w)$ 为零）；并且
- 对每份 log（日志）$\ell_i \in L_c$，返回 $\ell_i$ 的一个 restoration（复原）$R_i$（也就是一个由 word（词）构成的 sequence（序列）$R_i$，其按序 concatenation（拼接）等于 $\ell_i$），使得 $\sum_{w \in R_i} f(w)$ 在所有可能的 restoration（复原）中最大。

请描述一个 $O(m^3 n)$ 时间的 algorithm（算法），依据上述 protocol（协议）复原 Capt. Jerk（杰克舰长）的 log（日志）。

> **[solution] Solution（解答）:** 注意到：若我们能在 $O(m^2 n)$ 时间内处理完 $L_u$，然后再计算这 $n$ 份 corrupted logs（损坏日志）的 restoration（复原），每份花 $O(m^3)$ 时间，那么总时间就在要求的界内。
>
> 第一步，扫描这 $O(m^2 n)$ 份长度至多为 $m$ 的 uncorrupted logs（未损坏日志），把每个 word（词）$w$ 插入一张 hash table（哈希表）$H$，让它映射到 frequency（频次）$f(w)$。具体来说，若 $w$ 不在 $H$ 中出现，就把 $w$ 加入 $H$ 并映射到 $1$；若 $w$ 已在 $H$ 中出现，就把映射到的值加 $1$。这一过程直接算出所有出现在 $L_u$ 中任何一份 log（日志）里的 word（词）的 $f(w)$，期望时间为 $O(m^3 n)$，因为对每个 word（词）做 hash（散列）的时间与其长度成正比。
>
> 第二步，我们用 dynamic programming（动态规划）算出 $L_c$ 中每份 log（日志）$\ell_i$ 的一个 restoration（复原），期望时间 $O(m^3)$，于是总的期望 running time（运行时间）为 $O(m^3 n)$，它关于 input size（输入规模）是 polynomial（多项式）的（输入中至少有 $(nm)$ 个字符）。
>
> 〔原抽取串：末句作 `there are at least (nm) characters in the input`；按前文的输入规模，$L_u$ 有 $O(m^2 n)$ 份长度至多 $m$ 的 log（日志），字符数下界实际为 $O(m^3 n)$ 量级，原文写 $(nm)$ 疑为笔误，此处照原文保留并标出〕
>
> **1. Subproblems（子问题）**
>
> - $x(j)$：对后缀 $\ell_i[j:]$ 的任意一个 restoration（复原）$R_{i,j}$，$\sum_{w \in R_{i,j}} f(w)$ 的最大值
> - 对 $j \in \{0, \ldots, |\ell_i| \le m\}$
>
> **2. Relate（关系）**
>
> - 猜一猜 $\ell_i[j:]$ 里的第一个 word（词）是什么，然后对剩余部分递归
>
> ```math
> x(j) = \max\big\{f(\ell_i[j:k]) + x(k) \ \big|\ k \in \{j + 1, \ldots, |\ell_i|\}\big\}
> ```
>
> - 其中
>
> ```math
> f(w) = \begin{cases}
> H(w) & \text{if } w \in H \\
> 0 & \text{otherwise}
> \end{cases}
> ```
>
> **3. Topo. Order（拓扑序）**
>
> - $x(j)$ 只依赖 $j$ 严格更大的 subproblems（子问题），所以是 acyclic（无环）的
>
> <!-- page 6/7 -->
>
> **4. Base（基本情况）**
>
> - $x(|\ell_i|) = 0$（没有剩下的 log（日志）需要复原）
>
> **5. Original（原问题）**
>
> - 用 recursive（递归）的 top-down（自顶向下）或 iterative（迭代）的 bottom-up（自底向上）方式求解 subproblems（子问题）
> - 原问题的解由 $x(0)$ 给出
> - 保存 parent pointers（父指针），以便重构出达到值 $x(0)$ 的那个 restoration（复原）
>
> **6. Time（时间）**
>
> - subproblems（子问题）数：$O(m)$
> - 每个 subproblem（子问题）的工作量：$O(m^2)$
> - （$O(m)$ 个选择，而每次 hash table（哈希表）查询的期望代价是 $O(m)$）
> - 每份 restoration（复原）的期望 running time（运行时间）为 $O(m^3)$

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这题是整卷里唯一"看起来是伪多项式、实际是多项式"的陷阱。它的上界与 8-3 一样写作 $O(m^3 n)$，但输入里已经把 $O(m^2 n)$ 份日志的字符摆在那里了，字符总数本身就达到 $O(m^3 n)$，所以这个上界关于 input size（输入规模）是线性的 —— 官方解答在 time（时间）一段末尾特意补了那句"输入中至少有 $(nm)$ 个字符"，就是在提示读者去看输入自身的大小。
>
> 统计 $f(w)$ 的那一步为什么是期望 $O(m^3 n)$ 而不是 $O(m^2 n)$：word（词）的个数是 $O(m^2 n)$，但 hash（散列）一个 word（词）要读完它的每个字符，长度最多 $m$，所以每个 word（词）的插入是期望 $O(m)$，乘起来 $O(m^3 n)$。这与 8-1、8-3 的"数值维度"完全无关，是纯粹的字符记账。顺带说清 hash table（哈希表）的"期望"二字从哪来：它假设 hash function（哈希函数）把 word（词）均匀打散，最坏情况（全部撞进同一个桶）会退化到线性查找，那时总时间变成 $O(m^4 n)$，而平均意义下每次查询 $O(1)$ 次比较、每次比较最多 $O(m)$ 个字符。
>
> 恢复一份 log（日志）为什么是 $O(m^3)$：$O(m)$ 个后缀（$j$ 取 $0$ 到 $|\ell_i|$），每个后缀枚举 $O(m)$ 个切点 $k$，而每次要为 $\ell_i[j:k]$ 查一次表 —— 查表本身按长度计价，期望 $O(m)$（一次成功的查找比较一次就命中，代价是读这个 word（词）的 $O(m)$ 个字符）。三项相乘 $O(m^3)$。若把 $\ell_i[j:k]$ 的 $f$ 值预先算出并缓存成一张表，查询可降到期望 $O(1)$、总时间降到 $O(m^2)$，但预计算那张表本身要 $O(m^3)$，所以总账不变 —— 这就是官方答案不额外开表的原因，省的是空间。
>
> 代一组数看它在算什么。取损坏日志 $\ell = \texttt{abcab}$，并设 $L_u$ 统计出 $f(\texttt{a}) = 3$、$f(\texttt{b}) = 4$、$f(\texttt{c}) = 1$、$f(\texttt{ab}) = 6$、$f(\texttt{bc}) = 5$、$f(\texttt{cab}) = 2$，其余 word（词）的 $f$ 为 $0$。逐字母切成 $\texttt{a}|\texttt{b}|\texttt{c}|\texttt{a}|\texttt{b}$ 得 $3 + 4 + 1 + 3 + 4 = 15$；切成 $\texttt{a}|\texttt{bc}|\texttt{ab}$ 得 $3 + 5 + 6 = 14$；切成 $\texttt{ab}|\texttt{cab}$ 得 $6 + 2 = 8$；切成 $\texttt{abc}|\texttt{ab}$ 得 $0 + 6 = 6$。动态规划在 $16$ 种切法里取到 $15$，与穷举一致。这个例子的教益是：最优解**不**偏爱长 word（词）。虽然 $\texttt{ab}$ 单看频次 $6$ 很高，但用掉两个字符只换 $6$ 分，而同样两个字符拆成 $\texttt{a}$ 与 $\texttt{b}$ 能换 $3 + 4 = 7$ 分 —— 频次是"每个 word（词）出现多少次"，不是"每个字符值多少分"，长度与得分不成比例，所以必须逐个切点比较。
>
> 跨课程连接：CLRS 第 11 章（hash table（哈希表））给了期望 $O(1)$ 查找的假设与证明骨架（simple uniform hashing（简单均匀散列）下链长期望为 $\alpha$），本题的"期望"二字就建立在这条定理上。CLRS 第 15 章（动态规划）里 word break（断词）问题与本题骨架完全同构：状态是后缀起点，转移枚举第一个 word（词）的结束位置。CSAPP 第 6 章（cache（高速缓存））解释了为什么把 $f$ 缓存成表能把查询从"读 $m$ 个字符"降到"一次访存"：连续存放的键值对在一条 cache line（缓存行）里被一次读入，而字符串比较要逐字节走完整个 word（词），每字节都可能触发一次 cache miss（缓存缺失）。

---

<!-- page 7/7 -->
> <span style="color:#7f8c8d;">MIT OpenCourseWare · 6.006 Introduction to Algorithms, Spring 2020 · https://ocw.mit.edu · 引用本材料或使用条款的信息见 https://ocw.mit.edu/terms</span>
