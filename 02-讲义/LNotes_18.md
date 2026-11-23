# Lecture 18: Pseudopolynomial（伪多项式）

> Introduction to Algorithms: 6.006，Massachusetts Institute of Technology
> Instructors: Erik Demaine, Jason Ku, and Justin Solomon

---

## Dynamic Programming Steps (SRT BOT)（动态规划步骤）

1. Subproblem definition：subproblem $x \in X$。
   - 用文字、以 parameters 的形式描述一个 subproblem 的含义。
   - 常常取 input 的 subsets：序列的 prefixes、suffixes、contiguous substrings。
   - 常常把多个 input 上的可能 subsets 相乘。
   - 常常记录 partial state：通过递增某些 auxiliary variables 来增加 subproblems。
   - 常常取比给定 integer 更小的 integers（今天的重点）。
2. Relate subproblem solutions recursively：$x(i) = f(x(j), \dots)$，其中 $j < i$（可有一个或多个）。
   - 找出一个关于 subproblem solution 的问题：只要知道它的答案，就能把该 subproblem reduce 到更小的 subproblem(s)。
   - 对该问题的所有可能答案做 local brute-force。
3. Topological order：论证 relation 无环、subproblems 构成 DAG。
4. Base cases：
   - 对所有（可达的）独立 subproblems 给出解，即 relation 失效处。
5. Original problem：
   - 说明如何由 subproblem(s) 的解算出 original problem 的解。
   - 可能要用 parent pointers 还原真正的 solution，而不仅是 objective function 的值。
6. Time analysis：
   - $\sum_{x \in X} \text{work}(x)$；若对所有 $x \in X$ 有 $\text{work}(x) = O(W)$，则为 $|X| \cdot O(W)$。
   - $\text{work}(x)$ 度量 relation 中的 nonrecursive work；把 recursions 视为花费 $O(1)$ 时间。

## Rod Cutting（切杆）

- 给定一根长度为 $L$ 的 rod（杆），以及对所有 $\ell \in \{1, 2, \dots, L\}$ 给出长度为 $\ell$ 的杆的价值 $v(\ell)$。
- Goal：切割这根 rod，使切出的 pieces（各段）的价值之和最大。
- 例子：$L = 7$，$v = [0, 1, 10, 13, 18, 20, 31, 32]$。

| $\ell$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $v(\ell)$ | 0 | 1 | 10 | 13 | 18 | 20 | 31 | 32 |

- 也许可以 greedy（贪心地）取单位长度价值最大的那种切法？
- 不行！$\arg\max_{\ell} v[\ell]/\ell = 6$，而分成 $[6, 1]$ 得 $32$，并不是最优！
- Solution：$v[2] + v[2] + v[3] = 10 + 10 + 13 = 33$。
- 这是关于 partition（划分）价值的 maximization problem。

### 1. Subproblems（子问题）

- $x(\ell)$：切割长度为 $\ell$ 的 rod 能得到的最大价值。
- 其中 $\ell \in \{0, 1, \dots, L\}$。

### 2. Relate（关联）

- 第一段 piece 有某个长度 $p$（猜！）。
- $x(\ell) = \max\{v(p) + x(\ell - p) \mid p \in \{1, \dots, \ell\}\}$。
- （画出 dependency graph。）

### 3. Topological order（拓扑序）

- 按 $\ell$ 递增：subproblems $x(\ell)$ 只依赖严格更小的 $\ell$，故无环。

### 4. Base（基础情形）

- $x(0) = 0$（长度为零的 rod 没有价值！）。

### 5. Original problem（原问题）

- 切割长度为 $L$ 的 rod 能得到的最优价值是 $x(L)$。
- 存下选择以重建 cuts（切割方案）。
- 若当前 rod 长度为 $\ell$、最优选择为 $\ell'$，则剩下的 piece 为 $p = \ell - \ell'$。
- （这是 subproblem DAG 中的 maximum-weight path！）

### 6. Time（时间）

- subproblems 个数：$L + 1$。
- 每个 subproblem 的 work：$O(\ell) = O(L)$。
- 运行时间 $O(L^2)$。

## Is This Polynomial Time?（这是多项式时间吗？）

- (Strongly) polynomial time（强）多项式时间：running time 被 input size（以 words 度量）的 constant-degree polynomial（常次数多项式）从上方界住。
- 在 Rod Cutting 中，input size 是 $L + 1$ words（一个 integer $L$，以及 $v$ 中的 $L$ 个 integers）。
- $O(L^2)$ 是 $L + 1$ 的常次数多项式，所以答案是 YES：这是（强）多项式时间。

```python
# recursive
x = {}
def cut_rod(l, v):
    if l < 1:
        return 0                              # base case
    if l not in x:                            # check memo
        for piece in range(1, l + 1):         # try piece
            x_ = v[piece] + cut_rod(l - piece, v)   # recurrence
            if (l not in x) or (x[l] < x_):   # update memo
                x[l] = x_
    return x[l]
```

```python
# iterative
def cut_rod(L, v):
    x = [0] * (L + 1)                         # base case
    for l in range(L + 1):                    # topological order
        for piece in range(1, l + 1):         # try piece
            x_ = v[piece] + x[l - piece]      # recurrence
            if x[l] < x_:                     # update memo
                x[l] = x_
    return x[L]
```

```python
# iterative with parent pointers
def cut_rod_pieces(L, v):
    x = [0] * (L + 1)                         # base case
    parent = [None] * (L + 1)                 # parent pointers
    for l in range(1, L + 1):                 # topological order
        for piece in range(1, l + 1):         # try piece
            x_ = v[piece] + x[l - piece]      # recurrence
            if x[l] < x_:                     # update memo
                x[l] = x_
                parent[l] = l - piece         # update parent
    l, pieces = L, []
    while parent[l] is not None:              # walk back through parents
        piece = l - parent[l]
        pieces.append(piece)
        l = parent[l]
    return pieces
```

## Subset Sum（子集和）

- Input：$n$ 个 positive integers 组成的序列 $A = \{a_0, a_1, \dots, a_n\}$。
- Output：是否存在 $A$ 的一个 subset，其和恰好为 $T$？（即是否存在 $A' \subseteq A$ 使 $\sum_{a \in A'} a = T$？）
- 例子：$A = (1, 3, 4, 12, 19, 21, 22)$，$T = 47$，可以取 $A' = \{3, 4, 19, 21\}$。
- 这是 optimization problem 吗？不，是 decision problem（判定问题）！答案是 YES 或 NO、TRUE 或 FALSE。
- 上例答案是 YES。但对某些 $T$ 答案是 NO，例如 $2, 6, 9, 10, 11, \dots$。

### 1. Subproblems

- $x(i, t)$：$A[i:]$ 的某个 subset 之和能否恰好为 $t$？
- 其中 $i \in \{0, 1, \dots, n\}$，$t \in \{0, 1, \dots, T\}$。

### 2. Relate

- Idea：第一个 item $a_i$ 是否在合法的 subset $A'$ 中？（猜！）
- 若在，则用剩余的 items 试着凑出 $t - a_i$。
- 若不在，则用剩余的 items 试着凑出 $t$。

```math
x(i, t) = \text{OR}\begin{cases}
x(i + 1, t - A[i]) & \text{if } t \ge A[i] \\
x(i + 1, t) & \text{always}
\end{cases}
```

### 3. Topological order

- Subproblems $x(i, t)$ 只依赖严格更大的 $i$，故无环。
- 按 $i$ 递减的顺序求解。

### 4. Base

- 对 $i \in \{0, \dots, n\}$ 有 $x(i, 0) = \text{YES}$（空间恰好被填满！）。
- 对 $t \in \{1, \dots, T\}$ 有 $x(n, t) = \text{NO}$（没有更多 items 可用来填满）。
- † 原文此处写作 $x(0, t)$，但按前缀/后缀语义应为 $x(n, t)$；PDF 文字层的下标缺笔，按语义推定。

### 5. Original problem

- Original problem 由 $x(0, T)$ 给出。
- 例子：$A = (3, 4, 3, 1)$，$T = 6$，solution 为 $A' = (3, 3)$。
- Bottom up：求解所有 subproblems（该例有 35 个）。
- Top down：只求解可达的 subproblems。

### 6. Time

- subproblems 个数：$O(nT)$；每个 $O(1)$ work；总时间 $O(nT)$。

## Is This Polynomial?（这是多项式时间吗？）

- Input size 是 $n + 1$：一个 integer $T$ 加上 $A$ 中的 $n$ 个 integers。
- $O(nT)$ 是否被 $n + 1$ 的某个多项式从上方界住？NO，不一定。
- 在 $w$-bit word RAM 上，$T \le 2^w$ 且 $w \ge \lg(n + 1)$，但 $w$ 没有上界。
- 例如 $w = n$ 并非不合理，但此时运行时间是 $O(n 2^n)$，是指数级的。

## Pseudopolynomial

- 若 running time 被 input size 与 input integers 的常次数多项式从上方界住，就说该 algorithm 具有 pseudopolynomial time（伪多项式时间）。
- 当 integers 被 input size 多项式界住时（即 $n^{O(1)}$），这类 algorithms 就是多项式的（这与 Radix Sort 在 $O(n)$ 时间内运行是同一种情形）。
- Counting sort $O(n + u)$、radix sort $O(n \log_n u)$、direct-access array 构造 $O(n + u)$、Fibonacci $O(n)$，都是我们已经见过的 pseudopolynomial algorithms。
- Radix sort 其实是 weakly polynomial（弱多项式，介于 strongly polynomial 与 pseudopolynomial 之间的概念）：它被「以 bits 度量的 input size」的常次数多项式界住，也就是被 input integers 的对数的常次数多项式界住。
- 对比 Rod Cutting，它是多项式的：
  - 对 $L$ 有 pseudopolynomial 的依赖；
  - 但所幸 input 中也有 $L$ 个 integers；
  - 若只给定可出售的 rod 长度的 subset（即 Knapsack Problem，背包问题，它推广了 Rod Cutting 与 Subset Sum，见 recitation），该 algorithm 就只是 pseudopolynomial 的。

## Complexity（复杂度）

- 当 integers 不被多项式界住时，Subset Sum 能在多项式时间内求解吗？
- 若 $P \ne NP$，则不能。这句话意味着什么？下次课讲！

## Main Features of Dynamic Programs（动态规划的主要特征）

- 回顾本课的例子。
- Subproblems：
  - Prefix / suffixes：Bowling、LCS、LIS、Floyd–Warshall、Rod Cutting（其实巧合地是 integer subproblems）、Subset Sum。
  - Substrings：Alternating Coin Game、Arithmetic Parenthesization。
  - Multiple sequences：LCS。
  - Integers：Fibonacci、Rod Cutting、Subset Sum。
    - Pseudopolynomial：Fibonacci、Subset Sum。
  - Vertices：DAG shortest paths、Bellman–Ford、Floyd–Warshall。
- Subproblem constraints / expansion：
  - 无扩张的 constraint：LIS（要求包含第一个 item）。
  - $2\times$ expansion：Alternating Coin Game（谁先走？）、Arithmetic Parenthesization（min / max）。
  - $\Theta(1)\times$ expansion：Piano Fingering（第一个 finger 的分配）。
  - $\Theta(n)\times$ expansion：Bellman–Ford（# edges）。
- Relation：
  - Branching（分支数）= 每个 subproblem 中相依的 subproblems 个数。
  - $\Theta(1)$ branching：Fibonacci、Bowling、LCS、Alternating Coin Game、Floyd–Warshall、Subset Sum。
  - $\Theta(\text{degree})$ branching（running time 中 $|E|$ 的来源）：DAG shortest paths、Bellman–Ford。
  - $\Theta(n)$ branching：LIS、Arithmetic Parenthesization、Rod Cutting。
  - 组合多个 solutions（不是 subproblem DAG 中的 path）：Fibonacci、Floyd–Warshall、Arithmetic Parenthesization。
- Original problem：
  - 组合多个 subproblems：DAG shortest paths、Bellman–Ford、Floyd–Warshall、LIS、Piano Fingering。
