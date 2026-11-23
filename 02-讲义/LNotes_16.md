# Lecture 16: Dyn. Prog. Subproblems（动态规划的子问题）

> Introduction to Algorithms: 6.006，Massachusetts Institute of Technology
> Instructors: Erik Demaine, Jason Ku, and Justin Solomon

---

## Dynamic Programming Review（动态规划回顾）

- Recursion（递归），其中 subproblem dependencies（子问题依赖）有重叠、构成 DAG。
- “Recurse but re-use”（递归但复用）：Top down，记录并查表取 subproblem solutions。
- “Careful brute force”（小心的暴力）：Bottom up，按顺序做每个 subproblem。

## Dynamic Programming Steps (SRT BOT)（动态规划步骤）

1. Subproblem definition（子问题定义）：subproblem $x \in X$。
   - 用文字、以 parameters 的形式描述一个 subproblem 的含义。
   - 常常取 input 的 subsets：序列的 prefixes、suffixes、contiguous substrings。
   - 常常把多个 input 上的可能 subsets 相乘（multiply）。
   - 常常记录 partial state：通过递增某些 auxiliary variables 来增加 subproblems。
2. Relate subproblem solutions recursively（递归关联）：$x(i) = f(x(j), \dots)$，其中 $j < i$（可有一个或多个）。
   - 找出一个关于 subproblem solution 的问题：只要知道它的答案，就能把该 subproblem reduce 到更小的 subproblem(s)。
   - 对这个问题的所有可能答案做 local brute-force。
3. Topological order：论证 relation 无环、subproblems 构成 DAG。
4. Base cases：
   - 对所有（可达的）独立 subproblems 给出解，即 relation 失效处。
5. Original problem：
   - 说明如何由 subproblem(s) 的解算出 original problem 的解。
   - 可能要用 parent pointers 还原真正的 solution，而不仅是 objective function 的值。
6. Time analysis：
   - $\sum_{x \in X} \text{work}(x)$；若对所有 $x \in X$ 有 $\text{work}(x) = O(W)$，则为 $|X| \cdot O(W)$。
   - $\text{work}(x)$ 度量 relation 中的 nonrecursive work；把 recursions 视为花费 $O(1)$ 时间。

## Longest Common Subsequence (LCS)（最长公共子序列）

- 给定两个 strings（字符串）$A$ 与 $B$，找出 $A$ 的一个 longest（最长、不要求 contiguous）subsequence，使它也是 $B$ 的 subsequence。
- 例子：$A = \text{hieroglyphology}$，$B = \text{michaelangelo}$。
- Solution：hello 或 heglo 或 iello 或 ieglo，长度都是 5。
- 这是关于 subsequence 长度的 maximization problem（最大化问题）。

### 1. Subproblems

- $x(i, j)$ = suffixes（后缀）$A[i:]$ 与 $B[j:]$ 的最长 common subsequence 的长度。
- 其中 $0 \le i \le |A|$ 且 $0 \le j \le |B|$。

### 2. Relate（关联）

- 首字符要么 match（相同），要么不同。
- 若首字符相同，则某个 longest common subsequence 会用到它们。
  - （若没有 LCS 用到这对相同首字符，那么用上它只会让 solution 更好。）
  - （若某个 LCS 用了 $A[i]$ 的首字符却没用 $B[j]$ 的首字符，那么把 $B[j]$ 也配上同样是最优的。）
- 若首字符不同，它们不可能同时出现在一个 longest common subsequence 中。
- 于是猜：$A[i]$ 与 $B[j]$ 中哪一个不在 LCS 里。

```math
x(i, j) =
\begin{cases}
x(i + 1, j + 1) + 1 & \text{if } A[i] = B[j] \\
\max\{x(i + 1, j),\ x(i, j + 1)\} & \text{otherwise}
\end{cases}
```

- （画出所有矩形网格状的 dependency 的一个子集。）

### 3. Topological order（拓扑序）

- Subproblems $x(i, j)$ 只依赖严格更大的 $i$、或严格更大的 $j$、或两者都更大。
- 最容易表述的 order：按 $i + j$ 递减。
- 对 bottom-up code 好用的 order：先按 $i$ 递减，再按 $j$ 递减。

### 4. Base（基础情形）

- $x(i, |B|) = x(|A|, j) = 0$（其中一个 string 为空）。

### 5. Original problem（原问题）

- $A$ 与 $B$ 的 longest common subsequence 的长度是 $x(0, 0)$。
- 存 parent pointers 以重建 subsequence。
- 若 parent pointer 让两个 index 都递增，就把该 character 加入 LCS。

### 6. Time（时间）

- subproblems 个数：$(|A| + 1) \cdot (|B| + 1)$。
- 每个 subproblem 的 work：$O(1)$。
- 运行时间 $O(|A| \cdot |B|)$。

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

## Longest Increasing Subsequence (LIS)（最长递增子序列）

- 给定一个 string $A$，找出 $A$ 的一个 longestsubsequence，使它严格递增（lexicographically，按字典序）。
- 例子：$A = \text{carbohydrate}$。
- Solution：abort，长度为 5。
- 这是关于 subsequence 长度的 maximization problem。
- 尝试性的解：
  - 自然的 subproblems 是 $A$ 的 prefixes 或 suffixes，比如 suffix $A[i:]$。
  - 关于 $A[i:]$ 的 LIS 的自然问题是：$A[i]$ 是否在 LIS 中？（2 个可能答案。）
  - 但接下来如何在 $A[i + 1:]$ 上 recurse，并保证 subsequence 递增？
  - 修法：给 subproblems 加 constraint（约束），提供足够结构来保证 increasing 性质。

### 1. Subproblems

- $x(i)$ = 包含 $A[i]$ 的、suffix $A[i:]$ 的最长 increasing subsequence 的长度。
- 其中 $0 \le i \le |A|$。

### 2. Relate

- 我们已假定 $A[i]$ 在 LIS 中（作为第一个 element）。
- 下一个问题：LIS 的第二个 element 是什么？
  - 可以是任何满足 $j > i$ 且 $A[j] > A[i]$ 的 $A[j]$（这样才 increasing）。
  - 或者 $A[i]$ 就是 LIS 的最后一个 element。
- $x(i) = \max\bigl(\{1 + x(j) \mid i < j < |A|,\ A[j] > A[i]\} \cup \{1\}\bigr)$。

### 3. Topological order

- 按 $i$ 递减。

### 4. Base

- 不需要 base case，因为我们已经考虑了「$A[i]$ 是最后一个」这种可能。

### 5. Original problem

- LIS 的第一个 element 是什么？猜！
- $A$ 的 LIS 长度为 $\max\{x(i) \mid 0 \le i < |A|\}$。
- 存 parent pointers 以重建 subsequence。

### 6. Time

- subproblems 个数：$|A|$。
- 每个 subproblem 的 work：$O(|A|)$。
- 运行时间 $O(|A|^2)$。
- Exercise：通过 AVL tree augmentation（AVL 树增广）让每个 subproblem 只做 $O(\log |A|)$ work，从而加速到 $O(|A| \log |A|)$。

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

## Alternating Coin Game（交替取硬币游戏）

- 给定 $n$ 个硬币组成的序列，价值为 $v_0, v_1, \dots, v_{n-1}$。
- 两个 players（“me” 与 “you”）轮流行动。
- 每一回合，从剩余的硬币中取走第一个或最后一个。
- 我先手；我的目标是让我取走的硬币总价值最大。
- 第一个 solution 利用这是 zero-sum game（零和博弈）：我拿走所有你没拿的。

### 1. Subproblems

- 选择与 game 状态相对应的 subproblems。
- 对从 $i$ 到 $j$ 的每个 contiguous subsequence of coins，$0 \le i \le j < n$。
- $x(i, j)$ = 从价值为 $v_i, \dots, v_j$ 的硬币出发、我能取到的最大总价值。

### 2. Relate

- 我必须选 coin $i$ 或 coin $j$（猜！）。
- 然后轮到你，于是你分别会得到 $x(i + 1, j)$ 或 $x(i, j - 1)$ 的价值。
- 为算出我得多少，用硬币总价值减去这一份。

```math
x(i, j) = \max\left\{v_i + \sum_{k=i+1}^{j} v_k - x(i + 1, j),\ v_j + \sum_{k=i}^{j-1} v_k - x(i, j - 1)\right\}
```

### 3. Topological order

- 按 $j - i$ 递增。

### 4. Base

- $x(i, i) = v_i$。

### 5. Original problem

- $x(0, n - 1)$。
- 存 parent pointers 以重建 strategy（策略）。

### 6. Time

- subproblems 个数：$\Theta(n^2)$。
- 每个 subproblem 的 work：$\Theta(n)$（用于计算 sums）。
- 运行时间 $\Theta(n^3)$。
- Exercise：先用 dynamic programming（！）在 $\Theta(n^2)$ 时间内预计算所有 $\sum_{k=i}^{j} v_k$，从而加速到 $\Theta(n^2)$ 时间。

- 第二个 solution 使用 subproblem expansion（子问题扩张）：为「下一步轮到谁」增加 subproblems。

### 1. Subproblems

- 选择与 game 的完整状态相对应的 subproblems。
- 从 $i$ 到 $j$ 的 contiguous subsequence of coins，以及接下来轮到哪个 player $p$。
- $x(i, j, p)$ = 当 player $p \in \{\text{me}, \text{you}\}$ 从价值为 $v_i, \dots, v_j$ 的硬币出发时，我能取到的最大总价值。

### 2. Relate

- Player $p$ 必须选 coin $i$ 或 coin $j$（猜！）。
- 若 $p = \text{me}$，则价值归我；否则我什么都得不到。
- 然后轮到另一个 player。
- $x(i, j, \text{me}) = \max\{v_i + x(i + 1, j, \text{you}),\ v_j + x(i, j - 1, \text{you})\}$。
- $x(i, j, \text{you}) = \min\{x(i + 1, j, \text{me}),\ x(i, j - 1, \text{me})\}$。

### 3. Topological order

- 按 $j - i$ 递增。

### 4. Base

- $x(i, i, \text{me}) = v_i$。
- $x(i, i, \text{you}) = 0$。

### 5. Original problem

- $x(0, n - 1, \text{me})$。
- 存 parent pointers 以重建 strategy。

### 6. Time

- subproblems 个数：$\Theta(n^2)$。
- 每个 subproblem 的 work：$\Theta(1)$。
- 运行时间 $\Theta(n^2)$。

## Subproblem Constraints and Expansion（子问题约束与扩张）

- 现在我们已看到两个例子：对 subproblems 加 constraint 或做 expansion。
- 若你发现自己缺少信息来检验题目要求成立的条件，或者缺少可供 recurse 的自然 subproblem，就试试 subproblem constraint / expansion！
- 更多的 subproblems 与 constraints 让 relation 有更多可用的信息，从而让 DP 更可行。
- 通常这是 subproblems 数量与 relation 的分支 / 复杂度之间的 trade-off（权衡）。
- 下次课还有更多例子。
