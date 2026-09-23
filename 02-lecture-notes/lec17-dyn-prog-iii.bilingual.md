# Introduction to Algorithms: 6.006

## <span style="color:#2471a3;">**[lecture]**</span> <span style="color:#c0392b">Lecture 17: Dynamic Programming, Part 3 — APSP, Parenthesization, Piano（动态规划第三讲：全源最短路径、括号化、钢琴指法）</span>

Massachusetts Institute of Technology
Instructors: Erik Demaine, Jason Ku, and Justin Solomon

> <span style="color:#7f8c8d;">MIT 6.006 Spring 2020, Lecture 17 讲义（对应视频：Dynamic Programming, Part 3）</span>

---

## <span style="color:#2471a3;">**[section]**</span> <span style="color:#c0392b">Dynamic Programming Steps（SRT BOT 六步法回顾）</span>

本讲是 dynamic programming（动态规划）四讲中的**第三讲**。🎥 *Demaine 开场点明*："We are over halfway through into lecture three of four."（翻译：我们已经过半程，现在是四讲中的第三讲。） *上一讲末尾提到的 subproblem constraints and expansion（子问题约束与扩展）是本讲的主线——上讲的取硬币双人游戏把子问题翻倍（「我先手 / 你先手」两个版本），今天会看到更多这类例子。*

先快速回顾 SRT BOT 框架的六步：

**Step 1: Subproblem definition（子问题定义）**——子问题 $x \in X$：

- 用参数描述子问题的含义
- 通常取输入的 subsets（子集）：sequences（序列）的 prefixes（前缀）、suffixes（后缀）、contiguous substrings（连续子串）
- 对多个输入，常取各子集空间的 product（笛卡尔积）
- 常记录 partial state（部分状态）：通过递增辅助变量来扩展子问题

**Step 2: Relate subproblem solutions recursively（递归关联子问题解）**

```math
x(i) = f(x(j), \ldots) \quad \text{for one or more } j < i
```

- 找出关于子问题解的一个 question（问题）：如果知道它的答案，就能把当前子问题归约为更小的子问题
- 对问题的所有可能答案做 locally brute-force（局部暴力枚举）

**Step 3: Topological order（拓扑序）**——论证递推关系是无环的，子问题构成 DAG（有向无环图）

**Step 4: Base cases（基础情形）**

- 给出所有（可达的）独立子问题的解——递推关系在这些子问题上不再适用

**Step 5: Original problem（原问题）**

- 说明如何从子问题的解计算原问题的解
- 可能要用 parent pointers（父指针）恢复实际方案，而不只是目标函数值

**Step 6: Time analysis（时间分析）**

$\sum_{x \in X} \text{work}(x)$，或若对所有 $x \in X$ 都有 $\text{work}(x) = O(W)$，则总时间为 $|X| \cdot O(W)$

- $\text{work}(x)$ 度量递推中的非递归工作量；递归调用视为 $O(1)$ 时间

### <span style="color:#2471a3;">**[recall]**</span> <span style="color:#c0392b">Recall: DAG Shortest Paths（回顾：DAG 最短路径，L15）</span>

- Subproblems（子问题）：对所有 $v \in V$，求 $\delta(s, v)$
- Relation（递推关系）：

```math
\delta(s, v) = \min\{\delta(s, u) + w(u, v) \mid u \in \text{Adj}^-(v)\} \cup \{\infty\}
```

- Topological order（拓扑序）：$G$ 的拓扑序

> <span style="color:#7f8c8d;">L15（DAG Shortest Paths），见 lec15-recursive-algorithms.bilingual.md</span>

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 本讲是「子问题扩展」专题的总攻：四个例子共用一套动作——给子问题补一个约束/坐标，让递推有东西可递归、有环可断。先放进一张对比表，看清各自的扩展维度与定价：
> 
> | 问题               | 扩展或约束方式              | 扩展倍数/子问题规模    | 复杂度变化                              |
> | ---------------- | -------------------- | ------------- | ---------------------------------- |
> | Bellman-Ford     | 加「最多 $k$ 条边」坐标       | $\times O(V)$ | 单源 $O(VE)$，比 DAG 版多一维              |
> | Floyd–Warshall   | 加「只经 $1..k$ 号顶点」前缀约束 | $\times O(V)$ | 转移降到常数分支，总 $O(V^3)$                |
> | Parenthesization | 加 $\min/\max$ 双值坐标   | $\times 2$    | 子问题 $\times 2$，仍 $O(n^3)$          |
> | Piano Fingering  | 加「起始手指」坐标            | $\times F=5$  | $\Theta(n)\to\Theta(nF^2)$，与音符种数无关 |
> 
> 读表心法：**扩展倍数只要多项式，总时间就仍是多项式**——L16 那句 "as long as it stays a polynomial number, we'll get polynomial time" 在此四连发。🎥 *Demaine*："This gives you a flavor how, with subproblem expansion, I can capture almost any aspect of a problem that I want."（翻译：这让你尝到一点味道——借助子问题扩展，我几乎能捕捉到问题中我想要的任何方面。） 他还补了可操作的判据——🎥 *Demaine*："As long as the number of states that I need to keep track of is small, I can just multiply the number of subproblems by that state."（翻译：只要需要跟踪的状态数很少，我只需把子问题数乘以那个状态数。） 四条路径里最值得盯的是 Floyd–Warshall 的「顶点编号前缀 $1..k$」：它和 L16 的「序列前缀/后缀」子问题是**同一思想在不同载体上的体现**——L16 在序列下标上取前缀（$A[:i]$），本讲在顶点编号上取前缀（编号 $\le k$ 的顶点子集），载体结构不同（线性序 vs 任意编号），但「逐个放行一个元素、转移只多一个分支」的机制完全相同。另外三种各换一个维度：Bellman-Ford 扩**边数**、Parenthesization 扩**取值方向**（min 与 max 两套）、Piano 扩**边界状态**（起始手指）。这说明 subproblem expansion 不是单一招式，而是「缺什么状态就补什么坐标」的元模板——下一节 Guitar 会把它推到元组扩展的极限。

---

## <span style="color:#2471a3;">**[section]**</span> <span style="color:#c0392b">Single-Source Shortest Paths Revisited（重访单源最短路径）</span>

🎥 *Demaine 预告*："Today we'll see a bunch more examples of this idea [subproblem expansion]."（翻译：今天我们会看到这个想法（子问题扩展）的更多例子。）

**1. Subproblems（子问题）**

- **扩展子问题，加入更多信息来使递推无环！**（这是我们已经见过的子问题扩展的一个实例）
- $\delta_k(s, v)$ = 从 $s$ 到 $v$ 最多使用 $k$ 条边的路径的最小权重
- 对所有 $v \in V$ 和 $0 \le k \le |V|$

**2. Relate（递推）**

- 猜测从 $s$ 到 $v$ 最短路径上的最后一条边 $(u, v)$
- $\delta_k(s, v) = \min\{\delta_{k-1}(s, u) + w(u, v) \mid (u, v) \in E\} \cup \{\delta_{k-1}(s, v)\}$

**3. Topological order（拓扑序）**

- 递增 $k$：子问题只依赖 $k$ 严格更小的子问题

**4. Base（基础情形）**

- $\delta_0(s, s) = 0$，且对 $v \ne s$，$\delta_0(s, v) = \infty$（不能走任何边）
- （画子问题图）

**5. Original problem（原问题）**

- 若存在有限最短路径，则 $\delta(s, v) = \delta_{|V|-1}(s, v)$
- 否则某个 $\delta_{|V|}(s, v) < \delta_{|V|-1}(s, v)$，说明路径含 negative-weight cycle（负权环）
- 可记录 parent pointers（父指针）指向使递推取到最小值的子问题

**6. Time（时间）**

- 子问题数量：$|V| \times (|V| + 1)$
- 子问题 $\delta_k(s, v)$ 的工作量：$O(\text{deg}_{\text{in}}(v))$

```math
\sum_{k=0}^{|V|} \sum_{v \in V} O(\text{deg}_{\text{in}}(v)) = \sum_{k=0}^{|V|} O(|E|) = O(|V| \cdot |E|)
```

**这就是 Bellman-Ford 算法！（只是计算顺序略有不同）**

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这个递推就是 **Bellman-Ford 算法**——它示范了本讲第一个可命名模板：**time-expanded layering（分层摊开）**。带环图没法直接跑 DAG 最短路径（环会让拓扑序不存在），于是把图沿「已用边数 $k$」这个坐标复制成 $|V|+1$ 层，第 $k$ 层的子问题只从第 $k-1$ 层取数，环被强制「掰直」成无环图。🎥 *Demaine*："We're taking our graph that's cyclic, and by spreading it out over various copies of k and referencing always the smaller one, we get an acyclic graph."（翻译：我们把带环的图沿着 $k$ 的各份拷贝摊开，并且总是指向更小的那个 $k$，就得到一个无环图。） 你在 L15 学的 DAG 最短路径（CLRS §24.2）是「图本来就无环」，这里则是「加坐标人为造出无环」——这正是 L16 口诀 subproblem expansion 的第一例：把 6.042J 的拓扑排序思想，手动构造到带环图上（沿 $k$ 递增的次序就是一份人为设计的拓扑序）。**一处讲义笔误提示**：递推写的是 $(u,v)\in E$，严格说应枚举 $v$ 的入边 $u\in\text{Adj}^-(v)$（不在图中的 $(u,v)$ 视为 $+\infty$）；正文按讲义原文保留。顺带破一个「名词神话」：🎥 *Demaine*："Mostly because it sounded cool, and he was trying to impress government agencies giving him grants."（翻译：主要是因为它听起来很酷，他想打动给他拨款的政府机构。）——「动态规划」这名字是个营销产物，不描述任何数学结构，别被它唬住；算法的实质就是上面这一层摊开。

---

## <span style="color:#2471a3;">**[section]**</span> <span style="color:#c0392b">All-Pairs Shortest Paths: Floyd–Warshall（全源最短路径：Floyd–Warshall 算法）</span>

- 可以直接沿用 Bellman-Ford 的方式定义子问题 $\delta_k(u, v)$ = 从 $u$ 到 $v$ 最多用 $k$ 条边的最小权重
- 这样运行时间是 Bellman-Ford 的 $|V|$ 倍，即 $O(|V|^2 \cdot |E|) = O(|V|^4)$
- 从 L14 知道更好的算法：Johnson 算法达到 $O(|V|^2 \log |V| + |V| \cdot |E|) = O(|V|^3)$
- 可以用一个简单的 dynamic program（动态规划）达到 $\Theta(|V|^3)$ 的运行时间（稠密图下与 Johnson 持平），这就是 **Floyd–Warshall** 算法
- 给顶点编号，使 $V = \{1, 2, \ldots, |V|\}$

**1. Subproblems（子问题）**

- $d(u, v, k)$ = 从 $u$ 到 $v$ 的、只使用顶点集合 $\{1, 2, \ldots, k\} \cup \{u, v\}$ 中的顶点的路径的最小权重
- 对所有 $u, v \in V$ 和 $1 \le k \le |V|$

**2. Relate（递推）**

```math
x(u, v, k) = \min\{x(u, k, k-1) + x(k, v, k-1), \ x(u, v, k-1)\}
```

- **只有常数个分支！** 不再需要猜测上一条边/上一个顶点

**3. Topological order（拓扑序）**

- 递增 $k$：递推只依赖更小的 $k$

**4. Base（基础情形）**

- $x(u, u, 0) = 0$
- 若 $(u, v) \in E$，则 $x(u, v, 0) = w(u, v)$
- 若以上都不满足，则 $x(u, v, 0) = \infty$

**5. Original problem（原问题）**

- 对所有 $u, v \in V$，求 $x(u, v, |V|)$

**6. Time（时间）**

- $O(|V|^3)$ 个子问题
- 每个 $O(1)$ 工作量
- 总计 $O(|V|^3)$
- 每个子问题依赖数恒为常数，把运行时间里的 $O(|E|)$ 因子降到了 $O(|V|)$

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> Floyd–Warshall 的「神圣灵感」是换一个约束维度：Bellman-Ford 约束**边数**（$\le k$ 条），它约束**中间顶点编号**（只许途经 $\{1,\ldots,k\}$），两个分支正对应「顶点 $k$ 当不当中间点」。🎥 *Demaine*："This is the divine inspiration to define subproblems this way. It's a different constraint than the one we saw here, which was using at most k edges."（翻译：这就是以这种方式定义子问题的神圣灵感。它不同于刚才的约束——刚才用的是「最多 k 条边」。） 可命名的模板是**prefix admission（前缀放行）**：把「前缀」施加到顶点编号上，$1..k$ 是顶点集的一个前缀，从 $k=0$ 到 $|V|$ 逐个「放行」一个顶点当中间点——这与 L16 的前缀子问题一脉相承，只是作用对象从「序列下标」换成「顶点编号」。收益是转移从 Bellman-Ford 的「枚举入边 $O(|E|)$」降到「常数个分支」，总时间从 $O(|V||E|)$ 压到 $O(|V|^3)$。**第一处记号问题**：讲义在 Subproblems 里定义 $d(u,v,k)$，Relate 与 Base 里却写成 $x(u,v,k)$——这里的 $d$ 与 $x$ 是**同一条递推的不同记号，指同一个子问题**（两处都含「中间顶点 $\le k$」这条约束），阅读时不必区分、更不要当成两个变量；这是把「路径权重」习惯记成 $d$、把「通用子问题」习惯记成 $x$ 混写所致，不影响任何结论。对比 Johnson（CLRS §25.3）：先 Bellman-Ford 重赋权、再 $|V|$ 遍 Dijkstra，稀疏图更快；Floyd–Warshall 稠密图 $\Theta(|V|^3)$ 且不在乎负权边。

---

## <span style="color:#2471a3;">**[section]**</span> <span style="color:#c0392b">Arithmetic Parenthesization（算术表达式括号化）</span>

- Input（输入）：算术表达式 $a_0 \ *_1 \ a_1 \ *_2 \ a_2 \ \cdots \ *_{n-1} \ a_{n-1}$，其中每个 $a_i$ 是整数，每个 $*_i \in \{+, \times\}$
- Output（输出）：在何处加括号使表达式求值结果最大
- Example（例子）：$7 + 4 \times 3 + 5 \to ((7) + (4)) \times ((3) + (5)) = 88$
- **允许负整数！**
- Example（例子）：$7 + (-4) \times 3 + (-5) \to ((7) + ((-4) \times ((3) + (-5)))) = 15$

**1. Subproblems（子问题）**

- 只对每个子数组求最大值够吗？**不够！** $(-3) \times (-3) = 9 > (-2) \times (-2) = 4$
- $x(i, j, \text{opt})$ = 对 $a_i *_{i+1} \cdots *_{j-1} a_{j-1}$ 加括号所能得到的 opt（最优）值
- 对所有 $0 \le i < j \le n$ 和 $\text{opt} \in \{\min, \max\}$

**2. Relate（递推）**

- 猜测最外层括号的位置 / 最后一步被计算的运算
- $x(i, j, \text{opt}) = \text{opt}\{x(i, k, \text{opt}') \ *_k \ x(k, j, \text{opt}'') \mid i < k < j;\ \text{opt}', \text{opt}'' \in \{\min, \max\}\}$

**3. Topological order（拓扑序）**

- 递增 $j - i$：子问题 $x(i, j, \text{opt})$ 只依赖 $j - i$ 严格更小的子问题

**4. Base（基础情形）**

- $x(i, i+1, \text{opt}) = a_i$：只有一个数，没有运算了！

**5. Original problem（原问题）**

- $X(0, n, \max)$（讲义此处大写 $X$ 与递推的小写 $x$ 是同一子问题的记号混用，同 Floyd–Warshall 一节的 $d/x$，见下注）
- 存储 parent pointers（父指针）**两个**，以找出括号化方案（它构成一棵 binary tree（二叉树）！）

**6. Time（时间）**

- 子问题数量：少于 $n \cdot n \cdot 2 = O(n^2)$
- 每个子问题工作量 $O(n) \cdot 2 \cdot 2 = O(n)$
- 运行时间 $O(n^3)$

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 为什么必须同时求 min 和 max？因为乘法在负数上会「翻转」大小顺序：max 的转移里可能出现「两个很小的负数相乘」。🎥 *Demaine*："Because sometimes you want to take two very small negative numbers and product them together to get a larger positive number."（翻译：因为有时你想把两个非常小的负数乘在一起，得到一个更大的正数。） 具体机制：$x(i,j,\max)$ 的四个候选里，$\min\times\min$ 与 $\max\times\max$ 谁更大并不确定——两个负数相乘得正数，负得越「小」（绝对值越大）积反而越大，所以 max 也必须看向 min 分支。于是每个子问题维护 $(\min,\max)$ 对、转移穷举四种组合——可命名模板**min/max dual maintenance（双值扩展）**：目标只要 max，却因运算会反序而必须连带维护 min。这个现象在你正在学的实分析（100B, Thomson TBB）里是严格命题：$\mathbb{R}$ 是有序域，$a\le b$ 且 $c\ge 0$ 蕴含 $ac\le bc$，$c<0$ 时方向反转——「负负得正」只是它在整数上的实例。对照 CLRS §15.2 matrix-chain multiplication：递归骨架（猜最后一个切分点、区间子问题、$O(n^3)$）完全同构，但矩阵乘法不反序、只需单值，故 §15.2 是本题的「无符号」简化版；而区间 DP 的子问题形状（所有 $(i,j)$ 区间 + 猜切分点）又与 L16 硬币游戏同源。

---

## <span style="color:#2471a3;">**[section]**</span> <span style="color:#c0392b">Piano Fingering（钢琴指法）</span>

- 给定 $t_0, t_1, \ldots, t_{n-1}$ 共 $n$ 个要依次用右手弹奏的单音（以后会推广到多音、双手）
- 演奏者右手有手指 $1, 2, \ldots, F$（对多数人 $F = 5$）
- 给定难度度量 $d(t, f, t', f')$：从「音符 $t$ 用指法 $f$」过渡到「音符 $t'$ 用指法 $f'$」的难度
  - 通常是对各种困难项的罚分之和，例如：
  - $1 < f < f'$ 且 $t > t'$：不舒服（下一手指编号更大、手向高音侧移动，却要弹更低的音——手指走向与音高走向相反，需交叉手腕）
  - Legato（连奏，平滑弹奏）要求 $t \ne t'$（否则罚分为无穷）
  - Weak-finger rule（弱指规则）：尽量避免 $f' \in \{4, 5\}$（无名指、小指弱）
  - $\{f, f'\} = \{3, 4\}$：烦人（中指与无名指之间的过渡）
- Goal（目标）：给每个音符分配指法，使总难度最小

**First attempt（第一次尝试）：**

1. Subproblems（子问题）
   - $x(i)$ = 弹奏音符 $t_i, t_{i+1}, \ldots, t_{n-1}$ 的最小总难度
2. Relate（递推）
   - 猜测第一个手指：给 $t_i$ 分配指法 $f$
   - $x(i) = \min\{x(i+1) + d(t_i, f, t_{i+1}, ?) \mid 1 \le f \le F\}$
   - **信息不足，填不了 $?$**：需要知道 $x(i+1)$ 开头用的是哪个手指
   - 不同的起始手指对 $x(i+1)$ 和 $d(t_i, f, t_{i+1}, ?)$ 的影响可能好坏参半
   - 需要一张表，把「起始手指」映射到 $x(i+1)$ 的最优解
   - 即：需要用 start condition（起始条件）扩展子问题

> <span style="color:#7f8c8d;">「信息不足 → 扩展子问题」正是 L16 结尾口诀的现场演绎（节选）：If you lack the natural subproblem to recurse on, try subproblem constraint/expansion!（若缺少可递归的自然子问题，试试子问题约束/扩展！）</span>

**Solution（解法）：**

1. Subproblems（子问题）
   - $x(i, f)$ = 从「音符 $t_i$ 用指法 $f$」开始，弹奏音符 $t_i, t_{i+1}, \ldots, t_{n-1}$ 的最小总难度
   - 对所有 $0 \le i < n$ 和 $1 \le f \le F$
2. Relate（递推）
   - 猜测下一个手指：给 $t_{i+1}$ 分配指法 $f'$
   - $x(i, f) = \min\{x(i+1, f') + d(t_i, f, t_{i+1}, f') \mid 1 \le f' \le F\}$
3. Topological order（拓扑序）
   - 递减 $i$（$f$ 任意顺序）
4. Base（基础情形）
   - $x(n-1, f) = 0$（没有后续过渡）
5. Original problem（原问题）
   - $\min\{x(0, f) \mid 1 \le f \le F\}$
6. Time（时间）
   - $\Theta(n \cdot F)$ 个子问题
   - 每个子问题 $\Theta(F)$ 工作量
   - 总计 $\Theta(n \cdot F^2)$
   - **与音符种类数无关！**

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 第一次尝试失败的根因是「少了一个坐标」：$x(i)$ 只存后缀最优值，转移到 $x(i+1)$ 时却需要未知边界状态「下一段起始手指」来算 $d$。本质是 $x(i+1)$ 是多个「带不同起始手指」的最优值取 $\min$ 之后的**坍缩**——一旦取 min，起始手指信息就被不可逆地丢弃，而难度函数 $d$ 又依赖它。这与 L16 里 LIS 第一次失败的「归纳假设不够强」是同一症状。修法是把这个边界状态升格为子问题坐标 $x(i,f)$——可命名模板**state completion（坐标补全）**：转移缺什么状态，就把什么状态补成坐标。🎥 *Demaine*："So we're going to multiply the number of subproblems by capital F, which is just 5, so a very small subproblem expansion."（翻译：所以我们要把子问题数量乘以大写 $F$，也就是 5，这是非常小的子问题扩展。） 扩展倍数 $F=5$ 小到可忽略，子问题从 $\Theta(n)$ 到 $\Theta(nF)$，几乎免费。注意递推「猜下一个手指 $f'$」而非「猜当前手指」——当前手指 $f$ 已钉进坐标里，只剩一个自由选择。这与 6.042J 的「加强归纳假设」同构：假设不够强就证明更强命题（多带一个不变量）；而最后 $\min\{x(0,f)\}$ 把 $f$ 解绑——正是 L16 那句「递推需要约束，原问题负责解绑」。

---

## <span style="color:#2471a3;">**[section]**</span> <span style="color:#c0392b">Guitar Fingering（吉他指法）</span>

- 同一个音符最多有 $S$ 种弹法（$S$ 为琴弦数）
- 把「finger（手指）」重新定义为 tuple（元组）「(弹该音符的手指, 弹该音符的弦)」
- 整个算法中，$F$ 被替换为 $F \cdot S$
- 运行时间因此为 $\Theta(n \cdot F^2 \cdot S^2)$

## <span style="color:#2471a3;">**[section]**</span> <span style="color:#c0392b">Multiple Notes at Once（同时多个音符）</span>

- 现在假设 $t_i$ 是时刻 $i$ 要同时弹奏的一组音符
- 给定更大的过渡难度函数 $d(t, f, t', f')$
- Goal（目标）：找一个指法指派 $f_i : t_i \to \{1, 2, \ldots, F\}$（指定每个音符用哪个手指，吉他还包括哪根弦），使得

```math
\sum_{i=1}^{n-1} d(t_{i-1}, f_{i-1}, t_i, f_i)
```

最小

- 每个指法 $f_i$ 至多有 $T^F$ 种选择，其中 $T = \max_i |t_i|$
  - 对普通钢琴 $T \le F = 10$（但存在例外）
  - 对吉他 $T \le S$
- $\Theta(n \cdot T^F)$ 个子问题
- 每个子问题 $\Theta(T^F)$ 工作量
- 总计 $\Theta(n \cdot T^{2F})$ 时间
- 当 $T, F \le 10$ 时为 $\Theta(n)$ 时间

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 吉他一步把「手指」坐标扩成元组（手指, 弦），$F$ 整体替换为 $F\cdot S$——可命名模板**tuple expansion（元组扩展）**：一个坐标不够，就打包成多个属性的笛卡尔积，与 L16 LCS 的「多输入笛卡尔积」同招，只是作用对象换成「同一状态的多个属性」。但「同时多音符」暴露代价天花板。先说组合数：$t_i$ 有 $T$ 个音符，每个音符独立从 $F$ 个手指里选一个，乘法原理给 $F\times\cdots\times F=F^T$ 种指派。🎥 *Demaine*："And so this is 10 to the 10. It's a big constant, but it's constant, like a billion, 10 billion."（翻译：所以这是 $10^{10}$，即 100 亿。它是很大的常数，但终究是常数——大概 10 亿、100 亿这个量级。） **第二处记号问题**：讲义与 Demaine 都写 $T^F$，但正确应为 $F^T$（底数 $F$、指数 $T$）：「每指至多一键」恒有 $T \le F$，而最坏情形分析取 $T=F$，此时 $T^F = F^F = F^T$ 数值恰好相等，结论不变；当 $T < F$ 时两者不同，但差异只是常数因子，$\Theta$ 记号下的结论同样不受影响——阅读时一律按正确的 $F^T$ 理解。**另一个口径提示**：正文此处的 $F = 10$ 是双手十指口径（T 为同时音符数，每指至多一键），与前面 Piano Fingering 节「右手单手 $F=5$」的设定不同——讲义在两节之间切换了手指数口径，阅读时注意区分。按 SRT BOT Step 6 定价：子问题 $\Theta(nF^T)$、每个枚举 $\Theta(F^T)$ 后继，总价 $\Theta(nF^{2T})$——注意这是**时间复杂度**，DP 实际存储空间为 $\Theta(F^T)$（每层状态，可滚动复用）；它换掉的是对 $n$ 的指数枚举（暴力枚举全部指法序列有 $\prod_i F^{T_i} = F^{\sum_i T_i}$ 条），而对 $T$ 的指数 $F^{2T}$ 仍须钉死为常数。$T,F$ 钉成常数后总时间线性，但 $T$ 每加 1 状态数乘 $F$，指数藏在音符数里。心法：**子问题每扩一维，先问它是否让状态数指数化——多项式维放心扩，指数维必须钉成常数**。

## <span style="color:#2471a3;">**[section]**</span> <span style="color:#c0392b">Video Game Applications（电子游戏应用）</span>

- **Guitar Hero / Rock Band（吉他英雄 / 摇滚乐队）**
  - $F = 4$（通常只用 4 根手指，对应 5 种不同音符/按键）
- **Dance Dance Revolution（劲舞革命，跳舞机）**
  - $F = 2$（两只脚）
  - $T = 2$（同时至多两个音符）
  - Exercise（练习）：处理持续音符——把「每只脚的位置」（在箭头上还是中间）作为后缀子问题的附加状态

---

> <span style="color:#7f8c8d;">MIT OpenCourseWare — 6.006 Introduction to Algorithms, Spring 2020. Lecture 17 讲义翻译版。原文：https://ocw.mit.edu（Terms of Use 见 https://ocw.mit.edu/terms）</span>
