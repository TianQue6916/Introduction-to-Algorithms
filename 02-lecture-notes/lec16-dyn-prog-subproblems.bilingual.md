# Introduction to Algorithms: 6.006

## <span style="color:#2471a3;">**[lecture]**</span> <span style="color:#c0392b">Lecture 16: Dynamic Programming, Part 2 — LCS, LIS, Coins（动态规划第二讲：最长公共子序列、最长递增子序列、交替取硬币）</span>

Massachusetts Institute of Technology
Instructors: Erik Demaine, Jason Ku, and Justin Solomon

> <span style="color:#7f8c8d;">MIT 6.006 Spring 2020, Lecture 16 讲义（对应视频：Dynamic Programming, Part 2）</span>

---

## <span style="color:#2471a3;">**[section]**</span> <span style="color:#c0392b">Dynamic Programming Review（动态规划复习）</span>

本讲是 dynamic programming（动态规划）四讲中的**第二讲**。🎥 *Demaine 开场就点明*："We're now in step two out of four."（翻译：我们现在处于（四讲中的）第二讲。） *上一讲（Lecture 15）建立了 SRT BOT 框架，本讲通过三个例子探索三个新维度：多输入序列、子串型子问题、parent pointers（父指针）恢复方案，以及下一讲才完整展开的 subproblem constraint and expansion（子问题约束与扩展）。*

DP 的本质回顾：

- Recursion（递归）中 **subproblem dependencies（子问题依赖）重叠**，形成 DAG（有向无环图）
- **"Recurse but re-use"（递归但复用）**——即 top-down（自顶向下）实现：记录并查找子问题解（memoization，记忆化）
- **"Careful brute force"（精细的暴力枚举）**——即 bottom-up（自底向上）实现：按序求解每个子问题

### <span style="color:#2471a3;">**[step]**</span> <span style="color:#c0392b">Dynamic Programming Steps（SRT BOT 六步法）</span>

**Step 1: Subproblem definition（子问题定义）**——子问题 $x \in X$：

- 用参数描述子问题含义
- 通常取输入的 subsets（子集）：sequences（序列）的 prefixes（前缀）、suffixes（后缀）、contiguous substrings（连续子串）
- 对多输入，常取各输入子集的 **product（笛卡尔积）**
- 常记录 partial state（部分状态）：通过递增辅助变量扩展子问题

**Step 2: Relate subproblem solutions recursively（递归关联子问题解）**

```math
x(i) = f\big(x(j), \dots\big) \quad \text{for one or more } j < i
```

- 找出一个关于子问题解的 **question（问题）**：若知道答案，就能把子问题归约为更小的子问题
- 对问题的所有可能答案 **locally brute-force（局部暴力枚举）**

**Step 3: Topological order（拓扑序）**——论证关联是 acyclic（无环的），子问题构成 DAG。

**Step 4: Base cases（基例）**——为所有（可达的）关联失效的独立子问题给出解。

**Step 5: Original problem（原问题）**——说明如何从子问题解组装原问题解；可能要用 parent pointers（父指针）恢复 actual solution（实际方案），而不仅是 objective function（目标函数）值。

**Step 6: Time analysis（时间分析）**

```math
\sum_{x \in X} \text{work}(x) \quad \text{；若对所有 } x \in X \text{ 有 } \text{work}(x) = O(W)，\text{则为 } |X| \cdot O(W)
```

其中 $\text{work}(x)$ 衡量关联中的**非递归**工作量，递归调用视为 $O(1)$。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 🎥 Demaine 的原话："because we memoize, we'll only solve each subproblem once. And so in the end, the running time will be at most the number of subproblems times the non-recursive work done in that relation."（翻译：因为我们做了记忆化，每个子问题只会被求解一次；所以最终运行时间至多是子问题数乘以该递推中做的非递归工作量。） 公式 $|X| \cdot O(W)$ 的根基是两个互锁保证——memoization 让每个子问题只算一次，即便被多个「父」子问题调用也不重复计费；acyclic 依赖保证存在一个不陷入循环的合法求解顺序。🎥 Demaine 对 DAG 建模的表述极其精确："the vertices are subproblems. And I want to draw an edge from a smaller problem to a bigger problem... if evaluating B calls A, then I'll draw an arrow from A to B, from the things I need to do first to the things I'll do later."（翻译：顶点就是子问题；我想从较小的子问题向较大的子问题画一条边……如果计算 B 会调用 A，我就画一条从 A 指向 B 的箭头——从需要先算的东西指向之后才算的东西。） 注意边的方向是「被调用者 → 调用者」而非直觉的「大 → 小」——这是为了让拓扑序的语义一致：先算 A 再算 B。你在 6.006 前两周学的 DAG 最短路径（CLRS §24.2）和拓扑排序（CLRS §22.4）正是对同一结构的另一组操作：DP 的 bottom-up 填表本质上是手写了一个已知拓扑序的 relaxation，不需要跑 DFS 发现顺序。回到 acyclicity 的必要性——🎥 "for that to work, of course, the relations between subproblems must be acyclic"（翻译：当然，要让这套分析成立，子问题之间的依赖关系必须是无环的。）——这与 6.042J 归纳法中的「良基关系」（well-founded relation）要求完全一致：归纳必须沿一个没有无穷下降链的偏序走，否则归纳假设永远无法落地。把子问题依赖画成 DAG 不是辅助想象——它是 DP 正确性和复杂度分析的「硬」证明骨架。

---

## <span style="color:#2471a3;">**[section]**</span> <span style="color:#c0392b">Longest Common Subsequence（最长公共子序列，LCS）</span>

**问题：** 给定两个字符串 $A$ 和 $B$，找出 $A$ 的一个 longest subsequence（最长子序列）——它不必连续——使其同时是 $B$ 的 subsequence。

- **Example（例）：** $A = \text{hieroglyphology}$，$B = \text{michaelangelo}$
- **Solution（解）：** hello 或 heglo 或 iello 或 ieglo，长度均为 5
- 这是关于 subsequence 长度的 maximization problem（最大化问题）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 🎥 Demaine 在引入 LCS 之前先划了一条硬边界："Substring has to be some continuous range, some interval. Subsequence, you can take any subset of the letters... you can have blanks in between."（翻译：子串必须是一段连续的范围、一个区间；而子序列可以取字母的任意子集……中间可以有空隙。） 这个区分直接左右子问题形状的选型——substring 型问题天然需要 contiguous substrings 做子问题（本讲硬币游戏：从两端取硬币，留下的一定是连续区间，子问题数因此升到 $\Theta(n^2)$），而 subsequence 型问题用 suffix/prefix 就够（子问题数保持 $O(n)$）。用 6.042J 的术语说：substring 的子问题空间是序列的「区间」集合（所有 $(i,j)$ 对），subsequence 的子问题空间是序列的「后缀」集合——前者 $\Theta(n^2)$，后者 $\Theta(n)$，这个量级差是 DP 设计的第一步关键决策。🎥 Demaine 随后给出了 LCS 在计算生物学中的标准定位："It even has applications to things like computational biology. You have two DNA sequences. You want to measure how in common they are."（翻译：它甚至能用于计算生物学这类场景：你有两条 DNA 序列，想衡量它们有多相似。） 两条 DNA 的 LCS 长度直接衡量它们共有的最长保守区段——比对人类与黑猩猩基因组时，LCS 给出未被打乱顺序的最长匹配片段。🎥 他还提到了近亲 edit distance："One version of that... called edit distance."（翻译：其中一种版本叫编辑距离。） 编辑距离（允许插入/删除/替换，最小化总代价）与 LCS 共享子问题形状（suffix×suffix 笛卡尔积），区别仅在于递推的转移选项——LCS 只允许「匹配则对角线 +1 / 否则跳过一侧」，编辑距离多了「替换」操作，本质是同一种 DP 的两个变体。

### <span style="color:#2471a3;">**[step]**</span> <span style="color:#c0392b">1. Subproblems（子问题）</span>

- $x(i, j)$ = 后缀 $A[i:]$ 与 $B[j:]$ 的最长公共子序列长度
- 参数范围：$0 \le i \le |A|$，$0 \le j \le |B|$

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 🎥 Demaine 把这个技巧讲得极简："It's a very simple trick. We just take the product, multiply the subproblem spaces. In the sense of cross product of sets."（翻译：这是个很简单的技巧：直接取乘积，把子问题空间相乘——按集合的笛卡尔积来理解。） 单一序列时子问题空间是 $O(n)$ 的后缀集合；两个序列时，子问题变成一个二元组 $(i,j)$，每个坐标独立取后缀——总数是 $|A| \cdot |B|$，仍是多项式。关键直觉：这不是「两个空间加起来」，而是做笛卡尔积——从组合视角看，$O(n)$ 和 $O(n)$ 的乘积是 $O(n^2)$，与你学过的「多项式 × 多项式仍是多项式」闭包性质一致。🎥 Demaine 还特意解释了为什么把空后缀纳入子问题空间："I like to include the empty suffix... because that makes for really easy base cases."（翻译：我喜欢把空后缀也包含进来……因为这让基例变得非常容易写。） $i=|A|$ 或 $j=|B|$ 对应一条序列已耗尽，此时 LCS 长度为 0——base case 是递推自然下落到「无字符可匹配」的终点，而非额外打补丁。把边界条件纳入子问题空间本身，让递推的 for 循环统一处理所有下标——这与二叉搜索树用 sentinel 节点统一边界逻辑的设计哲学异曲同工。从 CLRS §15.4 看，子问题定义与教材完全一致：$c[i,j]$ 是 $X_i$ 与 $Y_j$ 的 LCS 长度，$i,j$ 的范围含 0（空序列）。更深层的设计智慧是：对多输入问题，笛卡尔积不仅「能用」，而且往往是唯一正确的子问题化道路——两个输入地位对称，任一输入的子问题退化都会丢失必要信息，只有完整保留笛卡尔积的每一格才能让递推在两条序列上同时「前进」。

### <span style="color:#2471a3;">**[step]**</span> <span style="color:#c0392b">2. Relate（关联）</span>

两种情形：**首字符匹配**或**不匹配**。

- **若首字符匹配**：存在某个最长公共子序列会用到它们
  - （若没有 LCS 用这对匹配的字符，用上它们只会改进解）
  - （若某 LCS 用了 $A[i]$ 而没用 $B[j]$，则把 $B[j]$ 配进来同样最优）
- **若不匹配**：它们不可能同时出现在某个最长公共子序列中
  - **Guess（猜测）：** $A[i]$ 或 $B[j]$ 至少有一个不在 LCS 中

```math
x(i, j) = \begin{cases}
x(i+1, j+1) + 1 & \text{if } A[i] = B[j] \\[4pt]
\max\{x(i+1, j),\ x(i, j+1)\} & \text{otherwise}
\end{cases}
```

（矩形网格依赖图：所有子问题构成一个 $(|A|+1) \times (|B|+1)$ 的网格，每个格子只向右下或向下/向右连边。）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 讲义里匹配情形括号中的注释不是随手写的旁注——它是**交换论证（exchange argument）**的完整演示，一个在算法正确性证明中反复出现的可复用模板。交换论证的骨架：假设存在一个最优解不具有性质 $P$，通过局部「交换」（swap）操作把它调整成另一个解，证明新解同样最优且具有 $P$。🎥 Demaine 在视频里的非正式版更直觉："You can actually guarantee that $A_i$ and $B_j$ might as well be in the longest common subsequence."（翻译：实际上你可以保证 $A_i$ 和 $B_j$ 不妨就出现在最长公共子序列里。） 他分两个子情形论证：(1) 若最优 LCS 中 $A_i$ 和 $B_j$ 都没有匹配任何字符——🎥 "that's silly... you can add this pair, and that would be a longer subsequence"（翻译：那就太傻了……你可以把这一对加进去，得到更长的子序列。）——直接加进去长度 +1，与最优性矛盾；(2) 若 $A_i$ 匹配了远处的 $B_k$（$k>j$），则 🎥 "I can just instead pair $i$ with $B_j$"（翻译：我可以直接把 $i$ 改配给 $B_j$。）——因为 $A_i=B_j$，把匹配对象从远处的 $B_k$ 换成眼前的 $B_j$，长度不变且仍是公共子序列。两个子情形合起来证明了「存在一个最优 LCS 同时使用 $A_i$ 和 $B_j$」——这正是交换论证的经典结论：最优解可以被「调整」成含某个特定结构而不变差。你在 6.006 后半程会反复遇到同类骨架：活动选择问题的贪心正确性、Huffman 编码的最优性、Kruskal 最小生成树算法——它们的证明结构全是「若最优解不含 X，则通过局部替换得到另一个不更差且含 X 的解」。把这个模板内化成肌肉记忆：一旦递推分支看上去「理所当然」而你想严格证明它，交换论证是第一个该试的工具。

### <span style="color:#2471a3;">**[step]**</span> <span style="color:#c0392b">3. Topological order（拓扑序）</span>

- 子问题 $x(i, j)$ 只依赖 $i$ 或 $j$ 严格更大的子问题
- 最简表述顺序：**decreasing $i + j$（按 $i+j$ 递减）**
- 便于 bottom-up 代码的顺序：**decreasing $i$，然后 decreasing $j$**（即从右下角向左上角逐行填表）

### <span style="color:#2471a3;">**[step]**</span> <span style="color:#c0392b">4. Base cases（基例）</span>

- $x(i, |B|) = x(|A|, j) = 0$——其中一条字符串为空

### <span style="color:#2471a3;">**[step]**</span> <span style="color:#c0392b">5. Original problem（原问题）</span>

- $A$ 与 $B$ 的最长公共子序列长度 = $x(0, 0)$
- 存储 parent pointers（父指针）以重建 subsequence：
  - 若父指针同时增加两个下标（即走了匹配分支），把该字符加入 LCS

### <span style="color:#2471a3;">**[step]**</span> <span style="color:#c0392b">6. Time（时间分析）</span>

- 子问题数：$(|A| + 1) \cdot (|B| + 1)$
- 每个子问题工作量：$O(1)$
- 总运行时间：$O(|A| \cdot |B|)$

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 从枚举 $A$ 的所有 $2^{|A|}$ 个子序列逐一检查，到 $O(|A|\cdot|B|)$ 的 DP——这不是常数优化，是问题复杂度的阶跃：指数级 → 多项式级。这个跃迁的数学本质是「子问题数 × 每子问题非递归工作」乘法公式——把「枚举所有方案」替换为「枚举 $O(n^2)$ 个状态、每个状态 $O(1)$ 转移」。🎥 Demaine 随后给出了一个贯穿多讲的统一视角："both of these dynamic programs could instead construct a graph and then run DAG shortest paths on it. But the point is these are the same thing."（翻译：这两个动态规划都可以改为构造一张图、然后在上面跑 DAG 最短路径；关键是它们在本质上是同一回事。） 把 LCS 的 $(|A|+1)\times(|B|+1)$ 子问题网格看成图：每个格点是一个顶点，不匹配时向右/向下画权重 0 的边，匹配时向右下画权重 $-1$ 的对角边——$x(0,0)$ 就是该 DAG 上从 $(0,0)$ 到 $(|A|,|B|)$ 的最短路径长度取负。🎥 他在 LIS 的 DAG 中也用了同一技巧："longest path is the same thing as shortest path if you just negate all the weights... if you put negative 1 on all of the diagonal edges and you put weight 0 everywhere else, then the shortest path... will correspond to the longest, the path with the most diagonal edges."（翻译：把所有权重取反，最长路径就等同于最短路径……如果给所有对角边赋权重 -1、其余边赋权重 0，那么最短路径就对应最长路径——也就是对角边最多的那条路径。） 你在 Lecture 12-13 学的 DAG 最短路径算法（CLRS §24.2）——先拓扑排序再按序 relaxation——与 DP 的 bottom-up 填表在数学上完全同构：DP 的拓扑序就是图的拓扑序，DP 的递推公式就是 relaxation（$d[v] = \min\{d[u]+w(u,v)\}$），DP 的 base case 就是源点距离初始化。🎥 Demaine 解释了为什么 DP 代码更简洁："you already know what the topological order is, you don't have to write a generic depth-first search algorithm, take the finishing order, reverse it, and then run DAG shortest paths with relaxation."（翻译：你已经知道拓扑序是什么了，不必写一个通用的深度优先搜索算法、取完成序、反转，再用松弛操作跑 DAG 最短路径。） 不是所有 DP 都能写成最短路径问题（Fibonacci 就不能），但 LCS 和 LIS 的网格/DAG 结构让这种等价变得透明——从指数暴力到多项式 DP，本质是把「路径枚举」换成了「DAG 最短路径」。

```python
def lcs(A, B):
    a, b = len(A), len(B)
    x = [[0] * (b + 1) for _ in range(a + 1)]
    for i in reversed(range(a)):
        for j in reversed(range(b)):
            if A[i] == B[j]:
                x[i][j] = x[i + 1][j + 1] + 1
            else:
                x[i][j] = max(x[i + 1][j], x[i][j + 1])
    return x[0][0]
```

> <span style="color:#7f8c8d;">代码对应讲义第 3 页底部；二维数组 $x$ 的维度是 $(a+1) \times (b+1)$，最后一行/一列天然为 0（Python 列表初始化），正好充当 base cases。</span>

---

## <span style="color:#2471a3;">**[section]**</span> <span style="color:#c0392b">Longest Increasing Subsequence（最长递增子序列，LIS）</span>

**问题：** 给定一个字符串 $A$，找出 $A$ 的一个最长 subsequence（子序列），使其（按字典序）**严格递增**。

- **Example（例）：** $A = \text{carbohydrate}$
- **Solution（解）：** abort，长度为 5
- 这是关于 subsequence 长度的 maximization problem（最大化问题）

**⚠️ 一次失败的尝试（关键教学环节）：**

- 自然的子问题是 $A$ 的 prefix/suffix，比如 suffix $A[i:]$
- 关于 $A[i:]$ 的 LIS 的自然问题是：**$A[i]$ 在不在 LIS 中？**（2 种x z答案）
- 但这样如何在 $A[i+1:]$ 上递归并保证是递增子序列？
- **Fix（修复）：** 给子问题**加约束**，提供足够结构来保证递增性质

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这个失败不是教学事故——它是子问题约束（subproblem constraint）的动机演示，值得从第一性原理拆解。🎥 Demaine 写出 $x(i) = \max\{x(i+1),\ 1+x(i+1)\}$ 后立刻自嘲"This is a very strange recurrence, right? Because this is always bigger than this one."（翻译：这是个非常奇怪的递推，对吧？因为这个分支（第二个）总是比那个（第一个）大。）——第二个分支恒大于第一个，递推退化成「永远把 $A[i]$ 放进去」，完全没检查递增性。根因比表面深：定义 $x(i)$ 为「后缀 $A[i{+}1:]$ 的 LIS 长度」时，归纳假设只告诉我们那个子问题的**长度**，却没说它的**第一个元素是谁**——于是 $A[i]$ 要和谁比大小？不知道。这触及 DP 与分治的本质分野：分治的子问题是「同一问题在更小输入上的答案」（如归并排序的左右两半），而 DP 的子问题可以是「**换了约束的相邻问题**」——你不必拘泥于原问题形式，可以给它加一个约束（这里是「必须从 $A[i]$ 开始」），只要这个约束能被递推利用、最终能被原问题汇总回来。从归纳法的角度看：归纳步需要更强的归纳假设——不是「后缀的 LIS 长度」，而是「以 $A[i]$ 开头的后缀 LIS 长度」——前者信息量不够支撑递推，后者多携带了一个「首元素已知」的不变量，递推就能写了。你学过的离散数学里"加强归纳假设"（strengthening the induction hypothesis）就是同一个道理：有时候归纳假设不够强，需要证明一个更强的命题才能让归纳步走通。这里的"更强命题"就是给子问题加约束。

### <span style="color:#2471a3;">**[step]**</span> <span style="color:#c0392b">1. Subproblems（子问题）</span>

- $x(i)$ = 后缀 $A[i:]$ 的 **包含 $A[i]$ 的** 最长递增子序列长度
- 参数范围：$0 \le i \le |A|$

### <span style="color:#2471a3;">**[step]**</span> <span style="color:#c0392b">2. Relate（关联）</span>

- 已知 $A[i]$ 在 LIS 中（它就是第一个元素）
- 下一个问题：**LIS 的第二个元素是谁？**
  - 可以是任意 $A[j]$，其中 $j > i$ 且 $A[j] > A[i]$（保证递增）
  - 或者 $A[i]$ 就是 LIS 的最后一个元素

```math
x(i) = \max\big\{\,1 + x(j) \mid i < j < |A|,\ A[j] > A[i]\,\big\} \cup \{1\}
```

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这条递推里藏着一个可命名的证明策略模板——**局部暴力枚举 + 约束筛选法**——三步走：(1) 识别「我不知道什么」——我不知道递增子序列的第二个元素 $j$ 是谁；(2) 枚举所有候选——$j$ 只有 $O(n)$ 个可能（$i < j < |A|$），全试一遍；(3) 用局部约束筛掉无效候选——只保留满足 $A[j] > A[i]$ 的 $j$，取 max。🎥 Demaine 把它总结成一条心法："Whenever there's something I don't know, I'll just brute force it."（翻译：凡是我不知道的东西，我就直接暴力枚举它。） 把未知量变成枚举维度，这就是 DP 的"精细暴力"本质。$\cup \{1\}$ 的设计同样值得拆：当 $A[i]$ 右边没有更大的元素时，max 作用在空集上在数学上没有定义，所以显式插入 $\{1\}$ 作为"退路"——$A[i]$ 自成一条长度为 1 的递增序列。更深刻的洞察在递增性的传递机制：约束 $A[j] > A[i]$ 只检查了**相邻两跳**是否递增，但 $x(j)$ 的归纳假设保证了从 $j$ 开始的剩余部分已经递增——于是 $A[i] < A[j] < \dots$ 串联后整体递增自动成立。这就是"全局性质局部化"：把「整个子序列递增」这一全局条件，压缩成对每一步跳跃的局部检查，归纳负责传递。你之前在离散数学里学的归纳证明模板里，这是"如果 $P(k)$ 成立且第 $k+1$ 步满足某条件，则 $P(k+1)$ 成立"的精确对应。

### <span style="color:#2471a3;">**[step]**</span> <span style="color:#c0392b">3. Topological order（拓扑序）</span>

- Decreasing $i$（$i$ 递减）

### <span style="color:#2471a3;">**[step]**</span> <span style="color:#c0392b">4. Base cases（基例）</span>

- **不需要单独基例**，因为递推中考虑了「$A[i]$ 是最后一个元素」的可能性（$\cup \{1\}$）

### <span style="color:#2471a3;">**[step]**</span> <span style="color:#c0392b">5. Original problem（原问题）</span>

- 整个 LIS 的第一个元素是谁？**Guess（猜）！**
- $A$ 的 LIS 长度 = $\max\{x(i) \mid 0 \le i < |A|\}$
- 存储 parent pointers（父指针）以重建子序列

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这是 DP 设计的一条可迁移心法——**约束是分给递推用的，原问题负责把它们汇总回来**。$x(i)$ 的定义加了约束「必须以 $A[i]$ 开头」之后，递推变得清爽（只需枚举第二个元素），但代价是 $x(i)$ 不再直接等于原问题的解——carbohydrate 的 LIS 是 abort，并不以第一个字母 c 开头。🎥 Demaine 的处理几乎是心法本身："Where do we start? There's only $n$ choices. Let's just take the max of all of them."（翻译：我们从哪里开始？只有 $n$ 种选择，把它们全部取最大值就行。）——把"起点未知"也当作一次局部暴力枚举，$\max\{x(i) \mid 0 \le i < |A|\}$ 就是汇总。定价逻辑清晰：给每个子问题绑了一个约束维度（起点位置），子问题数不变（还是 $O(n)$ 个），但原问题多了一层 $O(n)$ 的 max——总复杂度仍是 $O(n^2)$，不亏。对比 LCS：$x(i,j)$ 的定义没有额外约束，原问题 $x(0,0)$ 一步到位；LIS 因为加了约束，原问题就多了一层聚合。这个模式会在 Lecture 17 大放异彩——当你把子问题约束推到极致（比如不仅指定起点还指定终点、不仅指定一个参数还指定两个），原问题的汇总也会相应地更复杂，但只要子问题数和汇总量都是多项式，总时间就不炸。记住这个设计心法的压缩版：「**递推需要约束，原问题负责解绑**」。

### <span style="color:#2471a3;">**[step]**</span> <span style="color:#c0392b">6. Time（时间分析）</span>

- 子问题数：$|A|$

- 每个子问题工作量：$O(|A|)$

- 总运行时间：$O(|A|^2)$

- **Exercise（练习）：** *Speed up to $O(|A| \log |A|)$ by doing only $O(\log |A|)$ work per subproblem, via AVL tree augmentation*（通过 AVL tree augmentation（AVL 树增强），让每个子问题只做 $O(\log |A|)$ 工作量，把总时间加速到 $O(|A| \log |A|)$）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这个练习是 Lecture 7-8 AVL 树（平衡二叉搜索树）内容的直接应用：递推里的 $\max\{1 + x(j) \mid j > i,\ A[j] > A[i]\}$ 本质是一个**带约束的区间最大值查询**——「在位置 $i$ 右边、值大于 $A[i]$ 的所有 $j$ 中找 $x(j)$ 最大」。把 $(A[j], x(j))$ 按值 $A[j]$ 排序后建一棵以 $x(j)$ 为 key 的 augmented AVL 树，从右往左扫 $i$，每次查询「值域后缀最大值」$O(\log n)$、插入 $O(\log n)$，总时间 $O(n \log n)$。这与你熟悉的那套「数据结构加速 DP」套路（CLRS 里也有类似思想）一致：DP 的转移是「查询+更新」，遇到 $O(n)$ 的转移循环，就该想想能不能用 balanced BST / segment tree / Fenwick tree 把查询压到对数时间。值域压缩 + 线段树也能达到同样效果——两者是同一思想的两种实现。

```python
def lis(A):
    a = len(A)
    x = [1] * a
    for i in reversed(range(a)):
        for j in range(i, a):
            if A[j] > A[i]:
                x[i] = max(x[i], 1 + x[j])
    return max(x)
```

> <span style="color:#7f8c8d;">代码对应讲义第 5 页底部：$x$ 初始化为全 1（每个元素自身构成长度 1 的递增序列），内层循环实现 $\max\{1 + x(j) \mid j > i,\ A[j] > A[i]\}$，最后对整个 $x$ 取 max 即原问题。注意 $\cup \{1\}$ 由初始化天然实现。</span>

---

## <span style="color:#2471a3;">**[section]**</span> <span style="color:#c0392b">Alternating Coin Game（交替取硬币游戏）</span>

**问题：** 给定 $n$ 枚硬币的序列，价值为 $v_0, v_1, \dots, v_{n-1}$。

- 两名玩家（"me"（我）和 "you"（你））轮流行动
- 每轮从**剩余硬币中取第一枚或最后一枚**
- 我的目标：最大化我取到的硬币总价值，且**我先手**

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 贪心直觉说「先拿最大的」——硬币 $5,10,100,25$，一眼盯上 25，但你立刻拿走 100，我只得 $25+10=35$。正确策略是先拿 5，把 100「锁」在中间，你无论选 10 还是 25 我都下一步拿 100，最终我拿 $5+100=105$。🎥 *Demaine 原话*："25 is really good... But then, of course, you're going next. And you're going to choose 100."（翻译：25 确实很好……但接下来当然轮到你，你会拿走 100。） 贪心失败不是「局部最优≠全局最优」这句废话——关键是我的行动会改变对手能拿到什么，贪心框架里没有「对手会反制我」这个结构。这引出更深洞见：游戏状态决定子问题形状。两端取硬币，剩余永远是连续区间——🎥 *Demaine 指出*："As soon as I delete the first coin, and then maybe you take the second coin... Now you have an arbitrary substring in the middle."（翻译：一旦我取走第一枚硬币，然后你可能又取走第二枚……现在剩下的就是中间任意一段连续子序列了。） prefix 或 suffix 只能覆盖「只删一头」的历史，两端同时删必须上 substring（$\Theta(n^2)$ 个子问题）。日后遇「首尾操作」类问题，先问：操作会把连续区间打断吗？不打断→substring；只删一头→prefix/suffix 就够。

### <span style="color:#2471a3;">**[solution-1]**</span> <span style="color:#c0392b">第一种解法：利用 zero-sum（零和）性质</span>

先注意到这是一个 **zero-sum game（零和游戏）**：所有硬币最终被取完，我拿到的 = 总价值 − 你拿到的。

**1. Subproblems（子问题）**

- 选择与**游戏状态**对应的子问题：对每个连续子序列 $v_i, \dots, v_j$（$0 \le i \le j < n$）
- $x(i, j)$ = 我从 $v_i, \dots, v_j$ 开始能拿到的最大总价值

**2. Relate（关联）**

- 我必须选硬币 $i$ 或硬币 $j$（**Guess（猜）！**）
- 然后轮到你，你将分别得到 $x(i+1, j)$ 或 $x(i, j-1)$ 的价值
- 为了算出我的价值：用区间总价值**减去**你能拿到的

```math
x(i, j) = \max\left\{\,v_i + \sum_{k=i+1}^{j} v_k - x(i+1, j),\ \ v_j + \sum_{k=i}^{j-1} v_k - x(i, j-1)\,\right\}
```

**3. Topological order（拓扑序）**

- Increasing $j - i$（按区间长度递增）

**4. Base cases（基例）**

- $x(i, i) = v_i$（只剩一枚硬币，我拿走）

**5. Original problem（原问题）**

- $x(0, n-1)$
- 存储 parent pointers（父指针）以重建策略

**6. Time（时间分析）**

- 子问题数：$\Theta(n^2)$

- 每个子问题工作量：$\Theta(n)$（计算区间和）

- 总运行时间：$\Theta(n^3)$

- **Exercise（练习）：** *Speed up to $\Theta(n^2)$ time by precomputing all sums $\sum_{k=i}^{j} v_k$ in $\Theta(n^2)$ time, via dynamic programming (!)*（用 dynamic programming 在 $\Theta(n^2)$ 时间内预计算所有区间和 $\sum_{k=i}^{j} v_k$，把总时间加速到 $\Theta(n^2)$——区间和本身也靠 DP 算！）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 零和意味着所有硬币终被取完，所以我拿的 = 总价值 − 你拿的。递推里的 $\max\{v_i + \sum_{k=i+1}^j v_k - x(i+1,j),\ v_j + \sum_{k=i}^{j-1} v_k - x(i,j-1)\}$ 读作：「我拿 $v_i$，剩余区间总价值减去你（作为先手时）能拿的最大值」——$x$ 函数不区分谁先手，全靠「减」翻转视角，这是零和博弈最优雅的设计。🎥 *Demaine 点明*："exploiting that the game is zero-sum."（翻译：利用这个游戏是零和的这一性质。） 但每步转移要现算 $\Theta(n)$ 的区间和，总时间 $O(n^3)$。练习题的「用 DP 预计算区间和」直指一个可命名的模式：**聚合量预处理（Aggregate Precomputation）**——转移中反复出现求和/求积/区间最值，先 $O(n^2)$ 算完存好，以后 $O(1)$ 查。这正是你 6.006 前半学过的前缀和（prefix sums）在 DP 里的自然延伸：前缀和是 $\sum_{k=0}^{i} v_k$，区间和 $\sum_{k=i}^j v_k = \text{pref}[j] - \text{pref}[i-1]$，$O(n)$ 预处理后 $O(1)$ 查询。这里更粗暴——$\Theta(n^2)$ 个区间和全存进二维数组，因为 DP 本身就要填 $\Theta(n^2)$ 的表，不亏。CLRS §15 大量习题靠这招降 $n$ 的一次幂，与 CSAPP §3 循环优化里「把循环不变量提出来」是同构的工程直觉：重复算的就缓存。

### <span style="color:#2471a3;">**[solution-2]**</span> <span style="color:#c0392b">第二种解法：subproblem expansion（子问题扩展）</span>

第二种解法使用 **subproblem expansion（子问题扩展）**：为「你行动时」的情形增加子问题。

**1. Subproblems（子问题）**

- 选择与游戏**完整状态**对应的子问题：硬币区间 $[i, j]$ + 下一步行动的玩家 $p$
- $x(i, j, p)$ = 当玩家 $p \in \{\text{me}, \text{you}\}$ 从 $v_i, \dots, v_j$ 开始时，**我**能拿到的最大总价值

**2. Relate（关联）**

- 玩家 $p$ 必须选硬币 $i$ 或硬币 $j$（**Guess（猜）！**）
- 若 $p = \text{me}$，我拿到硬币价值；否则我什么也拿不到
- 然后轮到另一名玩家

```math
\begin{aligned}
x(i, j, \text{me}) &= \max\{\,v_i + x(i+1, j, \text{you}),\ \ v_j + x(i, j-1, \text{you})\,\} \\[4pt]
x(i, j, \text{you}) &= \min\{\,x(i+1, j, \text{me}),\ \ x(i, j-1, \text{me})\,\}
\end{aligned}
```

**3. Topological order（拓扑序）**

- Increasing $j - i$（按区间长度递增）

**4. Base cases（基例）**

- $x(i, i, \text{me}) = v_i$
- $x(i, i, \text{you}) = 0$

**5. Original problem（原问题）**

- $x(0, n-1, \text{me})$
- 存储 parent pointers（父指针）以重建策略

**6. Time（时间分析）**

- 子问题数：$\Theta(n^2)$
- 每个子问题工作量：$\Theta(1)$
- 总运行时间：$\Theta(n^2)$

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 解法一用零和减法隐式处理「轮到谁」，解法二直接把「轮到谁」变成子问题的第三个坐标 $p \in \{\text{me}, \text{you}\}$，子问题数翻倍（$2\Theta(n^2)=\Theta(n^2)$），但每个转移从 $\Theta(n)$ 压到 $O(1)$ 的 max/min。🎥 *Demaine 的口号*："Whenever you run into a new type of problem, just build more subproblems. As long as it stays a polynomial number, we'll get polynomial time."（翻译：每当遇到新类型的问题，就构造更多的子问题；只要子问题数量保持多项式级，就能得到多项式时间。） 这就是子问题扩展的定价逻辑：多项式 × 多项式仍是多项式——用子问题数量换转移复杂度。关键在「轮到对手时用 min」。🎥 *Demaine 说*："You're kind of a pain in the ass... you're trying to minimize my score."（翻译：你这家伙真让人头疼……你总想把我的得分压到最低。） 你拿的越多，我拿的越少——零和博弈下，你的最优选择恰是我的最坏情况。递推里 $x(i,j,\text{me}) = \max\{v_i + x(i+1,j,\text{you}),\ v_j + x(i,j-1,\text{you})\}$（我行动，从两个选项里取最好），$x(i,j,\text{you}) = \min\{x(i+1,j,\text{me}),\ x(i,j-1,\text{me})\}$（你行动，你替我选最差）。这「我 max 你 min」的交替结构是双人零和博弈 DP 的通用模板——它与你离散数学 6.042J 里学过的量词交替 $\forall \exists \forall \cdots$ 同构：max 对应「存在一个行动使收益最大」，min 对应「对所有对手行动，收益至少不低于」。日后学正式博弈论时，minimax theorem 会把这种直觉形式化，但骨架已在 6.006 这里搭好。要记住的模板：「完整状态 = 游戏局面 + 轮到谁，我行动取 max，对手行动取 min」。

---

## <span style="color:#2471a3;">**[section]**</span> <span style="color:#c0392b">Subproblem Constraints and Expansion（子问题约束与扩展）</span>

- 本讲已经看到了**两个**「约束或扩展子问题」的例子：
  - **LIS**：给子问题加约束——「LIS 必须以 $A[i]$ 开头」
  - **Coin game（解法二）**：扩展子问题——增加「轮到谁」这一坐标
- **如果发现缺乏足够信息来检查问题所需的条件，或缺乏可递归的自然子问题，就试试子问题约束/扩展！**
- 更多的子问题和约束给关联提供更多「抓手」，使 DP 更可行
- 通常存在 **trade-off（权衡）**：子问题数量 vs 关联的分支/复杂度
- 更多例子见下一讲

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 把本讲三例放进设计决策表，能看清 SRT BOT 框架外的第二层技能——子问题形状的选择。LCS 示范多输入笛卡尔积：两个序列各取 suffix，子问题空间是两者的 product，每多一个序列维度升一维。LIS 示范子问题约束：「设 $A[i]$ 必须在 LIS 里」把全局递增局部化——约束分给递推用，原问题再对所有约束取 max 汇总回来。Coin 示范子问题扩展：加 $p$ 坐标，翻倍子问题量换 $O(1)$ 转移。🎥 *Demaine 总结口号*："If you find yourself lacking information to check the desired conditions of the problem, or lack the natural subproblem to recurse on, try subproblem constraint/expansion!"（翻译：如果你发现自己缺少信息来检查问题所需的（约束）条件，或者缺少可以递归的自然子问题，那就试试子问题约束/扩展！） 这条口诀比任何单个算法值钱——DP 设计的真正战场在 Step 1（子问题定义），递推只是验收你选对了没有：选对了，递推自己会「长」出来；选错了，写出递推那一刻你就能感到不对（像 LIS 第一次尝试时 🎥 *Demaine 说的* "This is a very strange recurrence"（翻译：这是个非常奇怪的递推））。下一讲（Lecture 17）把 expansion 推向极致：APSP 子问题扩展到 $O(n^3)$，矩阵链括号化靠增长维度的子问题解决，钢琴演奏也在这框架里。CLRS 路线图：LCS→§15.4，LIS→§15.4 习题，零和博弈 DP→§15 习题；Lecture 17 的 APSP 对应 §25（Floyd-Warshall），矩阵链对应 §15.2。你正在学的 DP 四讲（Lecture 15–18）覆盖 CLRS §14–15 加上 §25，是 6.006 信息密度最高的模块——抓住「子问题设计」这根主轴，三讲内容（Lecture 15 的基础 + Lecture 16 的约束/扩展 + Lecture 17 的极致扩展）都在围绕它转。

| 问题        | 输入形状     | 子问题                                             | 关键设计动作               |
| --------- | -------- | ----------------------------------------------- | -------------------- |
| LCS       | 两个序列     | suffix × suffix 的乘积                             | 多输入取笛卡尔积             |
| LIS       | 单序列      | suffix + 约束「以 $A[i]$ 开头」                        | 加约束换可递归性；原问题对约束取 max |
| Coin game | 单序列（两端删） | substring + 坐标 $p \in \{\text{me},\text{you}\}$ | 扩展状态换 $O(1)$ 转移      |

🎥 *Demaine 的总结口号*："If you find yourself lacking information to check the desired conditions of the problem, or lack the natural subproblem to recurse on, try subproblem constraint/expansion!"（翻译：如果你发现自己缺少信息来检查问题所需的（约束）条件，或者缺少可以递归的自然子问题，那就试试子问题约束/扩展！） *这条经验比任何单个算法都值钱：DP 设计的难点不在写递推，而在选子问题——选对了，递推自己会「长」出来。* 预告：下一讲（Lecture 17）会把 expansion 推到极致（子问题数乘以 $n$ 甚至 $n^2$），你会在那里看到同一个思想如何解决 APSP（全源最短路径）、矩阵链括号化、钢琴演奏等完全不同的问题。对应 CLRS 的路线图：LCS 见 §15.4，LIS 见 §15.4 习题（及 6.006 Recitation 的 $O(n \log n)$ 版本），零和博弈 DP 的思想在 CLRS §15 的习题中也有体现。

---

> <span style="color:#7f8c8d;">MIT OpenCourseWare — 6.006 Introduction to Algorithms, Spring 2020. Lecture 16 讲义翻译版。原文：https://ocw.mit.edu（Terms of Use 见 https://ocw.mit.edu/terms）</span>
