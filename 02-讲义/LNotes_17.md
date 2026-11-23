# Lecture 17: Dyn. Prog. III（动态规划 III）

> Introduction to Algorithms: 6.006，Massachusetts Institute of Technology
> Instructors: Erik Demaine, Jason Ku, and Justin Solomon

---

## Dynamic Programming Steps (SRT BOT)（动态规划步骤）

1. Subproblem definition：subproblem $x \in X$。
   - 用文字、以 parameters 的形式描述一个 subproblem 的含义。
   - 常常取 input 的 subsets：序列的 prefixes、suffixes、contiguous substrings。
   - 常常把多个 input 上的可能 subsets 相乘。
   - 常常记录 partial state：通过递增某些 auxiliary variables 来增加 subproblems。
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

## Recall: DAG Shortest Paths [L15]（回顾：DAG 最短路径）

- Subproblems：所有 $v \in V$ 的 $\delta(s, v)$。
- Relation：

```math
\delta(s, v) = \min\bigl(\{\delta(s, u) + w(u, v) \mid u \in Adj^-(v)\} \cup \{\infty\}\bigr)
```

- Topo. order：$G$ 的 topological order。

## Single-Source Shortest Paths Revisited（重访单源最短路径）

### 1. Subproblems（子问题）

- 扩张 subproblems 以加入信息，使结构变成 acyclic（无环）！
  - （这是我们已见过的一个 subproblem expansion 的例子。）
- $\delta_k(s, v)$ = 从 $s$ 到 $v$、使用至多 $k$ 条 edges 的 shortest path 的 weight。
- 其中 $v \in V$，$0 \le k \le |V|$。

### 2. Relate（关联）

- 猜从 $s$ 到 $v$ 的 shortest path 上的最后一条 edge $(u, v)$。
- $\delta_k(s, v) = \min\bigl(\{\delta_{k-1}(s, u) + w(u, v) \mid (u, v) \in E\} \cup \{\delta_{k-1}(s, v)\}\bigr)$。

### 3. Topological order（拓扑序）

- 按 $k$ 递增：subproblems 只依赖 $k$ 严格更小的 subproblems。

### 4. Base（基础情形）

- $\delta_0(s, s) = 0$；对 $v \ne s$ 有 $\delta_0(s, v) = \infty$（没有 edges）。
- （画出 subproblem graph。）

### 5. Original problem（原问题）

- 若存在有限的 shortest path，则 $\delta(s, v) = \delta_{|V|-1}(s, v)$。
- 否则某个 $\delta_{|V|}(s, v) < \delta_{|V|-1}(s, v)$，说明 path 含 negative-weight cycle。
- 可以记录 parent pointers，指向使 recurrence 取到最小的那个 subproblem。

### 6. Time（时间）

- subproblems 个数：$|V| \times (|V| + 1)$。
- subproblem $\delta_k(s, v)$ 的 work：$O(\deg_{in}(v))$。
- 总时间：

```math
\sum_{k=0}^{|V|} \sum_{v \in V} O(\deg_{in}(v)) = \sum_{k=0}^{|V|} O(|E|) = O(|V| \cdot |E|)
```

- 这不就是 Bellman-Ford 吗！（只是计算顺序略有不同。）

## All-Pairs Shortest Paths: Floyd–Warshall（全对最短路径：Floyd–Warshall）

- 可以像 Bellman–Ford 那样定义 subproblems：$\delta_k(u, v)$ = 从 $u$ 到 $v$、使用至多 $k$ 条 edges 的 path 的最小 weight。
- 得到的运行时间是 $|V|$ 次 Bellman–Ford，即 $O(|V|^2 \cdot |E|) = O(|V|^4)$。
- 从 L14 已知更好的 algorithm：Johnson 达到 $O(|V|^2 \log |V| + |V| \cdot |E|) = O(|V|^3)$。
- 用一个简单的 dynamic program —— 称为 Floyd–Warshall —— 也能达到 $\Theta(|V|^3)$ 运行时间（对 dense graphs 与 Johnson 相当）。
- 给 vertices 编号，使 $V = \{1, 2, \dots, |V|\}$。

### 1. Subproblems

- $d(u, v, k)$ = 从 $u$ 到 $v$、只使用 $\{1, 2, \dots, k\} \cup \{u, v\}$ 中 vertices 的 path 的最小 weight。
- 其中 $u, v \in V$，$1 \le k \le |V|$。

### 2. Relate

- $x(u, v, k) = \min\{x(u, k, k - 1) + x(k, v, k - 1),\ x(u, v, k - 1)\}$。
- 只有 constant branching（常数分支）！不再需要猜前一个 vertex / edge。

### 3. Topological order

- 按 $k$ 递增：relation 只依赖更小的 $k$。

### 4. Base

- $x(u, u, 0) = 0$。
- 若 $(u, v) \in E$，则 $x(u, v, 0) = w(u, v)$。
- 若以上都不是，则 $x(u, v, 0) = \infty$。

### 5. Original problem

- 对所有 $u, v \in V$ 取 $x(u, v, |V|)$。

### 6. Time

- 有 $O(|V|^3)$ 个 subproblems。
- 每个 $O(1)$ work。
- 总计 $O(|V|^3)$。
- 每个 subproblem 只有常数个 dependencies，这把 running time 中的 $O(|E|)$ 因子降到了 $O(|V|)$。

## Arithmetic Parenthesization（算术加括号）

- Input：arithmetic expression（算术表达式）$a_0 \ast_1 a_1 \ast_2 a_2 \cdots \ast_{n-1} a_{n-1}$，其中每个 $a_i$ 是 integer，每个 $\ast_i \in \{+, \times\}$。
- Output：括号加在哪里，才能使表达式的求值最大。
- 例子：$7 + 4 \times 3 + 5 \to ((7) + (4)) \times ((3) + (5)) = 88$。
- 允许 negative integers（负整数）！
- 例子：$7 + (-4) \times 3 + (-5) \to ((7) + ((-4) \times ((3) + (-5)))) = 15$。

### 1. Subproblems

- 只需对每个 subarray 取最大就够了吗？不够！$(-3) \times (-3) = 9 > (-2) \times (-2) = 4$。
- $x(i, j, \text{opt})$ = 对 $a_i \ast_{i+1} \cdots \ast_{j-1} a_{j-1}$ 加括号所能得到的 opt 值。
- 其中 $0 \le i < j \le n$，$\text{opt} \in \{\min, \max\}$。

### 2. Relate

- 猜最外层括号的位置 / 最后求值的那个 operation。
- $x(i, j, \text{opt}) = \text{opt}\bigl\{x(i, k, \text{opt}') \ast_k x(k, j, \text{opt}'') \mid i < k < j;\ \text{opt}', \text{opt}'' \in \{\min, \max\}\bigr\}$。

### 3. Topological order

- 按 $j - i$ 递增：subproblem $x(i, j, \text{opt})$ 只依赖 $j - i$ 严格更小的 subproblems。

### 4. Base

- $x(i, i + 1, \text{opt}) = a_i$：只剩一个数，没有 operations 可做了！

### 5. Original problem

- $x(0, n, \max)$。
- 存 parent pointers（两个！）以找出 parenthesization（它构成一棵 binary tree！）。

### 6. Time

- subproblems 个数：少于 $n \cdot n \cdot 2 = O(n^2)$。
- 每个 subproblem 的 work：$O(n) \cdot 2 \cdot 2 = O(n)$。
- 运行时间 $O(n^3)$。

## Piano Fingering（钢琴指法）

- 给定 $n$ 个单音组成的序列 $t_0, t_1, \dots, t_{n-1}$，用右手弹奏（之后会推广到多个音与双手）。
- 演奏者有右手指 $1, 2, \dots, F$（对多数人类 $F = 5$）。
- 给定难度度量 $d(t, f, t', f')$：从「用 finger $f$ 弹 note $t$」转到「用 finger $f'$ 弹 note $t'$」的难度。
  - 通常是各种难度的 penalty（惩罚）之和，例如：
  - $1 < f < f'$ 且 $t > t'$ 是不舒服的。
  - Legato（连奏、平滑）要求 $t \ne t'$（否则 penalty 无限大）。
  - Weak-finger rule（弱指规则）：尽量避免 $f' \in \{4, 5\}$。
  - $\{f, f'\} = \{3, 4\}$ 的组合很恼人。
- Goal：给 notes 分配 fingers，使总难度最小。

### First attempt（第一次尝试）

#### 1. Subproblems

- $x(i)$ = 弹奏 notes $t_i, t_{i+1}, \dots, t_{n-1}$ 的最小总难度。

#### 2. Relate

- 猜第一个 finger：给 $t_i$ 分配 $f$。
- $x(i) = \min\{x(i + 1) + d(t_i, f, t_{i+1}, \text{?}) \mid 1 \le f \le F\}$。
- 没有足够信息填出那个 $\text{?}$！
- 需要知道 $x(i + 1)$ 起手用的是哪个 finger。
- 但不同的起手 finger 会同时影响 $x(i + 1)$ 与 $d(t_i, f, t_{i+1}, \text{?})$，可能一好一坏。
- 需要一张表，把起手 fingers 映射到 $x(i + 1)$ 的 optimal solutions。
- 也就是说，需要用 start condition（起始条件）来 expand subproblems。

### Solution（解法）

#### 1. Subproblems

- $x(i, f)$ = 在 note $t_i$ 上以 finger $f$ 起手、弹奏 notes $t_i, t_{i+1}, \dots, t_{n-1}$ 的最小总难度。
- 其中 $0 \le i < n$，$1 \le f \le F$。

#### 2. Relate

- 猜下一个 finger：给 $t_{i+1}$ 分配 $f'$。
- $x(i, f) = \min\{x(i + 1, f') + d(t_i, f, t_{i+1}, f') \mid 1 \le f' \le F\}$。

#### 3. Topological order

- 按 $i$ 递减（$f$ 的顺序任意）。

#### 4. Base

- $x(n - 1, f) = 0$（没有 transition）。

#### 5. Original problem

- $\min\{x(0, f) \mid 1 \le f \le F\}$。

#### 6. Time

- $\Theta(n \cdot F)$ 个 subproblems。
- 每个 subproblem 的 work 为 $\Theta(F)$。
- 总时间 $\Theta(n \cdot F^2)$。
- 与不同 notes 的个数无关！

## Guitar Fingering（吉他指法）

- 同一个 note 最多有 $S$ 种弹法（$S$ = strings 的数量）。
- 把 “finger” 重定义为 tuple（弹该 note 的 finger，弹该 note 的 string）。
- 整个 algorithm 中，$F$ 被替换为 $F \cdot S$。
- 于是运行时间为 $\Theta(n \cdot F^2 \cdot S^2)$。

## Multiple Notes at Once（同时多个音）

- 现在假设 $t_i$ 是在时刻 $i$ 要弹的一组 notes。
- 给定更大的 transition difficulty function $d(t, f, t', f')$。
- Goal：给出指法 $f_i : t_i \to \{1, 2, \dots, F\}$，说明每个 note 怎么按（对吉他还要说明用哪根 string），使 $\sum_{i=1}^{n-1} d(t_{i-1}, f_{i-1}, t_i, f_i)$ 最小。
- 每个指法 $f_i$ 至多有 $T^F$ 种选择，其中 $T = \max_i |t_i|$。
  - 对普通钢琴 $T \le F = 10$（但有例外）。
  - 对吉他 $T \le S$。
- $\Theta(n \cdot T^F)$ 个 subproblems。
- 每个 subproblem 的 work 为 $\Theta(T^F)$。
- 时间 $\Theta(n \cdot T^{2F})$。
- 当 $T, F \le 10$ 时为 $\Theta(n)$ 时间。

## Video Game Applications（电子游戏应用）

- Guitar Hero / Rock Band：
  - $F = 4$（另有 5 个不同的 notes）。
- Dance Dance Revolution：
  - $F = 2$ 只脚。
  - $T = 2$（一次至多两个 notes）。
  - Exercise：处理 sustained notes（持续音），把「每只脚在哪里」（在某个箭头上，或在中间）作为额外状态加入 suffix subproblems。
