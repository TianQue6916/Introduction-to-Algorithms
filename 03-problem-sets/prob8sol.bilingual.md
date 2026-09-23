# Introduction to Algorithms: 6.006（算法导论）

Massachusetts Institute of Technology
Instructors: Erik Demaine（埃里克·德梅因）, Jason Ku（顾杰森）, and Justin Solomon（贾斯汀·所罗门）

## <span style="color:#2471a3;">**[session]**</span> <span style="color:#c0392b">Problem Session 8（习题课 8）</span>

> <span style="color:#7f8c8d;">MIT 6.006 Spring 2020, Problem Session 8 Solutions（习题课 8 解答，对应 Problem Set 8）· 主题：dynamic programming（动态规划）</span>

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 8-1. Sunny Studies（阳光学习计划）</span>

Tim the Beaver（海狸蒂姆）需要为考试复习，但天气越来越暖和，Tim 想花更多时间待在户外。天气越暖 Tim 越喜欢户外活动：具体来说，如果户外温度是高于零度的 $t$ 个整数单位，那么 Tim 在外面待一天后 happiness（幸福感）会增加 $t$（当 $t$ 为负时幸福感会下降）。在期末考试前的 $n$ 天里，每一天 Tim 要么学习，要么出去玩（同一天从不两者兼做）。为了保持学业不掉队，Tim 决心连续在户外玩的天数**不超过两天**。给定未来 $n$ 天的 weather forecast（天气预报）温度估计，描述一个 $O(n)$ 时间的 dynamic programming algorithm（动态规划算法），确定 Tim 应该在哪几天学习，才能使幸福感增加最多。

> **[solution] Solution（解答）:**
>
> **1. Subproblems（子问题）**
>
> - 设 $t(i)$ 为第 $i$ 天的温度
> - $x(i)$：第 $i$ 天到第 $n$ 天期间可能达到的最大幸福感增加量
>
> **2. Relate（关联）**
>
> - Guess（猜测）第 $i$ 天是学习还是出去玩会带来更多幸福感
> - 如果学习，幸福感不变，但第二天可以学习或玩，即 $x(i+1)$
> - 如果玩，幸福感改变 $t(i)$，并且要么
>   - 第 $i+1$ 天学习：$t(i) + x(i+2)$；或
>   - 第 $i+1$ 天也玩、第 $i+2$ 天学习：$t(i) + t(i+1) + x(i+3)$
> - 对 $i \in \{1, \dots, n-1\}$：
>
>   ```math
>   x(i) = \max\{x(i+1),\ t(i) + x(i+2),\ t(i) + t(i+1) + x(i+3)\}
>   ```
>
> **3. Topo. Order（拓扑序）**
>
> - 子问题 $x(i)$ 只依赖下标严格更大的子问题，因此 acyclic（无环）
>
> **4. Base（基例）**
>
> - $x(n) = \max\{0, t(n)\}$：如果只剩一天，要么玩要么学习
> - $x(n+1) = x(n+2) = 0$：如果没有更多天，无法再增加幸福感
>
> **5. Original（原问题）**
>
> - $x(1)$ 是从第 1 天到第 $n$ 天的最大幸福感增加量
> - 存储 parent pointers（父指针）以重构应该学习的天数
>
> **6. Time（时间分析）**
>
> - 子问题数：$x(i)$，$i \in \{1, \dots, n+2\}$，共 $n+2 = O(n)$ 个
> - 每个子问题的工作量：$O(1)$（branching factor，分支因子为常数）
> - 运行时间 $O(n)$

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 本题的设计问题（design question）是：如何把「连续玩不超过两天」这种**全局约束**翻译进 DP 的子问题结构，而不需要引入额外的状态维度。解法用的是**后缀窗口枚举法**——子问题取 suffixes（后缀）「从第 $i$ 天起」，Relate 阶段把最后一段可能的玩天窗口（0、1、2 天）逐项枚举出来，约束自动满足：窗口长度被限制为 2，任何方案都落在「今天学」「今天玩 + 明天学」「今天玩 + 明天玩 + 后天学」三个互斥分支里。这与你 [lec15]（SRT BOT 六步法）和 [lec16]（LIS、Coins）完全同构：子问题取后缀、Relate 做 local brute-force（局部暴力枚举）、Base 处理边界天。三个候选的窗口固定为 2，分支因子才是常数，复杂度才压到 $O(n)$——若把约束放宽成「连续最多 $k$ 天」，递推会变成 $k+1$ 项取 max，复杂度升为 $O(kn)$，窗口宽度就是 DP 的「记忆长度」。你在 LeetCode 见过的 House Robber（打家劫舍，相邻最多选一天）是窗口为 1 的退化情形，本题是同一族「滑动窗口约束」DP 的窗口为 2 版本——从 1 到 2 的变化展示了约束长度如何直接决定递推的分支数和状态结构。

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 8-2. Diffing Data（数据比对）</span>

操作系统 Menix 有一个 diff utility（差异比对工具）可以比较文件。一个 file（文件）是一个有序的 strings（字符串）序列，其中第 $i$ 个字符串称为文件的第 $i$ 行。对文件的一次单个 change（变更）是以下操作之一：

- 向文件插入单个新行；
- 从文件删除单个行；或
- 交换文件中两个相邻的行。

在 Menix 中，交换两行很便宜，因为它们已经在文件里了；但插入或删除一行很贵。从文件 $A$ 到文件 $B$ 的 diff 是任意 change 序列，按顺序应用于 $A$ 就能把它变换成 $B$，条件是在何一行最多被交换一次，且任何一对被交换的行在 $A$ 中相邻、在 $B$ 中也相邻。给定两个文件 $A$ 和 $B$，每个恰好包含 $n$ 行，描述一个 $O(kn + n^2)$ 时间的 algorithm（算法），返回从 $A$ 到 $B$ 的、最小化非交换变更数的 diff，假设任一文件中的任意一行长度最多为 $k$ 个 ASCII 字符。

> **[solution] Solution（解答）:**
>
> **1. Subproblems（子问题）**
>
> - 首先，用 hash table（哈希表）在 $O(kn)$ 时间内为每个唯一行分配一个编号
> - 现在每行可以在 $O(1)$ 时间内与其他行比较
> - $x(i, j)$：将 $A[:i]$ 变换为 $B[:j]$ 所需的最小非交换变更数
>
> **2. Relate（关联）**
>
> - 如果 $A[i] = B[j]$，则在剩余部分上递归
> - 否则，考虑最后应用的一个变更：
>   - 删除 $A[i]$
>   - 插入一行与 $B[j]$ 匹配
>   - 交换 $A[:i]$ 中最后两行，以匹配 $B[:j]$ 中最后两行
> - 如果 $A[i] = B[j]$：$x(i, j) = x(i-1, j-1)$
> - 否则：
>
>   ```math
>   x(i, j) = \min \begin{cases}
>   1 + x(i-1, j) & \text{删除} \\
>   1 + x(i, j-1) & \text{插入} \\
>   x(i-2, j-2) & \text{交换，若 } A[i] = B[j-1] \text{ 且 } A[i-1] = B[j]
>   \end{cases}
>   ```
>
> **3. Topo. Order（拓扑序）**
>
> - 子问题 $x(i, j)$ 只依赖 $i + j$ 严格更小的子问题，因此 acyclic
>
> **4. Base（基例）**
>
> - $x(0, 0) = 0$：所有行都已变换完成
> - $x(i, 0) = i$：必须删除剩余部分
> - $x(0, j) = j$：必须插入剩余部分
>
> **5. Original（原问题）**
>
> - 按定义即为 $x(n, n)$
> - 存储 parent pointers 以重构实际做了哪些变更（在 $A[i] \neq B[j]$ 的分支里，记住发生的是删除、插入还是交换）
>
> **6. Time（时间分析）**
>
> - 预处理：$O(kn)$
> - 子问题数：$(n+1)^2 = O(n^2)$，$x(i, j)$，$i, j \in \{0, 1, \dots, n\}$
> - 每个子问题的工作量：$O(1)$
> - 运行时间 $O(n^2)$

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 本题本质上是 **edit distance（编辑距离）** 家族的一员，与你 [lec15] 学过的 edit distance 以及 CLRS §15.4 的 **LCS（longest common subsequence，最长公共子序列）** 是同一个递推骨架：二维子问题 $x(i,j)$、按「最后一个操作」分情况、三分支取 $\min$。本题的增量是**交换操作**——它把常见的二分支（删/插）变成三分支，而且 swap 分支要看**两行**（$x(i-2, j-2)$）而不是一行，这正是「操作集合 → 递推分支」的对应关系：每个被允许的操作都对应一个「吃进多少输入」的分支。命名模板：**三分支最小代价递推**。两个值得注意的细节：一是「一行最多被交换一次、且交换对在 $A$、$B$ 中都相邻」的约束保证了交换分支只能作用于尾部两行，否则递推会指数爆炸；二是原文有两处笔误——Relate 部分的 "if $A[i] = A[j]$" 应为 $A[i] = B[j]$（否则条件恒真、递推退化），Original 部分的 "$x(n, n, 0)$" 应为 $x(n, n)$，译文已按正确含义处理。工业界的对应物：git diff 默认采用 Eugene Myers 1986 年提出的 **O(ND)** 算法（D 为两文件差异规模，通常远小于 $n^2$），它基于 LCS 的贪心化变体、空间线性，是对本 DP 的工程化改进。

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 8-3. Building Blocks（搭积木）</span>

Saggie Mimpson（萨吉·米普森）是一个喜欢搭积木塔的幼儿。她的每块积木都是一个 3D rectangular prism（三维长方体），其中每块积木 $b_i$ 有正整数 width（宽）$w_i$、height（高）$h_i$ 和 length（长）$\ell_i$，而且每种积木她至少有三块。每块积木可以定向，使得其任意一对相对的长方形面充当顶面和底面，积木在该定向下的 height 是这两个面之间的距离。Saggie 想通过把积木尽可能堆高来建造一座塔，但只有当一块定向积木 $b_i$ 的底面尺寸**严格小于**另一块定向积木 $b_j$ 的顶面尺寸¹ 时，她才能把 $b_i$ 堆在 $b_j$ 上面。给定她 $n$ 块积木的尺寸，描述一个 $O(n^2)$ 时间的 algorithm，确定 Saggie 能用她的积木建造的最高塔的高度。

> <span style="color:#7f8c8d;">¹ 如果积木 $b_i$ 的底面尺寸为 $p \times q$，积木 $b_j$ 的顶面尺寸为 $s \times t$，则在这种定向下 $b_i$ 可以堆在 $b_j$ 上，当且仅当：$p < s$ 且 $q < t$；或 $p < t$ 且 $q < s$。</span>

> **[solution] Solution（解答）:**
>
> **1. Subproblems（子问题）**
>
> - 每块积木可以按三种垂直定向之一使用
> - （不失一般性，积木底面总可以按较短边指向同一方向来堆放）
> - 因为堆叠要求底面尺寸严格递减，任何最优塔对每种积木类型最多使用三次（每种定向一次）
> - 对每块积木的尺寸排序并去重（例如用 hash table 在 $O(n)$ 时间内完成）
> - 对排序后尺寸为 $a \le b \le c$ 的每种积木类型，构造三种定向 $(a, b, c)$、$(a, c, b)$、$(b, c, a)$（最后一个维度对应 height），并在 $O(n)$ 时间内加入 oriented block list（定向积木列表）
> - （每种类型重复三次是允许的，因为每种至少有三块）
> - 在 $O(n \log n)$ 时间内按字典序排序（第一维度最显著）
> - 重新编号排序后的列表，其中积木 $i$ 的定向尺寸为 $(w_i, \ell_i, h_i)$ 且 $w_i \le \ell_i$
> - 任何可堆叠的定向积木塔都必须是该排序列表的 subsequence（子序列），因为 $w_i$ 已排序；但并非该列表的每个子序列都构成合法塔，因为 $\ell_i$ 不一定有序
> - $x(i)$：使用积木 $i$ 以及剩余积木 $1$ 到 $i-1$ 的任意子集搭成的塔的最大高度
>
> **2. Relate（关联）**
>
> - Guess（猜测）塔中下一块更低的积木，只从 $\ell_i$ 严格更小的积木中选择
>
>   ```math
>   x(i) = h_i + \max\big(\{0\} \cup \{x(j) \mid j \in \{1, \dots, i-1\} \text{ 且 } \ell_i < \ell_j\}\big)
>   ```
>
> **3. Topo. Order（拓扑序）**
>
> - 子问题 $x(i)$ 只依赖下标严格更小的子问题，因此 acyclic
>
> **4. Base（基例）**
>
> - $x(1) = h_1$：递推中的最大值平凡地为 0
>
> **5. Original（原问题）**
>
> - 某块积木必须是塔顶，因此比较所有可能的塔顶
> - $\max\{x(i) \mid i \in \{1, \dots, n\}\}$
>
> **6. Time（时间分析）**
>
> - 预处理：$O(n \log n)$
> - 子问题数：$n$，$x(i)$，$i \in \{1, \dots, n\}$
> - 每个子问题的工作量：$O(n)$
> - 计算最终解：$O(n)$
> - 运行时间 $O(n^2)$
> - 注意：这个问题可以用与 Recitation 15 中 **Longest Increasing Subsequence（最长递增子序列，LIS）** 类似的优化，在 $O(n \log n)$ 时间内解决。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 本题是经典的 **Box Stacking（箱子堆叠）** 问题，核心技巧可以命名为**排序降维法**：把「底面两个维度都严格递减」的二维偏序约束，通过按第一维排序消去一维——排序后任何合法塔必须是该序列的 subsequence，剩下只需检查第二维 $\ell$。这与你在 [lec16] 学的 LIS 完全同构：LIS 是一维偏序（数值递增），本题是二维偏序（$w$ 和 $\ell$ 都严格递减），递推 $x(i) = h_i + \max\{x(j) : \ell_i < \ell_j\}$ 与 LIS 的 $x(i) = 1 + \max\{x(j) : A[j] < A[i]\}$ 逐项对应，只是把「取 1」换成「加 $h_i$」。原文提到的 $O(n \log n)$ 优化正是 lec16 讲过的 patience sorting（耐心排序）思想：维护按 $\ell$ 值索引的数据结构，把「扫描所有更小 $j$」的 $O(n)$ 降为对数时间。另一个值得注意的观察是「每种积木最多使用三次」——因为堆叠要求严格递减，同一积木类型的三次使用对应三种定向，恰好是「3 种定向 × 严格递减链最长 3 段」的组合上限；这个观察把「无限供应」问题规约为「有限 $3n$ 个物品」，是构造子问题前的关键 preprocessing 洞察。

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 8-4. Princess Plum（梅子公主）</span>

Princess Plum（梅子公主）是一个电子游戏角色，正在一片数字 haunted forest（鬼林）中收集蘑菇。森林是一个 $n \times n$ 的方形 grid（网格），每个网格方格要么是 tree（树）、mushroom（蘑菇），要么是空的。如果两个方格共享一条边，Princess Plum 就可以从一个方格移动到另一个方格，但她不能进入含有树的方格。Princess Plum 从左上角方格出发，想到达右下角方格的家²。鬼林很吓人，所以她希望走一条 quick path（快捷路径）回家：一条从起点到家的 route（路线），经过最多 $2n-1$ 个方格（包括起点和家）。如果 Princess Plum 进入一个含有蘑菇的方格，她会捡起它。设 $k$ 为她在任意 quick path 上能捡到的最大蘑菇数，若一条 quick path 上她能捡到 $k$ 个蘑菇，则称该 quick path 为 optimal（最优）的。

> <span style="color:#7f8c8d;">² 假设起点和家的方格都是空的。</span>

<span style="color:#2471a3;">**[part]**</span> <span style="color:#00838f">**(a) [15 points]**</span> 给定森林网格的地图，描述一个 $O(n^2)$ 时间的 algorithm，返回穿过森林的 distinct（不同的）optimal quick paths 的数量，假设存在某条 quick path。

> **[solution] Solution（解答）:**
>
> **1. Subproblems（子问题）**
>
> - 设左上角方格为 $(1, 1)$，右下角方格为 $(n, n)$
> - 设 $F[i][j]$ 表示方格 $(i, j)$ 的内容
> - 定义两类子问题：一类用于最优蘑菇数，一类用于计算路径数
> - $k(i, j)$：在触碰 $i + j - 1$ 个方格的路径上，从 $(1, 1)$ 到达 $(i, j)$ 的最大蘑菇数
> - $x(i, j)$：触碰 $i + j - 1$ 个方格、收集 $k(i, j)$ 个蘑菇的、从 $(1, 1)$ 到 $(i, j)$ 的路径数
>
> **2. Relate（关联）**
>
> - 一条触碰 $i + j - 1$ 个方格、终止于 $(i, j)$ 的路径，必须延伸一条触碰 $i + j - 2$ 个方格、终止于其左邻或上邻的路径
> - 如果 $F[i][j]$ 含有树：
>   - 没有到 $(i, j)$ 的路径
>   - $k(i, j) = -\infty$ 且 $x(i, j) = 0$
> - 否则：
>   - 设 $m(i, j)$ 在 $F[i][j]$ 是蘑菇时为 $1$，否则为 $0$
>   - $k(i, j) = m(i, j) + \max(k(i-1, j),\ k(i, j-1))$
>   - $x(i, j)$ 等于所有满足「经由该前驱达到最优」条件的前驱 $x$ 值之和：
>
>   ```math
>   x(i, j) = \sum_{\substack{p \in \{(i-1,j),\ (i,j-1)\} \\ k(p) + m(i, j) = k(i, j)}} x(p)
>   ```
>
>   （即：若左邻达到最优则累加 $x(i-1, j)$，若上邻达到最优则累加 $x(i, j-1)$，两者都达到最优则累加两者之和，都不满足则为 $0$）
>
> **3. Topo. Order（拓扑序）**
>
> - 子问题 $k(i, j)$ 只依赖 $i + j$ 严格更小的 $k$ 子问题，因此 acyclic
> - 子问题 $x(i, j)$ 只依赖 $i + j$ 严格更小的 $x$ 子问题（以及不依赖任何 $x$ 子问题的 $k$ 子问题），因此 acyclic
>
> **4. Base（基例）**
>
> - $k(1, 1) = 0$：起点没有蘑菇
> - $x(1, 1) = 1$：起点处有一条路径
> - 负下标方格不可能
> - $k(0, i) = k(i, 0) = -\infty$，$i \in \{0, \dots, n\}$
> - $x(0, i) = x(i, 0) = 0$，$i \in \{0, \dots, n\}$
>
> **5. Original（原问题）**
>
> - 按定义即为 $x(n, n)$
>
> **6. Time（时间分析）**
>
> - 子问题数：$2(n+1)^2 = O(n^2)$，$k(i, j)$ 和 $x(i, j)$，$i, j \in \{0, 1, \dots, n\}$
> - 每个子问题的工作量：$O(1)$
> - 运行时间 $O(n^2)$

<span style="color:#2471a3;">**[part]**</span> <span style="color:#00838f">**(b) [25 points]**</span> 编写一个 Python 函数 `count_paths(F)`，实现你在 (a) 中的 algorithm。

> **[solution] Solution（解答）:**

```python
def count_paths(F):
    n = len(F)
    K = [[-float('inf')]*(n + 1) for _ in range(n + 1)]  # init K memo
    X = [[0]*(n + 1) for _ in range(n + 1)]  # init X memo
    for i in range(1, n + 1):  # bottom-up dynamic program
        for j in range(1, n + 1):
            if F[i - 1][j - 1] == 't':  # base case
                continue
            if i == 1 and j == 1:  # base case
                K[1][1], X[1][1] = 0, 1
                continue
            if F[i - 1][j - 1] == 'm':
                m = 1
            else:
                m = 0
            K[i][j] = m + max(K[i - 1][j], K[i][j - 1])
            if K[i - 1][j] + m == K[i][j]: X[i][j] += X[i - 1][j]
            if K[i][j - 1] + m == K[i][j]: X[i][j] += X[i][j - 1]
    return X[n][n]
```

> <span style="color:#7f8c8d;">代码要点：$K$ 表初值 $-\infty$ 充当「不可达」标记（含树方格保持 $-\infty$ 不更新），$X$ 表初值 $0$；$m$ 在蘑菇格为 $1$。两个 `if` 条件与递推中「$k$ 值相等才累加」一一对应——若两个前驱都达到最优，两个 `if` 同时成立，$X[i][j]$ 自动得两者之和，与求和式一致。边界 $k(0,i) = k(i,0) = -\infty$、$x(0,i) = x(i,0) = 0$ 由数组的零行/零列初值天然实现。</span>

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 本题展示的**值表 + 计数表双表法**是 DP 计数问题的标准套路：当题目要求「数出达到最优值的方案数」时，不能只维护一个最值表，而要同时维护两个表——$k$ 表存最值、$x$ 表存达到该最值的方案数，且 $x$ 的转移被「$k(p) + m(i,j) = k(i,j)$」这个条件门控：只有经由能达成全局最优的前驱，其路径数才被累加。这个门控是计数正确性的关键——如果直接无条件累加两个前驱的路径数，会把「非最优路径」也数进去。背后的直觉与你在 6.042J 学过的组合计数同源：一个 $n \times n$ 网格上只允许向右、向下走，从左上到右下的路径数是二项式系数（Pascal 三角——每个格子的路径数 = 左 + 上），本题的 DP 本质上就是在「只有右/下的 DAG」上数路径，树格点把对应路径数清零，蘑菇只影响 $k$ 值不改变路径结构。注意题目「最多 $2n-1$ 个方格」这一条件等价于「只能向右或向下走」（任何含左/上回退的路径都更长），这正是网格 DAG 的隐藏来源——识别出这个等价关系，问题就从「任意路径」降维成 DAG 上的路径计数，与 [lec15] 讲过的 DAG shortest paths（CLRS §24.2）共享同一拓扑序论证。

---

<span style="color:#2471a3;">**[source]**</span> **Source（来源）:** MIT OpenCourseWare — https://ocw.mit.edu

**6.006 Introduction to Algorithms（算法导论）** — Spring 2020 · [Terms of Use](https://ocw.mit.edu/terms)
