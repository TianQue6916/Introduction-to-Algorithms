# Introduction to Algorithms: 6.006

## <span style="color:#2471a3;">**[lecture]**</span> <span style="color:#c0392b">Lecture 20: Course Review（课程总复习）</span>

Massachusetts Institute of Technology
Instructors: Erik Demaine, Jason Ku, and Justin Solomon

> <span style="color:#7f8c8d;">MIT 6.006 Spring 2020, Lecture 20 译注（对应视频：Course Review）</span>

> 本讲义为中英行内双语译注，正文以中文为主，英文术语首次出现时标注 `English（中文）`，之后直接用 `English`。本讲是课程收官的复习课，无新算法与伪代码，重点在于把一学期的知识串成一张「如何解决算法问题」的方法论地图，并给出后续课程路线。核心概念首次出现时均给出英文原名 + 中文 + 一句可判定定义。

---

## Course Goals（课程目标）

6.006 这门课要解决三件事，并且要能「对人或对计算机」都表达清楚：

1. **Solve hard computational problems（求解困难的（hard）计算问题）**——输入规模不是常数（non-constant-sized inputs），会随问题变大。
2. **Argue an algorithm is correct（论证算法正确）**——手段是 **Induction（归纳法）** 与 **Recursion（递归）**。
3. **Argue an algorithm is “good”（论证算法「好」）**——手段是 **Asymptotics（渐近分析）** 与 **Model of Computation（计算模型）**。

> 判定口径：所谓「正确」= 对**所有**合法输入都终止并输出正确答案（用归纳法证明）；所谓「好」= 运行时间/空间在某个计算模型下的渐近增长可接受。

---

## Do there always exist “good” algorithms?（「好」算法总是存在吗？）

- **Most problems are not solvable efficiently（大多数问题不能高效求解）**，但我们关心的很多问题其实可以！
- 复杂度术语的准确定义（这组是本节的核心，逐一定义）：
  - **Polynomial（多项式）**：指「在**输入规模**（size of input）上是多项式的」。
  - **Pseudopolynomial（伪多项式）**：指「在输入规模**和输入中数值的大小**上都是多项式的」——比 polynomial 更强，因为数值的大小可以是输入位长的指数级。
  - **NP（Nondeterministic Polynomial time，非确定性多项式时间）**：解**可被多项式时间检验**的问题类，即给定一个 certificate（证书/解），能在多项式时间内判定它是否合法。
  - **NP-hard（NP 困难）**：这样一类问题——**任何** NP 中的问题都能在多项式时间内归约（reduce）到它；它是「至少和 NP 一样难」的问题集合。
  - **NP-complete（NP 完全）**：**NP-hard 与 NP 的交集**，即「既是 NP 又 NP-hard」的问题集合，是 NP 中最难的那批。

> 一句话串起来：**polynomial** 看的是「输入位长」上的多项式；**pseudopolynomial** 额外要求「数值大小」上也是多项式；**NP** 是「证书可快速验证」；**NP-hard** 是「能解所有 NP 问题」；**NP-complete** 是两者的交集。

---

## How to solve an algorithms problem?（如何解决一道算法题？）

两条总路线，本讲把它们各自拆开：

### 路线一：Reduce to a problem you know how to solve（归约到已知会解的问题）

把新问题**reduce（归约）**到已经掌握的标准问题上去。这门课覆盖的标准问题分两大块：

**1. Search / Sort（查找与排序，对应 Problem Set Q1）**

- **Search（查找）**分两类数据结构：
  - **Extrinsic（外部的，指基于「序列」的查找）**：在**Sequence（序列）**上做查找，关心的是元素的位置顺序。
  - **Intrinsic（内在的，指基于「集合」的查找）**：在 **Set（集合）** 上做查找，只关心「是否在集合里」，不关心顺序。
- **Sort（排序）**涉及三个概念：
  - **Comparison Model（比较模型）**：仅靠两两比较（compare）来排序的模型，下界为 $\Omega(n\log n)$ 次比较。
  - **Stability（稳定性）**：排序后，键值相等的元素仍保持它们原来的相对次序。
  - **In-place（原地）**：排序只用 $O(1)$ 额外空间。

**2. Graphs（图，对应 Problem Set Q2）**

- **Reachability（可达性）**：从一个顶点能否到达另一个顶点。
- **Connected Components（连通分量）**：无向图中互相可达的顶点构成的极大集合。
- **Cycle Detection（环检测）**：判断图中是否存在环。
- **Topological Sort（拓扑排序）**：对有向无环图（DAG）给顶点排一个线性序，使所有边都从较前的顶点指向较后的顶点。
- **Shortest Paths（最短路径）**两个变体：
  - **Single-Source Shortest Paths（单源最短路径，SSSP）**：从一个源点 $s$ 到所有其他顶点的最短路径。
  - **All-Pairs Shortest Paths（全源最短路径，APSP）**：所有顶点对之间的最短路径。

### 路线二：Design a new recursive algorithm（设计新的递归算法）

当无法直接归约时，自己设计算法，用到的设计范式（paradigm）：

- **Brute Force（暴力枚举）**：穷举所有候选解。
- **Divide & Conquer（分治）**：把问题递归地拆成几个子问题，分别解后合并。
- **Dynamic Programming（动态规划，DP）**：把问题拆成**有重叠**的子问题，缓存子问题结果避免重复计算（对应 Problem Set Q3）。
- **Greedy / Incremental（贪心 / 增量式）**：每步做局部最优选择，逐步构造解。

---

## Next Steps（后续课程）

### (U) 6.046: Design & Analysis of Algorithms（算法设计与分析，本科）

6.046 是 6.006 的直接延伸（extension）：

- **Data Structures（数据结构）**：Union-Find（并查集）、Amortization via potential analysis（势能法摊还分析）
- **Graphs（图）**：Minimum Spanning Trees（最小生成树，MST）、Network Flows / Cuts（网络流 / 割）
- **Algorithm Design Paradigms（算法设计范式）**：Divide & Conquer、Dynamic Programming、Greedy
- **Complexity（复杂性）**：Reductions（归约）

### Relax the Problem（放松问题定义）

换一种方式看待「正确 / 高效」，就能得到更多算法：

- **Randomized Algorithms（随机化算法）**：
  - 6.006 基本都是 **deterministic（确定性的）** 算法（hashing 除外，哈希本身依赖随机化）。
  - **Las Vegas（拉斯维加斯算法）**：**总是正确**，但运行时间**可能较慢**（以概率保证快，如 hashing）。
  - **Monte Carlo（蒙特卡洛算法）**：**总是快**，但结果**可能不正确**（以概率保证正确）。
  - 在结构化数据上，随机化通常能得到更快的算法。
- **Numerical Algorithms / Continuous Optimization（数值算法 / 连续优化）**：
  - 6.006 只处理**整数**。
  - 数值算法要**近似实数**：用时间换精度（pay time for precision）。
- **Approximation Algorithms（近似算法）**：
  - 输入是一个**优化问题**（在带权输出上求 min/max）。
  - 许多优化问题都是 NP-hard，求不到最优解。
  - 于是问：在多项式时间内，能**多接近最优解**？

### Change the Model of Computation（改变计算模型）

换掉「RAM 模型」这个默认假设：

- **Cache Models（缓存模型）**：考虑内存层级（memory hierarchy）的代价模型。
- **Quantum Computer（量子计算机）**：利用量子特性来加速。
- **Parallel Processors（并行处理器）**：用多个 CPU 而不是一个：
  - **Multicore（多核）**：大共享内存。
  - **Distributed cores（分布式核心）**：message passing（消息传递）。

---

## Future Courses（后续课程路线）

按「模型 / 应用」两类列出的进阶课程：

**Model（模型向）**

- **Computation / Complexity（计算 / 复杂性理论）**：6.045、6.840、6.841
- **Randomness（随机性）**：6.842
- **Quantum（量子计算）**：6.845
- **Distributed / message passing（分布式 / 消息传递）**：6.852
- **Multicore / shared memory（多核 / 共享内存）**：6.816、6.846
- **Constant Factors / Performance（常数因子 / 性能工程）**：6.172

**Application（应用向）**

- **Biology（生物信息）**：6.047
- **Game Theory（博弈论）**：6.853
- **Cryptography（密码学）**：6.875
- **Vision（计算机视觉）**：6.819
- **Graphics（图形学）**：6.837
- **Graph and Matrix（图与矩阵）**：6.890
- **Geometry（计算几何）**：6.850
- **Folding（折纸 / 折叠几何）**：6.849

---

### 参考

MIT OpenCourseWare, 6.006 Introduction to Algorithms, Spring 2020 — https://ocw.mit.edu/terms
