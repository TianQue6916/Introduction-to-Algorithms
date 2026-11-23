# Lecture 15: Recursive Algorithms（递归算法）

> Introduction to Algorithms: 6.006，Massachusetts Institute of Technology
> Instructors: Erik Demaine, Jason Ku, and Justin Solomon

---

## How to Solve an Algorithms Problem (Review)（如何求解算法问题：回顾）

- Reduce（归约）到你已经会的问题（使用某个 data structure 或 algorithm）。

| Search Data Structures（查找数据结构） | Sort Algorithms（排序算法） | Graph Algorithms（图算法） |
|---|---|---|
| Array | Insertion Sort | Breadth First Search |
| Linked List | Selection Sort | DAG Relaxation (DFS + Topo) |
| Dynamic Array | Merge Sort | Dijkstra |
| Sorted Array | Counting Sort | Bellman-Ford |
| Direct-Access Array | Radix Sort | Johnson |
| Hash Table | AVL Sort | |
| AVL Tree | Heap Sort | |
| Binary Heap | | |

- 自己设计 recursive algorithm（递归算法）：
  - 用 constant-sized（常数规模）的 program 求解任意 input。
  - 因此需要 looping 或 recursion，并用 induction（归纳）来分析。
  - Recursive function call（递归函数调用）：把它看成一个 graph，若 $B$ 调用 $A$，就连一条 $A \to B$ 的 directed edge。
  - 递归调用的 dependency graph（依赖图）必须无环（如果程序能够 terminate 的话）。
  - 按 graph 的形状分类：

| Class（类别） | Graph（图） |
|---|---|
| Brute Force | Star（星形） |
| Decrease & Conquer | Chain（链） |
| Divide & Conquer | Tree（树） |
| Dynamic Programming | DAG |
| Greedy / Incremental | Subgraph（子图） |

  - 困难之处在于：用 inductive 的方式思考，构造出作用于 subproblems（子问题）的 recurrence（递推式）。
  - 如何递归地求解一个问题（SRT BOT）：
    1. Subproblem definition（子问题定义）。
    2. Relate subproblem solutions recursively（递归地关联子问题的解）。
    3. Topological order on subproblems（子问题上的拓扑序，$\Rightarrow$ subproblem DAG）。
    4. Base cases of relation（递推关系的基础情形）。
    5. Original problem solution via subproblem(s)（由子问题的解得到原问题的解）。
    6. Time analysis（时间分析）。

## Merge Sort in SRT BOT Framework（SRT BOT 框架下的归并排序）

- 对含 $n$ 个 elements 的 array $A$ 做 merge sort，可在 SRT BOT 中表述如下：
  - Subproblems：$S(i, j)$ 表示 $A[i:j]$ 上 elements 排序后的 array，其中 $0 \le i \le j \le n$。
  - Relation：

```math
S(i, j) = \text{merge}(S(i, m), S(m, j)) \quad \text{where } m = \lfloor (i + j)/2 \rfloor
```

  - Topo. order：按 $j - i$ 递增。
  - Base cases：$S(i, i + 1) = [A[i]]$。
  - Original：$S(0, n)$。
  - Time：$T(n) = 2T(n/2) + O(n) = O(n \lg n)$。
- 在此情形下，subproblem DAG 是一棵树（divide & conquer）。

## Fibonacci Numbers（斐波那契数）

- 假设要计算第 $n$ 个 Fibonacci number $F_n$。
- Subproblems：$F(i)$ 表示第 $i$ 个 Fibonacci number $F_i$，其中 $i \in \{0, 1, \dots, n\}$。
- Relation：$F(i) = F(i - 1) + F(i - 2)$（这正是 Fibonacci numbers 的定义）。
- Topo. order：按 $i$ 递增。
- Base cases：$F(0) = 0$，$F(1) = 1$。
- Original prob.：$F(n)$。

```python
def fib(n):
    if n < 2: return n            # base case
    return fib(n - 1) + fib(n - 2)  # recurrence
```

- Divide and conquer 意味着一个递归调用的 tree（画出这棵树）。
- Time：$T(n) = T(n - 1) + T(n - 2) + O(1) > 2T(n - 2)$，故 $T(n) = \Omega(2^{n/2})$，是指数级的……:(
- Subproblem $F(k)$ 被计算了不止一次！（共 $F(n - k)$ 次。）
- 能不能避免这种浪费？

## Re-using Subproblem Solutions（复用子问题的解）

- 把 subproblem dependencies 画成一个 DAG。
- 求解方式二选一：
  - Top down（自顶向下）：把 subproblem solutions 记在 memo（备忘录）里并复用（recursion + memoization）。
  - Bottom up（自底向上）：按 topological sort order（拓扑排序序）求解 subproblems。
- 对 Fibonacci 而言，有 $n + 1$ 个 subproblems和少于 $2n$ 个 dependencies（edges）。
- 于是计算时间为 $O(n)$ 次 additions。

```python
# recursive solution (top down)
def fib(n):
    memo = {}
    def F(i):
        if i < 2: return i                     # base cases
        if i not in memo:                      # check memo
            memo[i] = F(i - 1) + F(i - 2)      # relation
        return memo[i]
    return F(n)                                # original
```

```python
# iterative solution (bottom up)
def fib(n):
    F = {}
    F[0], F[1] = 0, 1                          # base cases
    for i in range(2, n + 1):                  # topological order
        F[i] = F[i - 1] + F[i - 2]             # relation
    return F[n]                                # original
```

- 一个 subtlety（微妙之处）：Fibonacci numbers 会长到 $\Theta(n)$ bits 长，可能远大于 word size $w$。
- 每次 addition 花费 $O(\lceil n/w \rceil)$ 时间。
- 所以总代价为 $O(n \lceil n/w \rceil) = O(n + n^2/w)$ 时间。

## Dynamic Programming（动态规划）

- 这个奇怪的名字是 Richard Bellman 造的。
  - 他想要政府 funding（经费），需要一个酷名字来掩饰自己其实在做数学！:)
  - 字面意思：更新（dynamic）一个 plan 或 schedule（program）。
- 存在 recursive solution 意味着 subproblems 是可分解的（这条性质常称为 optimal substructure，最优子结构；它是 recursion 的性质，不只属于 dynamic programming）。
- Recursive algorithm 意味着一个 computation（计算）的 graph。
- 若 subproblem dependencies 有 overlap（重叠，即 DAG 中 in-degree $> 1$），就是 dynamic programming。
- “Recurse but re-use”（递归但复用）：top down，记录并查表取 subproblem solutions。
- “Careful brute force”（小心的暴力）：bottom up，按顺序做每个 subproblem。
- 常用于 counting（计数）/ optimization（优化）问题：这类问题的 recurrences 几乎自动就是正确的。

## How to Solve a Problem Recursively (SRT BOT)（如何递归求解问题）

1. Subproblem definition：subproblem $x \in X$。
   - 用文字、以 parameters（参数）的形式描述一个 subproblem 的含义。
   - 常常取 input 的 subsets：序列的 prefixes（前缀）、suffixes（后缀）、contiguous substrings（连续子串）。
   - 常常记录 partial state（部分状态）：通过递增某些 auxiliary variables（辅助变量）来增加 subproblems。
2. Relate subproblem solutions recursively：$x(i) = f(x(j), \dots)$，其中 $j < i$（可有一个或多个）。
3. Topological order：用它论证 relation 无环、且 subproblems 构成 DAG。
4. Base cases（基础情形）：
   - 对所有（可达的）独立 subproblems 给出解，即 relation 失效（break down）的地方。
5. Original problem（原问题）：
   - 说明如何由 subproblem(s) 的解算出 original problem 的解。
   - 可能要用 parent pointers（父指针）还原出真正的 solution，而不仅仅得到 objective function（目标函数）的值。
6. Time analysis：
   - 总时间为 $\sum_{x \in X} \text{work}(x)$；若对所有 $x \in X$ 都有 $\text{work}(x) = O(W)$，则为 $|X| \cdot O(W)$。
   - $\text{work}(x)$ 度量 relation 中的 nonrecursive work（非递归工作）；把 recursions 视为花费 $O(1)$ 时间。

## DAG Shortest Paths（DAG 最短路径）

- 回顾 DAG SSSP problem：给定 DAG $G$ 与 vertex $s$，对所有 $v \in V$ 计算 $\delta(s, v)$。
- Subproblems：所有 $v \in V$ 的 $\delta(s, v)$。
- Relation：

```math
\delta(s, v) = \min\bigl(\{\delta(s, u) + w(u, v) \mid u \in Adj^-(v)\} \cup \{\infty\}\bigr)
```

- Topo. order：$G$ 的 topological order。
- Base cases：$\delta(s, s) = 0$。
- Original：所有 subproblems。
- Time：

```math
\sum_{v \in V} O\bigl(1 + |Adj^-(v)|\bigr) = O(|V| + |E|)
```

- DAG Relaxation 与这个 dynamic program 算出同样的 min 值，只是：
  - 它是 step-by-step 地做（若新值 $<$ min，就通过 edge relaxation 更新 min），并且
  - 它站在 $u$ 与 $Adj^+(u)$ 的视角，而不是 $v$ 与 $Adj^-(v)$ 的视角。

## Bowling（保龄球）

- 给定 $n$ 个 pins（瓶），标号 $0, 1, \dots, n - 1$。
- Pin $i$ 的 value（价值）为 $v_i$。
- 一个与 pin 尺寸相近的 ball 可以击中：
  - 1 个 pin $i$，此时得到 $v_i$ 分；
  - 2 个相邻的 pins $i$ 与 $i + 1$，此时得到 $v_i \cdot v_{i+1}$ 分。
- 一个 pin 一旦被击中，就不能再被击中（已 removed）。
- 问题：投出零个或更多 ball，使总 points 最大。
- 例子：$[-1, 1, 1, 1, 9, 9, 3, -3, -5, 2, 2]$。

## Bowling Algorithms（保龄球算法）

- 先从一个更熟悉的 divide-and-conquer algorithm 入手：
  - Subproblems：$B(i, j)$ 表示只考虑 pins $i, i + 1, \dots, j - 1$ 时的最大 score，其中 $0 \le i \le j \le n$。
  - Relation：
    - $m = \lfloor (i + j)/2 \rfloor$。
    - 要么把 $m$ 与 $m + 1$ 一起击中，要么不。

```math
B(i, j) = \max\bigl\{v_m \cdot v_{m+1} + B(i, m) + B(m + 2, j),\ B(i, m + 1) + B(m + 1, j)\bigr\}
```

  - Topo. order：按 $j - i$ 递增。
  - Base cases：$B(i, i) = 0$，$B(i, i + 1) = \max\{v_i, 0\}$。
  - Original：$B(0, n)$。
  - Time：$T(n) = 4T(n/2) + O(1) = O(n^2)$。
- 这个 algorithm 能work，但不够快，也不好推广（例如推广到允许更大的 ball 一次击中三个 pins）。
- Dynamic programming algorithm：改用 suffixes。
  - Subproblems：$B(i)$ 表示只考虑 pins $i, i + 1, \dots, n - 1$ 时的最大 score，其中 $0 \le i \le n$。
  - Relation：
    - 对第一个 pin（原来的 pin $i$）可能发生的事做 local brute-force：跳过该 pin、击中一个 pin、击中两个 pins。
    - 归约到更短的 suffix 并 recurse，即 $B(i + 1)$ 或 $B(i + 2)$。
    - $B(i) = \max\{B(i + 1),\ v_i + B(i + 1),\ v_i \cdot v_{i+1} + B(i + 2)\}$。
  - Topo. order：按 $i$ 递减（$i = n, n - 1, \dots, 0$）。
  - Base cases：$B(n) = B(n + 1) = 0$。
  - Original：$B(0)$。
  - Time（假设使用 memoization）：
    - $\Theta(n)$ 个 subproblems $\times$ 每个 $\Theta(1)$ work。
    - 总时间 $\Theta(n)$。
- 又快又容易推广！
- 它等价于 subproblem DAG 中的 maximum-weight path（最大权路径）：

[Figure 1：subproblem DAG，vertices 为 $B_0, B_1, B_2, B_3, \dots, B_n$；每个 $B_i$ 有一条 weight 为 $\max\{v_i, 0\}$ 的 edge 指向 $B_{i+1}$，另有一条 weight 为 $v_i \cdot v_{i+1}$ 的 edge 指向 $B_{i+2}$；求从 $B_0$ 到 $B_n$ 的 maximum-weight path。]

## Bowling Code（保龄球代码）

- 把 SRT BOT 规格翻译成 code 是自动的、直截了当的。
- 上面 Bowling Dynamic Program 的结果如下：

```python
# recursive solution (top down)
def bowl(v):
    memo = {}
    def B(i):
        if i >= len(v): return 0                    # base cases
        if i not in memo:                           # check memo
            memo[i] = max(B(i+1),                    # relation: skip pin i
                          v[i] + B(i+1),             # OR bowl pin i separately
                          v[i] * v[i+1] + B(i+2))    # OR bowl pins i and i+1 together
        return memo[i]
    return B(0)                                     # original
```

```python
# iterative solution (bottom up)
def bowl(v):
    B = {}
    B[len(v)] = 0                                   # base cases
    B[len(v)+1] = 0
    for i in reversed(range(len(v))):               # topological order
        B[i] = max(B[i+1],                          # relation: skip pin i
                   v[i] + B[i+1],                   # OR bowl pin i separately
                   v[i] * v[i+1] + B[i+2])          # OR bowl pins i and i+1 together
    return B[0]                                     # original
```

## How to Relate Subproblem Solutions（如何关联子问题的解）

- 我们用来在 subproblem solutions 上定义 relation 的 general approach：
  - 找出一个关于 subproblem solution 的问题：只要知道这个问题的答案，就能把问题 reduce 到「更小的」subproblem(s)。
    - 在 bowling 的情形，这个问题是「开头的那两个 pins 我们怎么打？」
  - 然后对这个问题做 local brute-force：试遍所有可能的答案，取其中最好的。
    - 在 bowling 的情形，因为问题要求 maximize，所以取 max。
  - 另一种理解：把这看成「正确地猜出」该问题的答案并直接 recurse；但在实现上我们确实会检查所有可能的猜测，然后返回「最好」的那个。
- 效率的关键在于：这个问题的可能答案数量要小（polynomial 级），这样 brute forcing 才不会太贵。
- 计算 relation 时的 nonrecursive work 常常（但并非总是）等于我们尝试的答案个数。
